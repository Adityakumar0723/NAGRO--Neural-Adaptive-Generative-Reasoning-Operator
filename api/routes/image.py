"""Image generation and analysis endpoints for NAGRO 4.1."""

from __future__ import annotations
import base64
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse

from nagro.core.models import ImageRequest, ChatRequest, TaskType

router = APIRouter()


@router.post("/image/generate")
async def generate_image(request: ImageRequest, req: Request):
    engine = req.app.state.engine
    chat_req = ChatRequest(
        message=request.prompt,
        task_type=TaskType.IMAGE,
    )
    response = await engine.process(chat_req)
    return response


@router.post("/image/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze an uploaded image using NAGRO's self-built image analyzer."""
    if not file.content_type or not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Please upload an image file (PNG, JPG, etc.)"},
        )

    max_size = 10 * 1024 * 1024
    data = await file.read()
    if len(data) > max_size:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Image too large. Maximum size is 10 MB."},
        )

    from nagro.core.image_analyzer import analyze_image as do_analyze
    result = do_analyze(data)
    return result
