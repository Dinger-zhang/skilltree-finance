from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_OUTPUT_DIR = Path("experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001")

SIMULATION_REQUIRED_FIELDS = {
    "run_id",
    "node_id",
    "condition",
    "student_persona",
    "question",
    "student_answer",
}

JUDGE_REQUIRED_FIELDS = {
    "run_id",
    "node_id",
    "condition",
    "student_persona",
    "rule_score",
    "rule_passed",
    "judge_score",
    "judge_passed",
    "conflict_type",
}


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows = []
    errors = []
    if not path.exists():
        return rows, [f"WARNING missing file: {path}"]
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"WARNING invalid JSON at {path}:{line_number}: {exc}")
                continue
            if not isinstance(value, dict):
                errors.append(f"WARNING non-object JSON at {path}:{line_number}")
                continue
            rows.append(value)
    return rows, errors


def bool_label(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return str(value)


def counter_lines(title: str, counter: Counter[Any]) -> list[str]:
    lines = [f"{title}:"]
    if not counter:
        lines.append("  - <none>: 0")
        return lines
    for key, count in sorted(counter.items(), key=lambda item: str(item[0])):
        lines.append(f"  - {key}: {count}")
    return lines


def pass_rate_lines(title: str, rows: list[dict[str, Any]], keys: list[str]) -> list[str]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(str(row.get(key, "")) for key in keys)].append(row)

    lines = [f"{title}:"]
    if not grouped:
        lines.append("  - <none>: 0/0 (0.0%)")
        return lines

    for group_key, items in sorted(grouped.items(), key=lambda item: item[0]):
        passed = sum(1 for item in items if item.get("judge_passed") is True)
        total = len(items)
        rate = (passed / total * 100) if total else 0.0
        label = " x ".join(group_key)
        lines.append(f"  - {label}: {passed}/{total} ({rate:.1f}%)")
    return lines


def run_id_problem_count(
    simulation_rows: list[dict[str, Any]],
    judge_rows: list[dict[str, Any]],
) -> int:
    simulation_ids = [str(row.get("run_id", "")) for row in simulation_rows]
    judge_ids = [str(row.get("run_id", "")) for row in judge_rows]
    simulation_counter = Counter(simulation_ids)
    judge_counter = Counter(judge_ids)
    simulation_set = set(simulation_ids)
    judge_set = set(judge_ids)
    return (
        len(simulation_set - judge_set)
        + len(judge_set - simulation_set)
        + sum(1 for count in simulation_counter.values() if count > 1)
        + sum(1 for count in judge_counter.values() if count > 1)
    )


def numeric_values(rows: list[dict[str, Any]], field: str) -> list[float]:
    values = []
    for row in rows:
        value = row.get(field)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            values.append(float(value))
    return values


def score_summary_lines(field: str, rows: list[dict[str, Any]]) -> list[str]:
    values = numeric_values(rows, field)
    if not values:
        return [f"{field} min/max/avg: <none>"]
    return [
        f"{field} min/max/avg: {min(values):.4f} / {max(values):.4f} / {mean(values):.4f}"
    ]


def out_of_range_count(rows: list[dict[str, Any]], field: str) -> int:
    count = 0
    for row in rows:
        value = row.get(field)
        if isinstance(value, bool):
            continue
        if not isinstance(value, (int, float)):
            continue
        if value < 0 or value > 1:
            count += 1
    return count


def missing_field_lines(
    title: str,
    rows: list[dict[str, Any]],
    required_fields: set[str],
) -> tuple[list[str], int]:
    missing_counter: Counter[str] = Counter()
    rows_with_missing = 0
    for row in rows:
        missing = [field for field in sorted(required_fields) if field not in row]
        if missing:
            rows_with_missing += 1
            missing_counter.update(missing)

    lines = [f"{title}:"]
    if not missing_counter:
        lines.append("  - none")
        return lines, 0

    lines.append(f"  - WARNING rows_with_missing_fields: {rows_with_missing}")
    for field, count in sorted(missing_counter.items()):
        lines.append(f"  - {field}: missing in {count} rows")
    return lines, rows_with_missing


def run_id_check_lines(
    simulation_rows: list[dict[str, Any]],
    judge_rows: list[dict[str, Any]],
) -> list[str]:
    simulation_ids = [str(row.get("run_id", "")) for row in simulation_rows]
    judge_ids = [str(row.get("run_id", "")) for row in judge_rows]
    simulation_counter = Counter(simulation_ids)
    judge_counter = Counter(judge_ids)
    simulation_set = set(simulation_ids)
    judge_set = set(judge_ids)

    missing_in_judge = sorted(simulation_set - judge_set)
    extra_in_judge = sorted(judge_set - simulation_set)
    duplicated_simulation = sorted(run_id for run_id, count in simulation_counter.items() if count > 1)
    duplicated_judge = sorted(run_id for run_id, count in judge_counter.items() if count > 1)

    one_to_one = (
        not missing_in_judge
        and not extra_in_judge
        and not duplicated_simulation
        and not duplicated_judge
        and len(simulation_rows) == len(judge_rows)
    )

    lines = ["run_id correspondence:"]
    lines.append(f"  - one_to_one: {one_to_one}")
    lines.append(f"  - missing_in_judge: {len(missing_in_judge)}")
    lines.append(f"  - extra_in_judge: {len(extra_in_judge)}")
    lines.append(f"  - duplicated_in_simulation: {len(duplicated_simulation)}")
    lines.append(f"  - duplicated_in_judge: {len(duplicated_judge)}")
    if not one_to_one:
        lines.append("  - WARNING run_id mismatch detected")
    for label, values in (
        ("missing_in_judge_sample", missing_in_judge),
        ("extra_in_judge_sample", extra_in_judge),
        ("duplicated_in_simulation_sample", duplicated_simulation),
        ("duplicated_in_judge_sample", duplicated_judge),
    ):
        if values:
            lines.append(f"  - {label}: {', '.join(values[:10])}")
    return lines


def build_summary(output_dir: Path) -> list[str]:
    simulation_path = output_dir / "simulation_runs.jsonl"
    judge_path = output_dir / "judge_results.jsonl"

    simulation_rows, simulation_errors = read_jsonl(simulation_path)
    judge_rows, judge_errors = read_jsonl(judge_path)

    lines = [
        "Synthetic Student Lab Output Check",
        f"output_dir: {output_dir}",
        f"simulation_runs: {simulation_path}",
        f"judge_results: {judge_path}",
        "",
        "Basic counts:",
        f"  - simulation_runs.jsonl rows: {len(simulation_rows)}",
        f"  - judge_results.jsonl rows: {len(judge_rows)}",
    ]

    if simulation_errors or judge_errors:
        lines.append("")
        lines.append("JSONL load warnings:")
        lines.extend(f"  - {error}" for error in [*simulation_errors, *judge_errors])

    lines.append("")
    lines.extend(run_id_check_lines(simulation_rows, judge_rows))

    lines.append("")
    lines.extend(counter_lines("student_persona distribution", Counter(row.get("student_persona") for row in simulation_rows)))
    lines.append("")
    lines.extend(counter_lines("condition distribution", Counter(row.get("condition") for row in simulation_rows)))
    lines.append("")
    lines.extend(counter_lines("node_id distribution", Counter(row.get("node_id") for row in simulation_rows)))
    lines.append("")
    lines.extend(counter_lines("conflict_type distribution", Counter(row.get("conflict_type") for row in judge_rows)))
    lines.append("")
    lines.extend(counter_lines("judge_passed distribution", Counter(bool_label(row.get("judge_passed")) for row in judge_rows)))
    lines.append("")
    lines.extend(counter_lines("rule_passed distribution", Counter(bool_label(row.get("rule_passed")) for row in judge_rows)))

    lines.append("")
    lines.extend(pass_rate_lines("judge_passed pass rate by condition", judge_rows, ["condition"]))
    lines.append("")
    lines.extend(pass_rate_lines("judge_passed pass rate by persona", judge_rows, ["student_persona"]))
    lines.append("")
    lines.extend(pass_rate_lines("judge_passed pass rate by node_id", judge_rows, ["node_id"]))
    lines.append("")
    lines.extend(pass_rate_lines("judge_passed pass rate by node_id x condition", judge_rows, ["node_id", "condition"]))

    error_count = sum(1 for row in judge_rows if str(row.get("error_message", "")).strip())
    empty_student_answer_count = sum(
        1 for row in simulation_rows if not str(row.get("student_answer", "")).strip()
    )
    judge_score_oob = out_of_range_count(judge_rows, "judge_score")
    rule_score_oob = out_of_range_count(judge_rows, "rule_score")

    lines.append("")
    lines.append("Data quality checks:")
    lines.append(f"  - error_message non-empty count: {error_count}")
    if error_count:
        lines.append("  - WARNING non-empty error_message found")
    lines.append(f"  - student_answer empty count: {empty_student_answer_count}")
    if empty_student_answer_count:
        lines.append("  - WARNING empty student_answer found")
    lines.append(f"  - judge_score out of [0, 1] count: {judge_score_oob}")
    if judge_score_oob:
        lines.append("  - WARNING judge_score out of range")
    lines.append(f"  - rule_score out of [0, 1] count: {rule_score_oob}")
    if rule_score_oob:
        lines.append("  - WARNING rule_score out of range")

    lines.append("")
    lines.extend(score_summary_lines("judge_score", judge_rows))
    lines.extend(score_summary_lines("rule_score", judge_rows))

    lines.append("")
    sim_missing_lines, sim_missing_count = missing_field_lines(
        "simulation_runs required field check",
        simulation_rows,
        SIMULATION_REQUIRED_FIELDS,
    )
    lines.extend(sim_missing_lines)

    lines.append("")
    judge_missing_lines, judge_missing_count = missing_field_lines(
        "judge_results required field check",
        judge_rows,
        JUDGE_REQUIRED_FIELDS,
    )
    lines.extend(judge_missing_lines)

    severe_problem_count = (
        len(simulation_errors)
        + len(judge_errors)
        + run_id_problem_count(simulation_rows, judge_rows)
        + sim_missing_count
        + judge_missing_count
        + error_count
        + judge_score_oob
        + rule_score_oob
        + empty_student_answer_count
    )
    lines.append("")
    lines.append("Overall:")
    if severe_problem_count:
        lines.append(f"  - WARNING severe_or_actionable_problem_count: {severe_problem_count}")
    else:
        lines.append("  - no severe structural problems detected")

    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Synthetic Student Lab output JSONL files.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory containing simulation_runs.jsonl and judge_results.jsonl.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    lines = build_summary(output_dir)
    text = "\n".join(lines) + "\n"
    print(text, end="")

    summary_path = output_dir / "check_summary.txt"
    summary_path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
