"""Bluesky research tool via AT Protocol API."""

from __future__ import annotations

import httpx
from crewai.tools import BaseTool

from ...config import settings

BSKY_API = "https://public.api.bsky.app"


class BlueskyResearchTool(BaseTool):
    name: str = "bluesky_research"
    description: str = (
        "Search Bluesky social platform for trending discussions "
        "and community sentiment about business topics."
    )

    def _run(self, query: str) -> str:
        try:
            client = httpx.Client(timeout=15)
            results = []

            # Search posts (public API, no auth needed for search)
            resp = client.get(
                f"{BSKY_API}/xrpc/app.bsky.feed.searchPosts",
                params={"q": query, "limit": 15},
            )

            if resp.status_code == 200:
                data = resp.json()
                for post in data.get("posts", []):
                    record = post.get("record", {})
                    text = record.get("text", "")
                    author = post.get("author", {})
                    handle = author.get("handle", "unknown")

                    results.append(
                        f"- @{handle}: {text[:300]}\n"
                        f"  Likes: {post.get('likeCount', 0)} | "
                        f"Reposts: {post.get('repostCount', 0)} | "
                        f"Replies: {post.get('replyCount', 0)}\n"
                        f"  Posted: {record.get('createdAt', 'unknown')}"
                    )
            else:
                results.append(f"Bluesky search returned status {resp.status_code}")

            client.close()
            return "\n\n".join(results[:10]) if results else f"No Bluesky results for '{query}'"

        except Exception as e:
            return f"Bluesky error: {str(e)}"
