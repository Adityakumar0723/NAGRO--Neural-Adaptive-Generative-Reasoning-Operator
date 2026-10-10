"""Math agent for NAGRO 4.1 — local inference."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import MATH_PROMPT


class MathAgent(BaseAgent):
    def __init__(self):
        super().__init__("math", MATH_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        enhanced = (
            f"{message}\n\n"
            "Solve this step by step:\n"
            "1. Understand what is being asked\n"
            "2. Identify the relevant formulas/methods\n"
            "3. Show each calculation step clearly\n"
            "4. Verify the answer\n"
            "5. Provide the final answer clearly marked"
        )
        messages = history + [{"role": "user", "content": enhanced}]
        try:
            return self._generate(messages)
        except FileNotFoundError:
            return self._fallback_response(message)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        enhanced = (
            f"{message}\n\nSolve this step by step with clear working."
        )
        try:
            for chunk in self._generate_stream(enhanced):
                yield chunk
        except FileNotFoundError:
            yield self._fallback_response(message)
