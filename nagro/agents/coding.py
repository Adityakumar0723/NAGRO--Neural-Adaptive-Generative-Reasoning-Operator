"""Coding agent for NAGRO 4.1 - Code generation, debugging, review."""

from __future__ import annotations
from typing import Any, AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import CODING_PROMPT


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("coding", CODING_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        enhanced_message = self._enhance_coding_prompt(message)
        messages = history + [{"role": "user", "content": enhanced_message}]
        return await self._call_llm(llm_client, llm_type, messages, max_tokens=8192)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> AsyncIterator[str]:
        enhanced_message = self._enhance_coding_prompt(message)
        messages = history + [{"role": "user", "content": enhanced_message}]
        async for chunk in self._call_llm_stream(
            llm_client, llm_type, messages, max_tokens=8192
        ):
            yield chunk

    def _enhance_coding_prompt(self, message: str) -> str:
        msg_lower = message.lower()

        if any(w in msg_lower for w in ["debug", "error", "fix", "bug", "issue"]):
            return (
                f"{message}\n\n"
                "Please analyze this issue step by step:\n"
                "1. Identify the root cause\n"
                "2. Explain why it happens\n"
                "3. Provide the corrected code\n"
                "4. Suggest how to prevent similar issues"
            )

        if any(w in msg_lower for w in ["review", "improve", "optimize"]):
            return (
                f"{message}\n\n"
                "Please review this code for:\n"
                "1. Bugs and potential issues\n"
                "2. Performance improvements\n"
                "3. Code style and best practices\n"
                "4. Security considerations"
            )

        return (
            f"{message}\n\n"
            "Provide complete, production-ready code with:\n"
            "- Clear structure and organization\n"
            "- Error handling where appropriate\n"
            "- Brief comments for complex logic only"
        )
