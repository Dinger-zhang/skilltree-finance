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

import yaml


LAB_DIR = Path(__file__).resolve().parent
REPO_ROOT = LAB_DIR.parents[1]
B_CHAIN_ID = "B. 从交易到利润表"
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
    "question",
    "student_answer",
    "used_node_ids",
    "rule_score",
    "rule_passed",
    "judge_score",
    "judge_passed",
    "matched_reasoning_points",
    "missing_reasoning_points",
    "misconception_tags",
    "external_knowledge_suspicion",
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


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    path = config_path or LAB_DIR / "config.yaml"
    config = load_yaml(path)
    config.setdefault("experiment_id", "ssl_v0_3_minimal")
    config.setdefault("chain_id", B_CHAIN_ID)
    config.setdefault("mock_mode", True)
    config.setdefault("pass_ratio", 0.6)
    config.setdefault("conditions", list(DEFAULT_CONDITIONS))
    config.setdefault("allow_graph_fallback", True)
    return config


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
) -> tuple[list[dict[str, Any]], bool]:
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


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", str(text).lower())


def point_tokens(point: str) -> list[str]:
    tokens = []
    for token in re.split(r"[/,，、；;:：。\.\s]+", str(point)):
        normalized = normalize_text(token)
        if len(normalized) >= 2:
            tokens.append(normalized)
    return tokens


def point_matches(answer: str, point: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_point = normalize_text(point)
    if normalized_point and normalized_point in normalized_answer:
        return True
    tokens = point_tokens(point)
    return any(token in normalized_answer for token in tokens)


def evaluate_rule(
    answer: str,
    expected_points: list[str],
    pass_ratio: float,
) -> dict[str, Any]:
    expected = [str(point) for point in expected_points if str(point).strip()]
    matched = [point for point in expected if point_matches(answer, point)]
    missing = [point for point in expected if point not in matched]
    score = len(matched) / len(expected) if expected else 0.0
    required_count = max(1, math.ceil(len(expected) * pass_ratio)) if expected else 1
    return {
        "rule_score": round(score, 4),
        "rule_passed": len(matched) >= required_count,
        "matched_reasoning_points": matched,
        "missing_reasoning_points": missing,
        "required_count": required_count,
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
    expected_points: list[str],
    traps: list[str],
    pass_ratio: float,
    condition: str,
) -> dict[str, Any]:
    expected = [str(point) for point in expected_points if str(point).strip()]
    matched = [
        point
        for point in expected
        if strict_point_matches(answer, point) or semantic_point_matches(answer, point)
    ]
    missing = [point for point in expected if point not in matched]
    score = len(matched) / len(expected) if expected else 0.0
    tags = detect_misconception_tags(answer, traps)

    if "无法从当前材料推出" in answer and condition != "no_course_baseline":
        score = min(score, 0.2)
        tags.append("insufficient_materials")
    if condition == "hidden_transfer" and "rote_repetition" in tags:
        score = min(score, 0.4)
    if any(tag.endswith("_confusion") for tag in tags) or "trap_hit" in tags:
        score = min(score, 0.4)

    passed = score >= pass_ratio
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
        "question": "",
        "student_answer": "",
        "used_node_ids": [],
        "rule_score": None,
        "rule_passed": None,
        "judge_score": None,
        "judge_passed": None,
        "matched_reasoning_points": [],
        "missing_reasoning_points": [],
        "misconception_tags": [],
        "external_knowledge_suspicion": False,
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


class OpenAICompatibleClient:
    def __init__(self, settings: dict[str, Any]) -> None:
        self.settings = settings
        self.model = str(settings.get("model") or "")
        self.temperature = float(settings.get("temperature", 0.0))
        self.timeout_seconds = int(settings.get("timeout_seconds", 60))
        api_key_env = str(settings.get("api_key_env") or "")
        base_url_env = str(settings.get("base_url_env") or "")
        self.api_key = os.getenv(api_key_env) if api_key_env else ""
        self.base_url = (os.getenv(base_url_env) if base_url_env else "") or ""

    def is_configured(self) -> bool:
        return bool(self.model and self.api_key and self.base_url)

    def chat(self, messages: list[dict[str, str]], json_mode: bool = False) -> str:
        if not self.is_configured():
            raise RuntimeError("LLM client is enabled but model, API key, or base URL is missing")
        url = self.base_url.rstrip("/") + "/v1/chat/completions"
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
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc
        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("LLM response missing choices[0].message.content") from exc


def parse_json_object(raw_text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM returned non-JSON output") from exc
    if not isinstance(parsed, dict):
        raise ValueError("LLM JSON output must be an object")
    return parsed


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
