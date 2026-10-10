"""NAGRO 4.1 configuration — fully self-built, no external APIs."""

from __future__ import annotations
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_prefix": ""}

    # Model Identity
    model_name: str = "NAGRO 4.1"
    model_version: str = "4.1.0"

    # Local Model Paths
    nagro_model_path: str = "models/"
    nagro_llm_model: str = "mistral-7b-instruct-v0.3.Q4_K_M.gguf"
    nagro_image_model: str = "stabilityai/sdxl-turbo"
    nagro_embedding_model: str = "all-MiniLM-L6-v2"

    # Inference Settings — Opus 5.5 level context window
    nagro_context_length: int = 200000  # 200K tokens — matches top-tier models
    nagro_max_tokens: int = 16384       # 16K output tokens
    nagro_gpu_layers: int = 0
    nagro_threads: int = 4
    nagro_batch_size: int = 512
    nagro_temperature: float = 0.7
    nagro_top_p: float = 0.9
    nagro_top_k: int = 40
    nagro_repeat_penalty: float = 1.1

    # Image Generation
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
    def llm_model_path(self) -> Path:
        return Path(self.nagro_model_path) / self.nagro_llm_model

    @property
    def models_dir(self) -> Path:
        return Path(self.nagro_model_path)


settings = Settings()
