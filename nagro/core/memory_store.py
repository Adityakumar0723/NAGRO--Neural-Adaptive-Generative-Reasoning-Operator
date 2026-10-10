"""
NAGRO 4.1 — Persistent Memory Store.

Long-term memory that survives across sessions using SQLite.
Remembers conversations, user preferences, learned facts, and context.
No external database — everything local.
"""

from __future__ import annotations
import sqlite3
import json
import time
from pathlib import Path
from contextlib import contextmanager


class MemoryStore:
    """Persistent memory store using local SQLite."""

    def __init__(self, db_path: str = "data/nagro_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at REAL,
                    updated_at REAL,
                    message_count INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    task_type TEXT,
                    timestamp REAL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                );

                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    key TEXT,
                    value TEXT,
                    metadata TEXT,
                    created_at REAL,
                    updated_at REAL,
                    access_count INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                );

                CREATE TABLE IF NOT EXISTS learned_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT,
                    source TEXT,
                    confidence REAL DEFAULT 0.8,
                    category TEXT,
                    created_at REAL
                );

                CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
                CREATE INDEX IF NOT EXISTS idx_memories_cat ON memories(category);
                CREATE INDEX IF NOT EXISTS idx_facts_cat ON learned_facts(category);
            """)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # --- Conversation Persistence ---

    def save_conversation(self, conv_id: str, title: str, messages: list[dict]):
        now = time.time()
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO conversations (id, title, created_at, updated_at, message_count) "
                "VALUES (?, ?, ?, ?, ?)",
                (conv_id, title, now, now, len(messages)),
            )
            conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
            for msg in messages:
                conn.execute(
                    "INSERT INTO messages (id, conversation_id, role, content, task_type, timestamp) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (msg.get("id", ""), conv_id, msg["role"], msg["content"],
                     msg.get("task_type", ""), msg.get("timestamp", now)),
                )

    def load_conversation(self, conv_id: str) -> dict | None:
        with self._conn() as conn:
            conv = conn.execute(
                "SELECT * FROM conversations WHERE id = ?", (conv_id,)
            ).fetchone()
            if not conv:
                return None
            messages = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp",
                (conv_id,),
            ).fetchall()
            return {
                "id": conv["id"],
                "title": conv["title"],
                "messages": [dict(m) for m in messages],
            }

    def list_conversations(self, limit: int = 50) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, title, updated_at, message_count FROM conversations "
                "ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def delete_conversation(self, conv_id: str):
        with self._conn() as conn:
            conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
            conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))

    # --- Long-Term Memory ---

    def remember(self, category: str, key: str, value: str, metadata: dict | None = None):
        now = time.time()
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT id FROM memories WHERE category = ? AND key = ?",
                (category, key),
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE memories SET value = ?, metadata = ?, updated_at = ? "
                    "WHERE id = ?",
                    (value, json.dumps(metadata or {}), now, existing["id"]),
                )
            else:
                conn.execute(
                    "INSERT INTO memories (category, key, value, metadata, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (category, key, value, json.dumps(metadata or {}), now, now),
                )

    def recall(self, category: str, key: str | None = None) -> list[dict]:
        with self._conn() as conn:
            if key:
                rows = conn.execute(
                    "SELECT * FROM memories WHERE category = ? AND key = ?",
                    (category, key),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM memories WHERE category = ? ORDER BY updated_at DESC",
                    (category,),
                ).fetchall()
            for row in rows:
                conn.execute(
                    "UPDATE memories SET access_count = access_count + 1 WHERE id = ?",
                    (row["id"],),
                )
            return [dict(r) for r in rows]

    def forget(self, category: str, key: str):
        with self._conn() as conn:
            conn.execute(
                "DELETE FROM memories WHERE category = ? AND key = ?",
                (category, key),
            )

    # --- User Preferences ---

    def set_preference(self, key: str, value: str):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO user_preferences (key, value, updated_at) VALUES (?, ?, ?)",
                (key, value, time.time()),
            )

    def get_preference(self, key: str, default: str = "") -> str:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT value FROM user_preferences WHERE key = ?", (key,)
            ).fetchone()
            return row["value"] if row else default

    def get_all_preferences(self) -> dict[str, str]:
        with self._conn() as conn:
            rows = conn.execute("SELECT key, value FROM user_preferences").fetchall()
            return {r["key"]: r["value"] for r in rows}

    # --- Learned Facts ---

    def learn_fact(self, fact: str, source: str = "conversation", confidence: float = 0.8, category: str = "general"):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO learned_facts (fact, source, confidence, category, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (fact, source, confidence, category, time.time()),
            )

    def recall_facts(self, category: str | None = None, limit: int = 20) -> list[dict]:
        with self._conn() as conn:
            if category:
                rows = conn.execute(
                    "SELECT * FROM learned_facts WHERE category = ? ORDER BY confidence DESC LIMIT ?",
                    (category, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM learned_facts ORDER BY confidence DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [dict(r) for r in rows]

    # --- Stats ---

    def get_stats(self) -> dict:
        with self._conn() as conn:
            convs = conn.execute("SELECT COUNT(*) as c FROM conversations").fetchone()["c"]
            msgs = conn.execute("SELECT COUNT(*) as c FROM messages").fetchone()["c"]
            mems = conn.execute("SELECT COUNT(*) as c FROM memories").fetchone()["c"]
            facts = conn.execute("SELECT COUNT(*) as c FROM learned_facts").fetchone()["c"]
            return {
                "conversations": convs,
                "messages": msgs,
                "memories": mems,
                "learned_facts": facts,
                "db_size_mb": round(self.db_path.stat().st_size / (1024 * 1024), 2)
                if self.db_path.exists() else 0,
            }
