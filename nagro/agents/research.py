"""Research agent for NAGRO 4.1 — self-built web search, no API keys."""

from __future__ import annotations
from typing import AsyncIterator

from nagro.agents.base import BaseAgent
from nagro.core.prompts import RESEARCH_PROMPT


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("research", RESEARCH_PROMPT)

    async def execute(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> str:
        search_results = await self._web_search(message)

        enhanced = (
            f"User Query: {message}\n\n"
            f"Web Search Results:\n{search_results}\n\n"
            "Based on these search results and your knowledge, provide a "
            "comprehensive, well-structured response with source citations."
        )

        messages = history + [{"role": "user", "content": enhanced}]
        try:
            return self._generate(messages, max_tokens=4096)
        except FileNotFoundError:
            return (
                f"**NAGRO 4.1 Research Results**\n\n"
                f"**Query:** {message}\n\n"
                f"{search_results}\n\n"
                f"*Note: LLM model not loaded. Showing raw search results. "
                f"Run `python download_model.py` to enable AI-powered analysis.*"
            )

    async def execute_stream(
        self,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        result = await self.execute(message, history)
        yield result

    async def _web_search(self, query: str) -> str:
        """Search the web using DuckDuckGo (free, no API key)."""
        from nagro.tools.web_search import search_web

        try:
            results = await search_web(query, num_results=5)
            if not results:
                return "[No search results found]"

            formatted = []
            for i, item in enumerate(results, 1):
                formatted.append(
                    f"{i}. **{item.get('title', 'N/A')}**\n"
                    f"   URL: {item.get('link', 'N/A')}\n"
                    f"   {item.get('snippet', 'No description')}\n"
                )
            return "\n".join(formatted)
        except Exception as e:
            return f"[Search error: {e}]"
