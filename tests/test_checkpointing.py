"""Tests for checkpoint persistence."""

import pytest
from app.state import AgentState, SearchResult
from app.graph import create_graph
from app.db.checkpointing import clear_checkpoints, get_checkpoint_saver


def test_checkpoint_saver_creation():
    """Test that checkpoint saver is created successfully."""
    saver = get_checkpoint_saver()
    assert saver is not None


def test_graph_with_checkpoint():
    """Test graph invocation with checkpoint config."""
    thread_id = "test-session-1"
    
    # Clear previous checkpoints
    clear_checkpoints()
    
    # Create graph with checkpointer
    saver = get_checkpoint_saver()
    graph = create_graph(checkpointer=saver)
    
    # First invocation saves checkpoint
    result1 = graph.invoke(
        {
            "user_input": "What is testing?",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id}}
    )
    
    assert result1 is not None
    assert result1["iteration"] >= 1


def test_multiple_sessions_isolated():
    """Test that different thread_ids maintain separate states."""
    clear_checkpoints()
    
    saver = get_checkpoint_saver()
    graph = create_graph(checkpointer=saver)
    
    thread_id_1 = "session-1"
    thread_id_2 = "session-2"
    
    # Run with thread_id_1
    result1 = graph.invoke(
        {
            "user_input": "Query 1",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id_1}}
    )
    
    # Run with thread_id_2
    result2 = graph.invoke(
        {
            "user_input": "Query 2",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id_2}}
    )
    
    # Both should complete independently
    assert result1["user_input"] == "Query 1"
    assert result2["user_input"] == "Query 2"
