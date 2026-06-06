from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union


DB_PATH = Path("data/skilltree_finance.sqlite3")
PathLike = Union[str, Path]


def now_text() -> str:
    return datetime.now().isoformat(timespec="seconds")


def connect(db_path: PathLike = DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_code TEXT,
            class_name TEXT,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            phase TEXT NOT NULL CHECK(phase IN ('pretest', 'posttest')),
            question_id TEXT NOT NULL,
            selected_answer TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL CHECK(is_correct IN (0, 1)),
            created_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS node_status (
            student_id INTEGER NOT NULL,
            node_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('locked', 'available', 'completed')),
            updated_at TEXT NOT NULL,
            PRIMARY KEY(student_id, node_id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS learning_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            node_id TEXT,
            action TEXT NOT NULL,
            detail TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );

        CREATE INDEX IF NOT EXISTS idx_answers_student_phase
            ON answers(student_id, phase);

        CREATE INDEX IF NOT EXISTS idx_logs_student_time
            ON learning_logs(student_id, created_at);
        """
    )
    conn.commit()


def get_or_create_student(
    conn: sqlite3.Connection,
    name: str,
    student_code: str = "",
    class_name: str = "",
) -> int:
    clean_name = name.strip()
    clean_code = student_code.strip()
    clean_class = class_name.strip()

    if clean_code:
        row = conn.execute(
            "SELECT id FROM students WHERE student_code = ? ORDER BY id LIMIT 1",
            (clean_code,),
        ).fetchone()
    else:
        row = conn.execute(
            """
            SELECT id FROM students
            WHERE name = ? AND COALESCE(class_name, '') = ?
            ORDER BY id LIMIT 1
            """,
            (clean_name, clean_class),
        ).fetchone()

    if row:
        return int(row["id"])

    cursor = conn.execute(
        """
        INSERT INTO students(name, student_code, class_name, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (clean_name, clean_code, clean_class, now_text()),
    )
    conn.commit()
    return int(cursor.lastrowid)


def get_student(conn: sqlite3.Connection, student_id: int) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()


def save_answer(
    conn: sqlite3.Connection,
    student_id: int,
    phase: str,
    question_id: str,
    selected_answer: str,
    correct_answer: str,
) -> None:
    conn.execute(
        """
        INSERT INTO answers(
            student_id, phase, question_id, selected_answer,
            correct_answer, is_correct, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            phase,
            question_id,
            selected_answer,
            correct_answer,
            int(selected_answer == correct_answer),
            now_text(),
        ),
    )
    conn.commit()


def get_latest_answers(
    conn: sqlite3.Connection,
    student_id: int,
    phase: str,
) -> list[sqlite3.Row]:
    rows = conn.execute(
        """
        SELECT a.*
        FROM answers a
        JOIN (
            SELECT question_id, MAX(id) AS latest_id
            FROM answers
            WHERE student_id = ? AND phase = ?
            GROUP BY question_id
        ) latest ON latest.latest_id = a.id
        ORDER BY a.question_id
        """,
        (student_id, phase),
    ).fetchall()
    return list(rows)


def get_node_statuses(conn: sqlite3.Connection, student_id: int) -> dict[str, str]:
    rows = conn.execute(
        "SELECT node_id, status FROM node_status WHERE student_id = ?",
        (student_id,),
    ).fetchall()
    return {row["node_id"]: row["status"] for row in rows}


def set_node_status(
    conn: sqlite3.Connection,
    student_id: int,
    node_id: str,
    status: str,
) -> None:
    conn.execute(
        """
        INSERT INTO node_status(student_id, node_id, status, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id, node_id) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at
        """,
        (student_id, node_id, status, now_text()),
    )
    conn.commit()


def ensure_node_statuses(
    conn: sqlite3.Connection,
    student_id: int,
    nodes: list[dict[str, Any]],
) -> None:
    existing = get_node_statuses(conn, student_id)
    for node in nodes:
        node_id = str(node["id"])
        if node_id in existing:
            continue
        initial_status = "available" if not node.get("prerequisites") else "locked"
        set_node_status(conn, student_id, node_id, initial_status)


def log_event(
    conn: sqlite3.Connection,
    student_id: int,
    action: str,
    node_id: Optional[str] = None,
    detail: str = "",
) -> None:
    conn.execute(
        """
        INSERT INTO learning_logs(student_id, node_id, action, detail, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (student_id, node_id, action, detail, now_text()),
    )
    conn.commit()


def get_learning_logs(conn: sqlite3.Connection, student_id: int) -> list[sqlite3.Row]:
    rows = conn.execute(
        """
        SELECT node_id, action, detail, created_at
        FROM learning_logs
        WHERE student_id = ?
        ORDER BY id DESC
        LIMIT 100
        """,
        (student_id,),
    ).fetchall()
    return list(rows)
