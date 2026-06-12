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
                "hidden_failed_records": [],
                "hidden_failing_personas": Counter(),
                "no_course_baseline_fail": 0,
                "no_course_baseline_failing_personas": Counter(),
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
                node["hidden_failed_records"].append(record)
                node["hidden_failing_personas"].update([str(record.get("student_persona", ""))])
        if record.get("failure_type") == "rule_pass_llm_fail":
            node["false_pass"] += 1
        if record.get("failure_type") == "rule_fail_llm_pass":
            node["false_fail"] += 1
        if record.get("condition") == "no_course_baseline" and not bool_pass(record, "judge_passed"):
            node["no_course_baseline_fail"] += 1
            node["no_course_baseline_failing_personas"].update([str(record.get("student_persona", ""))])
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
    false_fail_rate = node["false_fail"] / total
    tag_pressure = min(1.0, sum(node["tags"].values()) / total)
    return (
        judge_failure_rate * 0.45
        + hidden_failure_rate * 0.3
        + false_pass_rate * 0.15
        + false_fail_rate * 0.05
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


def format_points(points: Any) -> str:
    if not isinstance(points, list) or not points:
        return "-"
    return "；".join(str(point) for point in points)


def conflict_attribution(record: dict[str, Any]) -> str:
    conflict_type = str(record.get("failure_type", ""))
    node_id = str(record.get("node_id", ""))
    tags = set(str(tag) for tag in record.get("misconception_tags", []))
    blocker = bool(record.get("rule_completeness_blocker")) or "completeness_blocker" in tags

    if conflict_type == "rule_fail_llm_pass":
        if node_id == "revenue_not_cash_receipt":
            return (
                "规则评分只按原始表述匹配，未识别“已经赚到”“钱还没进来”"
                "“客户欠款”等同义表达对应收入确认、未收现和应收款。"
            )
        return "规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。"

    if conflict_type == "rule_pass_llm_fail":
        if node_id == "gross_margin":
            return (
                "规则评分命中了公式复述，却没有要求本案例必须算出毛利 3500 元、"
                "毛利率 35%，也没有拦截“不能完整判断”这类完整性阻断语。"
            )
        if blocker:
            return "学生回答包含完整性阻断语，但规则评分仍允许关键词命中带来通过。"
        if "rote_repetition" in tags:
            return "学生主要复述课程规则，缺少对当前题干数值或交易事实的迁移应用。"
        return "规则评分只看局部关键词，未校验题干所需的案例计算或因果链是否完整。"

    return "暂无冲突归因。"


def conflict_recommendation(record: dict[str, Any]) -> str:
    conflict_type = str(record.get("failure_type", ""))
    node_id = str(record.get("node_id", ""))

    if conflict_type == "rule_fail_llm_pass" and node_id == "revenue_not_cash_receipt":
        return (
            "在 hidden transfer 案例中为三个要点增加 aliases："
            "“已经赚到这笔业务”映射“赊销可能先确认收入”，"
            "“钱还没进来/现金未必增加”映射“现金不一定增加”，"
            "“客户欠款/先挂应收”映射“应收账款”。"
        )

    if conflict_type == "rule_pass_llm_fail" and node_id == "gross_margin":
        return (
            "把本题评分点改为必答的案例结论：毛利=10000-6500=3500、"
            "毛利率=3500/10000=35%、仍未扣除销售/管理/研发/财务等期间费用；"
            "同时启用 completeness_blocker，出现“不能完整判断”时不得仅凭公式关键词通过。"
        )

    if conflict_type == "rule_fail_llm_pass":
        missing = format_points(record.get("missing_reasoning_points"))
        return f"为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：{missing}"

    if conflict_type == "rule_pass_llm_fail":
        return (
            "将题干中的关键数值、对象或期间判断拆为 required points；"
            "对只复述规则、拒绝迁移判断的回答加入 blocker 或降分。"
        )

    return "无需修改。"


def conflict_sample_lines(
    title: str,
    records: list[dict[str, Any]],
    max_samples: int,
) -> list[str]:
    lines = [f"### {title}"]
    if not records:
        lines.append("")
        lines.append("本次没有样本。")
        lines.append(
            "若后续出现样本，将逐条输出：node_id、condition、student_persona、"
            "question、student_answer、rule_score / judge_score、matched_reasoning_points、"
            "missing_reasoning_points、初步归因、课程或评分规则修改建议。"
        )
        return lines

    for index, record in enumerate(records[:max_samples], start=1):
        lines.append("")
        lines.append(f"{index}. node_id: `{record.get('node_id', '')}`")
        lines.append(f"   condition: `{record.get('condition', '')}`")
        lines.append(f"   student_persona: `{record.get('student_persona', '')}`")
        lines.append(f"   question: {short_text(record.get('question', ''), 360)}")
        lines.append(f"   student_answer: {short_text(record.get('student_answer', ''), 360)}")
        lines.append(
            f"   rule_score / judge_score: {record.get('rule_score')} / {record.get('judge_score')}"
        )
        if record.get("possible_rule_false_fail") or record.get("failure_type") == "rule_fail_llm_pass":
            lines.append("   review_label: possible_rule_false_fail")
        lines.append(
            "   matched_reasoning_points: "
            f"{format_points(record.get('matched_reasoning_points'))}"
        )
        lines.append(
            "   missing_reasoning_points: "
            f"{format_points(record.get('missing_reasoning_points'))}"
        )
        lines.append(f"   初步归因: {conflict_attribution(record)}")
        lines.append(f"   课程或评分规则修改建议: {conflict_recommendation(record)}")
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


NODE_COURSE_DIAGNOSTICS: dict[str, dict[str, Any]] = {
    "gross_margin": {
        "attribution": (
            "expected_reasoning_points 在节点层面只描述公式，未强制本例金额、比例和期间费用三项同时出现；"
            "guiding_questions 没有先让学生列收入和销售成本，也没有追问毛利到净利润之间还要扣什么；"
            "mastery_question 只问“毛利率高不等于净利润高”，太弱，无法暴露只背公式或漏答期间费用。"
        ),
        "guiding_questions": [
            "本例收入是多少？销售成本是多少？请先写出毛利计算式。",
            "毛利率的分母为什么是收入，而不是成本？",
            "毛利和净利润之间还会扣除哪些期间费用？",
        ],
        "mastery_question": (
            "改为要求学生同时写出毛利金额、毛利率、毛利尚未扣除的费用类型，"
            "例如：服装店收入 10000 元、销售成本 6500 元，请计算毛利和毛利率，"
            "并说明毛利距离净利润还少扣哪些费用。"
        ),
        "expected_points": [
            "本例毛利 = 10000 - 6500 = 3500 元",
            "本例毛利率 = 3500 / 10000 = 35%",
            "毛利还没有扣除销售、管理、研发、财务等期间费用",
        ],
        "common_misconceptions": [
            "只写出毛利或毛利率公式，就等于完成案例计算。",
            "算出毛利和毛利率后，就已经得到净利润。",
        ],
        "variant_case": (
            "新增一个餐饮店案例：收入 30000 元、食材直接成本 18000 元、"
            "另有店租和营销费，要求先算毛利和毛利率，再判断哪些费用尚未扣除。"
        ),
    },
    "expense_recognition": {
        "attribution": (
            "引导问题跳过了“员工已经完成本月工作”这一归属期间判断；"
            "mastery_question 只问为什么下月发也可能算本月费用，没有要求同时说明费用发生、未付款和利润影响；"
            "常见误区覆盖了“没付款就没有费用”，但缺少把工资场景拆成利润表和现金变化的练习。"
        ),
        "guiding_questions": [
            "员工本月已经完成工作，这个耗费服务于哪个会计期间？",
            "工资下月支付会不会改变本月费用归属？为什么？",
            "如果本月确认工资费用，本月利润表和现金分别怎样变化？",
        ],
        "mastery_question": (
            "改为给出“本月工作、下月付款”的工资场景，要求学生判断本月是否确认工资费用，"
            "并分别说明费用发生、现金付款时间和本期利润影响。"
        ),
        "expected_points": [
            "员工已完成本月工作，工资耗费服务于本期经营",
            "下月付款不阻止本月确认工资费用",
            "确认工资费用会减少本期利润，但本月现金可能暂不减少",
        ],
        "common_misconceptions": [
            "工资费用只有在实际发现金时才发生。",
            "费用确认只影响现金，不影响利润表期间归属。",
        ],
        "variant_case": (
            "新增一个房租案例：门店本月已使用房屋但下月支付租金，"
            "要求区分费用归属、本月利润影响和现金付款时间。"
        ),
    },
    "depreciation_amortization": {
        "attribution": (
            "前置知识中长期资产和费用的连接不够显性；"
            "guiding_questions 没有强制区分历史购置现金流、本期折旧费用和今年是否再次付款；"
            "mastery_question 偏概念解释，未要求学生把“成本分配、利润减少、非本期现金流出”三点同时写出。"
        ),
        "guiding_questions": [
            "烤箱购买付款发生在哪个期间？今年计提折旧是不是再次付现金？",
            "折旧把哪项长期资产成本分配到哪些受益期间？",
            "今年计提折旧时，利润表费用和资产账面价值分别可能怎样变化？",
        ],
        "mastery_question": (
            "改为给出“去年买烤箱、今年继续使用并计提折旧”的场景，要求学生说明折旧为何减少今年利润，"
            "以及为什么通常不代表今年再次现金流出。"
        ),
        "expected_points": [
            "购买烤箱的现金流通常发生在购置期间",
            "今年折旧是把长期资产成本分配到受益期间",
            "折旧费用减少今年利润，但通常不是今年再次现金流出",
        ],
        "common_misconceptions": [
            "折旧没有现金流出，所以不应进入利润表。",
            "每期折旧等于企业每期重新支付一笔现金。",
        ],
        "variant_case": (
            "新增一个软件摊销案例：去年一次性购买软件，今年按月摊销，"
            "要求判断本期利润、现金和资产账面价值的不同变化。"
        ),
    },
}


def counter_summary(counter: Counter, limit: int = 3) -> str:
    if not counter:
        return "-"
    return "；".join(f"{item}:{count}" for item, count in counter.most_common(limit))


def hidden_pass_rate_text(node: dict[str, Any]) -> str:
    total = int(node["hidden_total"])
    passes = total - int(node["hidden_judge_fail"])
    return f"{passes}/{total} ({pct(passes, total)})"


def hidden_failing_personas_text(node: dict[str, Any]) -> str:
    personas = sorted(
        persona
        for persona, count in node["hidden_failing_personas"].items()
        if count > 0
    )
    return ", ".join(personas) or "-"


def no_course_baseline_fail_text(node: dict[str, Any]) -> str:
    count = int(node.get("no_course_baseline_fail", 0))
    personas = sorted(
        persona
        for persona, fail_count in node.get("no_course_baseline_failing_personas", {}).items()
        if fail_count > 0
    )
    if count <= 0:
        return "0"
    return f"{count} ({', '.join(personas) or '-'})"


def record_missing_points(record: dict[str, Any]) -> list[str]:
    points = record.get("judge_missing_reasoning_points") or record.get("missing_reasoning_points", [])
    return [str(point) for point in points]


def typical_missing_points_text(node: dict[str, Any]) -> str:
    missing = Counter()
    for record in node["hidden_failed_records"]:
        missing.update(record_missing_points(record))
    if not missing:
        missing.update(node["missing_points"])
    return counter_summary(missing, 3)


def typical_answer_snippets_text(node: dict[str, Any]) -> str:
    snippets = []
    seen_personas = set()
    for record in node["hidden_failed_records"]:
        persona = str(record.get("student_persona", ""))
        if persona in seen_personas:
            continue
        seen_personas.add(persona)
        snippets.append(f"{persona}: {short_text(record.get('student_answer', ''), 120)}")
        if len(snippets) >= 2:
            break
    return "；".join(snippets) or "-"


def revenue_not_cash_receipt_course_suggestion_lines(node: dict[str, Any], rank: int) -> list[str]:
    node_id = str(node["node_id"])
    node_label = f"`{node_id}` {node.get('node_title', '')}".strip()
    lines = ["", f"### {rank}. {node_label}"]
    lines.append(
        "- 问题证据: "
        f"hidden_transfer 通过率 {hidden_pass_rate_text(node)}；"
        f"失败 persona: {hidden_failing_personas_text(node)}；"
        f"top_tags: {counter_summary(node['tags'], 3)}；"
        f"false_fail_count: {node['false_fail']}；"
        f"no_course_baseline_fail: {no_course_baseline_fail_text(node)}；"
        f"典型 missing_reasoning_points: {typical_missing_points_text(node)}；"
        f"典型学生回答片段: {typical_answer_snippets_text(node)}"
    )

    tags = set(str(tag) for tag in node["tags"])
    missing_points = node["missing_points"]
    suggestion_count = 0

    if "revenue_cash_confusion" in tags:
        lines.append(
            "- 课程强化: 强化“收入确认”和“现金收款”的对照，并加入典型误解提醒："
            "“没收到钱不代表不能确认收入；收入增加也不代表现金同步增加。”"
        )
        suggestion_count += 1

    if "rote_repetition" in tags:
        lines.append(
            "- 新增 guiding_question: 商品已经卖出、客户尚未付款、利润表收入、现金变化分别对应什么？"
        )
        suggestion_count += 1

    if int(node["false_fail"]) > 0:
        lines.append(
            "- 评分规则建议: 补充 rule aliases："
            "“现金要等到客户付款时才增加”、"
            "“现金不变”、"
            "“现金还没进来”、"
            "“收入确认不一定等于收到现金”、"
            "“客户后续付款”、"
            "“赊销导致现金流入延后”。"
        )
        suggestion_count += 1

    if missing_points.get("可能形成应收账款而不是现金流入", 0) > 0:
        lines.append(
            "- 课程材料补充: 显式加入“赊销形成应收账款，不是当期现金流入。”"
        )
        suggestion_count += 1

    if int(node.get("no_course_baseline_fail", 0)) > 0:
        lines.append(
            "- baseline 解读: no_course_baseline 下封闭学生答不出是预期行为，"
            "用于验证学生不会在没有材料时外推；不应直接视为课程失败。"
        )
        suggestion_count += 1

    if suggestion_count == 0:
        lines.append(
            "- 通用建议: 用“利润表收入 / 现金变化 / 应收账款”三列表格呈现赊销，"
            "要求学生逐格说明商品交付、客户未付款和后续收款分别影响什么。"
        )
    return lines


def course_suggestion_lines(node: dict[str, Any], rank: int) -> list[str]:
    node_id = str(node["node_id"])
    if node_id == "revenue_not_cash_receipt":
        return revenue_not_cash_receipt_course_suggestion_lines(node, rank)

    diagnostic = NODE_COURSE_DIAGNOSTICS.get(node_id)
    if diagnostic is None:
        return []

    node_label = f"`{node_id}` {node.get('node_title', '')}".strip()
    lines = ["", f"### {rank}. {node_label}"]
    lines.append(
        "- 问题证据: "
        f"hidden_transfer 通过率 {hidden_pass_rate_text(node)}；"
        f"失败 persona: {hidden_failing_personas_text(node)}；"
        f"top_tags: {counter_summary(node['tags'], 3)}；"
        f"典型 missing_reasoning_points: {typical_missing_points_text(node)}；"
        f"典型学生回答片段: {typical_answer_snippets_text(node)}"
    )
    lines.append(f"- 问题归因: {diagnostic['attribution']}")
    for question in diagnostic["guiding_questions"]:
        lines.append(f"- 新增 guiding_question: {question}")
    lines.append(f"- 修改 mastery_question 的具体方向: {diagnostic['mastery_question']}")
    for point in diagnostic["expected_points"]:
        lines.append(f"- 修改 expected_reasoning_points: {point}")
    for misconception in diagnostic["common_misconceptions"]:
        lines.append(f"- 增加 common_misconceptions: {misconception}")
    lines.append(f"- 新增变式案例: {diagnostic['variant_case']}")
    return lines


def course_suggestions(ranked_nodes: list[dict[str, Any]]) -> list[str]:
    lines = ["## 课程修改建议"]
    if not ranked_nodes:
        lines.append("")
        lines.append("暂无建议。")
        return lines
    lines.append("")
    lines.append("以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。")

    detailed_count = 0
    for node in ranked_nodes:
        if risk_score(node) <= 0:
            continue
        suggestion_lines = course_suggestion_lines(node, detailed_count + 1)
        if not suggestion_lines:
            continue
        lines.extend(suggestion_lines)
        detailed_count += 1
        if detailed_count >= 3:
            break

    if detailed_count == 0:
        lines.append("")
        lines.append("当前没有触发自动课程修改建议；请结合上方冲突样本人工抽查。")
    return lines


def report_mode_note(config: dict[str, Any]) -> str:
    if bool(config.get("mock_mode", True)):
        return "mock judge 仅用于验证数据流和报告结构，不等价于真实语义评分。"
    return "本报告使用真实 LLM judge，但仍需人工抽查关键冲突样本。"


def generate_report(
    config_path: str | None = None,
    overrides: dict[str, Any] | None = None,
) -> Path:
    config = load_config(config_path, overrides)
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

    lines.extend(["", "## 评分冲突样本", ""])
    lines.append("")
    lines.extend(
        conflict_sample_lines(
            "rule_fail_llm_pass",
            false_fails,
            max_samples,
        )
    )
    lines.append("")
    lines.extend(
        conflict_sample_lines(
            "rule_pass_llm_fail",
            false_passes,
            max_samples,
        )
    )

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
            f"- {report_mode_note(config)}",
            "- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。",
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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--mock-mode", action="store_true", help="Use mock output directory defaults.")
    mode.add_argument("--real-mode", action="store_true", help="Use real output directory defaults.")
    parser.add_argument("--output-dir", help="Directory containing judge_results.jsonl.")
    return parser.parse_args()


def args_to_overrides(args: argparse.Namespace) -> dict[str, Any]:
    mock_mode = None
    if args.mock_mode:
        mock_mode = True
    if args.real_mode:
        mock_mode = False
    return {
        "mock_mode": mock_mode,
        "output_dir": args.output_dir,
    }


def main() -> None:
    args = parse_args()
    path = generate_report(args.config, args_to_overrides(args))
    print(f"Wrote failure report: {path}")


if __name__ == "__main__":
    main()
