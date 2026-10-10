"""OpenAI-compatible API endpoint for NAGRO 4.1.

Allows NAGRO to work with any platform that supports OpenAI-compatible APIs.
Handles RAG planning requests (JSON) and direct chat (text).
"""

from __future__ import annotations
import time
import uuid
import json
import re
from typing import Optional

from fastapi import APIRouter, Request, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from nagro.core.models import ChatRequest
from nagro.core.config import settings

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
    response_format: Optional[dict] = None


def _wants_json(system_prompt: str, response_format: dict | None) -> bool:
    if response_format and response_format.get("type") == "json_object":
        return True
    sl = system_prompt.lower()
    json_signals = [
        "json", "plan", "structured output", "output format",
        "respond in the following format", "return a valid",
        "respond with a json", "format your response as",
        "parse", "schema", "```json",
    ]
    return any(s in sl for s in json_signals)


def _extract_json_schema_hint(system_prompt: str) -> str | None:
    patterns = [
        r'```json\s*(\{[^`]+\})\s*```',
        r'example[:\s]*(\{[^}]+\})',
        r'format[:\s]*(\{[^}]+\})',
        r'(\{["\']?\w+["\']?\s*:\s*[^}]+\})',
    ]
    for pat in patterns:
        match = re.search(pat, system_prompt, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
    return None


def _build_json_plan(user_message: str, nagro_answer: str, system_prompt: str) -> str:
    schema_hint = _extract_json_schema_hint(system_prompt)
    sl = system_prompt.lower()

    if "step" in sl and "action" in sl:
        plan = {
            "thought": f"The user asked: {user_message[:100]}. I can answer this directly.",
            "steps": [
                {
                    "step": 1,
                    "action": "direct_answer",
                    "input": user_message,
                    "output": nagro_answer[:500],
                }
            ],
        }
    elif "action" in sl and "input" in sl:
        plan = {
            "thought": f"I can answer this directly without external search.",
            "action": "Final Answer",
            "action_input": nagro_answer[:500],
        }
    elif "plan" in sl:
        plan = {
            "can_answer_directly": True,
            "needs_search": False,
            "plan": [],
            "response": nagro_answer[:500],
        }
    elif "tool" in sl or "function" in sl:
        plan = {
            "tool": "direct_response",
            "arguments": {"response": nagro_answer[:500]},
        }
    else:
        plan = {
            "response": nagro_answer[:500],
            "action": "answer",
            "requires_retrieval": False,
            "confidence": 0.95,
        }

    return json.dumps(plan, ensure_ascii=False)


def _truncate_messages(messages: list[OpenAIMessage], max_chars: int = 50000) -> tuple[str, str]:
    system_prompt = ""
    user_message = ""
    all_user_parts = []

    for msg in messages:
        if msg.role == "system":
            system_prompt = msg.content[:max_chars]
        elif msg.role == "user":
            all_user_parts.append(msg.content)
        elif msg.role == "assistant":
            pass

    if all_user_parts:
        user_message = all_user_parts[-1]
    elif messages:
        user_message = messages[-1].content

    if len(user_message) > max_chars:
        user_message = user_message[:max_chars]

    return system_prompt, user_message


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, req: Request):
    engine = req.app.state.engine

    system_prompt, user_message = _truncate_messages(request.messages)

    if not user_message:
        user_message = "hello"

    chat_req = ChatRequest(
        message=user_message,
        stream=False,
    )

    completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    created = int(time.time())

    if request.stream and not _wants_json(system_prompt, request.response_format):
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
    content = response.message

    if _wants_json(system_prompt, request.response_format):
        content = _build_json_plan(user_message, content, system_prompt)

    prompt_tokens = sum(len(m.content.split()) for m in request.messages)
    completion_tokens = len(content.split())

    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": "nagro-4.1",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content,
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
            "context_window": settings.nagro_context_length,
            "max_tokens": settings.nagro_max_tokens,
        }],
    }


@router.get("/models/nagro-4.1")
async def get_model():
    return {
        "id": "nagro-4.1",
        "object": "model",
        "created": 1700000000,
        "owned_by": "nagro",
        "permission": [],
        "root": "nagro-4.1",
        "parent": None,
        "context_window": settings.nagro_context_length,
        "max_tokens": settings.nagro_max_tokens,
    }
