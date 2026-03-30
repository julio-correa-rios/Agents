import logging
from app.state import AgentState


# def route_after_planner(state: AgentState):

#     # This is what it needs to get done after getting and understanding the task in the planner node
#     if state.needs_search:
#         return "executor"

#     return "responder"

logger = logging.getLogger(__name__)


def should_continue(state: AgentState):
    """
    Decide whether to continue the loop or end.
    """

    # If we have a final answer, stop
    if state.final_answer:
        logger.info(f"[Router] Final answer generated, ending")
        return "end"

    # If we've reached max iterations, stop
    if state.iteration >= state.max_iterations:
        logger.warning(f"[Router] Max iterations ({state.max_iterations}) reached, ending")
        return "end"

    # If search failed and we have no results, stop
    if state.search_results == [] and state.iteration > 1:
        logger.warning(f"[Router] No results found after iteration {state.iteration}, ending")
        return "end"

    logger.info(f"[Router] Continuing loop (iter={state.iteration}/{state.max_iterations})")
    return "continue"