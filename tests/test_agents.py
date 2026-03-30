import pytest
from unittest.mock import patch, MagicMock
from app.state import AgentState, SearchResult
from app.agents.planner import planner
from app.agents.executor import executor
from app.agents.filter import filter_results
from app.agents.responder import responder
from app.agents.router import should_continue


def test_planner_with_valid_json():
    """Test planner with valid JSON response."""
    state = AgentState(user_input="What is LangGraph?", iteration=0)
    
    with patch('app.agents.planner.get_llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = '{"thought": "Need to search", "action": "search", "action_input": "LangGraph"}'
        mock_llm.return_value.invoke.return_value = mock_response
        
        result = planner(state)
        
        assert result["action"] == "search"
        assert result["iteration"] == 1
        assert len(result["intermediate_steps"]) == 1


def test_planner_fallback_on_invalid_json():
    """Test planner fallback with invalid JSON."""
    state = AgentState(user_input="What is LangGraph?", iteration=0)
    
    with patch('app.agents.planner.get_llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = 'invalid json'
        mock_llm.return_value.invoke.return_value = mock_response
        
        result = planner(state)
        
        assert result["action"] == "search"  # Fallback
        assert result["iteration"] == 1


def test_executor_with_results():
    """Test executor with search results."""
    state = AgentState(
        user_input="What is LangGraph?",
        action="search",
        action_input="LangGraph",
        iteration=1
    )
    
    with patch('app.agents.executor.search_tool') as mock_search:
        mock_search.return_value = [
            {"content": "LangGraph is a tool...", "source": "example.com"}
        ]
        
        result = executor(state)
        
        assert result["search_status"] == "ok"
        assert len(result["search_results"]) == 1


def test_executor_empty_results():
    """Test executor with no results."""
    state = AgentState(
        user_input="What is LangGraph?",
        action="search",
        action_input="LangGraph",
        iteration=1
    )
    
    with patch('app.agents.executor.search_tool') as mock_search:
        mock_search.return_value = []
        
        result = executor(state)
        
        assert result["search_status"] == "empty"
        assert len(result["search_results"]) == 0


def test_filter_with_results():
    """Test filter with results."""
    state = AgentState(
        user_input="What is LangGraph?",
        search_results=[
            SearchResult(content="Relevant info", source="example.com"),
            SearchResult(content="Irrelevant info", source="other.com"),
        ],
        iteration=2
    )
    
    with patch('app.agents.filter.get_llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "0"  # Keep first result
        mock_llm.return_value.invoke.return_value = mock_response
        
        result = filter_results(state)
        
        assert result["filter_status"] == "ok"
        assert len(result["search_results"]) == 1


def test_router_continue():
    """Test router continues loop."""
    state = AgentState(user_input="test", iteration=1, max_iterations=3)
    decision = should_continue(state)
    assert decision == "continue"


def test_router_end_on_max_iterations():
    """Test router ends on max iterations."""
    state = AgentState(user_input="test", iteration=3, max_iterations=3)
    decision = should_continue(state)
    assert decision == "end"


def test_router_end_on_final_answer():
    """Test router ends when final answer exists."""
    state = AgentState(
        user_input="test",
        final_answer="The answer is...",
        iteration=1,
        max_iterations=3
    )
    decision = should_continue(state)
    assert decision == "end"