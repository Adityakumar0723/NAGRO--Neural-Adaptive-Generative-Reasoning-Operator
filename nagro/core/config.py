"""NAGRO 4.1 configuration management."""

from __future__ import annotations
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_prefix": ""}

    # Model Identity
    model_name: str = "NAGRO 4.1"
    model_version: str = "4.1.0"

    # LLM Provider
    nagro_llm_provider: str = Field(default="anthropic")
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Image Generation
    nagro_image_provider: str = Field(default="openai")
    stability_api_key: Optional[str] = None
    replicate_api_key: Optional[str] = None

    # Web Search
    serper_api_key: Optional[str] = None

    # Server
    nagro_host: str = "0.0.0.0"
    nagro_port: int = 8000
    nagro_debug: bool = True

    # Security
    nagro_secret_key: str = "change-this-to-a-random-secret-key"
    nagro_api_key: Optional[str] = None

    # Rate Limiting
    nagro_rate_limit: int = 60
    nagro_rate_window: int = 60

    def get_llm_api_key(self) -> str | None:
        providers = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
            "groq": self.groq_api_key,
        }
        return providers.get(self.nagro_llm_provider)

    def get_image_api_key(self) -> str | None:
        providers = {
            "openai": self.openai_api_key,
            "stability": self.stability_api_key,
            "replicate": self.replicate_api_key,
        }
        return providers.get(self.nagro_image_provider)


settings = Settings()
