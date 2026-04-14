from pydantic import BaseModel, Field
from typing import Literal, Optional, List


SearchStatus = Literal["ok", "empty", "error", "skipped"]
FilterStatus = Literal["ok", "no_results", "error", "all_filtered"]
ResponderStatus = Literal["ok", "no_data", "error"]


class SearchResult(BaseModel):
    content: str
    source: str


class StepRecord(BaseModel):
    thought: str
    action: str
    action_input: str
    iteration: int


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

    thought: Optional[str] = None
    action: Optional[str] = None
    action_input: Optional[str] = None

    search_results: List[SearchResult] = Field(default_factory=list)
    search_status: Optional[SearchStatus] = None
    filter_status: Optional[FilterStatus] = None
    responder_status: Optional[ResponderStatus] = None

    final_answer: Optional[str] = None

    intermediate_steps: List[StepRecord] = Field(default_factory=list)

    iteration: int = 0
    max_iterations: int = 3