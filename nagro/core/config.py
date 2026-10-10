"""NAGRO 4.1 configuration — 100% self-built, no external models or APIs."""

from __future__ import annotations
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_prefix": ""}

    # Model Identity
    model_name: str = "NAGRO 4.1"
    model_version: str = "4.1.0"

    # NAGRO Engine Settings (no external models needed)
    nagro_context_length: int = 200000
    nagro_max_tokens: int = 16384
    nagro_temperature: float = 0.7
    nagro_top_p: float = 0.9
    nagro_top_k: int = 40
    nagro_repeat_penalty: float = 1.1
    nagro_gpu_layers: int = 0
    nagro_threads: int = 4
    nagro_batch_size: int = 512

    # Image Generation (NAGRO's own procedural engine)
    nagro_image_steps: int = 4
    nagro_image_width: int = 1024
    nagro_image_height: int = 1024

    # Server
    nagro_host: str = "0.0.0.0"
    nagro_port: int = 8000
    nagro_debug: bool = True
    nagro_max_upload_mb: int = 100

    # Security
    nagro_secret_key: str = "change-this-to-a-random-secret-key"

    @property
    def models_dir(self) -> Path:
        return Path("data/")


settings = Settings()
