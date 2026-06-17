import sqlite3
from datetime import datetime

DB_PATH = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL CHECK(priority IN ('Alta', 'Média', 'Baixa')),
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)


def add_task(title: str, description: str, priority: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, priority, created_at) VALUES (?, ?, ?, ?)",
            (title, description, priority, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        return cursor.lastrowid


def get_tasks(priority_filter: str = "Todas", status_filter: str = "Todas") -> list:
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if priority_filter != "Todas":
        query += " AND priority = ?"
        params.append(priority_filter)

    if status_filter == "Concluídas":
        query += " AND completed = 1"
    elif status_filter == "Pendentes":
        query += " AND completed = 0"

    query += " ORDER BY CASE priority WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 WHEN 'Baixa' THEN 3 END, created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def toggle_task(task_id: int, completed: bool):
    with get_connection() as conn:
        conn.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (1 if completed else 0, task_id),
        )


def delete_task(task_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
