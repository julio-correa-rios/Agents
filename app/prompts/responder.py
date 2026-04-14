from app.state import AgentState

RESPONDER_FALLBACK_PROMPT = """The user asked the following question but no search results were found.
Answer the question using your own knowledge. If you truly cannot answer, say so.

Question:
{user_input}"""


RESPONDER_SYSTEM_PROMPT = """Answer the question using ONLY the context provided.

Rules:
- Use sources comprehensively
- Be concise and clear
- Do not make up content
- If context doesn't contain the answer, say so"""


def build_responder_user_prompt(state: AgentState) -> str:
    context = "\n\n".join(
        f"Source: {r.source}\nContent: {r.content}"
        for r in state.search_results
    )

    return f"""Question:
{state.user_input}

Context:
{context}"""
