import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState
from app.prompts.planner import PLANNER_SYSTEM_PROMPT, build_planner_user_prompt

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_planner_llm(messages):
    """Call LLM with retry logic."""
    llm = get_llm()
    return llm.invoke(messages).content


def planner(state: AgentState):

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=build_planner_user_prompt(state))
    ]

    logger.info(f"[Planner] Iteration {state.iteration}")

    try:
        response = _call_planner_llm(messages)
        logger.debug(f"[Planner] Raw response: {response}")
        parsed = json.loads(response)
    except Exception as e:
        logger.error(f"[Planner] Failed after retries: {e}", exc_info=True)
        parsed = {
            "thought": "Fallback to search",
            "action": "search",
            "action_input": state.user_input
        }

    thought = parsed.get("thought", "")
    action = parsed.get("action", "")
    action_input = parsed.get("action_input", "")

    if isinstance(action_input, dict):
        action_input = json.dumps(action_input)

    logger.info(f"[Planner] Action: {action} | Thought: {thought}")

    step_log = f"Thought: {thought} | Action: {action} | Input: {action_input}"

    updates = {
        "thought": thought,
        "action": action,
        "action_input": action_input,
        "intermediate_steps": state.intermediate_steps + [step_log],
        "iteration": state.iteration + 1
    }

    if action == "answer":
        updates["final_answer"] = action_input or "ready"

    return updates