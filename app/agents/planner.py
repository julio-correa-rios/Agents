from app.config.llm import get_llm
from app.state import AgentState



def planner(state: AgentState):


    llm = get_llm()
    
    prompt = f"""
    Decide if the following question requires web search.

    Question:
    {state.user_input}

    Respond strictly in this format:

    needs_search: true/false
    search_query: <query or empty>
    """

    response = llm.invoke(prompt).content.lower()

    needs_search = "true" in response

    query = None
    if needs_search:
        query = state.user_input

    return {
        "needs_search": needs_search,
        "search_query": query
    }