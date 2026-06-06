from __future__ import annotations

import json
from typing import Any


QUESTION_SINGLE = "single_choice"
QUESTION_MULTIPLE = "multiple_choice"
QUESTION_SHORT = "short_answer"

AUTO_GRADED_TYPES = {QUESTION_SINGLE, QUESTION_MULTIPLE}


def question_type(question: dict[str, Any]) -> str:
    explicit_type = question.get("type") or question.get("question_type")
    if explicit_type:
        return str(explicit_type)
    if "options" not in question:
        return QUESTION_SHORT
    if isinstance(question.get("answer"), list):
        return QUESTION_MULTIPLE
    return QUESTION_SINGLE


def question_score(question: dict[str, Any]) -> float:
    return float(question.get("score", 1))


def answer_keys(answer: Any) -> list[str]:
    if answer is None:
        return []
    if isinstance(answer, list):
        return sorted(str(item).strip() for item in answer if str(item).strip())
    if isinstance(answer, tuple):
        return sorted(str(item).strip() for item in answer if str(item).strip())
    text = str(answer).strip()
    if not text:
        return []
    if "," in text:
        return sorted(item.strip() for item in text.split(",") if item.strip())
    return [text]


def serialize_answer(answer: Any) -> str:
    if isinstance(answer, (list, tuple)):
        return json.dumps(list(answer), ensure_ascii=False)
    return "" if answer is None else str(answer)


def deserialize_answer(answer: str) -> Any:
    text = answer or ""
    if text.startswith("["):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return text


def correct_answer(question: dict[str, Any]) -> Any:
    return question.get("answer", question.get("reference_answer", ""))


def is_manual_question(question: dict[str, Any]) -> bool:
    return question_type(question) == QUESTION_SHORT


def grade_question(question: dict[str, Any], student_answer: Any) -> dict[str, Any]:
    q_type = question_type(question)
    max_score = question_score(question)
    expected_answer = correct_answer(question)

    if q_type == QUESTION_SHORT:
        return {
            "question_id": question["id"],
            "node_id": question.get("node_id", ""),
            "question_type": q_type,
            "selected_answer": serialize_answer(student_answer),
            "correct_answer": serialize_answer(expected_answer),
            "is_correct": False,
            "score": 0.0,
            "max_score": max_score,
            "needs_manual_grading": True,
        }

    selected_keys = answer_keys(student_answer)
    expected_keys = answer_keys(expected_answer)
    is_correct = selected_keys == expected_keys
    score = max_score if is_correct else 0.0

    return {
        "question_id": question["id"],
        "node_id": question.get("node_id", ""),
        "question_type": q_type,
        "selected_answer": serialize_answer(selected_keys if q_type == QUESTION_MULTIPLE else selected_keys[0] if selected_keys else ""),
        "correct_answer": serialize_answer(expected_keys if q_type == QUESTION_MULTIPLE else expected_keys[0] if expected_keys else ""),
        "is_correct": is_correct,
        "score": score,
        "max_score": max_score,
        "needs_manual_grading": False,
    }


def option_label(option_key: str, option_text: Any) -> str:
    return f"{option_key}. {option_text}"


def option_labels(question: dict[str, Any]) -> list[str]:
    return [
        option_label(option_key, option_text)
        for option_key, option_text in question.get("options", {}).items()
    ]


def selected_key(label: str) -> str:
    return label.split(".", 1)[0].strip()


def format_answer(answer: Any, options: dict[str, Any] | None = None) -> str:
    parsed_answer = deserialize_answer(answer) if isinstance(answer, str) else answer
    keys = answer_keys(parsed_answer)
    if not keys:
        return ""
    if not options:
        return "、".join(keys)
    return "；".join(option_label(key, options.get(key, "")) for key in keys)


def summarize_results(results: list[dict[str, Any]]) -> dict[str, float]:
    total_score = sum(float(result["score"]) for result in results)
    max_score = sum(float(result["max_score"]) for result in results)
    pending_manual = sum(1 for result in results if result["needs_manual_grading"])
    return {
        "total_score": total_score,
        "max_score": max_score,
        "pending_manual": float(pending_manual),
    }


def knowledge_point_scores(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for result in results:
        node_id = result.get("node_id") or "unknown"
        item = grouped.setdefault(
            node_id,
            {
                "node_id": node_id,
                "score": 0.0,
                "max_score": 0.0,
                "wrong_count": 0,
                "pending_manual": 0,
            },
        )
        item["score"] += float(result["score"])
        item["max_score"] += float(result["max_score"])
        if result["needs_manual_grading"]:
            item["pending_manual"] += 1
        elif float(result["score"]) < float(result["max_score"]):
            item["wrong_count"] += 1

    return list(grouped.values())


def weak_node_ids(results: list[dict[str, Any]]) -> list[str]:
    weak_nodes = []
    for result in results:
        if result.get("needs_manual_grading"):
            continue
        if float(result["score"]) < float(result["max_score"]):
            node_id = str(result.get("node_id") or "")
            if node_id and node_id not in weak_nodes:
                weak_nodes.append(node_id)
    return weak_nodes


def row_value(row: Any, key: str, default: Any = None) -> Any:
    try:
        if key in row.keys():
            value = row[key]
            return default if value is None else value
    except AttributeError:
        return row.get(key, default)
    return default


def results_from_answer_rows(rows: list[Any]) -> list[dict[str, Any]]:
    results = []
    for row in rows:
        max_score = float(row_value(row, "max_score", 1))
        score = float(row_value(row, "score", int(row_value(row, "is_correct", 0))))
        results.append(
            {
                "question_id": row_value(row, "question_id", ""),
                "node_id": row_value(row, "node_id", ""),
                "question_type": row_value(row, "question_type", QUESTION_SINGLE),
                "selected_answer": row_value(row, "selected_answer", ""),
                "correct_answer": row_value(row, "correct_answer", ""),
                "is_correct": bool(row_value(row, "is_correct", 0)),
                "score": score,
                "max_score": max_score,
                "needs_manual_grading": bool(row_value(row, "needs_manual_grading", 0)),
            }
        )
    return results

