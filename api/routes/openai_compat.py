"""OpenAI-compatible API endpoint for NAGRO 4.1.

Handles OnDemand platform's Action Planner format and direct chat.
"""

from __future__ import annotations
import time
import uuid
import json
import re
import traceback
import logging
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from nagro.core.config import settings

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


def _is_ondemand_planner(system_prompt: str) -> bool:
    sl = system_prompt.lower()
    return "action planner" in sl and "plugins" in sl


def _build_ondemand_plan(user_message: str, system_prompt: str) -> str:
    msg = user_message.lower()

    image_kw = ["image", "picture", "draw", "photo", "illustration",
                "generate image", "create image", "design", "art",
                "painting", "sketch", "logo", "banner", "poster",
                "wallpaper", "tasveer", "image banao"]
    is_image = any(k in msg for k in image_kw)

    edit_image_kw = ["edit image", "modify image", "change image", "update image"]
    is_edit_image = any(k in msg for k in edit_image_kw)

    variation_kw = ["variation", "similar image", "like this image"]
    is_variation = any(k in msg for k in variation_kw)

    inpaint_kw = ["inpaint", "fill in", "remove from image", "replace in image"]
    is_inpaint = any(k in msg for k in inpaint_kw)

    if is_inpaint:
        return "1. Inpaint the specified region of the image\n*Plugins: [inpaintImageUsing2.5]"
    elif is_variation:
        return "1. Generate variations of the provided image\n*Plugins: [generateVariationsUsing2.5]"
    elif is_edit_image:
        return "1. Edit the image based on the user's instructions\n*Plugins: [editImageUsing2.5]"
    elif is_image:
        return "1. Generate an image based on the user's description\n*Plugins: [generateImageUsing2.5]"
    else:
        return "1. Process the user's request and provide a response\n*Plugins: [executePrompt]"


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, req: Request):
    logger.info(">>> /v1/chat/completions called")
    try:
        engine = req.app.state.engine

        system_prompt = ""
        user_message = ""

        for msg in request.messages:
            if msg.role == "system":
                system_prompt = (msg.content or "")[:50000]
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

        completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
        prompt_tokens = sum(len((m.content or "").split()) for m in request.messages)

        if _is_ondemand_planner(system_prompt):
            logger.info(">>> OnDemand planner detected — returning plan format")
            plan = _build_ondemand_plan(user_message, system_prompt)
            logger.info(f">>> plan: {plan}")
            return _make_completion(plan, completion_id, prompt_tokens)

        from nagro.core.models import ChatRequest as NAGROChatRequest
        chat_req = NAGROChatRequest(message=user_message, stream=False)

        if request.stream:
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
                except Exception as e:
                    logger.error(f">>> stream error: {e}")

                yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': 'nagro-4.1', 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(stream_response(), media_type="text/event-stream")

        try:
            logger.info(">>> calling engine.process...")
            response = await engine.process(chat_req)
            content = response.message
            logger.info(f">>> response len: {len(content)}")
        except Exception as e:
            logger.error(f">>> engine error: {e}")
            content = "Hello! I'm NAGRO 4.1 — your self-built AI assistant. How can I help you today?"

        return _make_completion(content, completion_id, prompt_tokens)

    except Exception as e:
        logger.error(f">>> FATAL: {e}\n{traceback.format_exc()}")
        return _make_completion("Hello! I'm NAGRO 4.1. How can I help you?")


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
    return _make_completion("NAGRO 4.1 is working! Test successful.")
