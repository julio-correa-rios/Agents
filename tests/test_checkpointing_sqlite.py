"""Tests for SQLite checkpoint persistence."""

import pytest
from pathlib import Path
from app.graph import create_graph
from app.db.sqlite_checkpointer import SqliteCheckpointer, DB_PATH, init_sqlite_db


@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up database before and after each test."""
    # Remove existing database
    if DB_PATH.exists():
        DB_PATH.unlink()
    yield
    # Clean up after test
    if DB_PATH.exists():
        DB_PATH.unlink()


def test_sqlite_checkpointer_creation():
    """Test that SqliteCheckpointer initializes correctly."""
    checkpointer = SqliteCheckpointer()
    assert checkpointer is not None
    assert DB_PATH.exists()


def test_session_persistence():
    """Test that checkpoints are saved to SQLite."""
    checkpointer = SqliteCheckpointer()
    graph = create_graph(checkpointer=checkpointer)
    
    thread_id = "test-session-1"
    
    # First invocation
    result = graph.invoke(
        {
            "user_input": "¿Cuál es la capital de Francia?",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id}}
    )
    
    # Verify result
    assert result is not None
    assert "final_answer" in result or result.get("iteration", 0) >= 1
    
    # List sessions
    sessions = SqliteCheckpointer.list_sessions()
    assert len(sessions) > 0
    session_threads = [s["thread_id"] for s in sessions]
    assert thread_id in session_threads


def test_multi_session_isolation():
    """Test that different sessions maintain separate state."""
    checkpointer = SqliteCheckpointer()
    graph = create_graph(checkpointer=checkpointer)
    
    thread_id_1 = "test-session-a"
    thread_id_2 = "test-session-b"
    
    # First session
    result1 = graph.invoke(
        {
            "user_input": "¿Quién fue Mozart?",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id_1}}
    )
    
    # Second session
    result2 = graph.invoke(
        {
            "user_input": "¿Dónde nació Einstein?",
            "iteration": 0,
            "max_iterations": 1,
            "intermediate_steps": [],
            "search_results": []
        },
        config={"configurable": {"thread_id": thread_id_2}}
    )
    
    # Both should exist
    sessions = SqliteCheckpointer.list_sessions()
    session_threads = [s["thread_id"] for s in sessions]
    assert thread_id_1 in session_threads
    assert thread_id_2 in session_threads
    
    # Clear one session
    SqliteCheckpointer.clear_session(thread_id_1)
    
    # Verify only one remains
    sessions = SqliteCheckpointer.list_sessions()
    session_threads = [s["thread_id"] for s in sessions]
    assert thread_id_1 not in session_threads
    assert thread_id_2 in session_threads


def test_clear_all_checkpoints():
    """Test clearing all checkpoints."""
    checkpointer = SqliteCheckpointer()
    graph = create_graph(checkpointer=checkpointer)
    
    # Create multiple sessions
    for i in range(3):
        graph.invoke(
            {
                "user_input": f"Pregunta {i}",
                "iteration": 0,
                "max_iterations": 1,
                "intermediate_steps": [],
                "search_results": []
            },
            config={"configurable": {"thread_id": f"test-{i}"}}
        )
    
    # Verify multiple sessions exist
    sessions = SqliteCheckpointer.list_sessions()
    assert len(sessions) >= 3
    
    # Clear all
    SqliteCheckpointer.clear_all()
    
    # Verify empty
    sessions = SqliteCheckpointer.list_sessions()
    assert len(sessions) == 0
