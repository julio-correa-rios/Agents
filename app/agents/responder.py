from app.config.llm import get_llm
from app.state import AgentState


def responder(state: AgentState):
    
    llm = get_llm()

    prompt = f"""

    You are an AI assistant.

    Answer the question using ONLY the provided search results.

    If the results are insufficient or invalid, say so.

    Question:
    {state.user_input}

    Search Results:
    {state.search_results}

    Instructions:
    - Base your answer on the search results
    - Be concise
    - Cite key ideas when relevant
    - Do not invent information

    Structure:
    - Short answer
    - Key points
    - Recommendation

    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }