from app.state import AgentState


def route_after_planner(state: AgentState):

    # This is what it needs to get done after getting and understanding the task in the planner node
    if state.needs_search:
        return "executor"

    return "responder"