from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

SCHEMA = {
    "orders": """CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL,
        deadline TEXT NOT NULL,
        description TEXT NOT NULL,
        folder TEXT NOT NULL,
        filename TEXT NOT NULL,
        path TEXT NOT NULL,
        mime TEXT NOT NULL,
        status TEXT DEFAULT 'progress',
        completion_outgoing TEXT DEFAULT '',
        priority TEXT DEFAULT 'Звичайний',
        responsible TEXT DEFAULT '',
        category TEXT DEFAULT 'Інше',
        received_date TEXT DEFAULT '',
        tags TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT DEFAULT ''
    )""",
    "responses": """CREATE TABLE IF NOT EXISTS responses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        response_date TEXT NOT NULL,
        outgoing TEXT DEFAULT '',
        comment TEXT DEFAULT '',
        filename TEXT NOT NULL,
        path TEXT NOT NULL,
        mime TEXT NOT NULL,
        is_final INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    "events": """CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        details TEXT DEFAULT '',
        created_at TEXT NOT NULL
    )""",
    "settings": """CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)""",
}

MIGRATIONS = {
    "orders": {
        "completion_outgoing": "TEXT DEFAULT ''", "priority": "TEXT DEFAULT 'Звичайний'",
        "responsible": "TEXT DEFAULT ''", "category": "TEXT DEFAULT 'Інше'",
        "received_date": "TEXT DEFAULT ''", "tags": "TEXT DEFAULT ''", "updated_at": "TEXT DEFAULT ''",
    },
    "responses": {"is_final": "INTEGER DEFAULT 0"},
}


class Database:
    def __init__(self, path: Path):
        self.path = path
        self.initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            for sql in SCHEMA.values():
                conn.execute(sql)
            for table, columns in MIGRATIONS.items():
                existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
                for name, definition in columns.items():
                    if name not in existing:
                        conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_deadline ON orders(deadline)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_responsible ON orders(responsible)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_responses_order ON responses(order_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_events_order ON events(order_id)")

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> int:
        with self.connection() as conn:
            cur = conn.execute(sql, params)
            return int(cur.lastrowid or 0)

    def fetchone(self, sql: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        with self.connection() as conn:
            return conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        with self.connection() as conn:
            return conn.execute(sql, params).fetchall()

    def log(self, order_id: int, event_type: str, details: str = "") -> None:
        self.execute("INSERT INTO events(order_id,event_type,details,created_at) VALUES(?,?,?,?)", (order_id, event_type, details, datetime.now().isoformat(timespec="seconds")))

    def get_orders(self) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM orders ORDER BY CASE WHEN status='done' THEN 2 ELSE 0 END, deadline ASC, id DESC")

    def get_order(self, order_id: int) -> sqlite3.Row | None:
        return self.fetchone("SELECT * FROM orders WHERE id=?", (order_id,))

    def get_responses(self, order_id: int) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM responses WHERE order_id=? ORDER BY response_date DESC,id DESC", (order_id,))

    def get_events(self, order_id: int) -> list[sqlite3.Row]:
        return self.fetchall("SELECT * FROM events WHERE order_id=? ORDER BY created_at DESC,id DESC", (order_id,))

    def set_setting(self, key: str, value: str) -> None:
        self.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.fetchone("SELECT value FROM settings WHERE key=?", (key,))
        return str(row[0]) if row else default

    def delete_order(self, order_id: int) -> None:
        with self.connection() as conn:
            conn.execute("DELETE FROM responses WHERE order_id=?", (order_id,))
            conn.execute("DELETE FROM events WHERE order_id=?", (order_id,))
            conn.execute("DELETE FROM orders WHERE id=?", (order_id,))
