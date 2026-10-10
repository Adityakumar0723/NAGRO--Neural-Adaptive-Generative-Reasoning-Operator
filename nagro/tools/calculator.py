"""
NAGRO 4.1 — Self-Built Calculator.

Safe mathematical expression evaluator — no eval(), no exec().
Supports arithmetic, powers, roots, trig, logarithms.
"""

from __future__ import annotations
import math
import re
import operator

SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
    "gcd": math.gcd,
    "pi": math.pi,
    "e": math.e,
}

SAFE_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}


def safe_calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Uses Python's ast module — no eval/exec.
    """
    import ast

    expression = expression.strip()
    expression = expression.replace("^", "**")
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except (ValueError, TypeError, OverflowError) as e:
        return f"Error: {e}"
    except Exception:
        return f"Error: Could not evaluate '{expression}'"


def _eval_node(node) -> float | int:
    """Recursively evaluate an AST node safely."""
    import ast

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value}")

    if isinstance(node, ast.Name):
        name = node.id.lower()
        if name in SAFE_FUNCTIONS:
            val = SAFE_FUNCTIONS[name]
            if isinstance(val, (int, float)):
                return val
        raise ValueError(f"Unknown variable: {node.id}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_map = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        op_func = op_map.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported operator")
        if op_func == operator.pow and right > 1000:
            raise OverflowError("Exponent too large")
        return op_func(left, right)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id.lower()
        if func_name not in SAFE_FUNCTIONS:
            raise ValueError(f"Unknown function: {func_name}")
        func = SAFE_FUNCTIONS[func_name]
        if not callable(func):
            raise ValueError(f"{func_name} is not a function")
        args = [_eval_node(arg) for arg in node.args]
        return func(*args)

    raise ValueError(f"Unsupported expression type: {type(node).__name__}")
