from __future__ import annotations

import sys
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parents[1]
if str(LAB_DIR) not in sys.path:
    sys.path.insert(0, str(LAB_DIR))

from common import enhanced_rule_scorer  # noqa: E402


PASS_RATIO = 2 / 3

NET_PROFIT_POINTS = [
    "净利润大致等于收入扣除成本费用和税费",
    "净利润可能包含未收现收入",
    "净利润可能包含非现金费用所以不等于现金",
]

EXPENSE_RECOGNITION_POINTS = [
    "费用是为取得收入或维持经营发生的耗费",
    "费用发生不一定等于当期已经付款",
    "工资费用会减少本期利润",
]

ACCRUAL_VS_CASH_POINTS = [
    "权责发生制关注交易归属期间",
    "满足条件时未收款也可能确认收入",
    "已发生费用即使未付款也可能归入本期",
    "现金制关注现金实际收付时间",
]


def score(answer: str, expected_points: list[str]) -> dict:
    return enhanced_rule_scorer(answer, expected_points, PASS_RATIO)


def test_net_profit_generic_answer_should_not_full_pass() -> None:
    result = score(
        "材料说净利润不等于现金，所以净利润为正不一定代表现金充足。",
        NET_PROFIT_POINTS,
    )

    assert result["enhanced_rule_score"] <= 0.4
    assert result["enhanced_rule_passed"] is False


def test_net_profit_mechanism_answer_should_pass() -> None:
    result = score(
        "净利润是收入扣除成本和费用后的结果，但它不等于现金，因为收入可能已经确认但还没收到现金，"
        "折旧等非现金费用也会影响利润，所以净利润为正不一定现金充足。",
        NET_PROFIT_POINTS,
    )

    assert result["enhanced_rule_score"] >= 0.8
    assert result["enhanced_rule_passed"] is True


def test_expense_recognition_complete_answer_should_pass() -> None:
    result = score(
        "费用确认关注耗费是否服务于本期经营，而不是现金支付时间。员工本月完成工作，工资虽下月发放，"
        "但耗费服务于本月，所以应作为本月费用，并减少本期利润。",
        EXPENSE_RECOGNITION_POINTS,
    )

    assert result["enhanced_rule_score"] >= 0.8
    assert result["enhanced_rule_passed"] is True


def test_expense_recognition_contradiction_should_fail() -> None:
    result = score(
        "员工本月完成工作，费用发生不一定等于付款。但我觉得没付款就没有费用，所以本月不应该确认工资费用。",
        EXPENSE_RECOGNITION_POINTS,
    )

    assert result["contradiction_detected"] is True
    assert result["enhanced_rule_passed"] is False


def test_accrual_vs_cash_reversed_definition_should_fail() -> None:
    result = score(
        "权责发生制关注现金是否实际收付，而现金制关注交易归属期间。没付款就没有费用。",
        ACCRUAL_VS_CASH_POINTS,
    )

    assert result["contradiction_detected"] is True
    assert result["enhanced_rule_passed"] is False
