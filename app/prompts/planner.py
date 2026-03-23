import json
import logging
from app.config.llm import get_llm
from app.state import AgentState

logger = logging.getLogger(__name__)

PLANNER_SYSTEM_PROMPT = """
You are an AI agent using the ReAct framework.

You must:
- Think step by step
- Decide whether to search or answer
- Avoid irrelevant entities (e.g., do not confuse similar institutions)
- Prefer precise and specific search queries

You must return ONLY valid JSON.

Format:
{
  "thought": "...",
  "action": "search" | "answer",
  "action_input": "..."
}
"""

def build_planner_user_prompt(state):

    history = "\n".join(state.intermediate_steps)

    return f"""
    Question:
    {state.user_input}

    Previous steps:
    {history}

    Context:
    {[r.content for r in state.search_results]}
    """