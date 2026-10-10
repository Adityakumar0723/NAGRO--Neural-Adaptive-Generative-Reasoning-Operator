"""Web search tool for NAGRO 4.1."""

from __future__ import annotations
import httpx
from nagro.core.config import settings


async def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Search the web using Serper API."""
    if not settings.serper_api_key:
        return []

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://google.serper.dev/search",
                json={"q": query, "num": num_results},
                headers={
                    "X-API-KEY": settings.serper_api_key,
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("organic", [])
    except Exception:
        return []


async def search_news(query: str, num_results: int = 5) -> list[dict]:
    """Search for news articles."""
    if not settings.serper_api_key:
        return []

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://google.serper.dev/news",
                json={"q": query, "num": num_results},
                headers={
                    "X-API-KEY": settings.serper_api_key,
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("news", [])
    except Exception:
        return []
