import logging
from app.state import AgentState, SearchResult
from app.tools.search_tool import search_tool

# Initialising the logger
logger = logging.getLogger(__name__)

def executor(state: AgentState) -> dict:

    logger.info(f"[Executor] Action: {state.action}")

    if (state.action or "").strip().lower() != "search":
        return {}

    query = state.action_input or state.user_input

    logger.info(f"[Executor] Searching: {query}")

    raw_results = search_tool(query)

    results = [
        SearchResult(
            content=r.get("content", ""),
            source=r.get("source", "")
        )
        for r in raw_results
    ]

    logger.info(f"[Executor] Parsed results: {len(results)}")

    return {
        "search_results": results
    }