import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from app.state import AgentState, SearchResult
from app.tools.search_tool import search_tool

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _search_with_retry(query: str):
    """Search with retry logic."""
    return search_tool(query)


def executor(state: AgentState) -> dict:

    logger.info(f"[Executor] Iteration {state.iteration} | Action: {state.action}")

    if (state.action or "").strip().lower() != "search":
        return {"search_status": "skipped"}

    query = state.action_input or state.user_input

    logger.info(f"[Executor] Searching: {query}")

    try:
        raw_results = _search_with_retry(query)
        logger.info(f"[Executor] Got {len(raw_results)} raw results")
    except Exception as e:
        logger.error(f"[Executor] Search failed after retries: {e}", exc_info=True)
        return {
            "search_results": [],
            "search_status": "error"
        }

    if not raw_results:
        logger.warning(f"[Executor] No results found for query: {query}")
        return {
            "search_results": [],
            "search_status": "empty"
        }

    results = [
        SearchResult(
            content=r.get("content", ""),
            source=r.get("source", "")
        )
        for r in raw_results
    ]

    logger.info(f"[Executor] Parsed {len(results)} results successfully")

    return {
        "search_results": results,
        "search_status": "ok"
    }