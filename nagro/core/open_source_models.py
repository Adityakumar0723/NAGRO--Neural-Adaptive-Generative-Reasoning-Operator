"""
NAGRO 4.1 — Open Source Model Integration
Uses free inference APIs for open source models. NO API keys needed.
Models: Qwen, Mistral, Phi (NO LLaMA/Meta, NO OpenAI, NO Anthropic, NO Google)

NAGRO Brain decides WHEN to use these models.
These models provide ENHANCED answers when the knowledge base needs help.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.parse
import logging
import random
from typing import Iterator

logger = logging.getLogger("nagro.models")

# ═══════════════════════════════════════════════════════
#  FREE OPEN SOURCE MODELS (No API Key Required)
# ═══════════════════════════════════════════════════════

MODELS = {
    "mistral": {
        "name": "Mistral 7B Instruct",
        "id": "mistralai/Mistral-7B-Instruct-v0.3",
        "provider": "Mistral AI (France)",
        "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
    },
    "qwen": {
        "name": "Qwen2.5 3B Instruct",
        "id": "Qwen/Qwen2.5-3B-Instruct",
        "provider": "Alibaba (Qwen Team)",
        "url": "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-3B-Instruct",
    },
    "phi": {
        "name": "Phi-3.5 Mini Instruct",
        "id": "microsoft/Phi-3.5-mini-instruct",
        "provider": "Microsoft Research",
        "url": "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct",
    },
    "qwen-coder": {
        "name": "Qwen2.5 Coder 1.5B",
        "id": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "provider": "Alibaba (Qwen Team)",
        "url": "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-1.5B-Instruct",
    },
    "zephyr": {
        "name": "Zephyr 7B Beta",
        "id": "HuggingFaceH4/zephyr-7b-beta",
        "provider": "HuggingFace Research",
        "url": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
    },
}

DEFAULT_MODEL = "mistral"
CODE_MODEL = "qwen-coder"


def _call_model(model_key: str, prompt: str, max_tokens: int = 1024,
                temperature: float = 0.7) -> str | None:
    """Call a free open source model via HuggingFace Inference API. No API key."""
    model = MODELS.get(model_key, MODELS[DEFAULT_MODEL])
    url = model["url"]

    payload = json.dumps({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False,
        },
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "User-Agent": "NAGRO/4.1",
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and data:
                text = data[0].get("generated_text", "")
                if text:
                    return text.strip()
            elif isinstance(data, dict):
                text = data.get("generated_text", "")
                if text:
                    return text.strip()
    except urllib.error.HTTPError as e:
        if e.code == 503:
            logger.info(f"Model {model_key} is loading, trying next...")
        elif e.code == 429:
            logger.info(f"Rate limited on {model_key}, trying next...")
        else:
            logger.debug(f"Model {model_key} error {e.code}: {e.reason}")
    except Exception as e:
        logger.debug(f"Model {model_key} failed: {e}")

    return None


def generate_with_model(prompt: str, task: str = "general",
                         max_tokens: int = 1024) -> str | None:
    """
    Generate a response using open source models.
    Tries multiple models as fallback. NAGRO decides when to call this.
    Returns None if all models fail (NAGRO brain handles fallback).
    """
    if task == "code":
        order = ["qwen-coder", "qwen", "mistral", "phi"]
    elif task == "reasoning":
        order = ["mistral", "phi", "qwen", "zephyr"]
    elif task == "creative":
        order = ["zephyr", "mistral", "phi", "qwen"]
    else:
        order = ["mistral", "qwen", "phi", "zephyr"]

    for model_key in order:
        result = _call_model(model_key, prompt, max_tokens)
        if result and len(result) > 20:
            logger.info(f"Got response from {model_key} ({len(result)} chars)")
            return result

    return None


def generate_chat(messages: list[dict], task: str = "general",
                   max_tokens: int = 1024) -> str | None:
    """
    Generate from chat messages using open source models.
    Converts chat format to prompt for the model.
    """
    prompt_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            prompt_parts.append(f"[INST] <<SYS>>\n{content}\n<</SYS>>\n")
        elif role == "user":
            prompt_parts.append(f"[INST] {content} [/INST]")
        elif role == "assistant":
            prompt_parts.append(content)

    if not prompt_parts:
        return None

    prompt = "\n".join(prompt_parts)
    return generate_with_model(prompt, task, max_tokens)


def enhance_answer(question: str, knowledge: str,
                    max_tokens: int = 512) -> str | None:
    """
    Use an open source model to enhance/rewrite a knowledge base answer.
    Makes the response more natural and conversational.
    """
    prompt = (
        f"[INST] Based on this information, provide a clear and helpful answer "
        f"to the question. Be concise but thorough.\n\n"
        f"Question: {question}\n\n"
        f"Information:\n{knowledge[:2000]}\n\n"
        f"Answer: [/INST]"
    )
    return generate_with_model(prompt, "general", max_tokens)


def get_available_models() -> list[dict]:
    """Return info about available open source models."""
    return [
        {
            "key": k,
            "name": v["name"],
            "provider": v["provider"],
            "model_id": v["id"],
        }
        for k, v in MODELS.items()
    ]
