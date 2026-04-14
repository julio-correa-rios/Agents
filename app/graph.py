from langgraph.graph import StateGraph, END

from app.state import AgentState

from app.agents.planner import planner
from app.agents.executor import executor
from app.agents.filter import filter_results
from app.agents.responder import responder
from app.agents.router import route_after_planner, should_continue


def create_graph(checkpointer=None):
    """
    Create and compile the agent graph.
    
    Args:
        checkpointer: Optional checkpoint saver. For FastAPI use only.
        
    Returns:
        Compiled graph
    """
    
    workflow = StateGraph(AgentState)

    # nodes
    workflow.add_node("planner", planner)
    workflow.add_node("executor", executor)
    workflow.add_node("filter", filter_results)
    workflow.add_node("responder", responder)

    # entry
    workflow.set_entry_point("planner")

    # planner routes to executor (search) or directly to responder (answer)
    workflow.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "executor": "executor",
            "responder": "responder"
        }
    )
    workflow.add_edge("executor", "filter")

    # conditional routing
    workflow.add_conditional_edges(
        "filter",
        should_continue,
        {
            "continue": "planner",
            "end": "responder"
        }
    )

    # Compile without checkpointer (LangGraph CLI compatibility)
    # Checkpointer added only in FastAPI (main.py)
    return workflow.compile(checkpointer=checkpointer)


# Lazy singleton for LangGraph CLI (avoids compilation at import time)
_cli_graph = None


def get_graph():
    global _cli_graph
    if _cli_graph is None:
        _cli_graph = create_graph()
    return _cli_graph