

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Dict, Any


DB_PATH = Path(__file__).with_name("tasks.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицу tasks, если её нет."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);"
        )


def add_task(user_id: int, text: str) -> int:
    text = text.strip()
    if not text:
        raise ValueError("Текст задачи пустой")

    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO tasks(user_id, text) VALUES(?, ?)",
            (int(user_id), text),
        )
        return int(cur.lastrowid)


def list_tasks(user_id: int) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, text, created_at FROM tasks WHERE user_id = ? ORDER BY id",
            (int(user_id),),
        ).fetchall()

    return [{"id": int(r["id"]), "text": str(r["text"]), "created_at": str(r["created_at"])} for r in rows]


def delete_task(user_id: int, task_id: int) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM tasks WHERE user_id = ? AND id = ?",
            (int(user_id), int(task_id)),
        )
        return cur.rowcount > 0


def update_task(user_id: int, task_id: int, new_text: str) -> bool:
    new_text = new_text.strip()
    if not new_text:
        raise ValueError("Новый текст задачи пустой")

    with _connect() as conn:
        cur = conn.execute(
            "UPDATE tasks SET text = ? WHERE user_id = ? AND id = ?",
            (new_text, int(user_id), int(task_id)),
        )
        return cur.rowcount > 0