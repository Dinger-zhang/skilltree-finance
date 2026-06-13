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

REVENUE_RECOGNITION_POINTS = [
    "收入来自销售商品或提供服务",
    "完成交付或服务后可能满足收入确认条件",
    "收入确认不一定依赖现金已经到账",
]

REVENUE_NOT_CASH_POINTS = [
    "赊销可能先确认收入",
    "未收现金时现金不一定增加",
    "可能形成应收账款而不是现金流入",
]

DEPRECIATION_POINTS = [
    "折旧是长期资产成本在多个期间的分摊",
    "折旧费用会减少当期利润",
    "折旧通常不是当期现金流出",
]

GROSS_MARGIN_POINTS = [
    "毛利等于收入减销售成本",
    "毛利率等于毛利除以收入",
    "毛利还没有扣除销售管理研发财务等期间费用",
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


def test_gross_margin_boundary_only_answer_should_not_pass() -> None:
    result = score(
        "因为毛利还不是净利润。",
        GROSS_MARGIN_POINTS,
    )

    assert result["enhanced_rule_passed"] is False
    assert result["enhanced_rule_score"] <= 0.5


def test_gross_margin_missing_rate_formula_should_not_pass() -> None:
    result = score(
        "根据材料，毛利等于收入减销售成本，但毛利还不是净利润，因此毛利率高不等于净利润一定高。",
        GROSS_MARGIN_POINTS,
    )

    assert result["enhanced_rule_passed"] is False


def test_revenue_recognition_cash_only_answer_should_not_pass() -> None:
    result = score(
        "材料说，收入确认不一定等于收到现金。",
        REVENUE_RECOGNITION_POINTS,
    )

    assert result["enhanced_rule_passed"] is False


def test_revenue_recognition_cash_required_contradiction_should_fail() -> None:
    result = score(
        "不能确认收入，因为还没收到现金。客户下月才付款，所以收入应该在下月收到现金时确认。",
        REVENUE_RECOGNITION_POINTS,
    )

    assert result["contradiction_detected"] is True
    assert result["enhanced_rule_passed"] is False


def test_revenue_not_cash_contradiction_should_fail() -> None:
    result = score(
        "本月利润表上不应该确认收入，因为没有收到现金。收入必须是在收到现金时才能确认，所以收入等于收款。",
        REVENUE_NOT_CASH_POINTS,
    )

    assert result["contradiction_detected"] is True
    assert result["enhanced_rule_passed"] is False


def test_depreciation_cash_outflow_contradiction_should_fail() -> None:
    result = score(
        "折旧减少利润是因为它被计入费用，但折旧实际上就是每个月为资产付出去的钱，所以它也算是现金流出。",
        DEPRECIATION_POINTS,
    )

    assert result["contradiction_detected"] is True
    assert result["enhanced_rule_passed"] is False
