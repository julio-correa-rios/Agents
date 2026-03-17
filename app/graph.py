from langgraph.graph import StateGraph, END

from app.state import AgentState

from app.agents.planner import planner
from app.agents.executor import executor
from app.agents.responder import responder
from app.agents.router import route_after_planner


workflow = StateGraph(AgentState)

# nodes
workflow.add_node("planner", planner)
workflow.add_node("executor", executor)
workflow.add_node("responder", responder)

# entry
workflow.set_entry_point("planner")

# conditional routing
workflow.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "executor": "executor",
        "responder": "responder"
    }
)

# flow
workflow.add_edge("executor", "responder")
workflow.add_edge("responder", END)

graph = workflow.compile()