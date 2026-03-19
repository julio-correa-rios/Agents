from app.config.llm import get_llm
from app.state import AgentState


def responder(state: AgentState):
    
    llm = get_llm()

    # Adding the context from the search results
    context = "\n\n".join([
        f"Source: {r.source}\nContent: {r.content}"
        for r in state.search_results
    ])

    prompt = f"""
    Answer the question using ONLY the context.

    Question:
    {state.user_input}

    Context:
    {context}

    Rules:
    - Use sources comprehensively
    - Be concise
    - Do not make up content
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }