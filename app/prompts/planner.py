from app.state import AgentState

PLANNER_SYSTEM_PROMPT = """You are an AI research agent using the ReAct framework.

Your job:
- Think step by step about what information is needed
- Choose "search" to gather more information, or "answer" if you can fully answer the question
- When searching, write precise and specific queries
- Avoid irrelevant entities (e.g., do not confuse similarly named institutions or people)

Decision criteria:
- If the context already contains enough information to fully answer the question, choose "answer" and write the complete answer in action_input
- If the context is missing, incomplete, or you need to verify something, choose "search" with a targeted query
- Refine your search queries based on previous steps to avoid repeating the same searches
"""


def build_planner_user_prompt(state: AgentState) -> str:
    history = "\n".join(state.intermediate_steps) if state.intermediate_steps else "None yet."

    context = "\n\n".join(
        f"[{i}] {r.content}" for i, r in enumerate(state.search_results)
    ) if state.search_results else "No context gathered yet."

    return f"""Question:
{state.user_input}

Previous steps:
{history}

Context gathered so far:
{context}"""