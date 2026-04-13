from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class SearchResult(BaseModel):
    content: str
    source: str


class PlannerDecision(BaseModel):
    """The planner's structured output: a ReAct-style thought + action."""
    thought: str = Field(description="Step-by-step reasoning about what to do next")
    action: Literal["search", "answer"] = Field(description="Whether to search for more info or answer directly")
    action_input: str = Field(description="The search query if action is 'search', or the final answer if action is 'answer'")


class FilterDecision(BaseModel):
    """The filter's structured output: which result indices to keep."""
    indices: List[int] = Field(description="List of zero-based indices of relevant results to keep")


class AgentState(BaseModel):

    user_input: str

    # --- NEW (ReAct logic implemented in this new branch) ---
    thought: Optional[str] = None
    action: Optional[str] = None
    action_input: Optional[str] = None

    # Updating this comment due to implementing a smarter parsing logic
    # needs_search: Optional[bool] = None
    # search_query: Optional[str] = None

    # Existing from baseline implementation
    search_results: List[SearchResult] = Field(default_factory=list)
    search_status: Optional[str] = None  # "ok", "empty", "error", "skipped"
    filter_status: Optional[str] = None  # "ok", "no_results", "error", "all_filtered"
    responder_status: Optional[str] = None  # "ok", "no_data", "error"

    final_answer: Optional[str] = None
    
    # --- MEMORY ---
    intermediate_steps: List[str] = Field(default_factory=list)

    # Adding this one to track the iterations over topk results
    # Loop control logic
    iteration: int = 0
    max_iterations: int = 3