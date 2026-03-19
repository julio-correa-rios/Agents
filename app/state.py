from pydantic import BaseModel, Field
from typing import Optional, List


class SearchResult(BaseModel):
    content: str
    source: str

class AgentState(BaseModel):

    user_input: str

    # Updating this comment due to implementing a smarter parsing logic
    needs_search: Optional[bool] = None
    search_query: Optional[str] = None

    search_results: List[SearchResult] = Field(default_factory=list)

    final_answer: Optional[str] = None

    # Adding this one to track the iterations over topk results
    iteration: int = 0