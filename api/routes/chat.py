"""Chat endpoints for NAGRO 4.1."""

from __future__ import annotations
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from nagro.core.models import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest, req: Request):
    engine = req.app.state.engine

    if request.stream:
        async def generate():
            async for chunk in engine.process_stream(request):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(generate(), media_type="text/event-stream")

    response = await engine.process(request)
    return response


class AgenticRequest(BaseModel):
    task: str
    max_steps: int = 10


@router.post("/agent")
async def agentic_task(request: AgenticRequest, req: Request):
    """Run a multi-step agentic task with tool use and reasoning."""
    engine = req.app.state.engine
    result = await engine.process_agentic(request.task, request.max_steps)
    return result


class IngestRequest(BaseModel):
    doc_id: str
    content: str
    metadata: dict | None = None


@router.post("/knowledge/ingest")
async def ingest_document(request: IngestRequest, req: Request):
    """Add a document to the RAG knowledge base."""
    engine = req.app.state.engine
    engine.ingest_document(request.doc_id, request.content, request.metadata)
    return {"status": "ingested", "doc_id": request.doc_id}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, req: Request):
    engine = req.app.state.engine
    conv = engine.get_conversation(conversation_id)
    if not conv:
        return {"error": "Conversation not found"}
    return conv


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, req: Request):
    engine = req.app.state.engine
    if engine.clear_conversation(conversation_id):
        return {"status": "deleted"}
    return {"error": "Conversation not found"}
