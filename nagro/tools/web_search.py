"""NAGRO 4.1 Web Search — free, self-built, no API key needed."""

from __future__ import annotations
import logging

logger = logging.getLogger("nagro.search")


class WebSearch:
    """Synchronous web search using DuckDuckGo."""

    def search(self, query: str, max_results: int = 8) -> list[dict]:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                logger.info(f"Search '{query[:50]}' returned {len(results)} results")
                return results
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")

        try:
            return self._fallback_search(query, max_results)
        except Exception as e:
            logger.warning(f"Fallback search failed: {e}")
            return []

    def _fallback_search(self, query: str, max_results: int) -> list[dict]:
        import urllib.request
        import urllib.parse
        import re

        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        results = []
        blocks = re.findall(
            r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?'
            r'class="result__snippet"[^>]*>(.*?)</(?:td|div)',
            html, re.DOTALL
        )
        for href, title, snippet in blocks[:max_results]:
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            href = re.sub(r'.*uddg=([^&]+).*', r'\1', href)
            href = urllib.parse.unquote(href)
            if title and snippet:
                results.append({"title": title, "body": snippet, "href": href})

        logger.info(f"Fallback search returned {len(results)} results")
        return results


async def search_web(query: str, num_results: int = 5) -> list[dict]:
    ws = WebSearch()
    results = ws.search(query, num_results)
    return [
        {"title": r.get("title", ""), "link": r.get("href", ""), "snippet": r.get("body", "")}
        for r in results
    ]


async def search_news(query: str, num_results: int = 5) -> list[dict]:
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=num_results))
            return [
                {"title": r.get("title", ""), "link": r.get("url", ""),
                 "snippet": r.get("body", ""), "date": r.get("date", ""),
                 "source": r.get("source", "")}
                for r in results
            ]
    except Exception:
        return []
