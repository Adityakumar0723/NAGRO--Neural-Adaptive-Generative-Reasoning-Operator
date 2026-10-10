"""File upload and processing endpoints for NAGRO 4.1."""

from __future__ import annotations
import uuid
from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse

from nagro.core.config import settings
from nagro.tools.document_processor import (
    read_text_file, read_code_file, read_csv_file, get_file_summary,
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".java", ".cpp", ".c", ".go",
    ".rs", ".rb", ".php", ".html", ".css", ".sql", ".sh", ".yaml",
    ".yml", ".json", ".xml", ".csv", ".log", ".env", ".toml", ".ini",
    ".r", ".swift", ".kt", ".scala", ".lua", ".dart", ".tex",
}


@router.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    analyze: bool = Form(default=True),
    ingest_to_rag: bool = Form(default=False),
    req: Request = None,
):
    """Upload a file for processing, analysis, or RAG ingestion."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content={"error": f"File type '{ext}' not supported. Supported: {', '.join(sorted(ALLOWED_EXTENSIONS))}"},
        )

    if file.size and file.size > settings.nagro_max_upload_mb * 1024 * 1024:
        return JSONResponse(
            status_code=400,
            content={"error": f"File too large. Max: {settings.nagro_max_upload_mb} MB"},
        )

    # Save file
    file_id = str(uuid.uuid4())[:8]
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    content = await file.read()
    save_path.write_bytes(content)

    result = {
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": len(content),
        "path": str(save_path),
    }

    # Analyze if requested
    if analyze:
        if ext == ".csv":
            analysis = read_csv_file(str(save_path))
        elif ext in (".py", ".js", ".ts", ".java", ".cpp", ".go", ".rs"):
            analysis = read_code_file(str(save_path))
            # Run code analysis for Python
            if ext == ".py":
                from nagro.tools.code_analyzer import CodeAnalyzer
                analyzer = CodeAnalyzer()
                code_analysis = analyzer.analyze_python(content.decode("utf-8", errors="replace"))
                analysis["code_analysis"] = {
                    "functions": code_analysis.functions,
                    "classes": code_analysis.classes,
                    "complexity": code_analysis.complexity,
                    "issues": code_analysis.issues,
                    "suggestions": code_analysis.suggestions,
                    "summary": code_analysis.summary,
                }
        else:
            analysis = {"content_preview": content.decode("utf-8", errors="replace")[:2000]}

        result["analysis"] = analysis

    # Ingest to RAG if requested
    if ingest_to_rag and req:
        engine = req.app.state.engine
        text = content.decode("utf-8", errors="replace")
        engine.ingest_document(
            doc_id=f"file_{file_id}",
            text=text,
            metadata={"filename": file.filename, "type": ext},
        )
        result["rag_ingested"] = True

    return result


@router.post("/files/analyze")
async def analyze_file_content(req: Request):
    """Analyze code or text passed directly in the request body."""
    body = await req.json()
    code = body.get("code", "")
    language = body.get("language", "python")

    if not code:
        return {"error": "No code provided"}

    from nagro.tools.code_analyzer import CodeAnalyzer
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_any(code, language)

    return {
        "language": analysis.language,
        "lines_of_code": analysis.lines_of_code,
        "functions": analysis.functions,
        "classes": analysis.classes,
        "complexity": analysis.complexity,
        "issues": analysis.issues,
        "suggestions": analysis.suggestions,
        "summary": analysis.summary,
    }


@router.post("/files/execute")
async def execute_code_endpoint(req: Request):
    """Execute code safely and return the result."""
    body = await req.json()
    code = body.get("code", "")
    language = body.get("language", "python")
    timeout = body.get("timeout", 10)

    if not code:
        return {"error": "No code provided"}

    from nagro.tools.code_executor import execute_code
    result = execute_code(code, language, timeout)
    return result
