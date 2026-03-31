"""Checkpoint and state persistence with SQLite."""

import logging
from pathlib import Path
from app.db.sqlite_checkpointer import SqliteCheckpointer

logger = logging.getLogger(__name__)

# Singleton instance
_saver_instance = None


def get_checkpoint_saver():
    """
    Get or create a checkpoint saver with SQLite persistence.
    
    Data is persisted in checkpoints.db and survives server restarts.
    Uses hybrid approach: MemorySaver for speed + SQLite for durability.
    
    Returns:
        SqliteCheckpointer instance for checkpoint management
    """
    
    global _saver_instance
    if _saver_instance is None:
        logger.info("[Checkpointing] Initializing SqliteCheckpointer with persistent storage")
        _saver_instance = SqliteCheckpointer()
    
    return _saver_instance


def list_sessions():
    """List all saved sessions."""
    return SqliteCheckpointer.list_sessions()


def clear_session(thread_id: str):
    """Clear a specific session's checkpoints."""
    return SqliteCheckpointer.clear_session(thread_id)


def clear_all_checkpoints():
    """Clear all checkpoints (use with caution)."""
    return SqliteCheckpointer.clear_all()


def clear_checkpoint_saver():
    """
    Clear checkpoint saver (reset for testing).
    """
    global _saver_instance
    _saver_instance = None
    logger.info("[Checkpointing] Cleared checkpoint saver")

