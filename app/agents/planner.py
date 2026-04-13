import logging

from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.llm import get_llm
from app.state import AgentState, PlannerDecision
from app.prompts.planner import PLANNER_SYSTEM_PROMPT, build_planner_user_prompt

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_planner_llm(messages) -> PlannerDecision:
    llm = get_llm().with_structured_output(PlannerDecision)
    return llm.invoke(messages)


def planner(state: AgentState):
    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=build_planner_user_prompt(state))
    ]

    logger.info(f"[Planner] Iteration {state.iteration}")

    try:
        decision = _call_planner_llm(messages)
    except Exception as e:
        logger.error(f"[Planner] Failed after retries: {e}", exc_info=True)
        decision = PlannerDecision(
            thought="Fallback to search",
            action="search",
            action_input=state.user_input
        )

    logger.info(f"[Planner] Action: {decision.action} | Thought: {decision.thought}")

    step_log = f"Thought: {decision.thought} | Action: {decision.action} | Input: {decision.action_input}"

    updates = {
        "thought": decision.thought,
        "action": decision.action,
        "action_input": decision.action_input,
        "intermediate_steps": state.intermediate_steps + [step_log],
        "iteration": state.iteration + 1
    }

    if decision.action == "answer":
        updates["final_answer"] = decision.action_input

    return updates