from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import diagnosis


def assert_error_type(
    student_answer: str,
    correct_answer: str,
    question_meta: dict,
    expected_error_type: str,
) -> None:
    result = diagnosis.diagnose_answer(
        "test_question",
        student_answer,
        correct_answer,
        question_meta,
    )
    assert result["is_correct"] is False
    assert result["error_type"] == expected_error_type, result
    assert result["weak_node_ids"], result
    assert result["recommended_node_ids"], result


def test_correct_answer() -> None:
    result = diagnosis.diagnose_answer(
        "q_correct",
        "资产 = 负债 + 所有者权益",
        "资产 = 负债 + 所有者权益",
        {"node_id": "accounting_equation"},
    )
    assert result["is_correct"] is True
    assert result["error_type"] == ""
    assert result["weak_node_ids"] == []
    assert result["recommended_node_ids"] == []


def test_ratio_formula_error() -> None:
    assert_error_type(
        "总负债 / 总资产",
        "流动资产 / 流动负债",
        {
            "node_id": "current_ratio",
            "error_tags": ["ratio_formula_error"],
            "prerequisites": ["working_capital"],
        },
        diagnosis.ERROR_RATIO_FORMULA,
    )


def test_profit_cashflow_confusion() -> None:
    assert_error_type(
        "因为净利润增加，所以一定有现金流入",
        "利润基于权责发生制，现金流关注实际现金收付，二者可能不同步",
        {
            "node_id": "accrual_vs_cash",
            "question": "为什么利润和现金流可能不同？",
            "prerequisites": ["net_profit", "cash_flow_overview"],
        },
        diagnosis.ERROR_PROFIT_CASHFLOW,
    )


def test_liability_asset_confusion() -> None:
    assert_error_type(
        "资产",
        "负债",
        {
            "node_id": "balance_sheet_liabilities_equity",
            "prerequisites": ["accounting_equation"],
        },
        diagnosis.ERROR_LIABILITY_ASSET,
    )


def test_calculation_error() -> None:
    assert_error_type(
        "30",
        "40",
        {
            "node_id": "debt_to_asset",
            "question": "总资产 200，总负债 80，资产负债率是多少？",
            "error_tags": ["calculation_error"],
            "prerequisites": ["balance_sheet_assets"],
        },
        diagnosis.ERROR_CALCULATION,
    )


def test_statement_misread() -> None:
    assert_error_type(
        "经营活动",
        "考勤活动",
        {
            "node_id": "cash_flow_overview",
            "question": "现金流量表通常不包括哪一类活动？",
            "error_tags": ["statement_misread"],
            "prerequisites": ["financial_statement_overview"],
        },
        diagnosis.ERROR_STATEMENT_MISREAD,
    )


def test_prerequisite_missing() -> None:
    result = diagnosis.diagnose_answer(
        "q_prerequisite",
        "不知道",
        "资产等于负债加所有者权益",
        {
            "node_id": "accounting_equation",
            "error_tags": ["prerequisite_missing"],
            "prerequisites": ["financial_statement_overview"],
        },
    )
    assert result["error_type"] == diagnosis.ERROR_PREREQUISITE_MISSING
    assert "financial_statement_overview" in result["weak_node_ids"]
    assert result["recommended_node_ids"] == ["financial_statement_overview"]


def run_all_tests() -> None:
    test_correct_answer()
    test_ratio_formula_error()
    test_profit_cashflow_confusion()
    test_liability_asset_confusion()
    test_calculation_error()
    test_statement_misread()
    test_prerequisite_missing()


if __name__ == "__main__":
    run_all_tests()
    print("diagnosis tests passed")
