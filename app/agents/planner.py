import json
import logging
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.llm import get_llm
from app.state import AgentState
from app.prompts.planner import PLANNER_SYSTEM_PROMPT, build_planner_user_prompt

logger = logging.getLogger(__name__)


def planner(state: AgentState):

    llm = get_llm()

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=build_planner_user_prompt(state))
    ]

    logger.info(f"[Planner] Iteration {state.iteration}")

    response = llm.invoke(messages).content

    logger.debug(f"[Planner] Raw response: {response}")

    try:
        parsed = json.loads(response)
    except Exception as e:
        logger.error(f"[Planner] JSON parsing failed: {e}", exc_info=True)
        parsed = {
            "thought": "Fallback to search",
            "action": "search",
            "action_input": state.user_input
        }

    thought = parsed.get("thought", "")
    action = parsed.get("action", "")
    action_input = parsed.get("action_input", "")

    logger.info(f"[Planner] Action: {action}")
    logger.debug(f"[Planner] Thought: {thought}")

    step_log = f"Thought: {thought} | Action: {action} | Input: {action_input}"

    updates = {
        "thought": thought,
        "action": action,
        "action_input": action_input,
        "intermediate_steps": state.intermediate_steps + [step_log],
        "iteration": state.iteration + 1
    }

    if action == "answer":
        updates["final_answer"] = "ready"

    return updates