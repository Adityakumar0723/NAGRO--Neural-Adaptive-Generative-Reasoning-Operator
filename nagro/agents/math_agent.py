"""Math agent for NAGRO 4.1 - Mathematical problem solving."""

from __future__ import annotations
from typing import Any, AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import MATH_PROMPT


class MathAgent(BaseAgent):
    def __init__(self):
        super().__init__("math", MATH_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        enhanced_message = (
            f"{message}\n\n"
            "Solve this step by step:\n"
            "1. Understand what is being asked\n"
            "2. Identify the relevant formulas/methods\n"
            "3. Show each calculation step clearly\n"
            "4. Verify the answer\n"
            "5. Provide the final answer clearly marked"
        )
        messages = history + [{"role": "user", "content": enhanced_message}]
        return await self._call_llm(llm_client, llm_type, messages)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> AsyncIterator[str]:
        enhanced_message = (
            f"{message}\n\n"
            "Solve this step by step with clear working."
        )
        messages = history + [{"role": "user", "content": enhanced_message}]
        async for chunk in self._call_llm_stream(llm_client, llm_type, messages):
            yield chunk
