from __future__ import annotations

import asyncio
import logging
import re
from typing import Optional

import feedparser
import httpx
from readability import Document

logger = logging.getLogger(__name__)

USER_AGENT = "MorningCall/0.1 (personal news briefing)"


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()


async def _fetch_feed(client: httpx.AsyncClient, source: str, url: str, per_feed: int) -> list[dict]:
    articles = []
    try:
        resp = await client.get(url)
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:per_feed]:
            article = await _extract_article(client, entry, source)
            if article:
                articles.append(article)
    except Exception as e:
        logger.warning("Failed to fetch %s: %s", source, e)
    return articles


async def _extract_article(client: httpx.AsyncClient, entry: dict, source: str) -> dict | None:
    link = entry.get("link", "")
    title = entry.get("title", "")

    # Try to get full article body
    body = ""
    if link:
        try:
            resp = await client.get(link)
            doc = Document(resp.text)
            body = _strip_tags(doc.summary())[:2000]
        except Exception:
            pass

    # Fall back to feed summary/description
    if not body:
        body = _strip_tags(entry.get("summary", entry.get("description", "")))[:2000]

    if not title:
        return None

    return {
        "source": source,
        "title": title,
        "url": link,
        "published": entry.get("published", ""),
        "body": body,
    }


async def fetch_all_feeds(feeds: dict[str, str], per_feed: int = 3) -> list[dict]:
    async with httpx.AsyncClient(
        timeout=15,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        tasks = [_fetch_feed(client, source, url, per_feed) for source, url in feeds.items()]
        results = await asyncio.gather(*tasks)

    articles = [a for group in results for a in group]
    logger.info("Fetched %d articles from %d feeds", len(articles), len(feeds))
    return articles
