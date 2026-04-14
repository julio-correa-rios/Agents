from app.state import AgentState

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
