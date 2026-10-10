"""Base agent class for NAGRO 4.1."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from nagro.core.prompts import NAGRO_SYSTEM_PROMPT


class BaseAgent(ABC):
    """Base class for all NAGRO agents."""

    def __init__(self, name: str, system_prompt: str = ""):
        self.name = name
        self.system_prompt = NAGRO_SYSTEM_PROMPT + "\n\n" + system_prompt

    @abstractmethod
    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        """Execute the agent's task and return the response."""
        ...

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> AsyncIterator[str]:
        """Execute with streaming output."""
        result = await self.execute(message, history, llm_client, llm_type)
        yield result

    async def _call_anthropic(
        self,
        client: Any,
        messages: list[dict],
        system: str,
        max_tokens: int = 4096,
    ) -> str:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text

    async def _call_anthropic_stream(
        self,
        client: Any,
        messages: list[dict],
        system: str,
        max_tokens: int = 4096,
    ) -> AsyncIterator[str]:
        async with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def _call_openai(
        self,
        client: Any,
        messages: list[dict],
        system: str,
        max_tokens: int = 4096,
    ) -> str:
        full_messages = [{"role": "system", "content": system}] + messages
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=full_messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def _call_openai_stream(
        self,
        client: Any,
        messages: list[dict],
        system: str,
        max_tokens: int = 4096,
    ) -> AsyncIterator[str]:
        full_messages = [{"role": "system", "content": system}] + messages
        stream = await client.chat.completions.create(
            model="gpt-4o",
            messages=full_messages,
            max_tokens=max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _call_groq(
        self,
        client: Any,
        messages: list[dict],
        system: str,
        max_tokens: int = 4096,
    ) -> str:
        full_messages = [{"role": "system", "content": system}] + messages
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def _call_llm(
        self,
        llm_client: Any,
        llm_type: str,
        messages: list[dict],
        max_tokens: int = 4096,
    ) -> str:
        if llm_client is None:
            return self._fallback_response(messages[-1]["content"] if messages else "")

        if llm_type == "anthropic":
            return await self._call_anthropic(
                llm_client, messages, self.system_prompt, max_tokens
            )
        elif llm_type == "openai":
            return await self._call_openai(
                llm_client, messages, self.system_prompt, max_tokens
            )
        elif llm_type == "groq":
            return await self._call_groq(
                llm_client, messages, self.system_prompt, max_tokens
            )
        return self._fallback_response(messages[-1]["content"] if messages else "")

    async def _call_llm_stream(
        self,
        llm_client: Any,
        llm_type: str,
        messages: list[dict],
        max_tokens: int = 4096,
    ) -> AsyncIterator[str]:
        if llm_client is None:
            yield self._fallback_response(messages[-1]["content"] if messages else "")
            return

        if llm_type == "anthropic":
            async for chunk in self._call_anthropic_stream(
                llm_client, messages, self.system_prompt, max_tokens
            ):
                yield chunk
        elif llm_type == "openai":
            async for chunk in self._call_openai_stream(
                llm_client, messages, self.system_prompt, max_tokens
            ):
                yield chunk
        else:
            yield await self._call_llm(llm_client, llm_type, messages, max_tokens)

    def _fallback_response(self, message: str) -> str:
        return (
            "⚠️ **NAGRO 4.1 - No LLM Provider Configured**\n\n"
            "I received your message but no LLM API key is configured. "
            "Please set up your API keys in the `.env` file:\n\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your API key (Anthropic, OpenAI, or Groq)\n"
            "3. Restart the server\n\n"
            f"Your message: *{message[:200]}...*" if len(message) > 200
            else f"Your message: *{message}*"
        )
