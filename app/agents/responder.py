from app.config.llm import get_llm
from app.state import AgentState

llm = get_llm()


def responder(state: AgentState):

    prompt = f"""
    Answer the question clearly.

    Question:
    {state.user_input}

    Search results:
    {state.search_results}

    Structure your answer:

    - Short answer
    - Key points
    - Recommendation
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }