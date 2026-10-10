"""Research endpoints for NAGRO 4.1."""

from __future__ import annotations
from fastapi import APIRouter, Request

from nagro.core.models import ResearchRequest, ChatRequest, TaskType

router = APIRouter()


@router.post("/research")
async def research(request: ResearchRequest, req: Request):
    engine = req.app.state.engine
    chat_req = ChatRequest(
        message=request.query,
        task_type=TaskType.RESEARCH,
    )
    response = await engine.process(chat_req)
    return response
