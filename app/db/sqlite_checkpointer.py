"""SQLite-based checkpoint saver for persistent session storage."""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from collections import ChainMap
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)

# Database path
DB_PATH = Path("checkpoints.db")


def _json_encoder_default(obj: Any) -> Any:
    """Custom JSON encoder for non-serializable objects."""
    if isinstance(obj, ChainMap):
        return dict(obj)
    elif hasattr(obj, '__dict__'):
        # Try to serialize attributes
        try:
            return str(obj)
        except:
            return f"<{type(obj).__name__}>"
    else:
        return str(obj)


def init_sqlite_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create checkpoints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            checkpoint_id TEXT,
            checkpoint_ns TEXT DEFAULT '',
            config TEXT,
            state_values TEXT,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(thread_id, checkpoint_id, checkpoint_ns)
        )
    """)
    
    # Create index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_thread_id ON checkpoints(thread_id)
    """)
    
    conn.commit()
    conn.close()
    logger.info(f"[SQLite] Database initialized at {DB_PATH}")


class SqliteCheckpointer(MemorySaver):
    """
    Hybrid checkpointer: uses MemorySaver for fast in-memory access,
    persists to SQLite for durability.
    """
    
    def __init__(self, db_path: Path = DB_PATH):
        super().__init__()
        self.db_path = db_path
        init_sqlite_db()
        logger.info("[SqliteCheckpointer] Initialized with persistent storage")
    
    def put(self, config: Dict[str, Any], values: Dict[str, Any], 
            metadata: Dict[str, Any], thread_ns: tuple = ("default",)):
        """Save checkpoint to memory and SQLite."""
        # Save to memory first
        super().put(config, values, metadata, thread_ns)
        
        # Save to SQLite - only keep essential info
        thread_id = config.get("configurable", {}).get("thread_id", "unknown")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id", str(datetime.now().timestamp()))
        # Handle both dict and tuple formats for thread_ns
        checkpoint_ns = ""
        if isinstance(thread_ns, dict):
            checkpoint_ns = str(thread_ns)
        elif isinstance(thread_ns, (tuple, list)) and len(thread_ns) > 0:
            checkpoint_ns = thread_ns[0]
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create simplified config with only essential info
            simple_config = {
                "configurable": config.get("configurable", {})
            }
            
            # Serialize to JSON with custom encoder for non-serializable objects
            config_json = json.dumps(simple_config, default=_json_encoder_default)
            values_json = json.dumps(values, default=_json_encoder_default)
            metadata_json = json.dumps(metadata, default=_json_encoder_default)
            
            cursor.execute("""
                INSERT OR REPLACE INTO checkpoints 
                (thread_id, checkpoint_id, checkpoint_ns, config, state_values, metadata, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                thread_id,
                checkpoint_id,
                checkpoint_ns,
                config_json,
                values_json,
                metadata_json
            ))
            
            conn.commit()
            conn.close()
            logger.debug(f"[SQLite] Saved checkpoint for {thread_id}")
        except Exception as e:
            logger.error(f"[SQLite] Error saving checkpoint: {e}")
    
    def get(self, config: Dict[str, Any], thread_ns: tuple = ("default",)):
        """Retrieve checkpoint (first from memory, fallback to SQLite)."""
        # Try memory first
        result = super().get(config, thread_ns)
        if result:
            return result
        
        # Fallback to SQLite
        thread_id = config.get("configurable", {}).get("thread_id", "unknown")
        # Handle both dict and tuple formats for thread_ns
        checkpoint_ns = ""
        if isinstance(thread_ns, dict):
            checkpoint_ns = str(thread_ns)
        elif isinstance(thread_ns, (tuple, list)) and len(thread_ns) > 0:
            checkpoint_ns = thread_ns[0]
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT config, state_values, metadata FROM checkpoints
                WHERE thread_id = ? AND checkpoint_ns = ?
                ORDER BY created_at DESC LIMIT 1
            """, (thread_id, checkpoint_ns))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logger.debug(f"[SQLite] Recovered checkpoint for {thread_id}")
                return {
                    "config": json.loads(row[0]),
                    "values": json.loads(row[1]),
                    "metadata": json.loads(row[2])
                }
        except Exception as e:
            logger.error(f"[SQLite] Error retrieving checkpoint: {e}")
        
        return None
    
    @staticmethod
    def list_sessions() -> List[Dict[str, Any]]:
        """List all saved sessions with metadata."""
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT thread_id, COUNT(*) as checkpoint_count, 
                       MAX(updated_at) as last_updated
                FROM checkpoints
                GROUP BY thread_id
                ORDER BY last_updated DESC
            """)
            
            sessions = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return sessions
        except Exception as e:
            logger.error(f"[SQLite] Error listing sessions: {e}")
            return []
    
    @staticmethod
    def clear_session(thread_id: str) -> bool:
        """Delete all checkpoints for a specific session."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
            conn.commit()
            conn.close()
            
            logger.info(f"[SQLite] Cleared session {thread_id}")
            return True
        except Exception as e:
            logger.error(f"[SQLite] Error clearing session: {e}")
            return False
    
    @staticmethod
    def clear_all() -> bool:
        """Clear all checkpoints (use with caution)."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM checkpoints")
            conn.commit()
            conn.close()
            
            logger.warning("[SQLite] Cleared all checkpoints")
            return True
        except Exception as e:
            logger.error(f"[SQLite] Error clearing all checkpoints: {e}")
            return False
