from __future__ import annotations

from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit

import yaml


LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]
B_CHAIN_ID = "B. 从交易到利润表"
DEFAULT_MOCK_OUTPUT_DIR = LAB_DIR / "outputs" / "ssl_v0_3_minimal"
DEFAULT_REAL_OUTPUT_DIR = LAB_DIR / "outputs" / "ssl_real_smoke"
DEFAULT_CONDITIONS = (
    "no_course_baseline",
    "node_only",
    "chain_so_far",
    "hidden_transfer",
)


FALLBACK_B_NODES: list[dict[str, Any]] = [
    {
        "id": "income_statement_boundary",
        "title": "交易进入利润表的边界",
        "layer": 1,
        "chain": B_CHAIN_ID,
        "type": "concept",
        "prerequisites": [],
        "derives": ["revenue_recognition"],
        "core_question": "哪些交易应该进入利润表，哪些只是现金或融资变化？",
        "scenario": "奶茶店卖出饮品，也可能收到借款或股东投入。不是所有现金流入都代表经营收入。",
        "guiding_questions": [
            "这件事是否来自销售商品或提供服务？",
            "它反映经营成果，还是只是资金来源变化？",
            "它会形成收入、成本或费用吗？",
        ],
        "rule_summary": "利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。",
        "common_misconceptions": [
            "把所有收到的钱都当成收入。",
            "把借款或股东投入当成利润。",
        ],
        "mastery_question": "为什么银行借款通常不应作为营业收入进入利润表？",
        "expected_reasoning_points": [
            "利润表记录一段期间的经营成果",
            "销售商品或提供服务才通常形成收入",
            "借款是筹资活动不是营业收入",
        ],
    },
    {
        "id": "revenue_recognition",
        "title": "收入确认",
        "layer": 2,
        "chain": B_CHAIN_ID,
        "type": "rule",
        "prerequisites": ["income_statement_boundary"],
        "derives": ["revenue_not_cash_receipt"],
        "core_question": "什么时候可以说企业本期赚到了收入？",
        "scenario": "设计公司本月完成并交付海报，但客户下月才付款。",
        "guiding_questions": [
            "服务是否已经完成或商品是否已经交付？",
            "客户付款时间会不会改变本期经营成果？",
            "收入确认关注赚到还是收到现金？",
        ],
        "rule_summary": "收入通常来自销售商品或提供服务；在权责发生制下，收入确认不一定等于收到现金。",
        "common_misconceptions": [
            "没收到现金就一定不能确认收入。",
            "所有进账都属于收入。",
        ],
        "mastery_question": "客户下月付款时，本月完成服务为什么仍可能确认收入？",
        "expected_reasoning_points": [
            "收入来自销售商品或提供服务",
            "完成交付或服务后可能满足收入确认条件",
            "收入确认不一定依赖现金已经到账",
        ],
    },
    {
        "id": "revenue_not_cash_receipt",
        "title": "收入不等于收款",
        "layer": 3,
        "chain": B_CHAIN_ID,
        "type": "contrast",
        "prerequisites": ["revenue_recognition"],
        "derives": ["expense_recognition"],
        "core_question": "为什么利润表收入增加，不一定代表现金已经增加？",
        "scenario": "批发商赊销商品，客户 45 天后付款。",
        "guiding_questions": [
            "商品是否已经卖出？",
            "现金是否已经收到？",
            "未收款时资产负债表可能出现什么项目？",
        ],
        "rule_summary": "收入记录赚到的经营成果；收款记录现金进入。赊销会让收入和现金流入出现时间差。",
        "common_misconceptions": [
            "收入增加就等于现金增加。",
            "赊销没有收到钱所以没有经营成果。",
        ],
        "mastery_question": "赊销商品时，为什么可能确认收入但现金没有增加？",
        "expected_reasoning_points": [
            "赊销可能先确认收入",
            "未收现金时现金不一定增加",
            "可能形成应收账款而不是现金流入",
        ],
    },
    {
        "id": "expense_recognition",
        "title": "费用确认",
        "layer": 4,
        "chain": B_CHAIN_ID,
        "type": "rule",
        "prerequisites": ["income_statement_boundary"],
        "derives": ["depreciation_amortization"],
        "core_question": "什么时候应把经营耗费记入本期费用？",
        "scenario": "员工已经完成本月工作，但工资下月发放。",
        "guiding_questions": [
            "耗费是否服务于本期经营？",
            "费用发生是否必须等到现金支付？",
            "费用会如何影响利润？",
        ],
        "rule_summary": "费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。",
        "common_misconceptions": [
            "没付款就没有费用。",
            "费用都代表当期现金流出。",
        ],
        "mastery_question": "为什么本月工资下月才发，也可能作为本月费用？",
        "expected_reasoning_points": [
            "费用是为取得收入或维持经营发生的耗费",
            "费用发生不一定等于当期已经付款",
            "工资费用会减少本期利润",
        ],
    },
    {
        "id": "depreciation_amortization",
        "title": "折旧与摊销是成本分配",
        "layer": 5,
        "chain": B_CHAIN_ID,
        "type": "rule",
        "prerequisites": ["expense_recognition"],
        "derives": ["gross_margin"],
        "core_question": "长期资产的成本为什么要分摊到多个期间？",
        "scenario": "面包店去年买烤箱，今年继续使用并按月计提折旧。",
        "guiding_questions": [
            "烤箱服务的是一个月还是多个期间？",
            "折旧影响利润时，是否一定发生新的现金付款？",
            "折旧把什么分配到使用期间？",
        ],
        "rule_summary": "折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。",
        "common_misconceptions": [
            "折旧就是每月真的付出一笔钱。",
            "折旧不会影响报表。",
        ],
        "mastery_question": "为什么折旧会减少利润，但通常不是当期现金流出？",
        "expected_reasoning_points": [
            "折旧是长期资产成本在多个期间的分摊",
            "折旧费用会减少当期利润",
            "折旧通常不是当期现金流出",
        ],
    },
    {
        "id": "gross_margin",
        "title": "毛利形成",
        "layer": 6,
        "chain": B_CHAIN_ID,
        "type": "calculation",
        "prerequisites": ["revenue_recognition", "expense_recognition"],
        "derives": ["net_profit"],
        "core_question": "收入扣除直接销售成本后得到什么？",
        "scenario": "服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。",
        "guiding_questions": [
            "销售成本是否直接对应卖出的商品？",
            "收入减销售成本得到什么？",
            "毛利是否已经扣除了所有期间费用？",
        ],
        "rule_summary": "毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。",
        "common_misconceptions": [
            "毛利率就是净利率。",
            "毛利高就一定最终赚钱。",
        ],
        "mastery_question": "为什么毛利率高不等于净利润一定高？",
        "expected_reasoning_points": [
            "毛利等于收入减销售成本",
            "毛利率等于毛利除以收入",
            "毛利还没有扣除销售管理研发财务等期间费用",
        ],
    },
    {
        "id": "net_profit",
        "title": "净利润推导",
        "layer": 7,
        "chain": B_CHAIN_ID,
        "type": "calculation",
        "prerequisites": ["gross_margin"],
        "derives": ["accrual_vs_cash"],
        "core_question": "如何从收入、成本和费用推出净利润？",
        "scenario": "公司有收入、销售成本和期间费用，暂不考虑税费。",
        "guiding_questions": [
            "收入先扣除哪些成本和费用？",
            "净利润反映经营成果还是现金余额？",
            "为什么利润为正仍可能现金紧张？",
        ],
        "rule_summary": "净利润大致是收入扣除成本、费用和税费后的结果，但净利润不等于现金。",
        "common_misconceptions": [
            "净利润为正就一定不缺钱。",
            "收入高的企业利润一定高。",
        ],
        "mastery_question": "为什么净利润为正仍不一定代表现金充足？",
        "expected_reasoning_points": [
            "净利润大致等于收入扣除成本费用和税费",
            "净利润可能包含未收现收入",
            "净利润可能包含非现金费用所以不等于现金",
        ],
    },
    {
        "id": "accrual_vs_cash",
        "title": "权责发生制与现金制",
        "layer": 8,
        "chain": B_CHAIN_ID,
        "type": "contrast",
        "prerequisites": ["revenue_recognition", "expense_recognition", "net_profit"],
        "derives": [],
        "core_question": "为什么同一笔业务在利润表和现金流中可能落在不同期间？",
        "scenario": "咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。",
        "guiding_questions": [
            "收入和费用属于哪个期间？",
            "现金实际在哪个期间收付？",
            "权责发生制和现金制分别关注什么？",
        ],
        "rule_summary": "权责发生制关注交易归属期间，现金制关注现金实际收付时间。",
        "common_misconceptions": [
            "权责发生制更关注现金是否实际收付。",
            "没付款就没有费用。",
        ],
        "mastery_question": "权责发生制和现金制的核心区别是什么？",
        "expected_reasoning_points": [
            "权责发生制关注交易归属期间",
            "满足条件时未收款也可能确认收入",
            "已发生费用即使未付款也可能归入本期",
            "现金制关注现金实际收付时间",
        ],
    },
]


REQUIRED_OUTPUT_FIELDS = (
    "run_id",
    "graph_version",
    "chain_id",
    "node_id",
    "condition",
    "student_persona",
    "student_model",
    "judge_model",
    "student_request_id",
    "judge_request_id",
    "question",
    "student_answer",
    "student_raw_response",
    "judge_raw_response",
    "student_parse_error",
    "judge_parse_error",
    "evidence_status",
    "persona_behavior_trace",
    "used_node_ids",
    "rule_score",
    "rule_score_detail",
    "rule_passed",
    "judge_score",
    "judge_passed",
    "matched_reasoning_points",
    "missing_reasoning_points",
    "misconception_tags",
    "external_knowledge_suspicion",
    "possible_rule_false_fail",
    "failure_type",
    "error_message",
    "created_at",
)


def resolve_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def load_yaml(path: str | Path) -> dict[str, Any]:
    with resolve_path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def write_yaml(path: str | Path, data: dict[str, Any]) -> None:
    with resolve_path(path).open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def apply_config_overrides(
    config: dict[str, Any],
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not overrides:
        return config

    if overrides.get("mock_mode") is not None:
        config["mock_mode"] = bool(overrides["mock_mode"])
    if overrides.get("output_dir"):
        config["output_dir"] = str(overrides["output_dir"])
    if overrides.get("max_nodes") is not None:
        config["max_nodes"] = int(overrides["max_nodes"])

    selected_node_ids = list(overrides.get("selected_node_ids") or [])
    node_id = overrides.get("node_id")
    if node_id:
        selected_node_ids = [str(node_id)]
    if selected_node_ids:
        config["selected_node_ids"] = [str(item) for item in selected_node_ids]

    for client_key, model_key in (
        ("student_client", "student_model"),
        ("judge_client", "judge_model"),
    ):
        if overrides.get(model_key):
            client_config = config.setdefault(client_key, {})
            client_config["model"] = str(overrides[model_key])
            client_config["enabled"] = True

    for client_key, override_key, setting_key in (
        ("student_client", "student_api_key_env", "api_key_env"),
        ("student_client", "student_base_url_env", "base_url_env"),
        ("judge_client", "judge_api_key_env", "api_key_env"),
        ("judge_client", "judge_base_url_env", "base_url_env"),
    ):
        if overrides.get(override_key):
            config.setdefault(client_key, {})[setting_key] = str(overrides[override_key])

    return config


def finalize_runtime_config(config: dict[str, Any]) -> dict[str, Any]:
    files = config.setdefault("files", {})
    files.setdefault("chain_definitions", "data/chain_definitions.yaml")
    files.setdefault("personas", "experiments/synthetic_student_lab/personas.yaml")
    files.setdefault("transfer_cases", "experiments/synthetic_student_lab/transfer_cases.yaml")
    files.setdefault("simulation_runs", "simulation_runs.jsonl")
    files.setdefault("judge_results", "judge_results.jsonl")
    files.setdefault("node_failure_report", "node_failure_report.md")

    mock_mode = bool(config.get("mock_mode", True))
    output_dir = resolve_path(config.get("output_dir", DEFAULT_MOCK_OUTPUT_DIR))
    if not mock_mode and output_dir == DEFAULT_MOCK_OUTPUT_DIR:
        config["output_dir"] = str(DEFAULT_REAL_OUTPUT_DIR)

    for client_key in ("student_client", "judge_client"):
        client_config = config.setdefault(client_key, {})
        client_config.setdefault("enabled", True)
        client_config.setdefault("provider", "openai_compatible")
        client_config.setdefault("model", "")
        client_config.setdefault("temperature", 0.0)
        client_config.setdefault("timeout_seconds", 60)
    config["student_client"].setdefault("api_key_env", "SSL_STUDENT_API_KEY")
    config["student_client"].setdefault("base_url_env", "SSL_STUDENT_BASE_URL")
    config["judge_client"].setdefault("api_key_env", "SSL_JUDGE_API_KEY")
    config["judge_client"].setdefault("base_url_env", "SSL_JUDGE_BASE_URL")
    return config


def load_config(
    config_path: str | Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = config_path or LAB_DIR / "config.yaml"
    config = load_yaml(path)
    config.setdefault("experiment_id", "ssl_v0_3_minimal")
    config.setdefault("chain_id", B_CHAIN_ID)
    config.setdefault("mock_mode", True)
    config.setdefault("pass_ratio", 0.6)
    config.setdefault("conditions", list(DEFAULT_CONDITIONS))
    config.setdefault("allow_graph_fallback", True)
    apply_config_overrides(config, overrides)
    return finalize_runtime_config(config)


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def file_sha256_short(path: str | Path) -> str:
    resolved = resolve_path(path)
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    return digest[:12]


def graph_version(graph_path: str | Path, graph_data: dict[str, Any]) -> str:
    explicit = graph_data.get("version") or graph_data.get("graph_version")
    if explicit:
        return str(explicit)
    return f"sha256:{file_sha256_short(graph_path)}"


def load_graph(path: str | Path) -> tuple[list[dict[str, Any]], str]:
    data = load_yaml(path)
    nodes = data.get("nodes", [])
    if not isinstance(nodes, list):
        raise ValueError("knowledge_graph.yaml must contain a top-level list field: nodes")
    return [dict(node) for node in nodes], graph_version(path, data)


def find_chain_definition(data: dict[str, Any], chain_id: str) -> dict[str, Any] | None:
    chains = data.get("chains", [])
    if isinstance(chains, dict):
        chain = chains.get(chain_id)
        return dict(chain) if isinstance(chain, dict) else None
    if not isinstance(chains, list):
        return None
    for chain in chains:
        if isinstance(chain, dict) and str(chain.get("id", "")) == chain_id:
            return dict(chain)
    return None


def chain_definition_entries(chain: dict[str, Any]) -> list[Any]:
    nodes = chain.get("nodes")
    if isinstance(nodes, list) and nodes:
        return nodes
    node_ids = chain.get("node_ids")
    if isinstance(node_ids, list) and node_ids:
        return node_ids
    return []


def normalize_chain_definition_node(
    entry: Any,
    graph_by_id: dict[str, dict[str, Any]],
    chain_id: str,
    position: int,
) -> dict[str, Any]:
    if isinstance(entry, str):
        if entry not in graph_by_id:
            raise ValueError(f"chain_definitions.yaml references unknown node id: {entry}")
        raw_node = dict(graph_by_id[entry])
    elif isinstance(entry, dict):
        node_id = str(entry.get("id", ""))
        if not node_id:
            raise ValueError("chain_definitions.yaml node entry is missing id")
        raw_node = {**graph_by_id.get(node_id, {}), **entry}
    else:
        raise ValueError(f"Unsupported chain_definitions.yaml node entry: {entry!r}")

    normalized = normalize_reasoning_node(raw_node, chain_id)
    normalized["chain"] = chain_id
    normalized["layer"] = position
    return normalized


def select_chain_definition_nodes(
    graph_nodes: list[dict[str, Any]],
    chain_id: str,
    chain_definition_path: str | Path,
) -> list[dict[str, Any]] | None:
    resolved = resolve_path(chain_definition_path)
    if not resolved.exists():
        return None

    data = load_yaml(resolved)
    chain = find_chain_definition(data, chain_id)
    if chain is None:
        return None
    entries = chain_definition_entries(chain)
    if not entries:
        raise ValueError(f"chain_definitions.yaml chain {chain_id!r} has no nodes or node_ids")

    graph_by_id = {str(node.get("id", "")): dict(node) for node in graph_nodes}
    return [
        normalize_chain_definition_node(entry, graph_by_id, chain_id, index)
        for index, entry in enumerate(entries, start=1)
    ]


def to_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    result = []
    for item in items:
        if isinstance(item, dict):
            misconception = item.get("misconception", "")
            correction = item.get("correction", "")
            result.append("；".join(part for part in (misconception, correction) if part))
        else:
            result.append(str(item))
    return result


def normalize_reasoning_node(node: dict[str, Any], chain_id: str) -> dict[str, Any]:
    mastery_questions = node.get("mastery_questions") or []
    first_mastery = mastery_questions[0] if isinstance(mastery_questions, list) and mastery_questions else {}
    if isinstance(first_mastery, dict):
        mastery_question = first_mastery.get("question", "")
    else:
        mastery_question = str(first_mastery) if first_mastery else ""

    expected_points = to_string_list(node.get("expected_reasoning_points"))
    if not expected_points and isinstance(first_mastery, dict):
        expected_points = to_string_list(first_mastery.get("answer"))
    if not expected_points:
        expected_points = to_string_list(node.get("learning_objective"))

    normalized = {
        "id": str(node.get("id", "")),
        "title": str(node.get("title", node.get("id", ""))),
        "layer": int(node.get("layer", node.get("level", 999))),
        "chain": str(node.get("chain", chain_id)),
        "type": str(node.get("type", "concept")),
        "prerequisites": to_string_list(node.get("prerequisites")),
        "derives": to_string_list(node.get("derives")),
        "contrasts": to_string_list(node.get("contrasts")),
        "core_question": str(node.get("core_question", node.get("learning_objective", ""))),
        "scenario": str(node.get("scenario", node.get("explanation", ""))),
        "guiding_questions": to_string_list(node.get("guiding_questions")),
        "rule_summary": str(node.get("rule_summary", node.get("explanation", ""))),
        "common_misconceptions": to_string_list(node.get("common_misconceptions")),
        "mastery_question": str(node.get("mastery_question", mastery_question)),
        "expected_reasoning_points": expected_points,
    }
    if not normalized["guiding_questions"]:
        normalized["guiding_questions"] = ["请结合本节点材料说明你的推理过程。"]
    if not normalized["mastery_question"]:
        normalized["mastery_question"] = normalized["core_question"]
    return normalized


def select_chain_nodes(
    graph_nodes: list[dict[str, Any]],
    chain_id: str,
    allow_fallback: bool = True,
    chain_definition_path: str | Path | None = None,
) -> tuple[list[dict[str, Any]], bool]:
    definition_path = chain_definition_path or REPO_ROOT / "data" / "chain_definitions.yaml"
    chain_definition_nodes = select_chain_definition_nodes(
        graph_nodes,
        chain_id,
        definition_path,
    )
    if chain_definition_nodes:
        return chain_definition_nodes, False

    chain_nodes = [
        normalize_reasoning_node(node, chain_id)
        for node in graph_nodes
        if str(node.get("chain", "")) == chain_id
    ]
    if chain_nodes:
        return sorted(chain_nodes, key=lambda item: (item["layer"], item["id"])), False
    if not allow_fallback:
        raise ValueError(f"No nodes found with chain == {chain_id!r}")
    return [dict(node) for node in FALLBACK_B_NODES], True


def selected_node_indexes(
    chain_nodes: list[dict[str, Any]],
    selected_node_ids: list[str] | None = None,
    max_nodes: int | None = None,
) -> list[int]:
    id_to_index = {node["id"]: index for index, node in enumerate(chain_nodes)}
    if selected_node_ids:
        missing = [node_id for node_id in selected_node_ids if node_id not in id_to_index]
        if missing:
            raise ValueError(f"selected_node_ids not found in chain: {', '.join(missing)}")
        indexes = [id_to_index[node_id] for node_id in selected_node_ids]
    else:
        indexes = list(range(len(chain_nodes)))

    if max_nodes is not None:
        if max_nodes <= 0:
            raise ValueError("max_nodes must be greater than 0")
        indexes = indexes[:max_nodes]
    return indexes


def load_personas(path: str | Path) -> list[dict[str, Any]]:
    data = load_yaml(path)
    personas = data.get("personas", [])
    if not isinstance(personas, list) or not personas:
        raise ValueError("personas.yaml must contain a non-empty personas list")
    return [dict(persona) for persona in personas]


def load_transfer_cases(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    data = load_yaml(path)
    cases = data.get("cases", [])
    by_node: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        node_id = str(case.get("node_id", ""))
        if not node_id:
            continue
        by_node.setdefault(node_id, []).append(dict(case))
    return by_node


def transfer_case_for_node(
    node: dict[str, Any],
    cases_by_node: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    cases = cases_by_node.get(node["id"], [])
    if cases:
        return cases[0]
    return {
        "id": f"{node['id']}_auto_hidden_transfer",
        "node_id": node["id"],
        "case": node.get("scenario", ""),
        "question": node.get("mastery_question", node.get("core_question", "")),
        "expected_reasoning_points": node.get("expected_reasoning_points", []),
        "misconception_traps": node.get("common_misconceptions", []),
    }


def output_path(config: dict[str, Any], file_key: str) -> Path:
    files = config.get("files", {})
    output_dir = resolve_path(config.get("output_dir", LAB_DIR / "outputs" / "ssl_v0_3_minimal"))
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = files.get(file_key, file_key)
    return output_dir / filename


def write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None:
    resolved = resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    resolved = resolve_path(path)
    if not resolved.exists():
        raise FileNotFoundError(f"JSONL file not found: {resolved}")
    records = []
    with resolved.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {resolved}:{line_number}: {exc}") from exc
    return records


COMPLETENESS_BLOCKERS = (
    "不能完整判断",
    "无法完整判断",
    "不会判断",
    "不能判断",
    "不知道",
    "只能背规则",
    "只需要背规则",
)

RULE_PASS_RATIO_FLOOR = 2 / 3

BUILTIN_REASONING_POINT_ALIASES: dict[str, list[str]] = {
    "赊销可能先确认收入": [
        "赊销",
        "商品已经卖出",
        "货已经卖出",
        "已经交付",
        "可以确认收入",
        "可能确认收入",
        "利润表确认收入",
        "利润表可能确认收入",
        "收入确认遵循权责发生制",
    ],
    "未收现金时现金不一定增加": [
        "客户还没有付款",
        "客户尚未付款",
        "客户没有付款",
        "没有收到现金",
        "没有收到钱",
        "未收到现金",
        "未收到钱",
        "现金没有增加",
        "现金未增加",
        "现金并未增加",
        "现金不一定增加",
        "现金流入没有发生",
    ],
    "可能形成应收账款而不是现金流入": [
        "应收账款",
        "以后付款",
        "后付款",
        "后才付款",
        "天后付款",
        "天后才付款",
        "未来收款权利",
        "客户之后付款",
        "客户以后付款",
        "客户未来付款",
        "不是现金流入",
        "不是现金到账",
    ],
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", str(text).lower())


def point_tokens(point: str) -> list[str]:
    tokens = []
    for token in re.split(r"[/,，、；;:：。\.\s]+", str(point)):
        normalized = normalize_text(token)
        if len(normalized) >= 2:
            tokens.append(normalized)
    return tokens


def reasoning_point_text(point: Any) -> str:
    if isinstance(point, dict):
        for key in ("text", "point", "reasoning_point", "expected", "description"):
            value = point.get(key)
            if value is not None and str(value).strip():
                return str(value)
        return ""
    return str(point)


def reasoning_point_aliases(point: Any) -> list[str]:
    if not isinstance(point, dict):
        return []
    aliases = point.get("aliases", [])
    if aliases is None:
        return []
    if isinstance(aliases, list):
        return [str(alias) for alias in aliases if str(alias).strip()]
    return [str(aliases)] if str(aliases).strip() else []


def reasoning_point_required(point: Any) -> bool:
    return bool(point.get("required")) if isinstance(point, dict) else False


def normalize_reasoning_point(point: Any) -> dict[str, Any]:
    return {
        "text": reasoning_point_text(point).strip(),
        "aliases": reasoning_point_aliases(point),
        "required": reasoning_point_required(point),
    }


def normalize_expected_reasoning_points(points: list[Any]) -> list[dict[str, Any]]:
    return [
        config
        for config in (normalize_reasoning_point(point) for point in points)
        if config["text"]
    ]


def builtin_reasoning_point_aliases(point_text: str) -> list[str]:
    return BUILTIN_REASONING_POINT_ALIASES.get(point_text, [])


def reasoning_point_variants(point: Any) -> list[dict[str, str]]:
    config = normalize_reasoning_point(point)
    candidates = [
        {"source": "text", "value": config["text"]},
        *({"source": "alias", "value": alias} for alias in config["aliases"]),
        *(
            {"source": "builtin_alias", "value": alias}
            for alias in builtin_reasoning_point_aliases(config["text"])
        ),
    ]
    variants: list[dict[str, str]] = []
    seen: set[str] = set()
    for candidate in candidates:
        value = str(candidate["value"]).strip()
        key = normalize_text(value)
        if not value or key in seen:
            continue
        seen.add(key)
        variants.append({"source": candidate["source"], "value": value})
    return variants


def text_variant_matches(answer: str, variant: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_point = normalize_text(variant)
    if normalized_point and normalized_point in normalized_answer:
        return True
    tokens = point_tokens(variant)
    return any(token in normalized_answer for token in tokens)


def reasoning_point_match_detail(answer: str, point: Any) -> dict[str, Any]:
    config = normalize_reasoning_point(point)
    matched_by = [
        variant
        for variant in reasoning_point_variants(config)
        if text_variant_matches(answer, variant["value"])
    ]
    return {
        "point": config["text"],
        "required": config["required"],
        "matched": bool(matched_by),
        "matched_by": matched_by,
    }


def point_matched(answer: str, point: Any) -> bool:
    return bool(reasoning_point_match_detail(answer, point)["matched"])


def point_matches(answer: str, point: Any) -> bool:
    return point_matched(answer, point)


def has_completeness_blocker(answer: str) -> bool:
    normalized_answer = normalize_text(answer)
    return any(normalize_text(pattern) in normalized_answer for pattern in COMPLETENESS_BLOCKERS)


def evaluate_rule(
    answer: str,
    expected_points: list[Any],
    pass_ratio: float,
) -> dict[str, Any]:
    expected = normalize_expected_reasoning_points(expected_points)
    point_details = [reasoning_point_match_detail(answer, point) for point in expected]
    matched = [detail["point"] for detail in point_details if detail["matched"]]
    missing = [detail["point"] for detail in point_details if not detail["matched"]]
    required_missing = [
        detail["point"]
        for detail in point_details
        if detail["required"] and not detail["matched"]
    ]
    score = len(matched) / len(expected) if expected else 0.0
    configured_pass_ratio = float(pass_ratio)
    effective_pass_ratio = (
        configured_pass_ratio
        if configured_pass_ratio > 0.67
        else RULE_PASS_RATIO_FLOOR
    )
    required_count = (
        max(1, math.ceil((len(expected) * effective_pass_ratio) - 1e-9))
        if expected
        else 1
    )
    completeness_blocker = has_completeness_blocker(answer)
    rule_passed = len(matched) >= required_count
    failure_reason = ""
    if not rule_passed and required_missing:
        failure_reason = "missing_required_reasoning_points"
    if completeness_blocker:
        score = min(score, 0.4)
        rule_passed = False
        failure_reason = "completeness_blocker"
    elif not rule_passed and not failure_reason:
        failure_reason = "below_threshold"
    return {
        "rule_score": round(score, 4),
        "rule_passed": rule_passed,
        "matched_reasoning_points": matched,
        "missing_reasoning_points": missing,
        "required_missing_reasoning_points": required_missing,
        "required_count": required_count,
        "rule_score_detail": {
            "scoring_method": "matched_points / expected_points",
            "score": round(score, 4),
            "configured_pass_ratio": round(configured_pass_ratio, 4),
            "effective_pass_ratio": round(effective_pass_ratio, 4),
            "expected_count": len(expected),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "required_count": required_count,
            "completeness_blocker": completeness_blocker,
            "points": point_details,
        },
        "completeness_blocker": completeness_blocker,
        "rule_failure_reason": failure_reason,
    }


ENHANCED_SYNONYM_REPLACEMENTS = (
    ("收到现金", "现金收款"),
    ("现金到账", "现金收款"),
    ("现金流入", "现金收款"),
    ("收到钱", "现金收款"),
    ("收款", "现金收款"),
    ("客户付款", "现金收款"),
    ("确认收入", "收入确认"),
    ("记录收入", "收入确认"),
    ("计入收入", "收入确认"),
    ("利润表确认收入", "收入确认"),
    ("确认费用", "费用确认"),
    ("计入费用", "费用确认"),
    ("费用发生", "费用确认"),
    ("发生费用", "费用确认"),
    ("计提折旧", "折旧"),
    ("摊销", "折旧"),
    ("长期资产成本分摊", "折旧成本分摊"),
    ("资产成本分摊", "折旧成本分摊"),
    ("利润", "净利润"),
    ("经营成果", "净利润"),
    ("收入扣除成本费用", "净利润"),
    ("收入减成本费用", "净利润"),
)

CONTRADICTION_PATTERNS: dict[str, list[str]] = {
    "revenue_implies_cash": [
        "收入增加就一定现金增加",
        "收入增加说明现金也增加",
        "收入增加意味着现金也增加",
        "收入增加应该意味着现金也增加",
        "收入增加就代表现金增加",
        "收入就是现金流入",
        "收入就是收款",
        "收入等于收款",
    ],
    "cash_required_for_revenue": [
        "没收到钱所以不算收入",
        "没收到现金所以不算收入",
        "没收到钱就不算收入",
        "没收到现金就不算收入",
        "没收到钱就不能确认收入",
        "没收到现金就不能确认收入",
        "没收到钱怎么能算收入",
        "没收到现金怎么能算收入",
        "没有收到钱不能确认收入",
        "没有收到现金不能确认收入",
        "收入确认看的是有没有收到钱",
        "收入确认必须等到实际收款",
        "收入必须是在收到现金时才能确认",
        "收入应该在下月收到现金时确认",
        "收到现金时确认",
        "下月收到现金时确认",
        "没收到钱就不能算收入",
        "没收到现金就不能算收入",
        "必须等到实际收款",
    ],
    "payment_required_for_expense": [
        "没付款就没有费用",
        "没有付款就没有费用",
        "没付钱就没有费用",
        "费用就是付款",
    ],
    "profit_implies_cash": [
        "净利润为正就一定现金充足",
        "净利润为正就说明现金充足",
        "净利润为正就不缺钱",
        "净利润为正现金应该也不错",
        "净利润为正现金应该不错",
        "净利润为正现金应该增加",
        "净利润为正现金会增加",
        "利润为正就一定现金充足",
        "利润为正现金应该增加",
        "利润增加现金也增加",
        "赚钱就是现金增加",
    ],
    "depreciation_implies_cash_outflow": [
        "折旧减少利润就一定代表当期现金流出",
        "折旧就是每月付款",
        "折旧就是现金流出",
        "折旧代表当期付款",
        "折旧实际上就是每个月为资产付出去的钱",
        "折旧也算是现金流出",
        "折旧算是现金流出",
    ],
    "accrual_cash_basis_confusion": [
        "权责发生制主要看现金是否实际收付",
        "权责发生制看现金是否实际收付",
        "权责发生制关注现金实际收付",
        "现金制关注交易归属期间",
    ],
    "gross_margin_implies_net_profit": [
        "毛利高净利润一定高",
        "毛利高净利润肯定也高",
        "毛利率高就是净利率",
        "毛利率就是净利率",
        "毛利高就一定最终赚钱",
    ],
}


def enhanced_normalize_text(text: str) -> str:
    normalized = re.sub(r"[\s,，。；;：:、/\\.\?!！？（）()\[\]【】\"'“”‘’\-]+", "", str(text).lower())
    for source, target in ENHANCED_SYNONYM_REPLACEMENTS:
        normalized = normalized.replace(source.lower(), target.lower())
    return normalized


def evidence_normalize_text(text: str) -> str:
    return re.sub(r"[\s,，。；;：:、/\\.\?!！？（）()\[\]【】\"'“”‘’\-]+", "", str(text).lower())


def enhanced_text_contains(answer: str, variant: str) -> bool:
    normalized_answer = enhanced_normalize_text(answer)
    normalized_variant = enhanced_normalize_text(variant)
    if normalized_variant and normalized_variant in normalized_answer:
        return True
    tokens = [enhanced_normalize_text(token) for token in point_tokens(variant)]
    tokens = [token for token in tokens if len(token) >= 2]
    if not tokens:
        return False
    required = 1 if len(tokens) <= 2 else 2
    return sum(1 for token in tokens if token in normalized_answer) >= required


def has_any(normalized_text: str, terms: list[str]) -> bool:
    return any(enhanced_normalize_text(term) in normalized_text for term in terms)


def evidence_has_any(normalized_text: str, terms: list[str]) -> bool:
    return any(evidence_normalize_text(term) in normalized_text for term in terms)


NET_PROFIT_REASONING_POINTS = {
    "净利润大致等于收入扣除成本费用和税费": "profit_formula_or_deduction_path",
    "净利润可能包含未收现收入": "uncollected_revenue_reason",
    "净利润可能包含非现金费用所以不等于现金": "non_cash_expense_reason",
}

EXPENSE_RECOGNITION_REASONING_POINTS = {
    "费用是为取得收入或维持经营发生的耗费": "expense_consumption_reason",
    "费用发生不一定等于当期已经付款": "expense_not_payment_reason",
    "工资费用会减少本期利润": "expense_period_profit_reason",
}

GROSS_MARGIN_REASONING_POINTS = {
    "毛利等于收入减销售成本": "gross_margin_amount_formula",
    "毛利率等于毛利除以收入": "gross_margin_rate_formula",
    "毛利还没有扣除销售管理研发财务等期间费用": "gross_margin_period_expense_boundary",
}


def net_profit_evidence(answer: str) -> dict[str, bool]:
    answer_n = evidence_normalize_text(answer)
    formula = evidence_has_any(
        answer_n,
        [
            "收入扣除成本和费用",
            "收入扣除成本费用",
            "收入扣除成本费用和税费",
            "收入减成本费用",
            "收入减去成本和费用",
            "收入减去成本费用和税费",
            "扣除成本费用和税费后的结果",
            "收入-成本-费用",
            "收入扣除成本",
        ],
    ) and evidence_has_any(answer_n, ["净利润", "利润"])
    uncollected_revenue = evidence_has_any(
        answer_n,
        [
            "未收现收入",
            "收入可能已经确认但还没收到现金",
            "收入已经确认但还没收到现金",
            "确认收入但未收现金",
            "确认收入但还没收到现金",
            "确认收入但没有收到现金",
            "收入确认但客户尚未付款",
            "应收账款",
            "赊销",
            "客户还没有付款",
            "客户尚未付款",
        ],
    )
    non_cash_expense = evidence_has_any(
        answer_n,
        [
            "非现金费用",
            "折旧等非现金费用",
            "折旧",
            "摊销",
            "不代表现金流出",
            "不是当期现金流出",
            "没有现金流出",
        ],
    ) and evidence_has_any(answer_n, ["影响利润", "减少利润", "费用", "净利润", "利润"])
    conclusion = evidence_has_any(
        answer_n,
        [
            "净利润不等于现金",
            "利润不等于现金",
            "净利润为正不一定现金充足",
            "不一定代表现金充足",
            "不一定现金充足",
            "不代表现金充足",
        ],
    )
    return {
        "profit_formula_or_deduction_path": formula,
        "uncollected_revenue_reason": uncollected_revenue,
        "non_cash_expense_reason": non_cash_expense,
        "cash_not_equal_profit_conclusion": conclusion,
    }


def expense_recognition_evidence(answer: str) -> dict[str, bool]:
    answer_n = evidence_normalize_text(answer)
    consumption = evidence_has_any(
        answer_n,
        [
            "资源耗费",
            "经营耗费",
            "为经营发生",
            "为取得收入发生",
            "为取得收入或维持经营发生",
            "服务于本期经营",
            "服务于本月经营",
            "员工本月完成工作",
            "员工已经完成本月工作",
            "员工已经完成了工作",
            "耗费服务于本期",
            "耗费服务于本月",
            "维持经营发生",
        ],
    )
    not_payment = evidence_has_any(
        answer_n,
        [
            "不看现金支付时间",
            "不是现金支付时间",
            "不等于当期现金付款",
            "不一定等于当期现金付款",
            "工资下月才发",
            "工资虽下月发放",
            "工资下月发放",
            "下月才发",
            "下月发放",
            "费用确认不取决于是否已经付款",
            "不取决于是否已经付款",
            "不必等到付款",
            "未付款也可能确认费用",
        ],
    )
    period_profit = evidence_has_any(
        answer_n,
        [
            "作为本月费用",
            "作为本期费用",
            "计入本期费用",
            "计入本月费用",
            "影响本期利润",
            "减少本期利润",
            "归入本期经营",
            "本月费用",
            "本期费用",
            "工资费用会减少本期利润",
        ],
    )
    return {
        "expense_consumption_reason": consumption,
        "expense_not_payment_reason": not_payment,
        "expense_period_profit_reason": period_profit,
    }


def gross_margin_evidence(answer: str) -> dict[str, bool]:
    answer_n = evidence_normalize_text(answer)
    amount_formula = evidence_has_any(
        answer_n,
        [
            "毛利等于收入减销售成本",
            "毛利=收入-销售成本",
            "毛利是收入减销售成本",
            "收入减销售成本",
            "10000-6500",
            "1000065003500",
            "10000减6500得到3500",
        ],
    )
    rate_formula = evidence_has_any(
        answer_n,
        [
            "毛利率等于毛利除以收入",
            "毛利率=毛利/收入",
            "毛利率是毛利除以收入",
            "毛利除以收入",
            "3500/10000",
            "350010000",
            "35%",
        ],
    )
    period_boundary = evidence_has_any(
        answer_n,
        [
            "期间费用",
            "销售费用",
            "管理费用",
            "研发费用",
            "财务费用",
            "还没有扣除",
            "尚未扣除",
            "还不是净利润",
            "不是净利润",
            "净利润还需要减去其他费用",
        ],
    )
    return {
        "gross_margin_amount_formula": amount_formula,
        "gross_margin_rate_formula": rate_formula,
        "gross_margin_period_expense_boundary": period_boundary,
    }


def enhanced_semantic_match_reasons(answer: str, point_text: str) -> list[str]:
    answer_n = enhanced_normalize_text(answer)
    point_n = enhanced_normalize_text(point_text)
    reasons = []
    net_profit_evidence_map = net_profit_evidence(answer)
    expense_evidence_map = expense_recognition_evidence(answer)
    gross_margin_evidence_map = gross_margin_evidence(answer)

    if has_any(point_n, ["利润表", "经营成果"]) and has_any(
        answer_n,
        ["利润表记录经营成果", "利润表记录的是经营成果", "重点看收入成本费用", "一段期间的经营成果"],
    ):
        reasons.append("semantic:profit_statement_operating_result")

    if has_any(point_n, ["销售商品", "提供服务", "收入"]) and has_any(
        answer_n,
        ["销售商品", "提供服务", "商品已经卖出", "已经交付", "卖咖啡", "出售咖啡", "完成服务"],
    ):
        reasons.append("semantic:sales_or_service_revenue")

    if has_any(point_n, ["借款", "筹资", "融资", "营业收入"]) and has_any(
        answer_n,
        ["借款", "贷款", "资金来源", "筹资", "融资"],
    ) and has_any(answer_n, ["不是营业收入", "不是经营收入", "不应作为营业收入", "不是收入"]):
        reasons.append("semantic:borrowing_not_operating_revenue")

    if has_any(point_n, ["收入确认", "未收现金", "现金不一定", "现金收款"]) and has_any(
        answer_n,
        ["可以确认收入", "仍可能确认收入", "仍可确认收入", "本月确认收入", "先确认收入"],
    ) and has_any(answer_n, ["还没现金收款", "没有现金收款", "未现金收款", "现金没有增加", "现金不变", "客户尚未付款"]):
        reasons.append("semantic:revenue_recognition_not_cash")

    if has_any(point_n, ["应收账款", "不是现金流入"]) and has_any(
        answer_n,
        ["应收账款", "应收", "客户后续付款", "以后付款", "未来收款权利", "现金流入延后"],
    ):
        reasons.append("semantic:receivable_not_cash")

    expense_reason = EXPENSE_RECOGNITION_REASONING_POINTS.get(point_text)
    if expense_reason == "expense_consumption_reason" and expense_evidence_map[expense_reason]:
        reasons.append("semantic:expense_consumption_reason")
    if expense_reason == "expense_not_payment_reason" and expense_evidence_map[expense_reason]:
        reasons.append("semantic:expense_not_payment_reason")
    if expense_reason == "expense_period_profit_reason" and expense_evidence_map[expense_reason]:
        reasons.append("semantic:expense_period_profit_reason")

    if has_any(point_n, ["折旧", "长期资产", "成本分摊", "现金"]) and has_any(
        answer_n,
        ["折旧成本分摊", "长期资产", "多个期间", "受益期间"],
    ):
        reasons.append("semantic:depreciation_allocation")

    if has_any(point_n, ["折旧", "减少当期利润", "现金流出"]) and has_any(
        answer_n,
        ["不是现金流出", "不是再次付款", "非现金", "不代表当期现金流出"],
    ):
        reasons.append("semantic:depreciation_profit_not_cash")

    net_profit_reason = NET_PROFIT_REASONING_POINTS.get(point_text)
    if net_profit_reason == "profit_formula_or_deduction_path" and net_profit_evidence_map[net_profit_reason]:
        reasons.append("semantic:net_profit_formula_or_deduction_path")
    if net_profit_reason == "uncollected_revenue_reason" and net_profit_evidence_map[net_profit_reason]:
        reasons.append("semantic:net_profit_uncollected_revenue_reason")
    if net_profit_reason == "non_cash_expense_reason" and net_profit_evidence_map[net_profit_reason]:
        reasons.append("semantic:net_profit_non_cash_expense_reason")

    if has_any(point_n, ["权责发生制", "交易归属期间"]) and has_any(
        answer_n,
        [
            "权责发生制关注交易归属期间",
            "权责发生制看交易归属期间",
            "权责发生制按交易归属期间",
            "权责发生制关注收入费用归属",
            "权责发生制关注属于哪个期间",
            "收入和费用属于哪个期间",
        ],
    ):
        reasons.append("semantic:accrual_period")

    if has_any(point_n, ["现金制", "实际收付"]) and has_any(
        answer_n,
        [
            "现金制关注现金实际收付",
            "现金制看现金实际收付",
            "现金制按现金实际收付",
            "现金制关注实际收付时间",
            "现金制关注现金实际收付时间",
        ],
    ):
        reasons.append("semantic:cash_basis_receipts_payments")

    gross_margin_reason = GROSS_MARGIN_REASONING_POINTS.get(point_text)
    if gross_margin_reason == "gross_margin_amount_formula" and gross_margin_evidence_map[gross_margin_reason]:
        reasons.append("semantic:gross_margin_amount")

    if gross_margin_reason == "gross_margin_rate_formula" and gross_margin_evidence_map[gross_margin_reason]:
        reasons.append("semantic:gross_margin_rate")

    if (
        gross_margin_reason == "gross_margin_period_expense_boundary"
        and gross_margin_evidence_map[gross_margin_reason]
    ):
        reasons.append("semantic:period_expenses")

    return reasons


def enhanced_reasoning_point_match_detail(answer: str, point: Any) -> dict[str, Any]:
    config = normalize_reasoning_point(point)
    base_detail = reasoning_point_match_detail(answer, config)
    matched_by = list(base_detail["matched_by"])
    for variant in reasoning_point_variants(config):
        if enhanced_text_contains(answer, variant["value"]):
            matched_by.append({"source": f"normalized_{variant['source']}", "value": variant["value"]})
    for reason in enhanced_semantic_match_reasons(answer, config["text"]):
        matched_by.append({"source": reason, "value": config["text"]})

    unique = []
    seen = set()
    for match in matched_by:
        key = (str(match.get("source", "")), str(match.get("value", "")))
        if key in seen:
            continue
        seen.add(key)
        unique.append(match)

    return {
        "point": config["text"],
        "required": config["required"],
        "matched": bool(unique),
        "matched_by": unique,
    }


def detect_contradictions(answer: str) -> tuple[bool, list[str]]:
    normalized = enhanced_normalize_text(answer)
    tags = []
    for tag, patterns in CONTRADICTION_PATTERNS.items():
        if any(enhanced_normalize_text(pattern) in normalized for pattern in patterns):
            tags.append(tag)
    return bool(tags), sorted(set(tags))


def enhanced_rule_scorer(
    answer: str,
    expected_points: list[Any],
    pass_ratio: float,
) -> dict[str, Any]:
    expected = normalize_expected_reasoning_points(expected_points)
    point_details = [enhanced_reasoning_point_match_detail(answer, point) for point in expected]
    matched = [detail["point"] for detail in point_details if detail["matched"]]
    missing = [detail["point"] for detail in point_details if not detail["matched"]]
    base_score = len(matched) / len(expected) if expected else 0.0
    configured_pass_ratio = float(pass_ratio)
    effective_pass_ratio = configured_pass_ratio if configured_pass_ratio > 0.67 else RULE_PASS_RATIO_FLOOR
    required_count = (
        max(1, math.ceil((len(expected) * effective_pass_ratio) - 1e-9))
        if expected
        else 1
    )
    contradiction_detected, contradiction_tags = detect_contradictions(answer)
    completeness_blocker = has_completeness_blocker(answer)
    score = base_score
    scoring_notes = [
        "base exact/alias matching preserved",
        "normalized synonym and semantic matching applied",
    ]
    minimum_evidence: dict[str, Any] = {}
    expected_texts = {point["text"] for point in expected}
    if set(NET_PROFIT_REASONING_POINTS).issubset(expected_texts):
        evidence = net_profit_evidence(answer)
        mechanism_count = sum(
            1
            for key in (
                "profit_formula_or_deduction_path",
                "uncollected_revenue_reason",
                "non_cash_expense_reason",
            )
            if evidence[key]
        )
        minimum_evidence["net_profit"] = {
            **evidence,
            "mechanism_evidence_count": mechanism_count,
        }
        if evidence["cash_not_equal_profit_conclusion"] and mechanism_count == 0:
            score = min(score, 0.4)
            scoring_notes.append("net_profit conclusion-only answer capped at 0.4")
    if set(EXPENSE_RECOGNITION_REASONING_POINTS).issubset(expected_texts):
        evidence = expense_recognition_evidence(answer)
        minimum_evidence["expense_recognition"] = evidence
    if set(GROSS_MARGIN_REASONING_POINTS).issubset(expected_texts):
        evidence = gross_margin_evidence(answer)
        minimum_evidence["gross_margin"] = evidence
        if not (evidence["gross_margin_amount_formula"] and evidence["gross_margin_rate_formula"]):
            score = min(score, 0.5)
            scoring_notes.append("gross_margin formula evidence cap applied")
    if contradiction_detected and matched:
        score = min(0.5, max(0.0, score - 0.34))
        scoring_notes.append(
            "contradiction penalty and 0.5 score cap applied because answer contains a matched point and an opposing misconception"
        )
    if completeness_blocker:
        score = min(score, 0.4)
        scoring_notes.append("completeness blocker penalty applied")

    passed = len(matched) >= required_count and score >= effective_pass_ratio and not completeness_blocker
    return {
        "enhanced_rule_score": round(score, 4),
        "enhanced_rule_passed": passed,
        "enhanced_matched_reasoning_points": matched,
        "enhanced_missing_reasoning_points": missing,
        "contradiction_detected": contradiction_detected,
        "contradiction_tags": contradiction_tags,
        "scoring_notes": scoring_notes,
        "enhanced_rule_score_detail": {
            "scoring_method": "old exact/keyword + normalized semantic matching - contradiction penalty",
            "base_score_before_penalty": round(base_score, 4),
            "effective_pass_ratio": round(effective_pass_ratio, 4),
            "expected_count": len(expected),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "required_count": required_count,
            "minimum_evidence": minimum_evidence,
            "points": point_details,
        },
    }


MISCONCEPTION_PATTERNS: dict[str, list[str]] = {
    "revenue_cash_confusion": [
        "收到现金才算收入",
        "没收到现金就没有收入",
        "所有现金流入都是收入",
        "借款也是收入",
        "收入就是收款",
    ],
    "profit_cash_confusion": [
        "利润就是现金",
        "利润为正就一定现金充足",
        "净利润为正就不缺钱",
        "赚钱就是现金增加",
    ],
    "expense_payment_confusion": [
        "没付款就没有费用",
        "费用就是付款",
        "费用都等于现金流出",
    ],
    "depreciation_payment_confusion": [
        "折旧就是每月付款",
        "折旧不影响利润",
    ],
    "gross_net_confusion": [
        "毛利率就是净利率",
        "毛利高就一定净利润高",
    ],
    "rote_repetition": [
        "我只需要背规则",
        "照规则说",
        "规则说",
    ],
}


def detect_misconception_tags(answer: str, traps: list[str] | None = None) -> list[str]:
    normalized = normalize_text(answer)
    tags = []
    if has_completeness_blocker(answer):
        tags.append("completeness_blocker")
    for tag, patterns in MISCONCEPTION_PATTERNS.items():
        if any(normalize_text(pattern) in normalized for pattern in patterns):
            tags.append(tag)
    for trap in traps or []:
        trap_tokens = point_tokens(str(trap))
        if trap_tokens and sum(1 for token in trap_tokens if token in normalized) >= min(2, len(trap_tokens)):
            tags.append("trap_hit")
            break
    return sorted(set(tags))


def strict_point_matches(answer: str, point: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_point = normalize_text(point)
    if normalized_point and normalized_point in normalized_answer:
        return True
    tokens = point_tokens(point)
    if not tokens:
        return False
    required = 1 if len(tokens) <= 2 else 2
    return sum(1 for token in tokens if token in normalized_answer) >= required


def semantic_point_matches(answer: str, point: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_point = normalize_text(point)
    semantic_rules = [
        (("赊销", "收入"), ("赚到",)),
        (("未收现金",), ("钱还没",)),
        (("现金不一定增加",), ("现金未必增加",)),
        (("应收账款",), ("客户欠款",)),
        (("收入确认", "现金"), ("赚到", "钱还没")),
        (("权责发生制", "交易归属期间"), ("归属", "期间")),
        (("现金制", "实际收付"), ("实际", "收钱")),
    ]
    for point_terms, answer_terms in semantic_rules:
        if all(term in normalized_point for term in point_terms) and all(
            term in normalized_answer for term in answer_terms
        ):
            return True
    return False


def mock_judge(
    answer: str,
    expected_points: list[Any],
    traps: list[str],
    pass_ratio: float,
    condition: str,
) -> dict[str, Any]:
    expected = normalize_expected_reasoning_points(expected_points)
    matched = [
        point["text"]
        for point in expected
        if any(strict_point_matches(answer, variant) for variant in [point["text"], *point["aliases"]])
        or semantic_point_matches(answer, point["text"])
    ]
    missing = [point["text"] for point in expected if point["text"] not in matched]
    required_missing = [
        point["text"]
        for point in expected
        if point["required"] and point["text"] not in matched
    ]
    score = len(matched) / len(expected) if expected else 0.0
    tags = detect_misconception_tags(answer, traps)

    if "无法从当前材料推出" in answer and condition != "no_course_baseline":
        score = min(score, 0.2)
        tags.append("insufficient_materials")
    if condition == "hidden_transfer" and "rote_repetition" in tags:
        score = min(score, 0.4)
    if required_missing:
        score = min(score, 0.4)
    if "completeness_blocker" in tags:
        score = min(score, 0.4)
    if any(tag.endswith("_confusion") for tag in tags) or "trap_hit" in tags:
        score = min(score, 0.4)

    passed = score >= pass_ratio and not required_missing and "completeness_blocker" not in tags
    return {
        "judge_score": round(score, 4),
        "judge_passed": passed,
        "matched_reasoning_points": matched,
        "missing_reasoning_points": missing,
        "misconception_tags": sorted(set(tags)),
        "external_knowledge_suspicion": False,
        "failure_reason": "" if passed else "missing_or_confused_reasoning_points",
    }


def comparison_label(rule_passed: bool | None, judge_passed: bool | None) -> str:
    if rule_passed and judge_passed:
        return "both_pass"
    if rule_passed and not judge_passed:
        return "rule_pass_llm_fail"
    if not rule_passed and judge_passed:
        return "rule_fail_llm_pass"
    return "both_fail"


def complete_output_fields(record: dict[str, Any]) -> dict[str, Any]:
    completed = dict(record)
    defaults = {
        "run_id": "",
        "graph_version": "",
        "chain_id": "",
        "node_id": "",
        "condition": "",
        "student_persona": "",
        "student_model": "",
        "judge_model": "",
        "student_request_id": "",
        "judge_request_id": "",
        "question": "",
        "student_answer": "",
        "student_raw_response": "",
        "judge_raw_response": "",
        "student_parse_error": "",
        "judge_parse_error": "",
        "evidence_status": "",
        "persona_behavior_trace": "",
        "used_node_ids": [],
        "rule_score": None,
        "rule_score_detail": {},
        "rule_passed": None,
        "judge_score": None,
        "judge_passed": None,
        "matched_reasoning_points": [],
        "missing_reasoning_points": [],
        "misconception_tags": [],
        "external_knowledge_suspicion": False,
        "possible_rule_false_fail": False,
        "failure_type": "",
        "error_message": "",
        "created_at": now_iso(),
    }
    for field in REQUIRED_OUTPUT_FIELDS:
        completed.setdefault(field, defaults[field])
    return completed


def material_for_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": node["id"],
        "title": node["title"],
        "core_question": node["core_question"],
        "scenario": node["scenario"],
        "guiding_questions": node["guiding_questions"],
        "rule_summary": node["rule_summary"],
        "common_misconceptions": node["common_misconceptions"],
        "mastery_question": node["mastery_question"],
    }


def materials_for_condition(
    nodes: list[dict[str, Any]],
    node_index: int,
    condition: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    if condition == "no_course_baseline":
        return [], []
    if condition == "node_only":
        node = nodes[node_index]
        return [material_for_node(node)], [node["id"]]
    if condition in {"chain_so_far", "hidden_transfer"}:
        selected = nodes[: node_index + 1]
        return [material_for_node(node) for node in selected], [node["id"] for node in selected]
    raise ValueError(f"Unknown condition: {condition}")


def deterministic_run_id(
    experiment_id: str,
    graph_version_value: str,
    persona_id: str,
    node_id: str,
    condition: str,
) -> str:
    raw = "|".join([experiment_id, graph_version_value, persona_id, node_id, condition])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


class LLMParseError(ValueError):
    def __init__(
        self,
        message: str,
        raw_response: str,
        request_id: str = "",
    ) -> None:
        super().__init__(message)
        self.raw_response = raw_response
        self.parse_error = message
        self.request_id = request_id


def normalize_chat_completions_url(base_url: str) -> str:
    """Normalize an OpenAI-compatible base URL to the chat completions endpoint."""
    cleaned = str(base_url or "").strip().rstrip("/")
    if not cleaned:
        return ""

    parts = urlsplit(cleaned)
    path_parts = [part for part in parts.path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[-2:] == ["chat", "completions"]:
        normalized_path_parts = path_parts
    elif path_parts and path_parts[-1] == "v1":
        normalized_path_parts = [*path_parts, "chat", "completions"]
    else:
        normalized_path_parts = [*path_parts, "v1", "chat", "completions"]

    normalized_path = "/" + "/".join(normalized_path_parts)
    return urlunsplit((parts.scheme, parts.netloc, normalized_path, "", ""))


def llm_request_error_message(
    *,
    status_code: int | str | None,
    request_url: str,
    response_text: str,
    error: Exception | None = None,
) -> str:
    response_excerpt = str(response_text or "")[:500]
    parts = [
        "LLM request failed:",
        f"status_code={status_code if status_code is not None else ''};",
        f"request_url={request_url};",
        f"response_text={response_excerpt}",
    ]
    if error is not None:
        parts.append(f"error={type(error).__name__}: {error}")
    return " ".join(parts)


class OpenAICompatibleClient:
    def __init__(self, settings: dict[str, Any]) -> None:
        self.settings = settings
        self.model = str(settings.get("model") or "")
        self.temperature = float(settings.get("temperature", 0.0))
        self.timeout_seconds = int(settings.get("timeout_seconds", 60))
        self.config_error = ""
        if str(settings.get("api_key") or "").strip():
            self.config_error = "Do not put API keys in config; set the configured api_key_env instead"
        api_key_env = str(settings.get("api_key_env") or "")
        base_url_env = str(settings.get("base_url_env") or "")
        self.api_key = os.getenv(api_key_env) if api_key_env else ""
        self.base_url = (os.getenv(base_url_env) if base_url_env else "") or ""
        self.request_url = normalize_chat_completions_url(self.base_url)

    def is_configured(self) -> bool:
        return bool(self.model and self.api_key and self.base_url)

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        json_mode: bool = False,
    ) -> dict[str, Any]:
        if self.config_error:
            raise RuntimeError(self.config_error)
        if not self.is_configured():
            raise RuntimeError("LLM client is enabled but model, API key, or base URL is missing")
        url = self.request_url
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            url,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        status_code: int | None = None
        raw_body = ""
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                raw_body = response.read().decode("utf-8", errors="replace")
                status_code = response.getcode()
                request_id = response.headers.get("x-request-id", "")
                data = json.loads(raw_body)
        except HTTPError as exc:
            try:
                raw_body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                raw_body = ""
            raise RuntimeError(
                llm_request_error_message(
                    status_code=exc.code,
                    request_url=url,
                    response_text=raw_body,
                    error=exc,
                )
            ) from exc
        except (URLError, TimeoutError) as exc:
            raise RuntimeError(
                llm_request_error_message(
                    status_code=status_code,
                    request_url=url,
                    response_text=raw_body,
                    error=exc,
                )
            ) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                llm_request_error_message(
                    status_code=status_code,
                    request_url=url,
                    response_text=raw_body,
                    error=exc,
                )
            ) from exc
        try:
            content = str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("LLM response missing choices[0].message.content") from exc
        return {
            "content": content,
            "request_id": str(data.get("id") or request_id or ""),
            "request_url": url,
            "status_code": status_code,
        }

    def chat(self, messages: list[dict[str, str]], json_mode: bool = False) -> str:
        return self.chat_completion(messages, json_mode=json_mode)["content"]


def parse_json_object(raw_text: str) -> dict[str, Any]:
    text = str(raw_text or "")
    stripped = text.strip()
    if not stripped:
        raise LLMParseError("empty_response", text)

    candidates = [stripped]
    fenced = re.search(r"```(?:json)?\s*(.*?)`{3,}", stripped, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        candidates.append(fenced.group(1).strip())
    extracted = extract_first_json_object(stripped)
    if extracted:
        candidates.append(extracted)

    last_error: json.JSONDecodeError | None = None
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
            continue
        if not isinstance(parsed, dict):
            raise LLMParseError("LLM JSON output must be an object", text)
        return parsed

    detail = f": {last_error}" if last_error else ""
    raise LLMParseError(f"LLM returned non-JSON output{detail}", text)


def extract_first_json_object(text: str) -> str:
    start = text.find("{")
    while start != -1:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]
        start = text.find("{", start + 1)
    return ""


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def coerce_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in {"true", "yes", "1"}:
            return True
        if value.lower() in {"false", "no", "0"}:
            return False
    return default
