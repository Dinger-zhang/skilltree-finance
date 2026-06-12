from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_DIR = Path("experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired")
FOCUS_NODES = {
    "net_profit",
    "accrual_vs_cash",
    "expense_recognition",
    "revenue_recognition",
}
HUMAN_REVIEW_FIELDS = [
    "run_id",
    "node_id",
    "condition",
    "student_persona",
    "question",
    "student_answer",
    "rule_score",
    "rule_passed",
    "judge_score",
    "judge_passed",
    "conflict_type",
    "matched_reasoning_points",
    "missing_reasoning_points",
    "judge_matched_reasoning_points",
    "judge_missing_reasoning_points",
    "misconception_tags",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def write_text(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def short_text(value: Any, limit: int = 300) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def format_list(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "-"
    return "；".join(str(item) for item in value)


def pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0.0%"
    return f"{numerator / denominator * 100:.1f}%"


def merge_rows(simulation_rows: list[dict[str, Any]], judge_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sim_by_run_id = {str(row.get("run_id", "")): row for row in simulation_rows}
    return [{**sim_by_run_id.get(str(row.get("run_id", "")), {}), **row} for row in judge_rows]


def treatment_for_bad_record(record: dict[str, Any]) -> str:
    if str(record.get("student_parse_error", "")).strip() or str(record.get("judge_parse_error", "")).strip():
        return "inspect_prompt"
    if not str(record.get("student_answer", "")).strip():
        return "exclude"
    if "timed out" in str(record.get("error_message", "")).lower():
        return "retry"
    if "judge_error" in str(record.get("judge_failure_reason", "")):
        return "retry"
    if str(record.get("error_message", "")).strip():
        return "inspect_prompt"
    return "inspect_prompt"


def bad_record_reason(record: dict[str, Any]) -> list[str]:
    reasons = []
    if str(record.get("error_message", "")).strip():
        reasons.append("error_message")
    if not str(record.get("student_answer", "")).strip():
        reasons.append("empty_student_answer")
    if "judge_error" in str(record.get("judge_failure_reason", "")) or "judge_llm_error" in str(
        record.get("error_message", "")
    ):
        reasons.append("judge_error")
    if str(record.get("student_parse_error", "")).strip() or str(record.get("judge_parse_error", "")).strip():
        reasons.append("json_parse_error")
    return reasons


def build_bad_records(records: list[dict[str, Any]]) -> list[str]:
    bad = [record for record in records if bad_record_reason(record)]
    lines = ["# Bad Records", "", f"total_bad_records: {len(bad)}"]
    if not bad:
        lines.append("")
        lines.append("No bad records found.")
        return lines

    for index, record in enumerate(bad, start=1):
        lines.extend(
            [
                "",
                f"## {index}. `{record.get('run_id', '')}`",
                f"- reason: {', '.join(bad_record_reason(record))}",
                f"- run_id: `{record.get('run_id', '')}`",
                f"- node_id: `{record.get('node_id', '')}`",
                f"- condition: `{record.get('condition', '')}`",
                f"- student_persona: `{record.get('student_persona', '')}`",
                f"- question: {short_text(record.get('question', ''), 300)}",
                f"- student_answer: {short_text(record.get('student_answer', ''), 300)}",
                f"- error_message: {short_text(record.get('error_message', ''), 300)}",
                f"- student_parse_error: {short_text(record.get('student_parse_error', ''), 200)}",
                f"- judge_parse_error: {short_text(record.get('judge_parse_error', ''), 200)}",
                f"- suggested_action: {treatment_for_bad_record(record)}",
            ]
        )
    return lines


def build_conflict_samples(records: list[dict[str, Any]]) -> list[str]:
    false_passes = [record for record in records if record.get("conflict_type") == "rule_pass_llm_fail"]
    false_fails = [record for record in records if record.get("conflict_type") == "rule_fail_llm_pass"]
    false_fails = sorted(
        false_fails,
        key=lambda record: (
            float(record.get("judge_score", 0.0) or 0.0) - float(record.get("rule_score", 0.0) or 0.0),
            float(record.get("judge_score", 0.0) or 0.0),
        ),
        reverse=True,
    )[:20]

    lines = [
        "# Conflict Samples",
        "",
        f"rule_pass_llm_fail_count: {len(false_passes)}",
        f"rule_fail_llm_pass_listed_count: {len(false_fails)}",
    ]
    for title, items in (
        ("rule_pass_llm_fail", false_passes),
        ("rule_fail_llm_pass", false_fails),
    ):
        lines.extend(["", f"## {title}"])
        if not items:
            lines.append("")
            lines.append("No samples.")
            continue
        for index, record in enumerate(items, start=1):
            lines.extend(
                [
                    "",
                    f"### {index}. `{record.get('run_id', '')}`",
                    f"- node_id / condition / persona: `{record.get('node_id', '')}` / `{record.get('condition', '')}` / `{record.get('student_persona', '')}`",
                    f"- rule_score / judge_score: {record.get('rule_score')} / {record.get('judge_score')}",
                    f"- matched_reasoning_points: {format_list(record.get('matched_reasoning_points'))}",
                    f"- missing_reasoning_points: {format_list(record.get('missing_reasoning_points'))}",
                    f"- judge_matched_reasoning_points: {format_list(record.get('judge_matched_reasoning_points'))}",
                    f"- judge_missing_reasoning_points: {format_list(record.get('judge_missing_reasoning_points'))}",
                    f"- student_answer: {short_text(record.get('student_answer', ''), 300)}",
                ]
            )
    return lines


def pass_rate(items: list[dict[str, Any]]) -> tuple[int, int, str]:
    passed = sum(1 for item in items if item.get("judge_passed") is True)
    total = len(items)
    return passed, total, pct(passed, total)


def build_node_condition_summary(records: list[dict[str, Any]]) -> list[str]:
    by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_node_condition: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_node[str(record.get("node_id", ""))].append(record)
        by_node_condition[(str(record.get("node_id", "")), str(record.get("condition", "")))].append(record)

    lines = ["# Node And Condition Summary", ""]
    lines.append("## Focus Nodes")
    for node_id in sorted(FOCUS_NODES):
        items = by_node.get(node_id, [])
        passed, total, rate = pass_rate(items)
        conflicts = Counter(str(item.get("conflict_type", "")) for item in items)
        tags = Counter(tag for item in items for tag in item.get("misconception_tags", []))
        lines.extend(
            [
                "",
                f"### `{node_id}`",
                f"- judge_passed: {passed}/{total} ({rate})",
                f"- conflict_type: {dict(conflicts)}",
                f"- top_misconception_tags: {dict(tags.most_common(5))}",
            ]
        )
        for condition in sorted({str(item.get("condition", "")) for item in items}):
            condition_items = by_node_condition[(node_id, condition)]
            c_passed, c_total, c_rate = pass_rate(condition_items)
            lines.append(f"- {condition}: {c_passed}/{c_total} ({c_rate})")

    hidden = [record for record in records if record.get("condition") == "hidden_transfer"]
    h_passed, h_total, h_rate = pass_rate(hidden)
    lines.extend(
        [
            "",
            "## Hidden Transfer High Pass Rate",
            f"- overall hidden_transfer judge_passed: {h_passed}/{h_total} ({h_rate})",
        ]
    )
    hidden_rows = []
    for node_id in sorted(by_node):
        items = by_node_condition.get((node_id, "hidden_transfer"), [])
        if not items:
            continue
        passed, total, rate = pass_rate(items)
        hidden_rows.append((passed / total if total else 0.0, node_id, passed, total, rate))
    for rate_value, node_id, passed, total, rate in sorted(hidden_rows, reverse=True):
        marker = "high" if rate_value >= 0.8 else "normal"
        lines.append(f"- `{node_id}`: {passed}/{total} ({rate}) [{marker}]")

    lines.extend(["", "## node_only 0/3 Nodes"])
    zero_nodes = []
    for node_id in sorted(by_node):
        items = by_node_condition.get((node_id, "node_only"), [])
        if len(items) == 3 and sum(1 for item in items if item.get("judge_passed") is True) == 0:
            zero_nodes.append(node_id)
    if not zero_nodes:
        lines.append("- none")
    else:
        for node_id in zero_nodes:
            items = by_node_condition[(node_id, "node_only")]
            conflicts = Counter(str(item.get("conflict_type", "")) for item in items)
            personas = [
                str(item.get("student_persona", ""))
                for item in items
                if item.get("judge_passed") is not True
            ]
            lines.append(f"- `{node_id}`: 0/3, failing_personas={', '.join(personas)}, conflict_type={dict(conflicts)}")
    return lines


def review_record(record: dict[str, Any], reason: str) -> dict[str, Any]:
    reviewed = {
        field: record.get(field, [] if field.endswith("_points") or field == "misconception_tags" else "")
        for field in HUMAN_REVIEW_FIELDS
    }
    reviewed["review_reason"] = reason
    reviewed["suggested_human_fields"] = {
        "human_passed": None,
        "human_failure_type": "",
        "human_comment": "",
    }
    return reviewed


def add_review_sample(
    selected: list[dict[str, Any]],
    seen: set[str],
    record: dict[str, Any],
    reason: str,
) -> None:
    run_id = str(record.get("run_id", ""))
    if not run_id or run_id in seen:
        return
    selected.append(review_record(record, reason))
    seen.add(run_id)


def build_human_review_samples(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_many(items: list[dict[str, Any]], reason: str, limit: int | None = None) -> None:
        for item in items[: limit or len(items)]:
            add_review_sample(selected, seen, item, reason)

    false_passes = [record for record in records if record.get("conflict_type") == "rule_pass_llm_fail"]
    add_many(false_passes, "all_rule_pass_llm_fail")

    false_fails = sorted(
        [record for record in records if record.get("conflict_type") == "rule_fail_llm_pass"],
        key=lambda record: (
            float(record.get("judge_score", 0.0) or 0.0) - float(record.get("rule_score", 0.0) or 0.0),
            float(record.get("judge_score", 0.0) or 0.0),
        ),
        reverse=True,
    )
    add_many(false_fails, "high_judge_low_rule_rule_fail_llm_pass", 15)

    for node_id in ("accrual_vs_cash", "net_profit"):
        node_only_failures = [
            record
            for record in records
            if record.get("node_id") == node_id
            and record.get("condition") == "node_only"
            and record.get("judge_passed") is not True
        ]
        add_many(node_only_failures, f"{node_id}_node_only_failure")

    hidden_pass = [record for record in records if record.get("condition") == "hidden_transfer" and record.get("judge_passed") is True]
    hidden_fail = [record for record in records if record.get("condition") == "hidden_transfer" and record.get("judge_passed") is not True]
    add_many(hidden_pass, "hidden_transfer_pass", 4)
    add_many(hidden_fail, "hidden_transfer_fail", 4)

    baseline_fail = [
        record
        for record in records
        if record.get("condition") == "no_course_baseline" and record.get("judge_passed") is not True
    ]
    add_many(baseline_fail, "no_course_baseline_fail", 4)

    focus = [record for record in records if record.get("node_id") in {"net_profit", "accrual_vs_cash"}]
    focus = sorted(focus, key=lambda record: (record.get("node_id", ""), record.get("condition", ""), record.get("student_persona", "")))
    add_many(focus, "focus_node_net_profit_or_accrual_vs_cash", 6)

    personas = sorted({str(record.get("student_persona", "")) for record in records})
    conditions = sorted({str(record.get("condition", "")) for record in records})

    def count_selected(field: str, value: str) -> int:
        return sum(1 for item in selected if str(item.get(field, "")) == value)

    for persona in personas:
        candidates = [record for record in records if str(record.get("student_persona", "")) == persona]
        candidates = sorted(candidates, key=lambda record: (record.get("judge_passed") is True, record.get("condition", ""), record.get("node_id", "")))
        for record in candidates:
            if count_selected("student_persona", persona) >= 3:
                break
            add_review_sample(selected, seen, record, f"persona_coverage_{persona}")

    for condition in conditions:
        candidates = [record for record in records if str(record.get("condition", "")) == condition]
        candidates = sorted(candidates, key=lambda record: (record.get("judge_passed") is True, record.get("student_persona", ""), record.get("node_id", "")))
        for record in candidates:
            if count_selected("condition", condition) >= 3:
                break
            add_review_sample(selected, seen, record, f"condition_coverage_{condition}")

    node_ids = sorted({str(record.get("node_id", "")) for record in records})
    for node_id in node_ids:
        if any(item.get("node_id") == node_id for item in selected):
            continue
        candidates = [record for record in records if str(record.get("node_id", "")) == node_id]
        candidates = sorted(
            candidates,
            key=lambda record: (
                record.get("conflict_type") not in {"rule_fail_llm_pass", "rule_pass_llm_fail"},
                record.get("judge_passed") is True,
                record.get("condition", ""),
                record.get("student_persona", ""),
            ),
        )
        if candidates:
            add_review_sample(selected, seen, candidates[0], f"node_coverage_{node_id}")

    if len(selected) < 20:
        priority = sorted(
            records,
            key=lambda record: (
                str(record.get("error_message", "")) == "",
                record.get("conflict_type") not in {"rule_fail_llm_pass", "rule_pass_llm_fail"},
                record.get("condition") != "hidden_transfer",
                record.get("node_id") not in FOCUS_NODES,
            ),
        )
        for record in priority:
            if len(selected) >= 20:
                break
            add_review_sample(selected, seen, record, "fill_minimum_review_set")

    if len(selected) > 30:
        mandatory_reasons = {
            "all_rule_pass_llm_fail",
            "accrual_vs_cash_node_only_failure",
            "net_profit_node_only_failure",
            "hidden_transfer_pass",
            "hidden_transfer_fail",
        }
        mandatory = [
            item
            for item in selected
            if item["review_reason"] in mandatory_reasons or str(item["review_reason"]).startswith("node_coverage_")
        ]
        rest = [
            item
            for item in selected
            if item["review_reason"] not in mandatory_reasons and not str(item["review_reason"]).startswith("node_coverage_")
        ]
        selected = [*mandatory, *rest][:30]
    return selected


def build_human_review_markdown(samples: list[dict[str, Any]]) -> list[str]:
    lines = [
        "# Human Review Samples",
        "",
        f"total_samples: {len(samples)}",
        "",
        "## Coverage",
        "",
        f"- student_persona: {dict(Counter(sample.get('student_persona', '') for sample in samples))}",
        f"- condition: {dict(Counter(sample.get('condition', '') for sample in samples))}",
        f"- node_id: {dict(Counter(sample.get('node_id', '') for sample in samples))}",
        f"- conflict_type: {dict(Counter(sample.get('conflict_type', '') for sample in samples))}",
        "",
        "## Samples",
    ]
    for index, sample in enumerate(samples, start=1):
        lines.extend(
            [
                "",
                f"### {index}. `{sample.get('run_id', '')}`",
                f"- review_reason: {sample.get('review_reason', '')}",
                f"- node_id / condition / persona: `{sample.get('node_id', '')}` / `{sample.get('condition', '')}` / `{sample.get('student_persona', '')}`",
                f"- rule_score / judge_score: {sample.get('rule_score')} / {sample.get('judge_score')}",
                f"- rule_passed / judge_passed: {sample.get('rule_passed')} / {sample.get('judge_passed')}",
                f"- conflict_type: `{sample.get('conflict_type', '')}`",
                f"- misconception_tags: {format_list(sample.get('misconception_tags'))}",
                f"- matched_reasoning_points: {format_list(sample.get('matched_reasoning_points'))}",
                f"- missing_reasoning_points: {format_list(sample.get('missing_reasoning_points'))}",
                f"- judge_matched_reasoning_points: {format_list(sample.get('judge_matched_reasoning_points'))}",
                f"- judge_missing_reasoning_points: {format_list(sample.get('judge_missing_reasoning_points'))}",
                f"- question: {short_text(sample.get('question', ''), 500)}",
                f"- student_answer: {short_text(sample.get('student_answer', ''), 700)}",
                "",
                "human_passed:",
                "human_failure_type:",
                "human_comment:",
            ]
        )
    return lines


def write_human_review_jsonl(path: Path, samples: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for sample in samples:
            file.write(json.dumps(sample, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract issue samples from Synthetic Student Lab outputs.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory containing simulation_runs.jsonl and judge_results.jsonl.",
    )
    parser.add_argument(
        "--human-review-only",
        action="store_true",
        help="Only regenerate human_review_samples.jsonl and human_review.md.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    simulation_rows = read_jsonl(output_dir / "simulation_runs.jsonl")
    judge_rows = read_jsonl(output_dir / "judge_results.jsonl")
    records = merge_rows(simulation_rows, judge_rows)

    if not args.human_review_only:
        write_text(output_dir / "bad_records.md", build_bad_records(records))
        write_text(output_dir / "conflict_samples.md", build_conflict_samples(records))
        write_text(output_dir / "node_condition_summary.md", build_node_condition_summary(records))
    review_samples = build_human_review_samples(records)
    write_human_review_jsonl(output_dir / "human_review_samples.jsonl", review_samples)
    write_text(output_dir / "human_review.md", build_human_review_markdown(review_samples))

    if not args.human_review_only:
        print(f"Wrote bad_records.md")
        print(f"Wrote conflict_samples.md")
        print(f"Wrote node_condition_summary.md")
    print(f"Wrote human_review_samples.jsonl ({len(review_samples)} rows)")
    print(f"Wrote human_review.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
