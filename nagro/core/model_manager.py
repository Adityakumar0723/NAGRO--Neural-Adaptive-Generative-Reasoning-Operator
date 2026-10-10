"""NAGRO 4.1 Model Manager — download and manage local models."""

from __future__ import annotations
from pathlib import Path
from rich.console import Console

from nagro.core.config import settings

console = Console()

RECOMMENDED_MODELS = {
    "tiny": {
        "name": "Qwen2.5 0.5B Instruct — Ultra-light, 128K context",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "size": "~1 GB",
        "ram": "2 GB",
        "context": "128K",
    },
    "small": {
        "name": "Qwen2.5 1.5B Instruct — Fast & capable, 128K context",
        "model_id": "Qwen/Qwen2.5-1.5B-Instruct",
        "size": "~3 GB",
        "ram": "4 GB",
        "context": "128K",
    },
    "medium": {
        "name": "Qwen2.5 3B Instruct — Balanced, 128K context",
        "model_id": "Qwen/Qwen2.5-3B-Instruct",
        "size": "~6 GB",
        "ram": "8 GB",
        "context": "128K",
    },
    "large": {
        "name": "Phi-3.5 Mini Instruct (3.8B) — Strong reasoning, 128K context",
        "model_id": "microsoft/Phi-3.5-mini-instruct",
        "size": "~7.6 GB",
        "ram": "10 GB",
        "context": "128K",
    },
    "coder": {
        "name": "Qwen2.5 Coder 1.5B Instruct — Best for coding, 128K context",
        "model_id": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "size": "~3 GB",
        "ram": "4 GB",
        "context": "128K",
    },
    "reasoning": {
        "name": "Qwen2.5 7B Instruct — Deep reasoning, 128K context",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
        "size": "~15 GB",
        "ram": "16 GB",
        "context": "128K",
    },
}


def ensure_models_dir():
    models_dir = settings.models_dir
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def is_model_downloaded() -> bool:
    try:
        from huggingface_hub import snapshot_download
        from huggingface_hub.utils import LocalEntryNotFoundError
        snapshot_download(settings.nagro_llm_model, local_files_only=True)
        return True
    except Exception:
        return False


def list_available_models() -> list[dict]:
    models = []
    for key, info in RECOMMENDED_MODELS.items():
        try:
            from huggingface_hub import snapshot_download
            snapshot_download(info["model_id"], local_files_only=True)
            models.append({
                "name": info["name"],
                "model_id": info["model_id"],
                "key": key,
                "downloaded": True,
            })
        except Exception:
            pass
    return models


def download_model(model_key: str = "small") -> str:
    from huggingface_hub import snapshot_download

    if model_key not in RECOMMENDED_MODELS:
        model_key = "small"

    model_info = RECOMMENDED_MODELS[model_key]
    model_id = model_info["model_id"]

    console.print(f"\n[bold cyan]Downloading {model_info['name']}[/bold cyan]")
    console.print(f"  Model: {model_id}")
    console.print(f"  Size: {model_info['size']}")
    console.print(f"  RAM needed: {model_info['ram']}")
    console.print(f"  Context window: {model_info['context']}")
    console.print()

    path = snapshot_download(repo_id=model_id)

    console.print(f"[green]Download complete:[/green] {model_id}")
    return model_id


def download_default_model() -> str:
    return download_model("small")
