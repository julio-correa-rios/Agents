from pydantic import BaseModel, Field
from typing import Optional, List


class SearchResult(BaseModel):
    content: str
    source: str

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