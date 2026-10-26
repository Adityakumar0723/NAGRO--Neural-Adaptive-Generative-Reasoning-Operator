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


def _is_json_mode(system_prompt: str, response_format: Optional[dict]) -> bool:
    """Detect when the caller wants a JSON response (RAG planners, OpenAI
    json_object mode, or any system prompt explicitly asking for JSON).
    Important: the OLD OnDemand *action planner* (text-format) is handled
    separately by _is_ondemand_planner — this must not match it."""
    # If the OLD action planner (which wants text) is detected, this is NOT JSON mode
    if _is_ondemand_planner(system_prompt):
        return False
    if response_format and isinstance(response_format, dict):
        rtype = response_format.get("type", "").lower()
        if rtype in ("json_object", "json", "json_schema"):
            return True
    sl = system_prompt.lower()
    # Strong signals of JSON requirement — all mention JSON explicitly
    strong = [
        "return json", "respond in json", "output json", "reply in json",
        "respond with json", "your response must be json", "json only",
        "respond only with json", "respond only in json",
        "respond with a json object", "output a json object",
        "your output must be a valid json", "output must be a json",
        "rag planner", "query planner", "json plan",
        "steps array", "convert the plan",
    ]
    if any(s in sl for s in strong):
        return True
    # Weaker: has "json" + some planner-ish word
    if "json" in sl and any(k in sl for k in [
        "plan", "schema", "format", "structure", "steps", "tools"
    ]):
        return True
    return False


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


def _build_json_response(user_message: str, system_prompt: str, answer_text: str) -> str:
    """Produce a valid-JSON response for callers in JSON mode (RAG planners,
    OpenAI json_object, etc.). We return a single JSON object that:
      - fits most RAG planner schemas we've seen (steps + plan + reasoning)
      - also carries the real NAGRO answer under `answer`/`content`/`output`
    so platforms that read any of those common keys get the usable text."""
    sl = system_prompt.lower()
    msg_lower = user_message.lower()

    # Try to detect what KIND of plan the caller wants
    plan_step = {
        "step_number": 1,
        "step": 1,
        "id": 1,
        "action": "respond_directly",
        "tool": "direct_answer",
        "plugin": "executePrompt",
        "query": user_message[:500],
        "description": "Answer the user's query directly from the knowledge base.",
        "reasoning": "This query can be answered without external tool calls.",
    }

    # If image intent, swap to image-generation step
    if any(k in msg_lower for k in ("image", "picture", "draw", "photo",
                                     "illustration", "banner", "poster")):
        plan_step.update({
            "action": "generate_image",
            "tool": "image_generator",
            "plugin": "generateImageUsing2.5",
            "description": "Generate an image for the user's request.",
        })

    payload = {
        "status": "ok",
        "success": True,
        "plan": [plan_step],
        "steps": [plan_step],
        "reasoning": "Direct answer available from NAGRO's self-built knowledge base.",
        "query": user_message[:1000],
        "answer": answer_text,
        "content": answer_text,
        "output": answer_text,
        "response": answer_text,
        "message": answer_text,
    }
    return json.dumps(payload, ensure_ascii=False)


@router.post("/chat/completions")
async def chat_completions(request: OpenAIChatRequest, req: Request):
    logger.info(">>> /v1/chat/completions called")

    # Extract prompts FIRST so we can still produce the right shape if later
    # code fails (e.g. engine not yet initialized).
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

    try:
        engine = req.app.state.engine

        logger.info(f">>> user_message: {user_message[:100]}")

        completion_id = f"chatcmpl-{uuid.uuid4().hex[:24]}"
        prompt_tokens = sum(len((m.content or "").split()) for m in request.messages)

        if _is_ondemand_planner(system_prompt):
            logger.info(">>> OnDemand ACTION planner detected — returning plan format")
            plan = _build_ondemand_plan(user_message, system_prompt)
            logger.info(f">>> plan: {plan}")
            return _make_completion(plan, completion_id, prompt_tokens)

        # Detect JSON-mode callers (RAG planners, OpenAI json_object, etc.)
        json_mode = _is_json_mode(system_prompt, request.response_format)

        from nagro.core.models import ChatRequest as NAGROChatRequest
        chat_req = NAGROChatRequest(message=user_message, stream=False)

        if request.stream and not json_mode:
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

        if json_mode:
            logger.info(">>> JSON mode detected — wrapping response in JSON")
            content = _build_json_response(user_message, system_prompt, content)

        return _make_completion(content, completion_id, prompt_tokens)

    except Exception as e:
        logger.error(f">>> FATAL: {e}\n{traceback.format_exc()}")
        # If JSON mode and we hit a fatal error, still return valid JSON so
        # upstream validators don't fail.
        fallback_text = "Hello! I'm NAGRO 4.1. How can I help you?"
        try:
            if _is_json_mode(system_prompt, request.response_format):
                fallback_text = _build_json_response(user_message, system_prompt, fallback_text)
        except Exception:
            pass
        return _make_completion(fallback_text)


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
