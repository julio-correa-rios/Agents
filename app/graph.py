from langgraph.graph import StateGraph, END

from app.state import AgentState

from app.agents.planner import planner
from app.agents.executor import executor
from app.agents.responder import responder
from app.agents.router import should_continue


workflow = StateGraph(AgentState)

# nodes
workflow.add_node("planner", planner)
workflow.add_node("executor", executor)
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



graph = workflow.compile()