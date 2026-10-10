"""Research agent for NAGRO 4.1 - Web research and information synthesis."""

from __future__ import annotations
from typing import Any, AsyncIterator

import httpx

from nagro.agents.base import BaseAgent
from nagro.core.config import settings
from nagro.core.prompts import RESEARCH_PROMPT


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research", RESEARCH_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> str:
        search_results = await self._web_search(message)

        enhanced_message = (
            f"User Query: {message}\n\n"
            f"Web Search Results:\n{search_results}\n\n"
            "Based on these search results and your knowledge, provide a "
            "comprehensive, well-structured response. Cite sources where applicable."
        )

        messages = history + [{"role": "user", "content": enhanced_message}]
        return await self._call_llm(llm_client, llm_type, messages, max_tokens=8192)

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
        llm_client: Any,
        llm_type: str,
    ) -> AsyncIterator[str]:
        search_results = await self._web_search(message)

        enhanced_message = (
            f"User Query: {message}\n\n"
            f"Web Search Results:\n{search_results}\n\n"
            "Based on these search results and your knowledge, provide a "
            "comprehensive, well-structured response. Cite sources where applicable."
        )

        messages = history + [{"role": "user", "content": enhanced_message}]
        async for chunk in self._call_llm_stream(
            llm_client, llm_type, messages, max_tokens=8192
        ):
            yield chunk

    async def _web_search(self, query: str) -> str:
        if not settings.serper_api_key:
            return "[Web search unavailable - no SERPER_API_KEY configured]"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    "https://google.serper.dev/search",
                    json={"q": query, "num": 5},
                    headers={
                        "X-API-KEY": settings.serper_api_key,
                        "Content-Type": "application/json",
                    },
                )
                response.raise_for_status()
                data = response.json()

            results = []
            for i, item in enumerate(data.get("organic", [])[:5], 1):
                results.append(
                    f"{i}. **{item.get('title', 'N/A')}**\n"
                    f"   URL: {item.get('link', 'N/A')}\n"
                    f"   {item.get('snippet', 'No description')}\n"
                )

            if data.get("answerBox"):
                box = data["answerBox"]
                results.insert(0, f"**Quick Answer:** {box.get('answer', box.get('snippet', ''))}\n")

            return "\n".join(results) if results else "[No results found]"
        except Exception as e:
            return f"[Search error: {e}]"
