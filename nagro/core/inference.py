"""
NAGRO 4.1 — Self-Built Inference Engine

100% NAGRO's own AI brain. No PyTorch. No Transformers. No external models.
Uses web search + NLP + reasoning for intelligent responses.
"""

from __future__ import annotations
import threading
from typing import Iterator

from nagro.core.config import settings

_lock = threading.Lock()
_brain = None


def _get_brain():
    global _brain
    if _brain is not None:
        return _brain

    with _lock:
        if _brain is not None:
            return _brain
        from nagro.core.nagro_brain import NAGROBrain
        _brain = NAGROBrain()
        return _brain


def generate(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
    stop: list[str] | None = None,
) -> str:
    brain = _get_brain()
    response = brain.think(prompt, system_prompt=system_prompt)

    if stop:
        for s in stop:
            idx = response.find(s)
            if idx != -1:
                response = response[:idx]

    return response.strip()


def generate_with_history(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> str:
    brain = _get_brain()

    prompt_parts = []
    for msg in messages:
        if msg.get("role") == "user":
            prompt_parts.append(msg.get("content", ""))

    prompt = prompt_parts[-1] if prompt_parts else ""
    history = messages if len(messages) > 1 else None

    return brain.think(prompt, system_prompt=system_prompt, history=history).strip()


def generate_stream(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    brain = _get_brain()
    yield from brain.think_stream(prompt, system_prompt=system_prompt)


def generate_stream_with_history(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    brain = _get_brain()

    prompt_parts = []
    for msg in messages:
        if msg.get("role") == "user":
            prompt_parts.append(msg.get("content", ""))

    prompt = prompt_parts[-1] if prompt_parts else ""
    history = messages if len(messages) > 1 else None

    yield from brain.think_stream(prompt, system_prompt=system_prompt, history=history)


def count_tokens(text: str) -> int:
    return len(text.split())


def is_model_loaded() -> bool:
    return _brain is not None


def unload_model():
    global _brain
    with _lock:
        _brain = None


def get_model_info() -> dict:
    return {
        "loaded": _brain is not None,
        "model": "NAGRO 4.1 Self-Built Brain",
        "engine": "NAGRO Custom Engine",
        "context_length": settings.nagro_context_length,
        "max_tokens": settings.nagro_max_tokens,
        "open_source_models": [],
        "external_paid_apis": "none",
        "data_sources": [
            "Self-Built Knowledge Base (150+ topics)",
            "Self-Built Code Generator (50+ patterns)",
            "Wikipedia API (free)",
            "DuckDuckGo Search (free)",
        ],
    }
