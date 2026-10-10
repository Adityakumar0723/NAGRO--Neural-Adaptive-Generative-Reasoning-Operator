"""NAGRO 4.1 Local Inference Engine — runs LLM entirely on your machine."""

from __future__ import annotations
import threading
from typing import Iterator
from pathlib import Path

from nagro.core.config import settings

_lock = threading.Lock()
_llm_instance = None


def _get_llm():
    """Lazy-load the LLM model (singleton)."""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    with _lock:
        if _llm_instance is not None:
            return _llm_instance

        from llama_cpp import Llama

        model_path = settings.llm_model_path
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                f"Run 'python -m nagro.core.model_manager' to download a model, "
                f"or place a GGUF model file in the '{settings.nagro_model_path}' directory."
            )

        _llm_instance = Llama(
            model_path=str(model_path),
            n_ctx=settings.nagro_context_length,
            n_threads=settings.nagro_threads,
            n_gpu_layers=settings.nagro_gpu_layers,
            verbose=False,
        )
        return _llm_instance


def generate(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
    stop: list[str] | None = None,
) -> str:
    """Generate a response using the local LLM."""
    llm = _get_llm()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=stop or [],
    )

    return response["choices"][0]["message"]["content"]


def generate_with_history(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> str:
    """Generate a response with conversation history."""
    llm = _get_llm()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    response = llm.create_chat_completion(
        messages=full_messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response["choices"][0]["message"]["content"]


def generate_stream(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    """Stream tokens from the local LLM."""
    llm = _get_llm()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    stream = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    for chunk in stream:
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content", "")
        if content:
            yield content


def generate_stream_with_history(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    """Stream tokens with conversation history."""
    llm = _get_llm()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    stream = llm.create_chat_completion(
        messages=full_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    for chunk in stream:
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content", "")
        if content:
            yield content


def is_model_loaded() -> bool:
    """Check if a model is currently loaded."""
    return _llm_instance is not None


def unload_model():
    """Unload the current model to free memory."""
    global _llm_instance
    with _lock:
        _llm_instance = None
