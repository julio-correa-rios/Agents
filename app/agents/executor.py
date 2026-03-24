import logging
from app.state import AgentState
from app.tools.search_tool import search_tool

# Initialising the logger
logger = logging.getLogger(__name__)

def executor(state: AgentState) -> dict:

    logger.info(f"[Executor] Action: {state.action}")

    if not state.action != "search":
        return {}

    query = state.action_input or state.user_input

    logger.info(f"[Executor] Searching: {query}")

    results = search_tool(query)

    logger.info(f"[Executor] Results count: {len(results)}")

    return {
        "search_results": results
    }
