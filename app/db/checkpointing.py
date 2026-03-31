"""Checkpoint and state persistence."""

import os
import logging
from pathlib import Path
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)

# Singleton instance
_saver_instance = None


def get_checkpoint_saver():
    """
    Get or create a checkpoint saver.
    
    Note: This uses MemorySaver for in-memory checkpointing.
    For persistence across server restarts, implement a custom
    saver with SQLAlchemy + SQLite or PostgreSQL.
    
    Returns:
        MemorySaver instance for checkpoint management
    """
    
    global _saver_instance
    if _saver_instance is None:
        logger.info("[Checkpointing] Initializing MemorySaver for session checkpointing")
        _saver_instance = MemorySaver()
    
    return _saver_instance


def clear_checkpoints():
    """
    Clear checkpoint saver (reset for testing).
    """
    global _saver_instance
    _saver_instance = None
    logger.info("[Checkpointing] Cleared checkpoint saver")

