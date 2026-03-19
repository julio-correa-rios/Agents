from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client once
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_tool(query: str) -> str:
    try:
        response = client.search(
            query=query,
            search_depth="basic",   # fast + cheap
            max_results=3           # keep it small
        )

        results = response.get("results", [])

        if not results:
            return "No relevant results found."

        formatted_results = []

        for i, r in enumerate(results, 1):
            content = r.get("content", "")
            url = r.get("url", "")

            formatted_results.append(
                f"Result {i}:\n{content}\nSource: {url}\n"
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Search error: {str(e)}"