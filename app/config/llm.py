import os

from langchain_openai import ChatOpenAI

_DEFAULTS = {
    "planner": "gpt-4o-mini",
    "filter": "gpt-4o-mini",
    "responder": "gpt-4o-mini",
}


def get_llm(role: str = "default", temperature: float = 0) -> ChatOpenAI:
    env_key = f"LLM_MODEL_{role.upper()}"
    model = os.getenv(env_key, _DEFAULTS.get(role, "gpt-4o-mini"))
    return ChatOpenAI(model=model, temperature=temperature)