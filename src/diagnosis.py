from __future__ import annotations

import re
from typing import Any, Optional


PUNCTUATION_PATTERN = re.compile(r"[\s，。！？、；：,.!?;:\"'（）()【】\[\]《》<>]+")


def normalize_text(text: Any) -> str:
    return PUNCTUATION_PATTERN.sub("", str(text or "").lower())


def keyword_set(text: Any) -> set[str]:
    normalized = normalize_text(text)
    if not normalized:
        return set()

    chunks = re.split(r"[和与及或的了是为在中]+", str(text or "").lower())
    words = {normalize_text(chunk) for chunk in chunks if len(normalize_text(chunk)) >= 2}
    if words:
        return words

    return {normalized[index : index + 2] for index in range(max(len(normalized) - 1, 0))}


def is_answer_correct(student_answer: Any, reference_answer: Any) -> bool:
    student_text = normalize_text(student_answer)
    reference_text = normalize_text(reference_answer)
    if not student_text or not reference_text:
        return False

    if student_text == reference_text:
        return True

    if len(reference_text) >= 2 and reference_text in student_text:
        return True

    if len(student_text) >= 2 and student_text in reference_text:
        return True

    reference_keywords = keyword_set(reference_answer)
    student_keywords = keyword_set(student_answer)
    if not reference_keywords:
        return False

    matched = len(reference_keywords & student_keywords)
    return matched / len(reference_keywords) >= 0.6


def recommend_fallback_node(
    node: dict[str, Any],
    node_map: dict[str, dict[str, Any]],
) -> Optional[str]:
    prerequisites = node.get("prerequisites", [])
    if prerequisites:
        return str(prerequisites[-1])

    current_level = int(node.get("level", 1))
    lower_level_nodes = [
        item for item in node_map.values() if int(item.get("level", 1)) < current_level
    ]
    if not lower_level_nodes:
        return None

    lower_level_nodes.sort(key=lambda item: (int(item.get("level", 1)), item.get("id", "")))
    return str(lower_level_nodes[-1]["id"])


def diagnose_answer(
    node: dict[str, Any],
    student_answer: Any,
    reference_answer: Any,
    node_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    student_text = normalize_text(student_answer)
    reference_keywords = keyword_set(reference_answer)
    student_keywords = keyword_set(student_answer)
    matched_keywords = reference_keywords & student_keywords
    recommended_node_id = recommend_fallback_node(node, node_map)

    if not student_text:
        error_type = "未作答"
        suggestion = "先回到节点解释部分，补全关键概念后再尝试。"
    elif reference_keywords and not matched_keywords:
        error_type = "核心概念缺失"
        suggestion = "答案没有覆盖参考答案中的核心关键词，建议回看学习目标和解释。"
    elif reference_keywords and len(matched_keywords) / len(reference_keywords) < 0.6:
        error_type = "理解不完整"
        suggestion = "答案触及了部分概念，但关键要素不足，建议补充完整定义和因果关系。"
    else:
        error_type = "表达不准确"
        suggestion = "答案方向接近，但表述与参考答案仍有差距，建议对照例题重新组织语言。"

    return {
        "is_correct": False,
        "error_type": error_type,
        "suggestion": suggestion,
        "recommended_node_id": recommended_node_id,
        "recommended_node_title": (
            node_map[recommended_node_id]["title"]
            if recommended_node_id and recommended_node_id in node_map
            else ""
        ),
    }

