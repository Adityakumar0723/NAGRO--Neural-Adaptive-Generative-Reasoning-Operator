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

    # Inference Settings
    nagro_context_length: int = 4096
    nagro_max_tokens: int = 2048
    nagro_gpu_layers: int = 0
    nagro_threads: int = 4
    nagro_temperature: float = 0.7

    # Image Generation
    nagro_image_steps: int = 4
    nagro_image_width: int = 512
    nagro_image_height: int = 512

    # Server
    nagro_host: str = "0.0.0.0"
    nagro_port: int = 8000
    nagro_debug: bool = True

    # Security
    nagro_secret_key: str = "change-this-to-a-random-secret-key"

    @property
    def llm_model_path(self) -> Path:
        return Path(self.nagro_model_path) / self.nagro_llm_model

    @property
    def models_dir(self) -> Path:
        return Path(self.nagro_model_path)


settings = Settings()
