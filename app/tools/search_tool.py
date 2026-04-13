import logging
import os

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_tool(query: str) -> list[dict]:
    """Run a Tavily search. Raises on API/network errors so callers can retry."""
    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        logger.warning(f"[SearchTool] No results returned for query: {query}")
        return []

    return [
        {
            "content": r.get("content", ""),
            "source": r.get("url", "")
        }
        for r in results
    ]