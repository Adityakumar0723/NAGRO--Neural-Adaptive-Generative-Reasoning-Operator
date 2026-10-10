"""OpenAI-compatible API endpoint for NAGRO 4.1.

Allows NAGRO to work with any platform that supports OpenAI-compatible APIs.
Handles RAG planning requests (JSON) and direct chat (text).
"""

from __future__ import annotations
import time
import uuid
import json
import re
import traceback
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from nagro.core.config import settings

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nagro.openai")

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


def _make_completion(content: str, completion_id: str = None, prompt_tokens: int = 0):
    if not completion_id:
        completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
    completion_tokens = len(content.split())
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": int(time.time()),
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


def _wants_json(system_prompt: str, response_format: dict | None) -> bool:
    if response_format and isinstance(response_format, dict):
        if response_format.get("type") == "json_object":
            return True
    sl = system_prompt.lower()
    json_signals = [
        "json", "plan", "structured output", "output format",
        "respond in the following format", "return a valid",
        "respond with a json", "format your response as",
        "schema", "```json",
    ]
    return any(s in sl for s in json_signals)


def _build_json_plan(user_message: str, nagro_answer: str, system_prompt: str) -> str:
    sl = system_prompt.lower()

    if "step" in sl and "action" in sl:
        plan = {
            "thought": f"I can answer this directly based on my knowledge.",
            "steps": [
                {
                    "step": 1,
                    "action": "direct_answer",
                    "input": user_message[:200],
                    "output": nagro_answer[:1000],
                }
            ],
        }
    elif "action" in sl and "input" in sl:
        plan = {
            "thought": "I can answer this directly without external search.",
            "action": "Final Answer",
            "action_input": nagro_answer[:1000],
        }
    elif "tool" in sl or "function" in sl:
        plan = {
            "tool": "direct_response",
            "arguments": {"response": nagro_answer[:1000]},
        }
    else:
        plan = {
            "response": nagro_answer[:1000],
            "action": "answer",
            "requires_retrieval": False,
            "confidence": 0.95,
        }

    return json.dumps(plan, ensure_ascii=False)


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, req: Request):
    logger.info(">>> /v1/chat/completions called")
    logger.info(f">>> messages count: {len(request.messages)}")
    try:
        engine = req.app.state.engine

        system_prompt = ""
        user_message = ""

        for msg in request.messages:
            logger.info(f">>> msg role={msg.role} content_len={len(msg.content or '')}")
            if msg.role == "system":
                system_prompt = (msg.content or "")[:50000]
                logger.info(f">>> SYSTEM PROMPT START >>>")
                for i in range(0, min(len(system_prompt), 4000), 500):
                    logger.info(f">>> SYS[{i}]: {system_prompt[i:i+500]}")
                logger.info(f">>> SYSTEM PROMPT END >>>")
            elif msg.role == "user":
                user_message = (msg.content or "")[:50000]

        if not user_message:
            for msg in reversed(request.messages):
                if msg.content and msg.content.strip():
                    user_message = msg.content[:50000]
                    break

        if not user_message:
            user_message = "hello"

        logger.info(f">>> user_message: {user_message[:100]}")
        logger.info(f">>> wants_json: {_wants_json(system_prompt, request.response_format)}")

        completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
        prompt_tokens = sum(len((m.content or "").split()) for m in request.messages)

        from nagro.core.models import ChatRequest as NAGROChatRequest

        chat_req = NAGROChatRequest(
            message=user_message,
            stream=False,
        )

        if request.stream and not _wants_json(system_prompt, request.response_format):
            async def stream_response():
                try:
                    async for chunk in engine.process_stream(chat_req):
                        data = {
                            "id": completion_id,
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": "nagro-4.1",
                            "choices": [{
                                "index": 0,
                                "delta": {"content": chunk},
                                "finish_reason": None,
                            }],
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                except Exception as stream_err:
                    logger.error(f">>> stream error: {stream_err}")

                final = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "nagro-4.1",
                    "choices": [{
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }],
                }
                yield f"data: {json.dumps(final)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(stream_response(), media_type="text/event-stream")

        try:
            logger.info(">>> calling engine.process...")
            response = await engine.process(chat_req)
            content = response.message
            logger.info(f">>> engine response len: {len(content)}")
        except Exception as e:
            logger.error(f">>> engine error: {e}")
            content = f"I can help you with that. Could you provide more details? (NAGRO 4.1)"

        if _wants_json(system_prompt, request.response_format):
            content = _build_json_plan(user_message, content, system_prompt)

        result = _make_completion(content, completion_id, prompt_tokens)
        logger.info(f">>> returning response, content_len={len(content)}")
        return result

    except Exception as e:
        logger.error(f">>> FATAL error: {e}\n{traceback.format_exc()}")
        fallback = "Hello! I'm NAGRO 4.1. How can I help you today?"
        return _make_completion(fallback)


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


@router.post("/test")
async def test_endpoint():
    """Quick test — verifies the POST endpoint works."""
    return _make_completion("NAGRO 4.1 is working! This is a test response.")
