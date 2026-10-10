"""Safe code execution for NAGRO 4.1."""

from __future__ import annotations
import sys
import io
import traceback
from typing import Any


def execute_python(code: str, timeout: int = 10) -> dict[str, Any]:
    """Execute Python code in a restricted environment."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = captured_out = io.StringIO()
    sys.stderr = captured_err = io.StringIO()

    result = {"success": False, "output": "", "error": "", "return_value": None}

    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "bool": bool,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sorted": sorted,
            "reversed": reversed,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
            "isinstance": isinstance,
            "type": type,
            "True": True,
            "False": False,
            "None": None,
        }
    }

    try:
        exec(code, safe_globals)
        result["success"] = True
        result["output"] = captured_out.getvalue()
    except Exception:
        result["error"] = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return result
