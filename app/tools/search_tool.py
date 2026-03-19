from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client once
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_tool(query: str) -> list[dict]:
    try:
        response = client.search(
            query=query,
            search_depth="basic",   # fast + cheap
            max_results=3           # keep it small
        )

        results = response.get("results", [])

        if not results:
            return []

        formatted_results = []

        for _, r in enumerate(results):
            
            formatted_results.append(
                {
                   "content": r.get("content", ""),
                   "source": r.get("url", "")
                }
            )

        return formatted_results

    except Exception as e:
        print (f"Search error: {str(e)}")
        return []