"""Singleton factory for the checkpoint saver."""

import logging
from app.db.sqlite_checkpointer import SqliteCheckpointer

logger = logging.getLogger(__name__)

_saver_instance = None


def get_checkpoint_saver() -> SqliteCheckpointer:
    global _saver_instance
    if _saver_instance is None:
        logger.info("[Checkpointing] Initializing SqliteCheckpointer")
        _saver_instance = SqliteCheckpointer()
    return _saver_instance


def clear_checkpoint_saver():
    """Reset the singleton (for testing)."""
    global _saver_instance
    _saver_instance = None

