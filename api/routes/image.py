"""Image generation endpoints for NAGRO 4.1."""

from __future__ import annotations
from fastapi import APIRouter, Request

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
