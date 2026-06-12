from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from common import comparison_label, enhanced_rule_scorer, read_jsonl, write_jsonl


DEFAULT_INPUT_DIR = Path("experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired")
DEFAULT_PASS_RATIO = 2 / 3
REPORTED_ISSUE_BASELINE = {
    "expense_recognition_enhanced_avg": 0.0,
    "expense_recognition_enhanced_rule_fail_llm_pass": 7,
    "overall_enhanced_rule_pass_llm_fail": 8,
    "net_profit_enhanced_rule_pass_llm_fail": 3,
    "net_profit_generic_run_id": "787b5003cc442550",
    "net_profit_generic_previous_score": 1.0,
}

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


def as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0.0%"
    return f"{numerator / denominator * 100:.1f}%"


def short_text(value: Any, limit: int = 220) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def format_list(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "-"
    return "；".join(str(item) for item in value)


def average(records: list[dict[str, Any]], field: str) -> float:
    if not records:
        return 0.0
    return mean(as_float(record.get(field)) for record in records)


def pass_count(records: list[dict[str, Any]], field: str) -> int:
    return sum(1 for record in records if record.get(field) is True)


def run_sanity_checks(pass_ratio: float) -> list[dict[str, Any]]:
    cases = [
        {
            "name": "net_profit_generic_answer_should_not_full_pass",
            "answer": "材料说净利润不等于现金，所以净利润为正不一定代表现金充足。",
            "expected_points": NET_PROFIT_POINTS,
            "expectation": "enhanced_rule_score <= 0.4 and enhanced_rule_passed is false",
            "check": lambda result: result["enhanced_rule_score"] <= 0.4 and result["enhanced_rule_passed"] is False,
        },
        {
            "name": "net_profit_mechanism_answer_should_pass",
            "answer": (
                "净利润是收入扣除成本和费用后的结果，但它不等于现金，因为收入可能已经确认但还没收到现金，"
                "折旧等非现金费用也会影响利润，所以净利润为正不一定现金充足。"
            ),
            "expected_points": NET_PROFIT_POINTS,
            "expectation": "enhanced_rule_score >= 0.8 and enhanced_rule_passed is true",
            "check": lambda result: result["enhanced_rule_score"] >= 0.8 and result["enhanced_rule_passed"] is True,
        },
        {
            "name": "expense_recognition_complete_answer_should_pass",
            "answer": (
                "费用确认关注耗费是否服务于本期经营，而不是现金支付时间。员工本月完成工作，工资虽下月发放，"
                "但耗费服务于本月，所以应作为本月费用，并减少本期利润。"
            ),
            "expected_points": EXPENSE_RECOGNITION_POINTS,
            "expectation": "enhanced_rule_score >= 0.8 and enhanced_rule_passed is true",
            "check": lambda result: result["enhanced_rule_score"] >= 0.8 and result["enhanced_rule_passed"] is True,
        },
        {
            "name": "expense_recognition_contradiction_should_fail",
            "answer": "员工本月完成工作，费用发生不一定等于付款。但我觉得没付款就没有费用，所以本月不应该确认工资费用。",
            "expected_points": EXPENSE_RECOGNITION_POINTS,
            "expectation": "contradiction_detected is true and enhanced_rule_passed is false",
            "check": lambda result: result["contradiction_detected"] is True and result["enhanced_rule_passed"] is False,
        },
        {
            "name": "accrual_vs_cash_reversed_definition_should_fail",
            "answer": "权责发生制关注现金是否实际收付，而现金制关注交易归属期间。没付款就没有费用。",
            "expected_points": ACCRUAL_VS_CASH_POINTS,
            "expectation": "contradiction_detected is true and enhanced_rule_passed is false",
            "check": lambda result: result["contradiction_detected"] is True and result["enhanced_rule_passed"] is False,
        },
    ]
    results = []
    for case in cases:
        result = enhanced_rule_scorer(case["answer"], case["expected_points"], pass_ratio)
        passed = bool(case["check"](result))
        results.append(
            {
                "name": case["name"],
                "passed": passed,
                "expectation": case["expectation"],
                "enhanced_rule_score": result["enhanced_rule_score"],
                "enhanced_rule_passed": result["enhanced_rule_passed"],
                "contradiction_detected": result["contradiction_detected"],
                "contradiction_tags": result["contradiction_tags"],
            }
        )
    return results


def rescore_records(records: list[dict[str, Any]], pass_ratio: float) -> list[dict[str, Any]]:
    rescored = []
    for record in records:
        enhanced = enhanced_rule_scorer(
            str(record.get("student_answer", "")),
            record.get("expected_reasoning_points", []),
            pass_ratio,
        )
        output = dict(record)
        output.update(enhanced)
        output["enhanced_conflict_type"] = comparison_label(
            output.get("enhanced_rule_passed"),
            output.get("judge_passed"),
        )
        output["enhanced_rule_score_delta"] = round(
            as_float(output.get("enhanced_rule_score")) - as_float(output.get("rule_score")),
            4,
        )
        rescored.append(output)
    return rescored


def node_summary(records: list[dict[str, Any]]) -> list[str]:
    by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_node[str(record.get("node_id", ""))].append(record)

    lines = [
        "| node_id | rows | old_avg | enhanced_avg | avg_delta | old_pass | enhanced_pass | old_rule_fail_llm_pass | enhanced_rule_fail_llm_pass |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for node_id in sorted(by_node):
        items = by_node[node_id]
        old_avg = average(items, "rule_score")
        enhanced_avg = average(items, "enhanced_rule_score")
        old_false_fail = sum(1 for item in items if item.get("conflict_type") == "rule_fail_llm_pass")
        enhanced_false_fail = sum(1 for item in items if item.get("enhanced_conflict_type") == "rule_fail_llm_pass")
        lines.append(
            f"| `{node_id}` | {len(items)} | {old_avg:.4f} | {enhanced_avg:.4f} | "
            f"{enhanced_avg - old_avg:+.4f} | {pass_count(items, 'rule_passed')} | "
            f"{pass_count(items, 'enhanced_rule_passed')} | {old_false_fail} | {enhanced_false_fail} |"
        )
    return lines


def biggest_changes(records: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda record: abs(as_float(record.get("enhanced_rule_score_delta"))),
        reverse=True,
    )[:limit]


def node_records(records: list[dict[str, Any]], node_id: str) -> list[dict[str, Any]]:
    return [record for record in records if record.get("node_id") == node_id]


def count_conflict(records: list[dict[str, Any]], field: str, value: str, node_id: str | None = None) -> int:
    return sum(
        1
        for record in records
        if record.get(field) == value and (node_id is None or record.get("node_id") == node_id)
    )


def by_run_id(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(record.get("run_id", "")): record for record in records}


def build_report(
    records: list[dict[str, Any]],
    output_jsonl: Path,
    previous_records: list[dict[str, Any]] | None = None,
    sanity_results: list[dict[str, Any]] | None = None,
) -> list[str]:
    previous_records = previous_records or []
    sanity_results = sanity_results or []
    total = len(records)
    old_rule_pass = pass_count(records, "rule_passed")
    enhanced_rule_pass = pass_count(records, "enhanced_rule_passed")
    old_false_fail = sum(1 for record in records if record.get("conflict_type") == "rule_fail_llm_pass")
    enhanced_false_fail = sum(1 for record in records if record.get("enhanced_conflict_type") == "rule_fail_llm_pass")
    old_false_pass = [record for record in records if record.get("conflict_type") == "rule_pass_llm_fail"]
    captured_false_pass = [record for record in old_false_pass if record.get("contradiction_detected") is True]
    contradiction_records = [record for record in records if record.get("contradiction_detected") is True]
    old_avg = average(records, "rule_score")
    enhanced_avg = average(records, "enhanced_rule_score")
    judge_avg = average(records, "judge_score")
    conflict_counts = Counter(str(record.get("enhanced_conflict_type", "")) for record in records)
    enhanced_false_passes = [record for record in records if record.get("enhanced_conflict_type") == "rule_pass_llm_fail"]

    expense_items = node_records(records, "expense_recognition")
    previous_expense_items = node_records(previous_records, "expense_recognition")
    expense_enhanced_avg = average(expense_items, "enhanced_rule_score")
    expense_enhanced_false_fail = count_conflict(
        records,
        "enhanced_conflict_type",
        "rule_fail_llm_pass",
        "expense_recognition",
    )
    previous_expense_avg = average(previous_expense_items, "enhanced_rule_score") if previous_expense_items else None
    previous_expense_false_fail = (
        count_conflict(previous_records, "enhanced_conflict_type", "rule_fail_llm_pass", "expense_recognition")
        if previous_expense_items
        else None
    )

    current_by_run_id = by_run_id(records)
    previous_by_run_id = by_run_id(previous_records)
    generic_run_id = REPORTED_ISSUE_BASELINE["net_profit_generic_run_id"]
    generic_record = current_by_run_id.get(generic_run_id, {})
    previous_generic_record = previous_by_run_id.get(generic_run_id, {})
    net_profit_false_pass = count_conflict(records, "enhanced_conflict_type", "rule_pass_llm_fail", "net_profit")
    previous_net_profit_false_pass = (
        count_conflict(previous_records, "enhanced_conflict_type", "rule_pass_llm_fail", "net_profit")
        if previous_records
        else None
    )
    sanity_passed = bool(sanity_results) and all(result["passed"] for result in sanity_results)
    expense_fixed = expense_enhanced_avg > 0 and expense_enhanced_false_fail < REPORTED_ISSUE_BASELINE[
        "expense_recognition_enhanced_rule_fail_llm_pass"
    ]
    generic_net_profit_fixed = as_float(generic_record.get("enhanced_rule_score")) <= 0.4 and generic_record.get(
        "enhanced_rule_passed"
    ) is False
    false_pass_reduced = (
        previous_net_profit_false_pass is None
        or net_profit_false_pass < previous_net_profit_false_pass
        or net_profit_false_pass == 0
    )
    contradiction_failures = [
        record
        for record in contradiction_records
        if record.get("enhanced_rule_passed") is True or as_float(record.get("enhanced_rule_score")) > 0.66
    ]

    if sanity_passed and expense_fixed and generic_net_profit_fixed and false_pass_reduced and not contradiction_failures:
        conclusion_status = "PASS"
        conclusion = "enhanced scorer 修复通过：expense_recognition 已改善，net_profit 泛泛结论被压低，矛盾答案未通过。"
    elif sanity_passed and expense_enhanced_avg > 0 and generic_net_profit_fixed:
        conclusion_status = "PARTIAL_PASS"
        conclusion = "enhanced scorer 关键边界测试通过，但仍存在需要人工复核的 residual conflict。"
    else:
        conclusion_status = "FAIL"
        conclusion = "enhanced scorer 未满足关键修复条件，需要继续收紧或补充语义规则。"

    lines = [
        "# Enhanced Rule Score Report",
        "",
        f"- output_jsonl: `{output_jsonl.as_posix()}`",
        f"- total_rows: {total}",
        "",
        "## Overall",
        "",
        f"- old_rule_score_avg: {old_avg:.4f}",
        f"- enhanced_rule_score_avg: {enhanced_avg:.4f}",
        f"- judge_score_avg: {judge_avg:.4f}",
        f"- old_rule_passed: {old_rule_pass}/{total} ({pct(old_rule_pass, total)})",
        f"- enhanced_rule_passed: {enhanced_rule_pass}/{total} ({pct(enhanced_rule_pass, total)})",
        f"- old_rule_fail_llm_pass: {old_false_fail}",
        f"- enhanced_rule_fail_llm_pass: {enhanced_false_fail}",
        f"- old_rule_pass_llm_fail: {len(old_false_pass)}",
        f"- old_rule_pass_llm_fail_with_contradiction_detected: {len(captured_false_pass)}/{len(old_false_pass)}",
        f"- reported_issue_baseline_enhanced_rule_pass_llm_fail: {REPORTED_ISSUE_BASELINE['overall_enhanced_rule_pass_llm_fail']}",
        f"- current_enhanced_rule_pass_llm_fail: {len(enhanced_false_passes)}",
        f"- enhanced_conflict_type: {dict(conflict_counts)}",
        f"- conclusion_status: {conclusion_status}",
        "",
        "## Targeted Fix Checks",
        "",
        "### expense_recognition",
        f"- reported_issue_baseline_enhanced_avg: {REPORTED_ISSUE_BASELINE['expense_recognition_enhanced_avg']:.4f}",
        f"- reported_issue_baseline_enhanced_rule_fail_llm_pass: {REPORTED_ISSUE_BASELINE['expense_recognition_enhanced_rule_fail_llm_pass']}",
        f"- previous_file_enhanced_avg: {'n/a' if previous_expense_avg is None else f'{previous_expense_avg:.4f}'}",
        f"- previous_file_enhanced_rule_fail_llm_pass: {'n/a' if previous_expense_false_fail is None else previous_expense_false_fail}",
        f"- current_enhanced_avg: {expense_enhanced_avg:.4f}",
        f"- current_enhanced_rule_fail_llm_pass: {expense_enhanced_false_fail}",
        "",
        "### net_profit",
        f"- generic_run_id: `{generic_run_id}`",
        f"- reported_issue_baseline_score: {REPORTED_ISSUE_BASELINE['net_profit_generic_previous_score']:.4f}",
        f"- reported_issue_baseline_net_profit_rule_pass_llm_fail: {REPORTED_ISSUE_BASELINE['net_profit_enhanced_rule_pass_llm_fail']}",
        f"- previous_file_score: {previous_generic_record.get('enhanced_rule_score', 'n/a')}",
        f"- current_score: {generic_record.get('enhanced_rule_score', 'n/a')}",
        f"- current_passed: {generic_record.get('enhanced_rule_passed', 'n/a')}",
        f"- previous_file_net_profit_rule_pass_llm_fail: {'n/a' if previous_net_profit_false_pass is None else previous_net_profit_false_pass}",
        f"- current_net_profit_rule_pass_llm_fail: {net_profit_false_pass}",
        "",
        "## Sanity Tests",
        "",
        f"- all_sanity_tests_passed: {sanity_passed}",
        "",
        "| test | passed | score | rule_passed | contradiction_detected | tags | expectation |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for result in sanity_results:
        lines.append(
            f"| `{result['name']}` | {result['passed']} | {result['enhanced_rule_score']} | "
            f"{result['enhanced_rule_passed']} | {result['contradiction_detected']} | "
            f"{format_list(result['contradiction_tags'])} | {result['expectation']} |"
        )

    lines.extend(
        [
        "",
        "## By Node",
        "",
        *node_summary(records),
        "",
        f"## Enhanced Rule Pass LLM Fail Samples ({len(enhanced_false_passes)})",
    ]
    )

    if not enhanced_false_passes:
        lines.append("")
        lines.append("- none")
    else:
        for index, record in enumerate(enhanced_false_passes, start=1):
            lines.extend(
                [
                    "",
                    f"### {index}. `{record.get('run_id', '')}`",
                    f"- node_id / condition / persona: `{record.get('node_id', '')}` / `{record.get('condition', '')}` / `{record.get('student_persona', '')}`",
                    f"- old_rule_score -> enhanced_rule_score: {record.get('rule_score')} -> {record.get('enhanced_rule_score')}",
                    f"- judge_score / judge_passed: {record.get('judge_score')} / {record.get('judge_passed')}",
                    f"- enhanced_matched_reasoning_points: {format_list(record.get('enhanced_matched_reasoning_points'))}",
                    f"- enhanced_missing_reasoning_points: {format_list(record.get('enhanced_missing_reasoning_points'))}",
                    f"- contradiction_tags: {format_list(record.get('contradiction_tags'))}",
                    f"- scoring_notes: {format_list(record.get('scoring_notes'))}",
                    f"- student_answer: {short_text(record.get('student_answer', ''), 260)}",
                ]
            )

    lines.extend(
        [
        "",
        "## Top 10 Score Changes",
        ]
    )

    for index, record in enumerate(biggest_changes(records), start=1):
        lines.extend(
            [
                "",
                f"### {index}. `{record.get('run_id', '')}`",
                f"- node_id / condition / persona: `{record.get('node_id', '')}` / `{record.get('condition', '')}` / `{record.get('student_persona', '')}`",
                f"- old_rule_score -> enhanced_rule_score: {record.get('rule_score')} -> {record.get('enhanced_rule_score')} ({record.get('enhanced_rule_score_delta'):+.4f})",
                f"- judge_score / judge_passed: {record.get('judge_score')} / {record.get('judge_passed')}",
                f"- old_conflict_type -> enhanced_conflict_type: `{record.get('conflict_type', '')}` -> `{record.get('enhanced_conflict_type', '')}`",
                f"- enhanced_matched_reasoning_points: {format_list(record.get('enhanced_matched_reasoning_points'))}",
                f"- enhanced_missing_reasoning_points: {format_list(record.get('enhanced_missing_reasoning_points'))}",
                f"- contradiction_tags: {format_list(record.get('contradiction_tags'))}",
                f"- scoring_notes: {format_list(record.get('scoring_notes'))}",
                f"- student_answer: {short_text(record.get('student_answer', ''), 260)}",
            ]
        )

    lines.extend(["", "## Contradiction Detected Samples", ""])
    if not contradiction_records:
        lines.append("- none")
    else:
        for index, record in enumerate(contradiction_records, start=1):
            lines.extend(
                [
                    f"{index}. `{record.get('run_id', '')}` | `{record.get('node_id', '')}` | `{record.get('condition', '')}` | "
                    f"`{record.get('student_persona', '')}` | old={record.get('rule_score')} enhanced={record.get('enhanced_rule_score')} "
                    f"judge={record.get('judge_score')} | tags={format_list(record.get('contradiction_tags'))}",
                    f"   - answer: {short_text(record.get('student_answer', ''), 220)}",
                ]
            )

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            f"- {conclusion}",
            "- 建议先修评分器再进入课程修改；当前差异主要来自同义表达识别和矛盾答案惩罚，而不是课程内容本身已经被证伪。",
        ]
    )
    return lines


def write_report(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rescore Synthetic Student Lab outputs with enhanced rule scorer.")
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing judge_results.jsonl.",
    )
    parser.add_argument(
        "--pass-ratio",
        type=float,
        default=DEFAULT_PASS_RATIO,
        help="Pass ratio for enhanced rule scoring.",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    judge_path = input_dir / "judge_results.jsonl"
    enhanced_path = input_dir / "judge_results.enhanced.jsonl"
    report_path = input_dir / "enhanced_rule_score_report.md"

    records = read_jsonl(judge_path)
    previous_records = read_jsonl(enhanced_path) if enhanced_path.exists() else []
    rescored = rescore_records(records, args.pass_ratio)
    sanity_results = run_sanity_checks(args.pass_ratio)
    write_jsonl(enhanced_path, rescored)
    write_report(report_path, build_report(rescored, enhanced_path, previous_records, sanity_results))

    print(f"Wrote {enhanced_path}")
    print(f"Wrote {report_path}")
    print(f"rows={len(rescored)}")
    print(f"old_rule_score_avg={average(rescored, 'rule_score'):.4f}")
    print(f"enhanced_rule_score_avg={average(rescored, 'enhanced_rule_score'):.4f}")
    print(f"sanity_tests_passed={all(result['passed'] for result in sanity_results)}")
    print(
        "rule_fail_llm_pass="
        f"{sum(1 for record in rescored if record.get('conflict_type') == 'rule_fail_llm_pass')} -> "
        f"{sum(1 for record in rescored if record.get('enhanced_conflict_type') == 'rule_fail_llm_pass')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
