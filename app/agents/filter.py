import logging
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState

logger = logging.getLogger(__name__)


FILTER_SYSTEM_PROMPT = """
You are a relevance filter.

Your job:
- Select ONLY results that are directly relevant to the question
- Remove results about different entities (e.g., different universities)
- Be strict: better to drop than include irrelevant info

Return ONLY a comma-separated list of indices (e.g., 0,2)
No explanation.
"""


def build_filter_user_prompt(state: AgentState):

    results_text = "\n\n".join([
        f"{i}. {r.content}"
        for i, r in enumerate(state.search_results)
    ])

    return f"""
    Question:
    {state.user_input}

    Results:
    {results_text}
    """


def filter_results(state: AgentState):

    logger.info("[Filter] Running relevance filter")

    if not state.search_results:
        logger.info("[Filter] No results to filter")
        return {}

    llm = get_llm()

    messages = [
        SystemMessage(content=FILTER_SYSTEM_PROMPT),
        HumanMessage(content=build_filter_user_prompt(state))
    ]

    response = llm.invoke(messages).content

    logger.debug(f"[Filter] Raw response: {response}")

    try:
        indices = [int(i.strip()) for i in response.split(",") if i.strip().isdigit()]
    except Exception as e:
        logger.error(f"[Filter] Failed to parse indices: {e}", exc_info=True)
        indices = list(range(len(state.search_results)))

    filtered = [
        state.search_results[i]
        for i in indices
        if i < len(state.search_results)
    ]

    logger.info(f"[Filter] Kept {len(filtered)} / {len(state.search_results)} results")

    return {
        "search_results": filtered
    }