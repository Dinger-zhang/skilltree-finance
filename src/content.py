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
    from src.knowledge_graph import load_knowledge_graph as load_graph

    return load_graph(path)


def load_questions(path: PathLike) -> dict[str, list[dict[str, Any]]]:
    data = load_yaml(path)
    return {
        "pretest": data.get("pretest", []),
        "posttest": data.get("posttest", []),
    }
