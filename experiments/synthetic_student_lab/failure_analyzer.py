from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Any


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from common import load_config, output_path, read_jsonl  # noqa: E402


def pct(numerator: float, denominator: float) -> str:
    if denominator <= 0:
        return "0.0%"
    return f"{(numerator / denominator) * 100:.1f}%"


def avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def short_text(text: str, limit: int = 180) -> str:
    stripped = " ".join(str(text).split())
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 3] + "..."


def bool_pass(record: dict[str, Any], field: str) -> bool:
    return bool(record.get(field))


def build_node_stats(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for record in records:
        node_id = str(record.get("node_id", ""))
        node = stats.setdefault(
            node_id,
            {
                "node_id": node_id,
                "node_title": record.get("node_title", ""),
                "total": 0,
                "rule_fail": 0,
                "judge_fail": 0,
                "hidden_total": 0,
                "hidden_judge_fail": 0,
                "false_pass": 0,
                "false_fail": 0,
                "rule_scores": [],
                "judge_scores": [],
                "tags": Counter(),
                "missing_points": Counter(),
            },
        )
        node["total"] += 1
        if not bool_pass(record, "rule_passed"):
            node["rule_fail"] += 1
        if not bool_pass(record, "judge_passed"):
            node["judge_fail"] += 1
        if record.get("condition") == "hidden_transfer":
            node["hidden_total"] += 1
            if not bool_pass(record, "judge_passed"):
                node["hidden_judge_fail"] += 1
        if record.get("failure_type") == "rule_pass_llm_fail":
            node["false_pass"] += 1
        if record.get("failure_type") == "rule_fail_llm_pass":
            node["false_fail"] += 1
        if isinstance(record.get("rule_score"), (int, float)):
            node["rule_scores"].append(float(record["rule_score"]))
        if isinstance(record.get("judge_score"), (int, float)):
            node["judge_scores"].append(float(record["judge_score"]))
        node["tags"].update(str(tag) for tag in record.get("misconception_tags", []))
        node["missing_points"].update(str(point) for point in record.get("missing_reasoning_points", []))
    return stats


def risk_score(node: dict[str, Any]) -> float:
    total = max(1, int(node["total"]))
    hidden_total = max(1, int(node["hidden_total"]))
    judge_failure_rate = node["judge_fail"] / total
    hidden_failure_rate = node["hidden_judge_fail"] / hidden_total
    false_pass_rate = node["false_pass"] / total
    tag_pressure = min(1.0, sum(node["tags"].values()) / total)
    return (
        judge_failure_rate * 0.45
        + hidden_failure_rate * 0.3
        + false_pass_rate * 0.2
        + tag_pressure * 0.05
    )


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return lines


def sample_lines(title: str, records: list[dict[str, Any]], max_samples: int) -> list[str]:
    lines = [f"## {title}"]
    if not records:
        lines.append("")
        lines.append("本次没有样本。")
        return lines
    for record in records[:max_samples]:
        lines.append("")
        lines.append(f"- run_id: `{record.get('run_id', '')}`")
        lines.append(f"- node: `{record.get('node_id', '')}` {record.get('node_title', '')}")
        lines.append(
            f"- persona/condition: `{record.get('student_persona', '')}` / `{record.get('condition', '')}`"
        )
        lines.append(f"- rule/judge: {record.get('rule_score')} -> {record.get('judge_score')}")
        lines.append(f"- question: {short_text(record.get('question', ''))}")
        lines.append(f"- answer: {short_text(record.get('student_answer', ''))}")
        missing = record.get("judge_missing_reasoning_points") or record.get("missing_reasoning_points", [])
        if missing:
            lines.append(f"- missing: {short_text('；'.join(str(item) for item in missing), 220)}")
        tags = record.get("misconception_tags", [])
        if tags:
            lines.append(f"- tags: {', '.join(str(tag) for tag in tags)}")
        if record.get("error_message"):
            lines.append(f"- error: {short_text(record.get('error_message', ''), 220)}")
    return lines


def hidden_transfer_rows(records: list[dict[str, Any]]) -> list[list[Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("condition") == "hidden_transfer":
            grouped[(str(record.get("node_id", "")), str(record.get("node_title", "")))].append(record)

    rows = []
    for (node_id, title), items in sorted(grouped.items()):
        judge_passes = sum(1 for item in items if bool_pass(item, "judge_passed"))
        avg_score = avg(
            [float(item.get("judge_score", 0.0)) for item in items if item.get("judge_score") is not None]
        )
        failing_personas = sorted(
            {
                str(item.get("student_persona", ""))
                for item in items
                if not bool_pass(item, "judge_passed")
            }
        )
        rows.append(
            [
                f"`{node_id}`",
                title,
                f"{judge_passes}/{len(items)}",
                f"{avg_score:.2f}",
                ", ".join(failing_personas) or "-",
            ]
        )
    return rows


def course_suggestions(ranked_nodes: list[dict[str, Any]]) -> list[str]:
    lines = ["## 课程修改建议"]
    if not ranked_nodes:
        lines.append("")
        lines.append("暂无建议。")
        return lines
    for node in ranked_nodes:
        if risk_score(node) <= 0:
            continue
        node_label = f"`{node['node_id']}` {node.get('node_title', '')}".strip()
        suggestions = []
        if node["false_pass"]:
            suggestions.append("收紧关键词规则，要求关键因果关系同时出现，降低 false_pass。")
        hidden_rate = node["hidden_judge_fail"] / max(1, node["hidden_total"])
        if hidden_rate >= 0.5:
            suggestions.append("增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。")
        if node["tags"]:
            top_tag = node["tags"].most_common(1)[0][0]
            suggestions.append(f"补充常见误区讲解，优先处理 `{top_tag}`。")
        if node["judge_fail"] / max(1, node["total"]) >= 0.5:
            suggestions.append("检查前置节点、引导问题和 mastery_question 是否存在跳步。")
        if not suggestions:
            suggestions.append("保持观察，优先人工复核具体失败样本。")
        lines.append("")
        lines.append(f"- {node_label}: {' '.join(suggestions)}")
    return lines


def generate_report(config_path: str | None = None) -> Path:
    config = load_config(config_path)
    simulation_records = read_jsonl(output_path(config, "simulation_runs"))
    judge_records = read_jsonl(output_path(config, "judge_results"))
    sim_by_run = {record.get("run_id"): record for record in simulation_records}
    merged = [{**sim_by_run.get(record.get("run_id"), {}), **record} for record in judge_records]

    report_settings = config.get("report", {})
    max_samples = int(report_settings.get("max_samples_per_section", 5))
    high_risk_top_n = int(report_settings.get("high_risk_top_n", 8))

    total = len(merged)
    rule_passes = sum(1 for record in merged if bool_pass(record, "rule_passed"))
    judge_passes = sum(1 for record in merged if bool_pass(record, "judge_passed"))
    false_passes = [record for record in merged if record.get("failure_type") == "rule_pass_llm_fail"]
    false_fails = [record for record in merged if record.get("failure_type") == "rule_fail_llm_pass"]
    hidden = [record for record in merged if record.get("condition") == "hidden_transfer"]
    hidden_judge_passes = sum(1 for record in hidden if bool_pass(record, "judge_passed"))
    manual_review = [
        record
        for record in merged
        if record.get("failure_type") in {"rule_pass_llm_fail", "rule_fail_llm_pass"}
        or record.get("external_knowledge_suspicion")
        or record.get("error_message")
        or (
            record.get("condition") == "hidden_transfer"
            and not bool_pass(record, "judge_passed")
        )
    ]

    node_stats = build_node_stats(merged)
    ranked_nodes = sorted(node_stats.values(), key=risk_score, reverse=True)

    graph_versions = sorted({str(record.get("graph_version", "")) for record in merged})
    personas = sorted({str(record.get("student_persona", "")) for record in merged})
    conditions = sorted({str(record.get("condition", "")) for record in merged})
    nodes = sorted({str(record.get("node_id", "")) for record in merged})
    fallback_count = sum(1 for record in merged if record.get("graph_fallback_used"))

    lines: list[str] = [
        "# Synthetic Student Lab v0.3 Minimal Report",
        "",
        "## 实验范围",
        "",
        f"- experiment_id: `{config.get('experiment_id', '')}`",
        f"- graph_version: `{', '.join(graph_versions)}`",
        f"- chain_id: `{config.get('chain_id', '')}`",
        f"- nodes: {len(nodes)}",
        f"- personas: {len(personas)} ({', '.join(personas)})",
        f"- conditions: {len(conditions)} ({', '.join(conditions)})",
        f"- total_runs: {total}",
        f"- graph_fallback_used_runs: {fallback_count}",
        "",
        "## 总体指标",
        "",
    ]
    lines.extend(
        markdown_table(
            ["metric", "value"],
            [
                ["rule_pass_rate", pct(rule_passes, total)],
                ["judge_pass_rate", pct(judge_passes, total)],
                ["hidden_transfer_judge_pass_rate", pct(hidden_judge_passes, len(hidden))],
                ["false_pass_count", len(false_passes)],
                ["false_fail_count", len(false_fails)],
                ["manual_review_count", len(manual_review)],
            ],
        )
    )

    lines.extend(["", "## 每个节点的失败率", ""])
    node_rows = []
    for node in sorted(node_stats.values(), key=lambda item: item["node_id"]):
        node_rows.append(
            [
                f"`{node['node_id']}`",
                node.get("node_title", ""),
                node["total"],
                pct(node["judge_fail"], node["total"]),
                pct(node["hidden_judge_fail"], node["hidden_total"]),
                node["false_pass"],
                node["false_fail"],
                f"{avg(node['judge_scores']):.2f}",
            ]
        )
    lines.extend(
        markdown_table(
            [
                "node_id",
                "title",
                "runs",
                "judge_failure_rate",
                "hidden_failure_rate",
                "false_pass",
                "false_fail",
                "avg_judge_score",
            ],
            node_rows,
        )
    )

    lines.extend(["", "## false_pass / false_fail 样本"])
    lines.extend(sample_lines("false_pass: rule_pass_llm_fail", false_passes, max_samples))
    lines.append("")
    lines.extend(sample_lines("false_fail: rule_fail_llm_pass", false_fails, max_samples))

    lines.extend(["", "## hidden transfer 表现", ""])
    lines.extend(
        markdown_table(
            ["node_id", "title", "judge_passes", "avg_judge_score", "failing_personas"],
            hidden_transfer_rows(merged),
        )
    )

    lines.extend(["", "## 高风险节点排行", ""])
    risk_rows = []
    for node in ranked_nodes[:high_risk_top_n]:
        top_tags = ", ".join(f"{tag}:{count}" for tag, count in node["tags"].most_common(3)) or "-"
        risk_rows.append(
            [
                f"`{node['node_id']}`",
                node.get("node_title", ""),
                f"{risk_score(node):.3f}",
                pct(node["judge_fail"], node["total"]),
                pct(node["hidden_judge_fail"], node["hidden_total"]),
                node["false_pass"],
                top_tags,
            ]
        )
    lines.extend(
        markdown_table(
            [
                "node_id",
                "title",
                "risk_score",
                "judge_failure_rate",
                "hidden_failure_rate",
                "false_pass",
                "top_tags",
            ],
            risk_rows,
        )
    )

    lines.append("")
    lines.extend(course_suggestions(ranked_nodes[:high_risk_top_n]))

    lines.append("")
    lines.extend(sample_lines("需要人工复核的样本", manual_review, max_samples))

    lines.extend(
        [
            "",
            "## 备注",
            "",
            "- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。",
            "- 当前 mock judge 用于验证数据流和报告结构，不等价于真实语义评分。",
            "- `graph_fallback_used_runs` 大于 0 表示当前图谱缺少链字段，实验使用了 B 链内置 fallback。",
        ]
    )

    report_path = output_path(config, "node_failure_report")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Synthetic Student Lab failure report.")
    parser.add_argument(
        "--config",
        default=str(CURRENT_DIR / "config.yaml"),
        help="Path to config.yaml",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = generate_report(args.config)
    print(f"Wrote failure report: {path}")


if __name__ == "__main__":
    main()
