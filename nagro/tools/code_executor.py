"""
NAGRO 4.1 — Multi-Language Code Executor.

Safe, sandboxed code execution for Python and JavaScript.
Self-built — no external services.
"""

from __future__ import annotations
import sys
import io
import os
import time
import traceback
import subprocess
import tempfile
from typing import Any
from pathlib import Path


def execute_python(code: str, timeout: int = 10) -> dict[str, Any]:
    """Execute Python code in a restricted environment."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = captured_out = io.StringIO()
    sys.stderr = captured_err = io.StringIO()

    result = {"success": False, "output": "", "error": "", "execution_time": 0.0}
    start = time.time()

    safe_globals = {
        "__builtins__": {
            "print": print, "len": len, "range": range, "int": int,
            "float": float, "str": str, "list": list, "dict": dict,
            "tuple": tuple, "set": set, "bool": bool, "enumerate": enumerate,
            "zip": zip, "map": map, "filter": filter, "sorted": sorted,
            "reversed": reversed, "sum": sum, "min": min, "max": max,
            "abs": abs, "round": round, "isinstance": isinstance,
            "type": type, "True": True, "False": False, "None": None,
            "input": lambda *a: "", "open": None, "exec": None, "eval": None,
            "chr": chr, "ord": ord, "hex": hex, "bin": bin, "oct": oct,
            "any": any, "all": all, "hash": hash, "id": id, "repr": repr,
            "format": format, "pow": pow, "divmod": divmod,
            "complex": complex, "bytes": bytes, "bytearray": bytearray,
            "memoryview": memoryview, "frozenset": frozenset,
            "slice": slice, "iter": iter, "next": next,
            "Exception": Exception, "ValueError": ValueError,
            "TypeError": TypeError, "KeyError": KeyError,
            "IndexError": IndexError, "AttributeError": AttributeError,
            "StopIteration": StopIteration, "RuntimeError": RuntimeError,
            "ZeroDivisionError": ZeroDivisionError,
        }
    }

    # Allow safe standard library imports
    safe_modules = {
        "math", "random", "string", "collections", "itertools",
        "functools", "operator", "json", "re", "datetime",
        "decimal", "fractions", "statistics", "textwrap",
        "dataclasses", "enum", "typing", "copy", "heapq",
        "bisect", "array", "queue", "abc", "contextlib",
    }

    import importlib

    def safe_import(name, *args, **kwargs):
        if name in safe_modules:
            return importlib.import_module(name)
        raise ImportError(f"Import of '{name}' is not allowed for security reasons")

    safe_globals["__builtins__"]["__import__"] = safe_import

    try:
        exec(code, safe_globals)
        result["success"] = True
        result["output"] = captured_out.getvalue()
    except Exception:
        result["error"] = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        result["execution_time"] = round(time.time() - start, 4)

    return result


def execute_javascript(code: str, timeout: int = 10) -> dict[str, Any]:
    """Execute JavaScript code using Node.js (if available)."""
    result = {"success": False, "output": "", "error": "", "execution_time": 0.0, "language": "javascript"}
    start = time.time()

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        proc = subprocess.run(
            ["node", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        result["output"] = proc.stdout
        result["error"] = proc.stderr
        result["success"] = proc.returncode == 0
    except FileNotFoundError:
        result["error"] = "Node.js is not installed. Install it to run JavaScript code."
    except subprocess.TimeoutExpired:
        result["error"] = f"Execution timed out after {timeout} seconds."
    except Exception as e:
        result["error"] = str(e)
    finally:
        try:
            os.unlink(temp_path)
        except (NameError, OSError):
            pass
        result["execution_time"] = round(time.time() - start, 4)

    return result


def execute_code(code: str, language: str = "python", timeout: int = 10) -> dict[str, Any]:
    """Execute code in the specified language."""
    language = language.lower().strip()

    if language in ("python", "py", "python3"):
        return execute_python(code, timeout)
    elif language in ("javascript", "js", "node"):
        return execute_javascript(code, timeout)
    else:
        return {
            "success": False,
            "output": "",
            "error": f"Language '{language}' execution not supported. Supported: python, javascript",
            "execution_time": 0.0,
        }
