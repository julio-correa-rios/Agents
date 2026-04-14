import logging

from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState
from app.prompts.responder import (
    RESPONDER_FALLBACK_PROMPT,
    RESPONDER_SYSTEM_PROMPT,
    build_responder_user_prompt,
)

logger = logging.getLogger(__name__)


def responder(state: AgentState):
    llm = get_llm("responder")

    logger.info(f"[Responder] Iteration {state.iteration} | Results: {len(state.search_results)}")

    if not state.search_results:
        if state.final_answer and state.final_answer != "ready":
            logger.info("[Responder] Using planner's direct answer (no search needed)")
            return {
                "final_answer": state.final_answer,
                "responder_status": "ok"
            }

        logger.warning("[Responder] No search results and no direct answer available")
        try:
            response = llm.invoke(
                RESPONDER_FALLBACK_PROMPT.format(user_input=state.user_input)
            )
            return {
                "final_answer": response.content,
                "responder_status": "ok"
            }
        except Exception as e:
            logger.error(f"[Responder] Fallback LLM call failed: {e}", exc_info=True)
            return {
                "final_answer": "I couldn't find enough information to answer your question. Try rephrasing it or searching for something more specific.",
                "responder_status": "no_data"
            }

    messages = [
        SystemMessage(content=RESPONDER_SYSTEM_PROMPT),
        HumanMessage(content=build_responder_user_prompt(state))
    ]

    try:
        response = llm.invoke(messages)
        logger.info("[Responder] Generated answer successfully")
        return {
            "final_answer": response.content,
            "responder_status": "ok"
        }
    except Exception as e:
        logger.error(f"[Responder] Failed to generate answer: {e}", exc_info=True)
        return {
            "final_answer": "An error occurred while generating the response. Please try again.",
            "responder_status": "error"
        }