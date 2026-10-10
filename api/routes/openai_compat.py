"""OpenAI-compatible API endpoint for NAGRO 4.1.

Allows NAGRO to work with any platform that supports OpenAI-compatible APIs.
Endpoint: POST /v1/chat/completions
"""

from __future__ import annotations
import time
import uuid
import json
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from nagro.core.models import ChatRequest

router = APIRouter()


class OpenAIMessage(BaseModel):
    role: str = "user"
    content: str = ""


class OpenAIChatRequest(BaseModel):
    model: str = "nagro-4.1"
    messages: list[OpenAIMessage] = []
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    stream: Optional[bool] = False
    stop: Optional[list[str]] = None
    n: Optional[int] = 1


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, req: Request):
    engine = req.app.state.engine

    user_message = ""
    system_prompt = ""
    for msg in request.messages:
        if msg.role == "user":
            user_message = msg.content
        elif msg.role == "system":
            system_prompt = msg.content

    if not user_message and request.messages:
        user_message = request.messages[-1].content

    chat_req = ChatRequest(
        message=user_message,
        stream=request.stream or False,
    )

    completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())

    if request.stream:
        async def stream_response():
            async for chunk in engine.process_stream(chat_req):
                data = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": "nagro-4.1",
                    "choices": [{
                        "index": 0,
                        "delta": {"content": chunk},
                        "finish_reason": None,
                    }],
                }
                yield f"data: {json.dumps(data)}\n\n"

            final = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": "nagro-4.1",
                "choices": [{
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }],
            }
            yield f"data: {json.dumps(final)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            stream_response(),
            media_type="text/event-stream",
        )

    response = await engine.process(chat_req)

    prompt_tokens = len(user_message.split())
    completion_tokens = len(response.message.split())

    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": "nagro-4.1",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response.message,
            },
            "finish_reason": "stop",
        }],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


@router.get("/models")
async def list_models():
    return {
        "object": "list",
        "data": [{
            "id": "nagro-4.1",
            "object": "model",
            "created": 1700000000,
            "owned_by": "nagro",
            "permission": [],
            "root": "nagro-4.1",
            "parent": None,
        }],
    }
