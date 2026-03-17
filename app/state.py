from pydantic import BaseModel, Field
from typing import Optional


class AgentState(BaseModel):

    user_input: str

    # Optional for future use
    needs_search: Optional[bool] = None

    search_query: Optional[str] = None

    search_results: Optional[str] = None

    final_answer: Optional[str] = None