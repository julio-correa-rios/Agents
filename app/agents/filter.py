import logging

from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState, FilterDecision
from app.prompts.filter import FILTER_SYSTEM_PROMPT, build_filter_user_prompt

logger = logging.getLogger(__name__)


def filter_results(state: AgentState):
    logger.info(f"[Filter] Iteration {state.iteration} | Results to filter: {len(state.search_results)}")

    if not state.search_results:
        logger.info("[Filter] No results to filter, returning empty")
        return {
            "search_results": [],
            "filter_status": "no_results"
        }

    try:
        llm = get_llm("filter").with_structured_output(FilterDecision)
        messages = [
            SystemMessage(content=FILTER_SYSTEM_PROMPT),
            HumanMessage(content=build_filter_user_prompt(state))
        ]
        decision = llm.invoke(messages)
        logger.debug(f"[Filter] Selected indices: {decision.indices}")
    except Exception as e:
        logger.error(f"[Filter] LLM call failed: {e}, using all results", exc_info=True)
        return {
            "search_results": state.search_results,
            "filter_status": "error"
        }

    filtered = [
        state.search_results[i]
        for i in decision.indices
        if 0 <= i < len(state.search_results)
    ]

    logger.info(f"[Filter] Kept {len(filtered)} / {len(state.search_results)} results")

    return {
        "search_results": filtered,
        "filter_status": "ok" if filtered else "all_filtered"
    }