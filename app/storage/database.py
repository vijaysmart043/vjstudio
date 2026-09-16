"""
Local SQLite database schema for persistent session history, presets, and statistics.
"""

import sqlite3
from pathlib import Path
from typing import Any, List, Optional
from app.core.paths import paths
from app.core.logger import logger


class Database:
    """Manages SQLite connection and schemas in user AppData."""

    _instance = None

    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or (paths.user_data_dir / "vjstudio.db")
        self._init_tables()

    @classmethod
    def get_instance(cls) -> "Database":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self) -> None:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Recent projects table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS recent_projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        file_path TEXT UNIQUE NOT NULL,
                        last_opened TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Broadcast session history
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS session_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_type TEXT NOT NULL,
                        start_time TIMESTAMP NOT NULL,
                        end_time TIMESTAMP,
                        duration_seconds REAL,
                        status TEXT
                    )
                """)
                conn.commit()
            logger.info("SQLite storage initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize SQLite database: {e}")


db = Database.get_instance()
