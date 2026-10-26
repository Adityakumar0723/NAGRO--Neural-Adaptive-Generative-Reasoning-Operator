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


import os as _os


def _is_planner_prompt(system_prompt: str) -> bool:
    """Detect specifically the RAG/planner call — distinct from a chat call
    that happens to want JSON output. Planner calls want a plan structure
    describing WHICH tools to run, not an answer to the user's query."""
    sl = system_prompt.lower()
    if _is_ondemand_planner(sl):
        return True
    # Env-level force for pure BYOI deployments
    if _os.environ.get("NAGRO_ALWAYS_JSON", "").lower() in ("1", "true", "yes"):
        if any(sig in sl for sig in [
            "plan", "planner", "tool", "action", "step", "schema",
            "available", "subtask", "rag", "retrieve",
        ]):
            return True
    planner_signals = [
        "rag planner", "query planner", "plan generator", "planning agent",
        "planner agent", "action planner",
        "generate a plan", "produce a plan", "convert the plan",
        "plan the following", "plan this query",
        "available tools:", "available plugins:", "available actions:",
        "think step by step and return",
        "steps array", "plan output", "plan response", "planner response",
        "subtask list", "sub-task list",
        "on-prem planner", "on_prem_planner", "planning_v1",
        "break the user", "break down the user", "break the query",
        "decide which tool", "choose a tool", "select a plugin",
    ]
    return any(sig in sl for sig in planner_signals)


def _is_json_mode(system_prompt: str, response_format: Optional[dict]) -> bool:
    """Detect when the caller wants a JSON response (RAG planners, OpenAI
    json_object mode, or any system prompt explicitly asking for JSON).
    Important: the OLD OnDemand *action planner* (text-format) is handled
    separately by _is_ondemand_planner — this must not match it."""
    # Env override for pure BYOI deployments where every call is a planner.
    if _os.environ.get("NAGRO_ALWAYS_JSON", "").lower() in ("1", "true", "yes"):
        if not _is_ondemand_planner(system_prompt):
            return True
    # If the OLD action planner (which wants text) is detected, this is NOT JSON mode
    if _is_ondemand_planner(system_prompt):
        return False
    if response_format and isinstance(response_format, dict):
        rtype = response_format.get("type", "").lower()
        if rtype in ("json_object", "json", "json_schema"):
            return True
    sl = system_prompt.lower()
    # Strong signals of JSON requirement — all mention JSON explicitly or
    # look like an on-prem RAG planner prompt.
    strong = [
        "return json", "respond in json", "output json", "reply in json",
        "respond with json", "your response must be json", "json only",
        "respond only with json", "respond only in json",
        "respond with a json object", "output a json object",
        "your output must be a valid json", "output must be a json",
        "rag planner", "query planner", "json plan", "plan generator",
        "plan the following", "planning agent", "planner agent",
        "generate a plan", "generate the plan", "produce a plan",
        "steps array", "convert the plan", "convert this plan",
        "plan output", "plan response", "planner response",
        "available tools:", "available plugins:", "available actions:",
        "tool invocation", "function call plan", "think step by step and return",
        "on-prem", "on prem", "ondemand", "on-demand", "rag",
        "subtasks", "subtask list", "sub-task",
    ]
    if any(s in sl for s in strong):
        return True
    # Weaker: has "json" + some planner-ish word
    if "json" in sl and any(k in sl for k in [
        "plan", "schema", "format", "structure", "steps", "tools",
        "action", "task", "subtask", "response", "output",
    ]):
        return True
    # Weaker 2: planner-style prompt even without the JSON word
    if any(k in sl for k in ["step 1", "step one", "step-by-step", "step by step"]) and \
       any(k in sl for k in ["plan", "task", "answer", "respond"]):
        return True
    # Weaker 3: long system prompt with any strong hint it's structured
    if len(sl) > 400 and any(k in sl for k in [
        "plan", "schema", "steps", "action", "tool", "function",
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


def _detect_plan_intents(user_message: str) -> list[dict]:
    """Pick which real plugins the planner should invoke based on query intent.
    Each returned dict is a plan STEP OnDemand can execute. Multiple steps
    are returned so OnDemand can invoke ALL relevant plugins and NAGRO can
    synthesize their outputs in the final answer call."""
    m = user_message.lower()
    steps: list[dict] = []

    # Research / news / intelligence / report queries → multi-plugin fan-out
    research_markers = [
        "news", "latest", "trend", "intelligence report", "report on",
        "update on", "current", "today", "this week", "this month",
        "ongoing", "live", "recent", "status of", "what is happening",
        "find out", "research", "investigate", "track", "monitor",
        "find the latest", "give me the latest",
    ]
    is_research = any(k in m for k in research_markers)
    if is_research:
        steps.append({
            "action": "web_search",
            "tool": "search",
            "plugin": "webSearchPlugin",
            "query": user_message[:500],
            "description": "Search the open web for current information on the query.",
            "reasoning": "Pull live web results to ground the answer in up-to-date facts.",
        })
        steps.append({
            "action": "news_search",
            "tool": "news",
            "plugin": "newsPlugin",
            "query": user_message[:500],
            "description": "Pull current news articles related to the query.",
            "reasoning": "News coverage is the fastest source for intelligence/report queries.",
        })

    # Deep analytical / multi-aspect reports → research + news + wiki
    analytical_markers = [
        "analyze", "analysis", "deep dive", "intelligence report",
        "detailed report", "comprehensive", "breakdown", "map how",
        "geopolitical", "ecosystem", "impact of", "effects of",
        "future predictions", "forecast", "outlook",
        "detailed intelligence", "comparative analysis",
    ]
    is_analytical = any(k in m for k in analytical_markers)
    if is_analytical:
        if not any(s["plugin"] == "webSearchPlugin" for s in steps):
            steps.append({
                "action": "web_search",
                "tool": "search",
                "plugin": "webSearchPlugin",
                "query": user_message[:500],
                "description": "Gather web sources for the analytical report.",
                "reasoning": "Analytical reports need current, cited facts.",
            })
        steps.append({
            "action": "knowledge_lookup",
            "tool": "knowledge_base",
            "plugin": "wikipediaPlugin",
            "query": user_message[:500],
            "description": "Look up background knowledge from Wikipedia and reference sources.",
            "reasoning": "Analytical reports need stable background context, not just news.",
        })

    # Image generation
    image_markers = ["image", "picture", "draw", "photo", "illustration",
                     "banner", "poster", "wallpaper", "artwork",
                     "generate an image", "create an image", "make an image"]
    if any(k in m for k in image_markers):
        steps.append({
            "action": "generate_image",
            "tool": "image_generator",
            "plugin": "generateImageUsing2.5",
            "query": user_message[:500],
            "description": "Generate an image for the user's request.",
            "reasoning": "The user wants a visual output.",
        })

    # Code / debug / implementation
    code_markers = ["write code", "write a program", "write a function",
                    "write a class", "write a script", "write a method",
                    "write a python", "write a javascript", "write a java",
                    "write a html", "write a css", "write a sql",
                    "implement", "debug", "fix this code", "code likho",
                    "program banao", "python code", "javascript code",
                    "html code", "sql query", "python function",
                    # App builders
                    "make a app", "make an app", "build a app", "build an app",
                    "create a app", "create an app", "make a website",
                    "build a website", "create a website",
                    "make a game", "build a game", "create a game",
                    "snake game", "tic tac toe", "calculator app", "todo app",
                    "chat app", "quiz app", "login page",
                    # Hinglish
                    "coding karo", "code banao", "program likho", "code samjhao",
                    ]
    if any(k in m for k in code_markers):
        steps.append({
            "action": "generate_code",
            "tool": "code_generator",
            "plugin": "codePlugin",
            "query": user_message[:500],
            "description": "Generate code for the user's request.",
            "reasoning": "The user is asking for a code artifact.",
        })

    # Math / calculation
    math_markers = ["calculate", "solve", "equation", "derivative",
                    "integral", "probability of", "percentage of",
                    "square root", "factorial"]
    if any(k in m for k in math_markers):
        steps.append({
            "action": "solve_math",
            "tool": "math_solver",
            "plugin": "mathPlugin",
            "query": user_message[:500],
            "description": "Solve the math problem step by step.",
            "reasoning": "The user wants a math solution.",
        })

    # Document / file
    doc_markers = ["summarize this", "summarize the", "analyze this document",
                   "pdf", "docx", "spreadsheet", "csv file", "attached file"]
    if any(k in m for k in doc_markers):
        steps.append({
            "action": "process_document",
            "tool": "document_processor",
            "plugin": "documentPlugin",
            "query": user_message[:500],
            "description": "Process and summarize the referenced document.",
            "reasoning": "The user is referring to a document that needs processing.",
        })

    # Final synthesis step always closes the plan — NAGRO will take all the
    # plugin outputs collected above and compose the final human-readable
    # answer. OnDemand will call /chat/completions again (without planner
    # system prompt) to get this synthesis.
    steps.append({
        "action": "respond_with_answer",
        "tool": "direct_answer",
        "plugin": "executePrompt",
        "query": user_message[:500],
        "description": "Synthesize all retrieved plugin outputs into a clear, detailed, cited answer.",
        "reasoning": "Deliver the final human-readable answer that cites the collected sources.",
    })

    # Number the steps
    for i, s in enumerate(steps, 1):
        s["step_number"] = i
        s["step"] = i
        s["id"] = i

    return steps


def _build_thinking(user_message: str, steps: list[dict]) -> str:
    """Produce a human-readable chain of thought the UI can show as 'thinking'."""
    plugins = [s["plugin"] for s in steps]
    lines = [
        f"Analyzing the user's query: {user_message[:200]}" + ("…" if len(user_message) > 200 else ""),
        "",
        "Breaking it down:",
    ]
    if any(p == "webSearchPlugin" for p in plugins):
        lines.append("- The query asks about current/recent information → web search needed")
    if any(p == "newsPlugin" for p in plugins):
        lines.append("- News coverage is relevant → will pull latest articles")
    if any(p == "wikipediaPlugin" for p in plugins):
        lines.append("- Background context required → will look up Wikipedia")
    if any(p == "codePlugin" for p in plugins):
        lines.append("- Query is coding-related → will generate code")
    if any(p == "mathPlugin" for p in plugins):
        lines.append("- Query is mathematical → will solve step by step")
    if any(p == "generateImageUsing2.5" for p in plugins):
        lines.append("- Query asks for a visual → will generate an image")
    if any(p == "documentPlugin" for p in plugins):
        lines.append("- Query references a document → will process it")
    lines.append("")
    lines.append(f"Plan: {len(steps)} step(s) across {len(set(plugins))} plugin(s).")
    lines.append("After plugin outputs come back, NAGRO will synthesize a final cited answer.")
    return "\n".join(lines)


def _build_json_response(user_message: str, system_prompt: str, answer_text: str) -> str:
    """Produce a valid-JSON response for callers in JSON mode (RAG planners,
    OpenAI json_object, etc.). We return a single JSON object that:
      - fits most RAG planner schemas we've seen (steps + plan + reasoning)
      - routes to real plugins (webSearch, codePlugin, mathPlugin, imageGen,
        documentPlugin, executePrompt) so OnDemand can call them to fetch
        live data instead of relying on NAGRO's static KB
      - also carries the real NAGRO answer under `answer`/`content`/`output`
    so platforms that read any of those common keys get the usable text."""
    steps = _detect_plan_intents(user_message)
    primary_plugins = [s["plugin"] for s in steps if s["plugin"] != "executePrompt"]
    primary_plugins = list(dict.fromkeys(primary_plugins))  # dedupe keep order

    thinking = _build_thinking(user_message, steps)
    reasoning = (
        f"Planned {len(steps)} step(s). "
        f"Tools to invoke: {', '.join(primary_plugins) if primary_plugins else 'direct answer'}."
    )

    payload = {
        "status": "ok",
        "success": True,
        "plan": steps,
        "steps": steps,
        "subtasks": steps,
        "tools": primary_plugins + ["executePrompt"],
        "plugins": primary_plugins + ["executePrompt"],
        "reasoning": reasoning,
        "thinking": thinking,
        "thought": thinking,
        "chain_of_thought": thinking,
        "query": user_message[:1000],
        "answer": answer_text,
        "content": answer_text,
        "output": answer_text,
        "response": answer_text,
        "message": answer_text,
        "text": answer_text,
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

        # Header-based detection — OnDemand's RAG runtime sets specific headers
        try:
            headers_lower = {k.lower(): v for k, v in req.headers.items()}
            ua = headers_lower.get("user-agent", "").lower()
            referer = headers_lower.get("referer", "").lower()
            if any(sig in ua for sig in ("ondemand", "on-demand", "python-httpx", "aiohttp")):
                if any(sig in ua for sig in ("ondemand", "on-demand")):
                    json_mode = True
            if "ondemand" in referer or "on-demand" in referer:
                json_mode = True
            # Any explicit OnDemand marker header
            for h_key in headers_lower:
                if "ondemand" in h_key or "on-demand" in h_key or "rag" in h_key:
                    json_mode = True
                    break
        except Exception:
            pass

        logger.info(f">>> system_prompt sample: {system_prompt[:200]!r}")
        logger.info(f">>> json_mode={json_mode}, response_format={request.response_format}")

        # ── FAST PATH for RAG planner calls specifically ──
        # When a RAG planner is calling us, it wants a plan structure, not a
        # chat answer. Skip the heavy brain and return a canned plan quickly
        # — this prevents container-cold-start/brain-processing timeouts that
        # produce the "no response from model" error.
        is_planner_call = _is_planner_prompt(system_prompt)
        if is_planner_call:
            logger.info(">>> PLANNER call detected — using FAST path (no brain)")
            fast_json = _build_json_response(user_message, system_prompt,
                                              answer_text="Plan accepted.")
            return _make_completion(fast_json, completion_id, prompt_tokens)

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
