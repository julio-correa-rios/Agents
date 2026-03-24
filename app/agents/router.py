from app.state import AgentState


# def route_after_planner(state: AgentState):

#     # This is what it needs to get done after getting and understanding the task in the planner node
#     if state.needs_search:
#         return "executor"

#     return "responder"

def should_continue(state: AgentState):

    if state.final_answer:
        return "end"

    if state.iteration >= state.max_iterations:
        return "end"

    return "continue"