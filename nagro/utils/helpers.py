"""Utility functions for NAGRO 4.1."""

from __future__ import annotations
import re
import time
from functools import wraps
from typing import Callable, Any


def extract_code_blocks(text: str) -> list[dict[str, str]]:
    """Extract code blocks from markdown text."""
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"language": lang or "text", "code": code.strip()} for lang, code in matches]


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable form."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure execution time."""
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed
    return wrapper


def sanitize_input(text: str) -> str:
    """Basic input sanitization."""
    text = text.strip()
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return text
