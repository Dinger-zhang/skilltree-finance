from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Union

from src.content import load_yaml


PathLike = Union[str, Path]

REQUIRED_NODE_FIELDS = (
    "id",
    "title",
    "layer",
    "chain",
    "type",
    "prerequisites",
    "derives",
    "contrasts",
    "core_question",
    "scenario",
    "guiding_questions",
    "rule_summary",
    "common_misconceptions",
    "mastery_question",
    "expected_reasoning_points",
)


class KnowledgeGraphError(ValueError):
    """Raised when the knowledge graph structure is invalid."""


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
        raise KnowledgeGraphError(
            f"Knowledge node {node_id} missing fields: {', '.join(missing)}"
        )

    node = dict(raw_node)
    node["id"] = str(node["id"])
    node["title"] = str(node["title"])
    node["layer"] = int(node["layer"])
    node["chain"] = str(node["chain"])
    node["type"] = str(node["type"])
    node["prerequisites"] = [str(item) for item in to_list(node["prerequisites"])]
    node["derives"] = [str(item) for item in to_list(node["derives"])]
    node["contrasts"] = [str(item) for item in to_list(node["contrasts"])]
    node["core_question"] = str(node["core_question"])
    node["scenario"] = str(node["scenario"])
    node["guiding_questions"] = [str(item) for item in to_list(node["guiding_questions"])]
    node["rule_summary"] = str(node["rule_summary"])
    node["common_misconceptions"] = [
        str(item) for item in to_list(node["common_misconceptions"])
    ]
    node["mastery_question"] = str(node["mastery_question"])
    node["expected_reasoning_points"] = [
        str(item) for item in to_list(node["expected_reasoning_points"])
    ]

    add_legacy_compatibility_fields(node)
    return node


def add_legacy_compatibility_fields(node: dict[str, Any]) -> None:
    """Populate old page fields without changing the v0.2 graph schema."""
    node["level"] = node["layer"]
    node["learning_objective"] = node["core_question"]
    node["explanation"] = f"{node['scenario']}\n\n{node['rule_summary']}"
    node["exercises"] = [
        {"prompt": question, "answer": "请结合本节点规则自行推理。"}
        for question in node["guiding_questions"]
    ]
    node["mastery_questions"] = [
        {
            "question": node["mastery_question"],
            "answer": "；".join(node["expected_reasoning_points"]),
        }
    ]


def load_knowledge_graph(path: PathLike) -> list[dict[str, Any]]:
    data = load_yaml(path)
    nodes = [normalize_node(node) for node in data.get("nodes", [])]
    validate_graph(nodes)
    return sorted(nodes, key=lambda node: (node["chain"], node["layer"], node["id"]))


def node_map(nodes: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {node["id"]: node for node in nodes}


def validate_graph(nodes: Iterable[dict[str, Any]]) -> None:
    node_list = list(nodes)
    ids = [node["id"] for node in node_list]
    duplicate_ids = sorted({node_id for node_id in ids if ids.count(node_id) > 1})
    if duplicate_ids:
        raise KnowledgeGraphError("Duplicate node ids: " + ", ".join(duplicate_ids))

    id_set = set(ids)
    errors = []
    for node in node_list:
        for prerequisite in node["prerequisites"]:
            if prerequisite not in id_set:
                errors.append(f"{node['id']} prerequisite -> {prerequisite}")
        for derived in node["derives"]:
            if derived not in id_set:
                errors.append(f"{node['id']} derives -> {derived}")

    if errors:
        raise KnowledgeGraphError("Unknown linked node ids: " + ", ".join(errors))


def get_prerequisite_nodes(
    nodes: Iterable[dict[str, Any]],
    node_id: str,
) -> list[dict[str, Any]]:
    by_id = node_map(nodes)
    node = by_id.get(node_id)
    if not node:
        return []
    return [by_id[item] for item in node["prerequisites"] if item in by_id]


def get_derived_nodes(
    nodes: Iterable[dict[str, Any]],
    node_id: str,
) -> list[dict[str, Any]]:
    by_id = node_map(nodes)
    node = by_id.get(node_id)
    if not node:
        return []
    return [by_id[item] for item in node["derives"] if item in by_id]


def group_nodes_by_chain(
    nodes: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[node["chain"]].append(node)

    return {
        chain: sorted(items, key=lambda item: (item["layer"], item["id"]))
        for chain, items in sorted(grouped.items())
    }


def chain_nodes(nodes: Iterable[dict[str, Any]], chain: str) -> list[dict[str, Any]]:
    return group_nodes_by_chain(nodes).get(chain, [])


def chain_labels(nodes: Iterable[dict[str, Any]]) -> list[str]:
    return list(group_nodes_by_chain(nodes).keys())
