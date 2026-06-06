from __future__ import annotations

import re
from typing import Any, Optional


ERROR_CONCEPT_CONFUSION = "concept_confusion"
ERROR_CALCULATION = "calculation_error"
ERROR_STATEMENT_MISREAD = "statement_misread"
ERROR_PREREQUISITE_MISSING = "prerequisite_missing"
ERROR_PROFIT_CASHFLOW = "profit_cashflow_confusion"
ERROR_LIABILITY_ASSET = "liability_asset_confusion"
ERROR_RATIO_FORMULA = "ratio_formula_error"

ERROR_TYPES = (
    ERROR_CONCEPT_CONFUSION,
    ERROR_CALCULATION,
    ERROR_STATEMENT_MISREAD,
    ERROR_PREREQUISITE_MISSING,
    ERROR_PROFIT_CASHFLOW,
    ERROR_LIABILITY_ASSET,
    ERROR_RATIO_FORMULA,
)

ERROR_EXPLANATIONS = {
    ERROR_CONCEPT_CONFUSION: "答案反映出核心概念理解不稳定，建议回看本题对应知识节点的定义和例题。",
    ERROR_CALCULATION: "答案方向可能接近，但数值或计算过程存在问题，建议重新检查公式、分子分母和计算步骤。",
    ERROR_STATEMENT_MISREAD: "答案与题干要求不匹配，可能没有准确理解题意或忽略了限定条件。",
    ERROR_PREREQUISITE_MISSING: "答案缺少前置知识支撑，建议先回退到前置节点补齐基础概念。",
    ERROR_PROFIT_CASHFLOW: "答案混淆了利润和现金流。利润基于权责发生制，现金流关注实际现金收付。",
    ERROR_LIABILITY_ASSET: "答案混淆了资产和负债。资产代表资源或未来经济利益，负债代表未来偿付义务。",
    ERROR_RATIO_FORMULA: "答案体现出财务比率公式使用错误，建议重新确认指标的分子、分母和含义。",
}

PUNCTUATION_PATTERN = re.compile(r"[\s，。！？、；：,.!?;:\"'（）()【】\[\]《》<>]+")
NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?%?")

PROFIT_WORDS = {"利润", "净利润", "盈利", "收益"}
CASHFLOW_WORDS = {"现金", "现金流", "收款", "付款", "经营现金流"}
ASSET_WORDS = {"资产", "应收", "存货", "设备", "货币资金", "固定资产"}
LIABILITY_WORDS = {"负债", "借款", "应付", "贷款", "偿还"}
RATIO_WORDS = {"比率", "率", "roe", "毛利率", "流动比率", "资产负债率", "公式", "/"}
CALCULATION_WORDS = {"计算", "多少", "公式", "%", "比率", "率"}
STATEMENT_WORDS = {"不包括", "不是", "错误", "最可能", "通常", "下列"}

TAG_TO_ERROR_TYPE = {
    "concept": ERROR_CONCEPT_CONFUSION,
    "concept_confusion": ERROR_CONCEPT_CONFUSION,
    "calculation": ERROR_CALCULATION,
    "calculation_error": ERROR_CALCULATION,
    "statement_misread": ERROR_STATEMENT_MISREAD,
    "misread": ERROR_STATEMENT_MISREAD,
    "prerequisite": ERROR_PREREQUISITE_MISSING,
    "prerequisite_missing": ERROR_PREREQUISITE_MISSING,
    "profit_cashflow": ERROR_PROFIT_CASHFLOW,
    "profit_cashflow_confusion": ERROR_PROFIT_CASHFLOW,
    "liability_asset": ERROR_LIABILITY_ASSET,
    "liability_asset_confusion": ERROR_LIABILITY_ASSET,
    "ratio_formula": ERROR_RATIO_FORMULA,
    "ratio_formula_error": ERROR_RATIO_FORMULA,
}

ERROR_RECOMMENDATION_HINTS = {
    ERROR_PROFIT_CASHFLOW: ["accrual_vs_cash", "cash_flow_overview", "net_profit"],
    ERROR_LIABILITY_ASSET: ["balance_sheet_assets", "balance_sheet_liabilities_equity", "accounting_equation"],
    ERROR_RATIO_FORMULA: ["gross_margin", "current_ratio", "debt_to_asset", "roe"],
    ERROR_CALCULATION: ["accounting_equation", "net_profit"],
}


def normalize_text(text: Any) -> str:
    return PUNCTUATION_PATTERN.sub("", str(text or "").lower())


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def normalize_tags(question_meta: dict[str, Any]) -> list[str]:
    return [str(tag).strip() for tag in to_list(question_meta.get("error_tags")) if str(tag).strip()]


def normalize_node_ids(value: Any) -> list[str]:
    seen = set()
    result = []
    for item in to_list(value):
        node_id = str(item).strip()
        if node_id and node_id not in seen:
            seen.add(node_id)
            result.append(node_id)
    return result


def keyword_set(text: Any) -> set[str]:
    normalized = normalize_text(text)
    if not normalized:
        return set()

    chunks = re.split(r"[和与及或的了是为在中、，。\s]+", str(text or "").lower())
    words = {normalize_text(chunk) for chunk in chunks if len(normalize_text(chunk)) >= 2}
    if words:
        return words

    return {normalized[index : index + 2] for index in range(max(len(normalized) - 1, 0))}


def contains_any(text: Any, words: set[str]) -> bool:
    normalized = normalize_text(text)
    return any(normalize_text(word) in normalized for word in words)


def extract_numbers(text: Any) -> list[str]:
    return [item.lower() for item in NUMBER_PATTERN.findall(str(text or ""))]


def answer_key_set(answer: Any) -> set[str]:
    if answer is None:
        return set()
    if isinstance(answer, (list, tuple, set)):
        return {normalize_text(item) for item in answer if normalize_text(item)}
    text = str(answer).strip()
    if not text:
        return set()
    if "," in text:
        return {normalize_text(item) for item in text.split(",") if normalize_text(item)}
    return {normalize_text(text)}


def is_answer_correct(student_answer: Any, reference_answer: Any) -> bool:
    if isinstance(reference_answer, (list, tuple, set)) or isinstance(student_answer, (list, tuple, set)):
        return answer_key_set(student_answer) == answer_key_set(reference_answer)

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

    reference_numbers = extract_numbers(reference_answer)
    if reference_numbers:
        student_numbers = extract_numbers(student_answer)
        if student_numbers and set(student_numbers) == set(reference_numbers):
            return True

    reference_keywords = keyword_set(reference_answer)
    student_keywords = keyword_set(student_answer)
    if not reference_keywords:
        return False

    matched = len(reference_keywords & student_keywords)
    return matched / len(reference_keywords) >= 0.6


def error_type_from_tags(tags: list[str]) -> Optional[str]:
    for tag in tags:
        error_type = TAG_TO_ERROR_TYPE.get(tag)
        if error_type:
            return error_type
    return None


def detect_specific_confusion(
    student_answer: Any,
    correct_answer: Any,
    question_meta: dict[str, Any],
) -> Optional[str]:
    tags = normalize_tags(question_meta)
    node_id = str(question_meta.get("node_id", ""))
    prompt = question_meta.get("question") or question_meta.get("prompt") or ""
    combined_question = f"{prompt} {node_id} {' '.join(tags)}"

    if (
        contains_any(combined_question, PROFIT_WORDS | CASHFLOW_WORDS)
        and contains_any(student_answer, PROFIT_WORDS)
        and contains_any(correct_answer, CASHFLOW_WORDS)
    ) or (
        contains_any(combined_question, PROFIT_WORDS | CASHFLOW_WORDS)
        and contains_any(student_answer, CASHFLOW_WORDS)
        and contains_any(correct_answer, PROFIT_WORDS)
    ):
        return ERROR_PROFIT_CASHFLOW

    if (
        contains_any(student_answer, ASSET_WORDS)
        and contains_any(correct_answer, LIABILITY_WORDS)
    ) or (
        contains_any(student_answer, LIABILITY_WORDS)
        and contains_any(correct_answer, ASSET_WORDS)
    ):
        return ERROR_LIABILITY_ASSET

    if contains_any(combined_question, RATIO_WORDS) and contains_any(student_answer, RATIO_WORDS):
        if extract_numbers(correct_answer) != extract_numbers(student_answer):
            return ERROR_RATIO_FORMULA

    return None


def detect_error_type(
    student_answer: Any,
    correct_answer: Any,
    question_meta: dict[str, Any],
) -> str:
    tags = normalize_tags(question_meta)
    tagged_error = error_type_from_tags(tags)

    if tagged_error:
        return tagged_error

    specific_error = detect_specific_confusion(student_answer, correct_answer, question_meta)
    if specific_error:
        return specific_error

    prompt = question_meta.get("question") or question_meta.get("prompt") or ""
    reference_numbers = extract_numbers(correct_answer)
    student_numbers = extract_numbers(student_answer)

    if contains_any(prompt, RATIO_WORDS) or contains_any(correct_answer, RATIO_WORDS):
        return ERROR_RATIO_FORMULA

    if reference_numbers and student_numbers and set(reference_numbers) != set(student_numbers):
        return ERROR_CALCULATION

    if reference_numbers and contains_any(prompt, CALCULATION_WORDS):
        return ERROR_CALCULATION

    if contains_any(prompt, STATEMENT_WORDS) and not keyword_set(student_answer) & keyword_set(correct_answer):
        return ERROR_STATEMENT_MISREAD

    if question_meta.get("prerequisites") and not keyword_set(student_answer) & keyword_set(correct_answer):
        return ERROR_PREREQUISITE_MISSING

    return ERROR_CONCEPT_CONFUSION


def unique_node_ids(node_ids: list[str]) -> list[str]:
    seen = set()
    result = []
    for node_id in node_ids:
        if node_id and node_id not in seen:
            seen.add(node_id)
            result.append(node_id)
    return result


def choose_weak_nodes(
    node_id: str,
    error_type: str,
    prerequisites: list[str],
) -> list[str]:
    weak_nodes = [node_id] if node_id else []
    if error_type == ERROR_PREREQUISITE_MISSING:
        weak_nodes.extend(prerequisites)
    return unique_node_ids(weak_nodes)


def choose_recommended_nodes(
    node_id: str,
    error_type: str,
    tags: list[str],
    prerequisites: list[str],
    question_meta: dict[str, Any],
) -> list[str]:
    explicit_recommendations = normalize_node_ids(question_meta.get("recommended_node_ids"))
    if explicit_recommendations:
        return explicit_recommendations

    tag_recommendations = []
    for tag in tags:
        if tag.startswith("recommend:"):
            tag_recommendations.append(tag.split(":", 1)[1])
    if tag_recommendations:
        return unique_node_ids(tag_recommendations)

    if error_type == ERROR_PREREQUISITE_MISSING and prerequisites:
        return prerequisites

    hints = ERROR_RECOMMENDATION_HINTS.get(error_type, [])
    matched_prerequisites = [item for item in prerequisites if item in hints]
    if matched_prerequisites:
        return matched_prerequisites

    if prerequisites:
        return [prerequisites[-1]]

    return [node_id] if node_id else []


def diagnose_answer(
    question_id: str,
    student_answer: Any,
    correct_answer: Any,
    question_meta: dict[str, Any],
) -> dict[str, Any]:
    """Diagnose a student's answer with local rules, no model calls."""
    meta = question_meta or {}
    is_correct = is_answer_correct(student_answer, correct_answer)
    node_id = str(meta.get("node_id", ""))
    prerequisites = normalize_node_ids(meta.get("prerequisites"))
    tags = normalize_tags(meta)

    if is_correct:
        return {
            "is_correct": True,
            "error_type": "",
            "explanation": "回答正确。",
            "weak_node_ids": [],
            "recommended_node_ids": [],
        }

    error_type = detect_error_type(student_answer, correct_answer, meta)
    weak_node_ids = choose_weak_nodes(node_id, error_type, prerequisites)
    recommended_node_ids = choose_recommended_nodes(
        node_id,
        error_type,
        tags,
        prerequisites,
        meta,
    )

    return {
        "is_correct": False,
        "error_type": error_type,
        "explanation": ERROR_EXPLANATIONS[error_type],
        "weak_node_ids": weak_node_ids,
        "recommended_node_ids": recommended_node_ids,
    }


def run_simple_tests() -> None:
    correct = diagnose_answer(
        "q_correct",
        "资产 = 负债 + 所有者权益",
        "资产 = 负债 + 所有者权益",
        {"node_id": "accounting_equation"},
    )
    assert correct["is_correct"] is True

    ratio = diagnose_answer(
        "q_ratio",
        "总资产 / 总负债",
        "流动资产 / 流动负债",
        {
            "node_id": "current_ratio",
            "error_tags": [ERROR_RATIO_FORMULA],
            "prerequisites": ["working_capital"],
        },
    )
    assert ratio["error_type"] == ERROR_RATIO_FORMULA
    assert ratio["recommended_node_ids"] == ["working_capital"]

    cashflow = diagnose_answer(
        "q_cashflow",
        "净利润增加",
        "经营现金流增加",
        {
            "node_id": "accrual_vs_cash",
            "question": "利润和现金流为什么可能不同？",
            "prerequisites": ["net_profit", "cash_flow_overview"],
        },
    )
    assert cashflow["error_type"] == ERROR_PROFIT_CASHFLOW

    liability_asset = diagnose_answer(
        "q_liability_asset",
        "资产",
        "负债",
        {
            "node_id": "balance_sheet_liabilities_equity",
            "prerequisites": ["accounting_equation"],
        },
    )
    assert liability_asset["error_type"] == ERROR_LIABILITY_ASSET


if __name__ == "__main__":
    run_simple_tests()
    print("diagnosis tests passed")
