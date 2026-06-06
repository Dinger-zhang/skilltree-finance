from __future__ import annotations

from pathlib import Path
from typing import Any, Union

import yaml


PathLike = Union[str, Path]


def load_yaml(path: PathLike) -> dict[str, Any]:
    """Load a YAML file and return an empty dict when the file is blank."""
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_knowledge_graph(path: PathLike) -> list[dict[str, Any]]:
    data = load_yaml(path)
    nodes = data.get("nodes", [])
    return sorted(nodes, key=lambda node: (node.get("level", 0), node.get("id", "")))


def load_questions(path: PathLike) -> dict[str, list[dict[str, Any]]]:
    data = load_yaml(path)
    return {
        "pretest": data.get("pretest", []),
        "posttest": data.get("posttest", []),
    }
