from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from common import (  # noqa: E402
    LLMParseError,
    OpenAICompatibleClient,
    complete_output_fields,
    evaluate_rule,
    load_config,
    load_graph,
    load_personas,
    load_transfer_cases,
    materials_for_condition,
    now_iso,
    read_jsonl,
    select_chain_nodes,
    write_jsonl,
)
from judge import (  # noqa: E402
    compute_conflict_type,
    llm_judge_response,
    safe_list,
    safe_point_list,
)
from run_simulation import build_question_and_expectations, llm_student_response  # noqa: E402


DEFAULT_SOURCE_DIR = CURRENT_DIR / "outputs" / "ssl_v0_3_real_b_chain_001"
DEFAULT_TARGET_DIR = CURRENT_DIR / "outputs" / "ssl_v0_3_real_b_chain_001_repaired"
MAX_RETRIES = 3


def first_model(records: list[dict[str, Any]], field: str, fallback: str) -> str:
    for record in records:
        value = str(record.get(field, "")).strip()
        if value and not value.startswith("mock_"):
            return value
    return fallback


def is_bad_record(record: dict[str, Any]) -> bool:
    return (
        bool(str(record.get("error_message", "")).strip())
        or not str(record.get("student_answer", "")).strip()
        or bool(str(record.get("student_parse_error", "")).strip())
        or bool(str(record.get("judge_parse_error", "")).strip())
    )


def needs_student_retry(record: dict[str, Any]) -> bool:
    return not str(record.get("student_answer", "")).strip()


def sanitize_used_node_ids(value: Any, allowed_used_node_ids: list[str]) -> list[str]:
    if not isinstance(value, list):
        return allowed_used_node_ids
    allowed = set(allowed_used_node_ids)
    return [str(node_id) for node_id in value if str(node_id) in allowed]


class RepairContext:
    def __init__(
        self,
        config: dict[str, Any],
        simulation_records: list[dict[str, Any]],
    ) -> None:
        self.config = config
        self.pass_ratio = float(config.get("pass_ratio", 0.6))
        graph_nodes, _graph_version_value = load_graph(config["graph_path"])
        files = config.get("files", {})
        self.chain_nodes, self.fallback_used = select_chain_nodes(
            graph_nodes,
            config["chain_id"],
            bool(config.get("allow_graph_fallback", True)),
            files.get("chain_definitions", config.get("chain_definitions_path", "data/chain_definitions.yaml")),
        )
        self.node_index_by_id = {
            str(node.get("id", "")): index
            for index, node in enumerate(self.chain_nodes)
        }
        self.personas_by_id = {
            str(persona.get("id", "")): persona
            for persona in load_personas(files.get("personas", "experiments/synthetic_student_lab/personas.yaml"))
        }
        self.cases_by_node = load_transfer_cases(
            files.get("transfer_cases", "experiments/synthetic_student_lab/transfer_cases.yaml")
        )
        self.student_model = first_model(
            simulation_records,
            "student_model",
            str(config.get("student_client", {}).get("model", "")),
        )
        self.judge_model = first_model(
            simulation_records,
            "judge_model",
            str(config.get("judge_client", {}).get("model", "")),
        )
        self.config.setdefault("student_client", {})["model"] = self.student_model
        self.config.setdefault("student_client", {})["enabled"] = True
        self.config.setdefault("judge_client", {})["model"] = self.judge_model
        self.config.setdefault("judge_client", {})["enabled"] = True
        self.student_client = OpenAICompatibleClient(self.config["student_client"])
        self.judge_client = OpenAICompatibleClient(self.config["judge_client"])
        self.student_prompt_path = CURRENT_DIR / "prompts" / "student_prompt.md"
        self.judge_prompt_path = CURRENT_DIR / "prompts" / "judge_prompt.md"

    def record_inputs(self, record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], str, list[dict[str, Any]], list[str], list[Any], list[str], str]:
        node_id = str(record.get("node_id", ""))
        if node_id not in self.node_index_by_id:
            raise ValueError(f"node_id not found in chain: {node_id}")
        node_index = self.node_index_by_id[node_id]
        node = self.chain_nodes[node_index]
        persona_id = str(record.get("student_persona", ""))
        if persona_id not in self.personas_by_id:
            raise ValueError(f"persona not found: {persona_id}")
        condition = str(record.get("condition", ""))
        materials, allowed_used_node_ids = materials_for_condition(
            self.chain_nodes,
            node_index,
            condition,
        )
        question, expected_points, traps, case_id = build_question_and_expectations(
            node,
            condition,
            self.cases_by_node,
        )
        return (
            node,
            self.personas_by_id[persona_id],
            question,
            materials,
            allowed_used_node_ids,
            expected_points,
            traps,
            case_id,
        )


def rerun_student_once(
    context: RepairContext,
    original_record: dict[str, Any],
) -> dict[str, Any]:
    (
        node,
        persona,
        question,
        materials,
        allowed_used_node_ids,
        expected_points,
        traps,
        case_id,
    ) = context.record_inputs(original_record)
    response = llm_student_response(
        context.student_client,
        persona,
        str(original_record.get("condition", "")),
        question,
        materials,
        context.student_prompt_path,
    )
    used_node_ids = sanitize_used_node_ids(response.get("used_node_ids", []), allowed_used_node_ids)
    repaired = {
        **original_record,
        "node_title": node.get("title", original_record.get("node_title", "")),
        "student_model": context.student_model,
        "judge_model": context.judge_model,
        "question": question,
        "student_answer": str(response.get("student_answer", "")),
        "student_request_id": str(response.get("student_request_id", "")),
        "student_raw_response": str(response.get("student_raw_response", "")),
        "student_parse_error": str(response.get("student_parse_error", "")),
        "used_node_ids": used_node_ids,
        "expected_reasoning_points": expected_points,
        "misconception_traps": traps,
        "misconception_tags": response.get("misconception_tags", []),
        "evidence_status": str(response.get("evidence_status", "")),
        "persona_behavior_trace": str(response.get("persona_behavior_trace", "")),
        "external_knowledge_suspicion": bool(response.get("external_knowledge_suspicion", False)),
        "case_id": case_id,
        "graph_fallback_used": context.fallback_used,
        "error_message": "",
        "repaired_at": now_iso(),
        "repair_action": "student_then_judge",
        "failed_after_retries": False,
    }
    return complete_output_fields(repaired)


def judge_record_once(
    context: RepairContext,
    simulation_record: dict[str, Any],
) -> dict[str, Any]:
    expected_points = safe_point_list(simulation_record.get("expected_reasoning_points"))
    rule_result = evaluate_rule(
        str(simulation_record.get("student_answer", "")),
        expected_points,
        context.pass_ratio,
    )
    completion = llm_judge_response(
        context.judge_client,
        simulation_record,
        context.pass_ratio,
        context.judge_prompt_path,
    )
    combined_tags = sorted(
        set(safe_list(simulation_record.get("misconception_tags")))
        | set(safe_list(completion.get("misconception_tags")))
    )
    external_suspicion = bool(simulation_record.get("external_knowledge_suspicion")) or bool(
        completion.get("external_knowledge_suspicion")
    )
    conflict_type = compute_conflict_type(
        bool(rule_result.get("rule_passed", False)),
        bool(completion.get("judge_passed", False)),
    )
    return complete_output_fields(
        {
            **simulation_record,
            "judge_model": context.judge_model,
            "rule_score": rule_result["rule_score"],
            "rule_passed": rule_result["rule_passed"],
            "rule_required_missing_reasoning_points": rule_result["required_missing_reasoning_points"],
            "rule_completeness_blocker": rule_result["completeness_blocker"],
            "rule_failure_reason": rule_result["rule_failure_reason"],
            "rule_score_detail": rule_result["rule_score_detail"],
            "judge_score": completion["judge_score"],
            "judge_passed": completion["judge_passed"],
            "judge_request_id": str(completion.get("judge_request_id", "")),
            "judge_raw_response": str(completion.get("judge_raw_response", "")),
            "judge_parse_error": str(completion.get("judge_parse_error", "")),
            "matched_reasoning_points": rule_result["matched_reasoning_points"],
            "missing_reasoning_points": rule_result["missing_reasoning_points"],
            "judge_matched_reasoning_points": completion["matched_reasoning_points"],
            "judge_missing_reasoning_points": completion["missing_reasoning_points"],
            "misconception_tags": combined_tags,
            "external_knowledge_suspicion": external_suspicion,
            "conflict_type": conflict_type,
            "failure_type": conflict_type,
            "possible_rule_false_fail": conflict_type == "rule_fail_llm_pass",
            "judge_failure_reason": completion.get("failure_reason", ""),
            "error_message": "",
            "repaired_at": now_iso(),
            "failed_after_retries": False,
        }
    )


def mark_student_failed(
    record: dict[str, Any],
    retry_count: int,
    error_message: str,
) -> dict[str, Any]:
    return complete_output_fields(
        {
            **record,
            "student_retry_count": retry_count,
            "retry_count": retry_count,
            "failed_after_retries": True,
            "repair_action": "student_then_judge",
            "repair_error_message": error_message,
            "error_message": f"student_repair_failed_after_retries: {error_message}",
            "repaired_at": now_iso(),
        }
    )


def mark_judge_failed(
    context: RepairContext,
    simulation_record: dict[str, Any],
    original_judge_record: dict[str, Any],
    retry_count: int,
    error_message: str,
    repair_action: str,
) -> dict[str, Any]:
    expected_points = safe_point_list(simulation_record.get("expected_reasoning_points"))
    rule_result = evaluate_rule(
        str(simulation_record.get("student_answer", "")),
        expected_points,
        context.pass_ratio,
    )
    conflict_type = compute_conflict_type(bool(rule_result.get("rule_passed", False)), False)
    return complete_output_fields(
        {
            **original_judge_record,
            **simulation_record,
            "judge_model": context.judge_model,
            "rule_score": rule_result["rule_score"],
            "rule_passed": rule_result["rule_passed"],
            "rule_required_missing_reasoning_points": rule_result["required_missing_reasoning_points"],
            "rule_completeness_blocker": rule_result["completeness_blocker"],
            "rule_failure_reason": rule_result["rule_failure_reason"],
            "rule_score_detail": rule_result["rule_score_detail"],
            "judge_score": 0.0,
            "judge_passed": False,
            "judge_raw_response": "",
            "judge_parse_error": "",
            "judge_matched_reasoning_points": [],
            "judge_missing_reasoning_points": expected_points,
            "conflict_type": conflict_type,
            "failure_type": conflict_type,
            "judge_failure_reason": "judge_repair_failed_after_retries",
            "judge_retry_count": retry_count,
            "retry_count": retry_count,
            "failed_after_retries": True,
            "repair_action": repair_action,
            "repair_error_message": error_message,
            "error_message": f"judge_repair_failed_after_retries: {error_message}",
            "repaired_at": now_iso(),
        }
    )


def retry_call(action: str, run_id: str, log_lines: list[str], func: Any) -> tuple[dict[str, Any] | None, int, str]:
    last_error = ""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = func()
            log_lines.append(f"  - {action} attempt {attempt}: success")
            return result, attempt, ""
        except (LLMParseError, RuntimeError, TimeoutError, ValueError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            log_lines.append(f"  - {action} attempt {attempt}: failed: {last_error}")
        except Exception as exc:  # noqa: BLE001 - repair log must preserve unexpected failures.
            last_error = f"{type(exc).__name__}: {exc}"
            log_lines.append(f"  - {action} attempt {attempt}: failed: {last_error}")
    log_lines.append(f"  - {action}: failed_after_retries for `{run_id}`")
    return None, MAX_RETRIES, last_error


def args_to_overrides(args: argparse.Namespace) -> dict[str, Any]:
    overrides: dict[str, Any] = {
        "mock_mode": False,
        "output_dir": str(args.target_dir),
    }
    for key in (
        "student_model",
        "judge_model",
        "student_api_key_env",
        "student_base_url_env",
        "judge_api_key_env",
        "judge_base_url_env",
    ):
        value = getattr(args, key)
        if value:
            overrides[key] = value
    return overrides


def repair_records(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    source_dir = Path(args.source_dir)
    target_dir = Path(args.target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    simulation_path = source_dir / "simulation_runs.jsonl"
    judge_path = source_dir / "judge_results.jsonl"
    simulation_records = read_jsonl(simulation_path)
    judge_records = read_jsonl(judge_path)
    simulation_by_run_id = {str(record.get("run_id", "")): dict(record) for record in simulation_records}
    judge_by_run_id = {str(record.get("run_id", "")): dict(record) for record in judge_records}

    merged_by_run_id = {
        run_id: {**simulation_by_run_id.get(run_id, {}), **judge_by_run_id.get(run_id, {})}
        for run_id in sorted(set(simulation_by_run_id) | set(judge_by_run_id))
    }
    bad_run_ids = [
        run_id
        for run_id, record in merged_by_run_id.items()
        if is_bad_record(record)
    ]

    config = load_config(args.config, args_to_overrides(args))
    context = RepairContext(config, simulation_records)

    repaired_simulation_by_run_id = {run_id: dict(record) for run_id, record in simulation_by_run_id.items()}
    repaired_judge_by_run_id = {run_id: dict(record) for run_id, record in judge_by_run_id.items()}

    log_lines = [
        "# Synthetic Student Lab Bad Record Repair Log",
        "",
        f"- source_dir: `{source_dir}`",
        f"- target_dir: `{target_dir}`",
        f"- total_simulation_records: {len(simulation_records)}",
        f"- total_judge_records: {len(judge_records)}",
        f"- bad_run_ids: {len(bad_run_ids)}",
        f"- max_retries_per_step: {MAX_RETRIES}",
        f"- student_model: `{context.student_model}`",
        f"- judge_model: `{context.judge_model}`",
        "",
    ]

    for run_id in bad_run_ids:
        original_simulation = repaired_simulation_by_run_id.get(run_id, {})
        original_judge = repaired_judge_by_run_id.get(run_id, {})
        merged = {**original_simulation, **original_judge}
        repair_action = "student_then_judge" if needs_student_retry(merged) else "judge_only"
        log_lines.extend(
            [
                f"## `{run_id}`",
                f"- node_id: `{merged.get('node_id', '')}`",
                f"- condition: `{merged.get('condition', '')}`",
                f"- student_persona: `{merged.get('student_persona', '')}`",
                f"- original_error_message: {merged.get('error_message', '')}",
                f"- action: {repair_action}",
            ]
        )

        simulation_for_judge = dict(original_simulation)
        if repair_action == "student_then_judge":
            student_result, retry_count, error_message = retry_call(
                "student",
                run_id,
                log_lines,
                lambda record=original_simulation: rerun_student_once(context, record),
            )
            if student_result is None:
                failed_simulation = mark_student_failed(original_simulation, retry_count, error_message)
                repaired_simulation_by_run_id[run_id] = failed_simulation
                repaired_judge_by_run_id[run_id] = mark_judge_failed(
                    context,
                    failed_simulation,
                    original_judge,
                    0,
                    "student retry failed; judge retry skipped",
                    repair_action,
                )
                log_lines.append("")
                continue
            student_result["student_retry_count"] = retry_count
            student_result["retry_count"] = retry_count
            repaired_simulation_by_run_id[run_id] = student_result
            simulation_for_judge = student_result
        else:
            simulation_for_judge = {
                **simulation_for_judge,
                "error_message": "",
                "repair_action": repair_action,
                "failed_after_retries": False,
                "repaired_at": now_iso(),
            }
            repaired_simulation_by_run_id[run_id] = complete_output_fields(simulation_for_judge)

        judge_result, retry_count, error_message = retry_call(
            "judge",
            run_id,
            log_lines,
            lambda record=simulation_for_judge: judge_record_once(context, record),
        )
        if judge_result is None:
            repaired_judge_by_run_id[run_id] = mark_judge_failed(
                context,
                simulation_for_judge,
                original_judge,
                retry_count,
                error_message,
                repair_action,
            )
        else:
            judge_result["judge_retry_count"] = retry_count
            judge_result["retry_count"] = retry_count
            judge_result["repair_action"] = repair_action
            repaired_judge_by_run_id[run_id] = complete_output_fields(judge_result)
        log_lines.append("")

    repaired_simulation_records = [
        repaired_simulation_by_run_id[str(record.get("run_id", ""))]
        for record in simulation_records
    ]
    repaired_judge_records = [
        repaired_judge_by_run_id[str(record.get("run_id", ""))]
        for record in judge_records
    ]
    log_lines.extend(
        [
            "## Summary",
            f"- output_simulation_records: {len(repaired_simulation_records)}",
            f"- output_judge_records: {len(repaired_judge_records)}",
            f"- repaired_run_ids: {', '.join(bad_run_ids) if bad_run_ids else '-'}",
            f"- failed_after_retries_count: {sum(1 for record in repaired_judge_records if record.get('failed_after_retries'))}",
        ]
    )

    target_simulation_path = target_dir / "simulation_runs.jsonl"
    target_judge_path = target_dir / "judge_results.jsonl"
    repair_log_path = target_dir / "repair_log.md"
    write_jsonl(target_simulation_path, repaired_simulation_records)
    write_jsonl(target_judge_path, repaired_judge_records)
    repair_log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return target_simulation_path, target_judge_path, repair_log_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair bad Synthetic Student Lab records with targeted retries.")
    parser.add_argument("--config", default=str(CURRENT_DIR / "config.yaml"))
    parser.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    parser.add_argument("--target-dir", default=str(DEFAULT_TARGET_DIR))
    parser.add_argument("--student-model")
    parser.add_argument("--judge-model")
    parser.add_argument("--student-api-key-env")
    parser.add_argument("--student-base-url-env")
    parser.add_argument("--judge-api-key-env")
    parser.add_argument("--judge-base-url-env")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    simulation_path, judge_path, repair_log_path = repair_records(args)
    print(f"Wrote repaired simulation runs: {simulation_path}")
    print(f"Wrote repaired judge results: {judge_path}")
    print(f"Wrote repair log: {repair_log_path}")


if __name__ == "__main__":
    main()
