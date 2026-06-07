from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Union

from src.content import load_yaml


PathLike = Union[str, Path]

STATUS_NOT_STARTED = "not_started"
STATUS_LEARNING = "learning"
STATUS_MASTERED = "mastered"
STATUS_WEAK = "weak"
STATUS_REVIEW = "review"

STATUS_VALUES = (
    STATUS_NOT_STARTED,
    STATUS_LEARNING,
    STATUS_MASTERED,
    STATUS_WEAK,
    STATUS_REVIEW,
)

STATUS_LABELS = {
    STATUS_NOT_STARTED: "未学习",
    STATUS_LEARNING: "学习中",
    STATUS_MASTERED: "已掌握",
    STATUS_WEAK: "薄弱",
    STATUS_REVIEW: "需要复习",
}

LABEL_TO_STATUS = {label: value for value, label in STATUS_LABELS.items()}

LEGACY_STATUS_MAP = {
    "locked": STATUS_NOT_STARTED,
    "available": STATUS_NOT_STARTED,
    "completed": STATUS_MASTERED,
    "未解锁": STATUS_NOT_STARTED,
    "可学习": STATUS_NOT_STARTED,
    "已完成": STATUS_MASTERED,
}

REQUIRED_NODE_FIELDS = (
    "id",
    "title",
    "level",
    "prerequisites",
    "learning_objective",
    "explanation",
    "common_misconceptions",
    "exercises",
    "mastery_questions",
)


def normalize_status(status: str | None) -> str:
    if not status:
        return STATUS_NOT_STARTED
    if status in STATUS_VALUES:
        return status
    if status in LABEL_TO_STATUS:
        return LABEL_TO_STATUS[status]
    return LEGACY_STATUS_MAP.get(status, STATUS_NOT_STARTED)


def status_label(status: str | None) -> str:
    return STATUS_LABELS[normalize_status(status)]


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_node(raw_node: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_NODE_FIELDS if field not in raw_node]
    if missing:
        node_id = raw_node.get("id", "<unknown>")
        raise ValueError(f"Knowledge node {node_id} missing fields: {', '.join(missing)}")

    node = dict(raw_node)
    node["id"] = str(node["id"])
    node["title"] = str(node["title"])
    node["level"] = int(node["level"])
    node["prerequisites"] = [str(item) for item in to_list(node["prerequisites"])]
    node["learning_objective"] = str(node["learning_objective"])
    node["explanation"] = str(node["explanation"])
    node["common_misconceptions"] = to_list(node["common_misconceptions"])
    node["exercises"] = to_list(node["exercises"])
    node["mastery_questions"] = to_list(node["mastery_questions"])
    return node


def load_knowledge_graph(path: PathLike) -> list[dict[str, Any]]:
    data = load_yaml(path)
    nodes = [normalize_node(node) for node in data.get("nodes", [])]
    validate_prerequisites(nodes)
    return sorted(nodes, key=lambda node: (node["level"], node["id"]))


def validate_prerequisites(nodes: Iterable[dict[str, Any]]) -> None:
    node_list = list(nodes)
    node_ids = {node["id"] for node in node_list}
    errors = []

    for node in node_list:
        for prerequisite in node["prerequisites"]:
            if prerequisite not in node_ids:
                errors.append(f"{node['id']} -> {prerequisite}")

    if errors:
        raise ValueError("Unknown prerequisite node ids: " + ", ".join(errors))


def group_nodes_by_level(nodes: Iterable[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[int(node["level"])].append(node)

    return {
        level: sorted(items, key=lambda item: item["id"])
        for level, items in sorted(grouped.items())
    }


def default_statuses(nodes: Iterable[dict[str, Any]]) -> dict[str, str]:
    return {node["id"]: STATUS_NOT_STARTED for node in nodes}

