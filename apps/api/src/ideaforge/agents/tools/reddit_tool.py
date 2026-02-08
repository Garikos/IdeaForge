"""Reddit research tool via PRAW."""

from __future__ import annotations

from crewai.tools import BaseTool

from ...config import settings

TARGET_SUBREDDITS = [
    "Entrepreneur", "SideProject", "startups", "SaaS",
    "BusinessIdeas", "passive_income", "indiehackers",
]


class RedditResearchTool(BaseTool):
    name: str = "reddit_research"
    description: str = (
        "Search Reddit entrepreneur and startup communities for "
        "pain points, business ideas, and community feedback."
    )

    def _run(self, query: str) -> str:
        if not settings.reddit_client_id or not settings.reddit_client_secret:
            return "Reddit tool: REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not configured"

        try:
            import praw

            reddit = praw.Reddit(
                client_id=settings.reddit_client_id,
                client_secret=settings.reddit_client_secret,
                user_agent=settings.reddit_user_agent,
            )

            results = []

            for subreddit_name in TARGET_SUBREDDITS[:5]:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    for post in subreddit.search(query, sort="relevance", limit=3):
                        top_comments = []
                        post.comments.replace_more(limit=0)
                        for comment in post.comments[:3]:
                            top_comments.append(comment.body[:200])

                        results.append(
                            f"r/{subreddit_name}: {post.title}\n"
                            f"  Score: {post.score} | Comments: {post.num_comments} | "
                            f"Upvote ratio: {post.upvote_ratio}\n"
                            f"  URL: https://reddit.com{post.permalink}\n"
                            f"  Top comments: {top_comments[:2]}"
                        )
                except Exception:
                    continue

            return "\n\n".join(results) if results else f"No Reddit results for '{query}'"

        except ImportError:
            return "Reddit tool: praw library not installed"
        except Exception as e:
            return f"Reddit error: {str(e)}"
