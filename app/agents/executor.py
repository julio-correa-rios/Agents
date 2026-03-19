from app.state import AgentState
from app.tools.search_tool import search_tool


def executor(state: AgentState) -> dict:

    if not state.needs_search:
        return {}

    results = search_tool(state.search_query)

    return {
        "search_results": results
    }