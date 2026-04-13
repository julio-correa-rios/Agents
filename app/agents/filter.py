import logging

from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState, FilterDecision

logger = logging.getLogger(__name__)


FILTER_SYSTEM_PROMPT = """You are a relevance filter.

Your job:
- Select ONLY results that are directly relevant to the question
- Remove results about different entities (e.g., different universities, different people)
- Be strict: it is better to drop a result than to include irrelevant information
- Return the indices (zero-based) of the results you want to keep
"""


def build_filter_user_prompt(state: AgentState) -> str:
    results_text = "\n\n".join(
        f"[{i}] {r.content}" for i, r in enumerate(state.search_results)
    )

    return f"""Question:
{state.user_input}

Results:
{results_text}"""


def filter_results(state: AgentState):
    logger.info(f"[Filter] Iteration {state.iteration} | Results to filter: {len(state.search_results)}")

    if not state.search_results:
        logger.info("[Filter] No results to filter, returning empty")
        return {
            "search_results": [],
            "filter_status": "no_results"
        }

    try:
        llm = get_llm().with_structured_output(FilterDecision)
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