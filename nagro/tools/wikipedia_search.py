"""
NAGRO 4.1 — Wikipedia Search (Free, No API Key)
Uses Wikipedia's public API to fetch reliable information.
"""
from __future__ import annotations
import urllib.request
import urllib.parse
import json
import re
import logging

logger = logging.getLogger("nagro.wikipedia")


def search_wikipedia(query: str, sentences: int = 8) -> str | None:
    """Search Wikipedia and return a summary. Free, no API key."""
    try:
        q = urllib.parse.quote(query)
        url = (
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
        )
        req = urllib.request.Request(url, headers={
            "User-Agent": "NAGRO/4.1 (AI Assistant; educational use)",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract", "")
            if extract and len(extract) > 50:
                title = data.get("title", query)
                return f"**{title}**\n\n{extract}"
    except Exception as e:
        logger.debug(f"Wikipedia summary failed for '{query}': {e}")

    try:
        return _wiki_search_api(query, sentences)
    except Exception as e:
        logger.debug(f"Wikipedia search API failed: {e}")
        return None


def _wiki_search_api(query: str, sentences: int = 8) -> str | None:
    """Fallback: use Wikipedia opensearch + extracts API."""
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": "3",
        "format": "json",
        "utf8": "1",
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "NAGRO/4.1 (AI Assistant; educational use)",
    })
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    results = data.get("query", {}).get("search", [])
    if not results:
        return None

    titles = [r["title"] for r in results[:3]]

    params2 = urllib.parse.urlencode({
        "action": "query",
        "prop": "extracts",
        "exintro": "1",
        "explaintext": "1",
        "exsentences": str(sentences),
        "titles": "|".join(titles),
        "format": "json",
        "utf8": "1",
    })
    url2 = f"https://en.wikipedia.org/w/api.php?{params2}"
    req2 = urllib.request.Request(url2, headers={
        "User-Agent": "NAGRO/4.1 (AI Assistant; educational use)",
    })
    with urllib.request.urlopen(req2, timeout=8) as resp2:
        data2 = json.loads(resp2.read().decode("utf-8"))

    pages = data2.get("query", {}).get("pages", {})
    parts = []
    for pid, page in pages.items():
        if pid == "-1":
            continue
        title = page.get("title", "")
        extract = page.get("extract", "")
        if extract and len(extract) > 50:
            parts.append(f"**{title}**\n\n{extract}")

    if parts:
        return "\n\n---\n\n".join(parts)
    return None


def wiki_quick(topic: str) -> str | None:
    """Quick one-shot: get the best Wikipedia extract for a topic."""
    cleaned = re.sub(
        r'^(what is|what are|who is|who was|explain|define|tell me about|describe)\s+',
        '', topic, flags=re.I
    ).strip().rstrip("?.")

    result = search_wikipedia(cleaned)
    if result:
        return result

    words = cleaned.split()
    if len(words) > 3:
        short = " ".join(words[:4])
        return search_wikipedia(short)

    return None
