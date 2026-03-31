from langgraph.graph import StateGraph, END

from app.state import AgentState

from app.agents.planner import planner
from app.agents.executor import executor
from app.agents.filter import filter_results
from app.agents.responder import responder
from app.agents.router import should_continue


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

    # flow
    workflow.add_edge("planner", "executor")
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
    if checkpointer:
        graph = workflow.compile(checkpointer=checkpointer)
    else:
        graph = workflow.compile()
    
    return graph


# Create graph instance WITHOUT checkpointer (for LangGraph CLI)
graph = create_graph()