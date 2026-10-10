"""NAGRO 4.1 Model Manager — NAGRO uses its own self-built engine."""

from __future__ import annotations


def is_model_downloaded() -> bool:
    return True


def list_available_models() -> list[dict]:
    return [{
        "name": "NAGRO 4.1 Self-Built Brain",
        "key": "nagro-brain",
        "downloaded": True,
    }]


RECOMMENDED_MODELS = {
    "nagro-brain": {
        "name": "NAGRO 4.1 — Self-Built AI Brain (No external models)",
        "size": "0 GB",
        "ram": "512 MB",
        "context": "200K",
    },
}


def ensure_models_dir():
    from pathlib import Path
    Path("data").mkdir(exist_ok=True)


def download_model(model_key: str = "nagro-brain") -> str:
    return "NAGRO 4.1 Self-Built Brain — No download needed"


def download_default_model() -> str:
    return download_model()
