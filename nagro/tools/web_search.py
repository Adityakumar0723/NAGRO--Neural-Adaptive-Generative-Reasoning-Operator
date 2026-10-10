"""NAGRO 4.1 Web Search — free, self-built, no API key needed."""

from __future__ import annotations


async def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Search the web using DuckDuckGo (free, no API key)."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", ""),
                }
                for r in results
            ]
    except Exception:
        return []


async def search_news(query: str, num_results: int = 5) -> list[dict]:
    """Search for news using DuckDuckGo (free, no API key)."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=num_results))
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source": r.get("source", ""),
                }
                for r in results
            ]
    except Exception:
        return []


async def fetch_page_content(url: str) -> str:
    """Fetch and extract text content from a web page."""
    try:
        import httpx
        from bs4 import BeautifulSoup
        from markdownify import markdownify

        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(url, headers={
                "User-Agent": "NAGRO/4.1 Research Agent"
            })
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = markdownify(str(soup.body or soup), strip=["img", "a"])
        # Truncate to reasonable length
        if len(text) > 5000:
            text = text[:5000] + "\n\n[Content truncated...]"
        return text
    except Exception as e:
        return f"[Failed to fetch: {e}]"
