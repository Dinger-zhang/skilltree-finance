from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from src.knowledge_graph import STATUS_NOT_STARTED, STATUS_VALUES, normalize_status


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


def create_node_status_table(conn: sqlite3.Connection) -> None:
    allowed_statuses = "', '".join(STATUS_VALUES)
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS node_status (
            student_id INTEGER NOT NULL,
            node_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('{allowed_statuses}')),
            updated_at TEXT NOT NULL,
            PRIMARY KEY(student_id, node_id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """
    )


def migrate_node_status_table(conn: sqlite3.Connection) -> None:
    row = conn.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = 'node_status'
        """
    ).fetchone()
    if not row:
        create_node_status_table(conn)
        return

    table_sql = row["sql"] or ""
    if STATUS_NOT_STARTED in table_sql and "locked" not in table_sql:
        return

    old_rows = conn.execute(
        "SELECT student_id, node_id, status, updated_at FROM node_status"
    ).fetchall()

    conn.execute("ALTER TABLE node_status RENAME TO node_status_legacy")
    create_node_status_table(conn)
    for old_row in old_rows:
        conn.execute(
            """
            INSERT OR REPLACE INTO node_status(student_id, node_id, status, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                old_row["student_id"],
                old_row["node_id"],
                normalize_status(old_row["status"]),
                old_row["updated_at"],
            ),
        )
    conn.execute("DROP TABLE node_status_legacy")


def table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def ensure_answers_table_columns(conn: sqlite3.Connection) -> None:
    columns = table_columns(conn, "answers")
    column_sql = {
        "question_type": "ALTER TABLE answers ADD COLUMN question_type TEXT",
        "node_id": "ALTER TABLE answers ADD COLUMN node_id TEXT",
        "score": "ALTER TABLE answers ADD COLUMN score REAL",
        "max_score": "ALTER TABLE answers ADD COLUMN max_score REAL",
        "needs_manual_grading": (
            "ALTER TABLE answers ADD COLUMN needs_manual_grading INTEGER DEFAULT 0"
        ),
        "grading_status": "ALTER TABLE answers ADD COLUMN grading_status TEXT",
    }
    for column_name, sql in column_sql.items():
        if column_name not in columns:
            conn.execute(sql)


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
            question_type TEXT,
            node_id TEXT,
            score REAL,
            max_score REAL,
            needs_manual_grading INTEGER DEFAULT 0,
            grading_status TEXT,
            created_at TEXT NOT NULL,
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

        CREATE TABLE IF NOT EXISTS node_learning_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            node_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            item_type TEXT NOT NULL,
            prompt TEXT NOT NULL,
            student_answer TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL CHECK(is_correct IN (0, 1)),
            duration_seconds INTEGER NOT NULL,
            error_type TEXT,
            recommended_node_id TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );

        CREATE INDEX IF NOT EXISTS idx_answers_student_phase
            ON answers(student_id, phase);

        CREATE INDEX IF NOT EXISTS idx_logs_student_time
            ON learning_logs(student_id, created_at);

        CREATE INDEX IF NOT EXISTS idx_node_learning_student_node
            ON node_learning_records(student_id, node_id);
        """
    )
    ensure_answers_table_columns(conn)
    migrate_node_status_table(conn)
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
    is_correct: Optional[bool] = None,
    question_type: str = "",
    node_id: str = "",
    score: Optional[float] = None,
    max_score: Optional[float] = None,
    needs_manual_grading: bool = False,
    grading_status: Optional[str] = None,
) -> None:
    answer_is_correct = selected_answer == correct_answer if is_correct is None else is_correct
    if max_score is None:
        max_score = 1.0
    if score is None:
        score = max_score if answer_is_correct else 0.0
    if grading_status is None:
        grading_status = "pending_manual" if needs_manual_grading else "auto_graded"

    conn.execute(
        """
        INSERT INTO answers(
            student_id, phase, question_id, selected_answer,
            correct_answer, is_correct, question_type, node_id,
            score, max_score, needs_manual_grading, grading_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            phase,
            question_id,
            selected_answer,
            correct_answer,
            int(answer_is_correct),
            question_type,
            node_id,
            float(score),
            float(max_score),
            int(needs_manual_grading),
            grading_status,
            now_text(),
        ),
    )
    conn.commit()


def save_answer_result(
    conn: sqlite3.Connection,
    student_id: int,
    phase: str,
    result: dict[str, Any],
) -> None:
    save_answer(
        conn,
        student_id,
        phase,
        result["question_id"],
        result["selected_answer"],
        result["correct_answer"],
        is_correct=bool(result["is_correct"]),
        question_type=str(result.get("question_type", "")),
        node_id=str(result.get("node_id", "")),
        score=float(result.get("score", 0)),
        max_score=float(result.get("max_score", 1)),
        needs_manual_grading=bool(result.get("needs_manual_grading", False)),
    )


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
    return {row["node_id"]: normalize_status(row["status"]) for row in rows}


def set_node_status(
    conn: sqlite3.Connection,
    student_id: int,
    node_id: str,
    status: str,
) -> None:
    normalized_status = normalize_status(status)
    conn.execute(
        """
        INSERT INTO node_status(student_id, node_id, status, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id, node_id) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at
        """,
        (student_id, node_id, normalized_status, now_text()),
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
        set_node_status(conn, student_id, node_id, STATUS_NOT_STARTED)


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


def save_node_learning_record(
    conn: sqlite3.Connection,
    student_id: int,
    node_id: str,
    item_id: str,
    item_type: str,
    prompt: str,
    student_answer: str,
    correct_answer: str,
    is_correct: bool,
    duration_seconds: int,
    error_type: str = "",
    recommended_node_id: str = "",
) -> None:
    conn.execute(
        """
        INSERT INTO node_learning_records(
            student_id, node_id, item_id, item_type, prompt,
            student_answer, correct_answer, is_correct, duration_seconds,
            error_type, recommended_node_id, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            node_id,
            item_id,
            item_type,
            prompt,
            student_answer,
            correct_answer,
            int(is_correct),
            int(duration_seconds),
            error_type,
            recommended_node_id,
            now_text(),
        ),
    )
    conn.commit()


def get_node_learning_records(
    conn: sqlite3.Connection,
    student_id: int,
    node_id: str,
    limit: int = 20,
) -> list[sqlite3.Row]:
    rows = conn.execute(
        """
        SELECT item_id, item_type, prompt, student_answer, correct_answer,
               is_correct, duration_seconds, error_type, recommended_node_id,
               created_at
        FROM node_learning_records
        WHERE student_id = ? AND node_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (student_id, node_id, limit),
    ).fetchall()
    return list(rows)
