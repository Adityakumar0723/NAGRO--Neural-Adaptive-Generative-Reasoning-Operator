"""Base agent class for NAGRO 4.1 — fully self-built local inference."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import AsyncIterator

from nagro.core.prompts import NAGRO_SYSTEM_PROMPT


class BaseAgent(ABC):
    """Base class for all NAGRO agents. Uses local models only."""

    def __init__(self, name: str, system_prompt: str = ""):
        self.name = name
        self.system_prompt = NAGRO_SYSTEM_PROMPT + "\n\n" + system_prompt

    @abstractmethod
    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        ...

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        result = await self.execute(message, history)
        yield result

    def _generate(
        self,
        messages: list[dict[str, str]],
        max_tokens: int | None = None,
    ) -> str:
        """Generate using the local NAGRO inference engine."""
        from nagro.core.inference import generate_with_history
        return generate_with_history(
            messages=messages,
            system_prompt=self.system_prompt,
            max_tokens=max_tokens,
        )

    def _generate_stream(
        self,
        prompt: str,
        max_tokens: int | None = None,
    ):
        """Stream tokens from the local NAGRO inference engine."""
        from nagro.core.inference import generate_stream
        return generate_stream(
            prompt=prompt,
            system_prompt=self.system_prompt,
            max_tokens=max_tokens,
        )

    def _fallback_response(self, message: str) -> str:
        return (
            "**NAGRO 4.1 — Model Not Loaded**\n\n"
            "No local model found. To set up NAGRO:\n\n"
            "```bash\n"
            "python download_model.py\n"
            "```\n\n"
            "This will download a free, open-source model (~4 GB) that runs "
            "entirely on your machine. No API keys needed.\n\n"
            f"Your message: *{message[:200]}*"
        )
