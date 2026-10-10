"""
NAGRO 4.1 — Document Processor.

Reads and processes various document formats (txt, pdf, code files, csv).
All local, no external services.
"""

from __future__ import annotations
from pathlib import Path


def read_text_file(filepath: str) -> str:
    """Read a plain text file."""
    path = Path(filepath)
    if not path.exists():
        return f"Error: File not found: {filepath}"
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def read_code_file(filepath: str) -> dict:
    """Read a code file and extract metadata."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = read_text_file(filepath)
    lines = content.split("\n")

    lang_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".java": "java", ".cpp": "cpp", ".c": "c", ".cs": "csharp",
        ".go": "go", ".rs": "rust", ".rb": "ruby", ".php": "php",
        ".html": "html", ".css": "css", ".sql": "sql", ".sh": "bash",
        ".yaml": "yaml", ".yml": "yaml", ".json": "json", ".xml": "xml",
        ".md": "markdown", ".r": "r", ".swift": "swift", ".kt": "kotlin",
    }

    return {
        "content": content,
        "language": lang_map.get(path.suffix.lower(), "unknown"),
        "filename": path.name,
        "lines": len(lines),
        "size_bytes": path.stat().st_size,
    }


def read_csv_file(filepath: str, max_rows: int = 100) -> dict:
    """Read a CSV file and return structured data."""
    import csv
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = []
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append(dict(row))
            return {
                "headers": reader.fieldnames or [],
                "rows": rows,
                "total_read": len(rows),
                "truncated": len(rows) >= max_rows,
            }
    except Exception as e:
        return {"error": str(e)}


def chunk_document(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Split a document into overlapping chunks for processing."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def extract_code_blocks(text: str) -> list[dict[str, str]]:
    """Extract code blocks from markdown-formatted text."""
    import re
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"language": lang or "text", "code": code.strip()} for lang, code in matches]


def get_file_summary(filepath: str) -> str:
    """Get a brief summary of a file's contents."""
    path = Path(filepath)
    if not path.exists():
        return f"File not found: {filepath}"

    size = path.stat().st_size
    suffix = path.suffix.lower()

    if suffix in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
        return f"Image file: {path.name} ({size} bytes)"

    if suffix in (".mp3", ".wav", ".ogg", ".flac"):
        return f"Audio file: {path.name} ({size} bytes)"

    if suffix in (".mp4", ".avi", ".mkv", ".mov"):
        return f"Video file: {path.name} ({size} bytes)"

    try:
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")
        preview = "\n".join(lines[:10])
        return (
            f"File: {path.name}\n"
            f"Size: {size} bytes | Lines: {len(lines)}\n"
            f"Preview:\n{preview}"
        )
    except (UnicodeDecodeError, Exception):
        return f"Binary file: {path.name} ({size} bytes)"
