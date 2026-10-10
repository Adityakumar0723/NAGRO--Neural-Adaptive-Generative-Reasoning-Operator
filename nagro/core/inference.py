"""
NAGRO 4.1 — Self-Built Inference Engine

Runs LLM entirely on your machine using NAGRO's own inference pipeline.
No llama.cpp, no external APIs. Built on PyTorch + Transformers.
Supports 200K context window (model-dependent).
"""

from __future__ import annotations
import threading
from typing import Iterator

from nagro.core.config import settings

_lock = threading.Lock()
_model = None
_tokenizer = None


def _get_model_and_tokenizer():
    global _model, _tokenizer
    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    with _lock:
        if _model is not None and _tokenizer is not None:
            return _model, _tokenizer

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_id = settings.nagro_llm_model

        _tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True,
        )
        if _tokenizer.pad_token is None:
            _tokenizer.pad_token = _tokenizer.eos_token

        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        device_map = "auto" if torch.cuda.is_available() else "cpu"

        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            device_map=device_map,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        _model.eval()

        return _model, _tokenizer


def _build_prompt(messages: list[dict[str, str]], tokenizer) -> str:
    try:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    except Exception:
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"<|system|>\n{content}")
            elif role == "user":
                parts.append(f"<|user|>\n{content}")
            elif role == "assistant":
                parts.append(f"<|assistant|>\n{content}")
        parts.append("<|assistant|>\n")
        return "\n".join(parts)


def generate(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
    stop: list[str] | None = None,
) -> str:
    import torch

    model, tokenizer = _get_model_and_tokenizer()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    text = _build_prompt(messages, tokenizer)
    inputs = tokenizer(text, return_tensors="pt", truncation=True,
                       max_length=settings.nagro_context_length)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=max(temperature, 0.01),
            do_sample=temperature > 0,
            top_p=settings.nagro_top_p,
            top_k=settings.nagro_top_k,
            repetition_penalty=settings.nagro_repeat_penalty,
            pad_token_id=tokenizer.pad_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)

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
    import torch

    model, tokenizer = _get_model_and_tokenizer()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    text = _build_prompt(full_messages, tokenizer)
    inputs = tokenizer(text, return_tensors="pt", truncation=True,
                       max_length=settings.nagro_context_length)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=max(temperature, 0.01),
            do_sample=temperature > 0,
            top_p=settings.nagro_top_p,
            top_k=settings.nagro_top_k,
            repetition_penalty=settings.nagro_repeat_penalty,
            pad_token_id=tokenizer.pad_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def generate_stream(
    prompt: str,
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    from threading import Thread
    from transformers import TextIteratorStreamer
    import torch

    model, tokenizer = _get_model_and_tokenizer()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    text = _build_prompt(messages, tokenizer)
    inputs = tokenizer(text, return_tensors="pt", truncation=True,
                       max_length=settings.nagro_context_length)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)

    gen_kwargs = {
        **inputs,
        "max_new_tokens": max_tokens,
        "temperature": max(temperature, 0.01),
        "do_sample": temperature > 0,
        "top_p": settings.nagro_top_p,
        "top_k": settings.nagro_top_k,
        "repetition_penalty": settings.nagro_repeat_penalty,
        "pad_token_id": tokenizer.pad_token_id,
        "streamer": streamer,
    }

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    for token_text in streamer:
        if token_text:
            yield token_text

    thread.join()


def generate_stream_with_history(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> Iterator[str]:
    from threading import Thread
    from transformers import TextIteratorStreamer
    import torch

    model, tokenizer = _get_model_and_tokenizer()
    max_tokens = max_tokens or settings.nagro_max_tokens
    temperature = temperature if temperature is not None else settings.nagro_temperature

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    text = _build_prompt(full_messages, tokenizer)
    inputs = tokenizer(text, return_tensors="pt", truncation=True,
                       max_length=settings.nagro_context_length)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)

    gen_kwargs = {
        **inputs,
        "max_new_tokens": max_tokens,
        "temperature": max(temperature, 0.01),
        "do_sample": temperature > 0,
        "top_p": settings.nagro_top_p,
        "top_k": settings.nagro_top_k,
        "repetition_penalty": settings.nagro_repeat_penalty,
        "pad_token_id": tokenizer.pad_token_id,
        "streamer": streamer,
    }

    thread = Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()

    for token_text in streamer:
        if token_text:
            yield token_text

    thread.join()


def count_tokens(text: str) -> int:
    try:
        _, tokenizer = _get_model_and_tokenizer()
        return len(tokenizer.encode(text))
    except Exception:
        return len(text) // 4 + 1


def is_model_loaded() -> bool:
    return _model is not None


def unload_model():
    global _model, _tokenizer
    with _lock:
        _model = None
        _tokenizer = None


def get_model_info() -> dict:
    if not is_model_loaded():
        return {"loaded": False}

    return {
        "loaded": True,
        "model": settings.nagro_llm_model,
        "context_length": settings.nagro_context_length,
        "max_tokens": settings.nagro_max_tokens,
        "gpu_layers": settings.nagro_gpu_layers,
        "threads": settings.nagro_threads,
    }
