"""Coding agent for NAGRO 4.1 — local inference."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import CODING_PROMPT


class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("coding", CODING_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        enhanced = self._enhance_coding_prompt(message)
        messages = history + [{"role": "user", "content": enhanced}]
        try:
            return self._generate(messages, max_tokens=4096)
        except Exception:
            return self._fallback_response(message)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        enhanced = self._enhance_coding_prompt(message)
        try:
            for chunk in self._generate_stream(enhanced, max_tokens=4096, history=history):
                yield chunk
        except Exception:
            yield self._fallback_response(message)

    def _enhance_coding_prompt(self, message: str) -> str:
        msg_lower = message.lower()

        if any(w in msg_lower for w in ["debug", "error", "fix", "bug", "issue"]):
            return (
                f"{message}\n\n"
                "Analyze this issue step by step:\n"
                "1. Identify the root cause\n"
                "2. Explain why it happens\n"
                "3. Provide the corrected code\n"
                "4. Suggest how to prevent similar issues"
            )

        if any(w in msg_lower for w in ["review", "improve", "optimize"]):
            return (
                f"{message}\n\n"
                "Review this code for:\n"
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
