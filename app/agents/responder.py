import logging
from app.config.llm import get_llm
from app.state import AgentState

logger = logging.getLogger(__name__)


def responder(state: AgentState):
    
    llm = get_llm()

    logger.info(f"[Responder] Iteration {state.iteration} | Results: {len(state.search_results)}")

    if not state.search_results:
        if state.final_answer and state.final_answer != "ready":
            logger.info("[Responder] Using planner's direct answer (no search needed)")
            return {
                "final_answer": state.final_answer,
                "responder_status": "ok"
            }

        logger.warning("[Responder] No search results and no direct answer available")
        prompt = f"""The user asked the following question but no search results were found.
            Answer the question using your own knowledge. If you truly cannot answer, say so.

            Question:
            {state.user_input}
            """
        try:
            response = llm.invoke(prompt)
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

    # Building context from search results
    context = "\n\n".join([
        f"Source: {r.source}\nContent: {r.content}"
        for r in state.search_results
    ])

    prompt = f"""
    Answer the question using ONLY the context provided.

    Question:
    {state.user_input}

    Context:
    {context}

    Rules:
    - Use sources comprehensively
    - Be concise and clear
    - Do not make up content
    - If context doesn't contain the answer, say so
    """

    try:
        response = llm.invoke(prompt)
        final_answer = response.content
        logger.info(f"[Responder] Generated answer successfully")
        return {
            "final_answer": final_answer,
            "responder_status": "ok"
        }
    except Exception as e:
        logger.error(f"[Responder] Failed to generate answer: {e}", exc_info=True)
        return {
            "final_answer": "Error procesando la respuesta. Intenta nuevamente.",
            "responder_status": "error"
        }