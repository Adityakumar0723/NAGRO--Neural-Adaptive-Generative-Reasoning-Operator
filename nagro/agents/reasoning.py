"""Reasoning agent for NAGRO 4.1 — local inference."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import REASONING_PROMPT


class ReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__("reasoning", REASONING_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        messages = history + [{"role": "user", "content": message}]
        try:
            return self._generate(messages)
        except Exception:
            return self._fallback_response(message)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        try:
            for chunk in self._generate_stream(message):
                yield chunk
        except Exception:
            yield self._fallback_response(message)
