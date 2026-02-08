"""Tool registry — maps source IDs to tool classes."""

from .google_trends import GoogleTrendsTool
from .google_search import GoogleSearchTool
from .reddit_tool import RedditResearchTool
from .hackernews_tool import HackerNewsResearchTool
from .youtube_tool import YouTubeResearchTool
from .github_tool import GitHubTrendingTool
from .devto_tool import DevToResearchTool
from .news_tool import NewsResearchTool
from .wikipedia_tool import WikipediaTrendsTool
from .bluesky_tool import BlueskyResearchTool
from .package_trends import PackageTrendsTool
from .economic_tool import EconomicDataTool
from .sentiment import SentimentAnalysisTool

# Registry: source_id -> tool class
# Used by ResearchCrew to dynamically assemble crews from user-selected sources
TOOL_REGISTRY: dict[str, type] = {
    "google_trends": GoogleTrendsTool,
    "google_search": GoogleSearchTool,
    "reddit": RedditResearchTool,
    "hackernews": HackerNewsResearchTool,
    "youtube": YouTubeResearchTool,
    "github": GitHubTrendingTool,
    "devto": DevToResearchTool,
    "news": NewsResearchTool,
    "wikipedia": WikipediaTrendsTool,
    "bluesky": BlueskyResearchTool,
    "packages": PackageTrendsTool,
    "economic": EconomicDataTool,
}

# Sentiment tool is always available but used independently
ANALYSIS_TOOLS = {
    "sentiment": SentimentAnalysisTool,
}

__all__ = [
    "TOOL_REGISTRY",
    "ANALYSIS_TOOLS",
    "GoogleTrendsTool",
    "GoogleSearchTool",
    "RedditResearchTool",
    "HackerNewsResearchTool",
    "YouTubeResearchTool",
    "GitHubTrendingTool",
    "DevToResearchTool",
    "NewsResearchTool",
    "WikipediaTrendsTool",
    "BlueskyResearchTool",
    "PackageTrendsTool",
    "EconomicDataTool",
    "SentimentAnalysisTool",
]
