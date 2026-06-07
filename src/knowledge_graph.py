from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Union

from src import graph as reasoning_graph


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

REQUIRED_NODE_FIELDS = reasoning_graph.REQUIRED_NODE_FIELDS


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


def normalize_node(raw_node: dict[str, Any]) -> dict[str, Any]:
    return reasoning_graph.normalize_node(raw_node)


def load_knowledge_graph(path: PathLike) -> list[dict[str, Any]]:
    return reasoning_graph.load_knowledge_graph(path)


def validate_prerequisites(nodes: Iterable[dict[str, Any]]) -> None:
    reasoning_graph.validate_graph(nodes)


def group_nodes_by_level(nodes: Iterable[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[int(node["level"])].append(node)

    return {
        level: sorted(items, key=lambda item: (item["chain"], item["id"]))
        for level, items in sorted(grouped.items())
    }


def default_statuses(nodes: Iterable[dict[str, Any]]) -> dict[str, str]:
    return {node["id"]: STATUS_NOT_STARTED for node in nodes}


def get_prerequisite_nodes(
    nodes: Iterable[dict[str, Any]],
    node_id: str,
) -> list[dict[str, Any]]:
    return reasoning_graph.get_prerequisite_nodes(nodes, node_id)


def get_derived_nodes(
    nodes: Iterable[dict[str, Any]],
    node_id: str,
) -> list[dict[str, Any]]:
    return reasoning_graph.get_derived_nodes(nodes, node_id)


def group_nodes_by_chain(
    nodes: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    return reasoning_graph.group_nodes_by_chain(nodes)


def chain_nodes(nodes: Iterable[dict[str, Any]], chain: str) -> list[dict[str, Any]]:
    return reasoning_graph.chain_nodes(nodes, chain)
