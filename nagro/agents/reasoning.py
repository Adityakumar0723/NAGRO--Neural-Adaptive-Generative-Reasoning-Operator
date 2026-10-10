"""Reasoning agent for NAGRO 4.1 - General chat and reasoning tasks."""

from __future__ import annotations
from typing import Any, AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import REASONING_PROMPT


class ReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__("reasoning", REASONING_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        messages = history + [{"role": "user", "content": message}]
        return await self._call_llm(llm_client, llm_type, messages)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> AsyncIterator[str]:
        messages = history + [{"role": "user", "content": message}]
        async for chunk in self._call_llm_stream(llm_client, llm_type, messages):
            yield chunk
