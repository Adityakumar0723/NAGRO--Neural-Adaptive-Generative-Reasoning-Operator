"""NAGRO 4.1 Model Manager — download and manage local models."""

from __future__ import annotations
import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from nagro.core.config import settings

console = Console()

RECOMMENDED_MODELS = {
    "small": {
        "name": "Phi-3 Mini (3.8B) — Fast, lightweight",
        "repo": "bartowski/Phi-3.5-mini-instruct-GGUF",
        "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf",
        "size": "~2.4 GB",
        "ram": "4 GB",
    },
    "medium": {
        "name": "Mistral 7B Instruct v0.3 — Balanced",
        "repo": "TheBloke/Mistral-7B-Instruct-v0.3-GGUF",
        "file": "mistral-7b-instruct-v0.3.Q4_K_M.gguf",
        "size": "~4.4 GB",
        "ram": "8 GB",
    },
    "large": {
        "name": "LLaMA 3.1 8B Instruct — Powerful",
        "repo": "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
        "file": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        "size": "~4.9 GB",
        "ram": "8 GB",
    },
    "xl": {
        "name": "Qwen2.5 14B Instruct — Maximum quality",
        "repo": "bartowski/Qwen2.5-14B-Instruct-GGUF",
        "file": "Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "size": "~8.7 GB",
        "ram": "16 GB",
    },
}


def ensure_models_dir():
    """Create models directory if it doesn't exist."""
    models_dir = settings.models_dir
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


def is_model_downloaded() -> bool:
    """Check if the configured LLM model is already downloaded."""
    return settings.llm_model_path.exists()


def list_available_models() -> list[dict]:
    """List all downloaded models."""
    models_dir = ensure_models_dir()
    models = []
    for f in models_dir.glob("*.gguf"):
        size_mb = f.stat().st_size / (1024 * 1024)
        models.append({
            "name": f.name,
            "path": str(f),
            "size_mb": round(size_mb, 1),
        })
    return models


def download_model(model_key: str = "medium") -> Path:
    """Download a recommended model from HuggingFace."""
    from huggingface_hub import hf_hub_download

    if model_key not in RECOMMENDED_MODELS:
        model_key = "medium"

    model_info = RECOMMENDED_MODELS[model_key]
    models_dir = ensure_models_dir()
    target_path = models_dir / model_info["file"]

    if target_path.exists():
        console.print(f"[green]Model already exists:[/green] {model_info['file']}")
        return target_path

    console.print(f"\n[bold cyan]Downloading {model_info['name']}[/bold cyan]")
    console.print(f"  Size: {model_info['size']}")
    console.print(f"  RAM needed: {model_info['ram']}")
    console.print()

    downloaded_path = hf_hub_download(
        repo_id=model_info["repo"],
        filename=model_info["file"],
        local_dir=str(models_dir),
        local_dir_use_symlinks=False,
    )

    console.print(f"[green]Download complete:[/green] {model_info['file']}")
    return Path(downloaded_path)


def download_default_model() -> Path:
    """Download the default medium model."""
    return download_model("medium")
