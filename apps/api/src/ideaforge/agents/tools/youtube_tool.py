"""YouTube research tool via Data API v3."""

from __future__ import annotations

from crewai.tools import BaseTool

from ...config import settings


class YouTubeResearchTool(BaseTool):
    name: str = "youtube_research"
    description: str = (
        "Search YouTube for trending videos, channels, and engagement "
        "metrics related to a business topic."
    )

    def _run(self, query: str) -> str:
        if not settings.youtube_api_key:
            return "YouTube tool: YOUTUBE_API_KEY not configured"

        try:
            from googleapiclient.discovery import build

            youtube = build("youtube", "v3", developerKey=settings.youtube_api_key)

            # Search for videos
            search_resp = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                order="relevance",
                maxResults=10,
            ).execute()

            video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]

            # Get video statistics
            stats_resp = youtube.videos().list(
                id=",".join(video_ids),
                part="statistics,snippet",
            ).execute()

            results = []
            for video in stats_resp.get("items", []):
                snippet = video["snippet"]
                stats = video.get("statistics", {})
                results.append(
                    f"- {snippet['title']}\n"
                    f"  Channel: {snippet['channelTitle']}\n"
                    f"  Views: {stats.get('viewCount', 'N/A')} | "
                    f"Likes: {stats.get('likeCount', 'N/A')} | "
                    f"Comments: {stats.get('commentCount', 'N/A')}\n"
                    f"  Published: {snippet['publishedAt']}\n"
                    f"  URL: https://youtube.com/watch?v={video['id']}"
                )

            return "\n\n".join(results) if results else f"No YouTube results for '{query}'"

        except ImportError:
            return "YouTube tool: google-api-python-client not installed"
        except Exception as e:
            return f"YouTube error: {str(e)}"
