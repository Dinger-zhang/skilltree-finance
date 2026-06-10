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
    OpenAICompatibleClient,
    complete_output_fields,
    deterministic_run_id,
    load_config,
    load_graph,
    load_personas,
    load_transfer_cases,
    materials_for_condition,
    now_iso,
    output_path,
    parse_json_object,
    select_chain_nodes,
    transfer_case_for_node,
    write_jsonl,
)


MOCK_STUDENT_MODEL = "mock_student_v0_3"
MOCK_JUDGE_MODEL = "mock_judge_v0_3"


def answer_from_points(points: list[str], prefix: str = "") -> str:
    if not points:
        return prefix + "无法从当前材料推出。"
    return prefix + "；".join(points) + "。"


def misconception_answer(node: dict[str, Any], condition: str) -> tuple[str, list[str]]:
    node_id = node["id"]
    if node_id in {"revenue_recognition", "revenue_not_cash_receipt"}:
        return (
            "我认为收到现金才算收入，没收到现金就没有收入，所以收入就是收款。",
            ["revenue_cash_confusion"],
        )
    if node_id in {"net_profit", "accrual_vs_cash"}:
        return (
            "净利润为正就说明不缺钱，赚钱就是现金增加，现金制和权责发生制差别不大。",
            ["profit_cash_confusion"],
        )
    if node_id in {"expense_recognition"}:
        return (
            "费用就是付款，没付款就没有费用，所以工资下月发就只能下月算费用。",
            ["expense_payment_confusion"],
        )
    if node_id in {"depreciation_amortization"}:
        return (
            "折旧就是每月重新付款；如果没有付款，折旧也不影响利润。",
            ["depreciation_payment_confusion"],
        )
    if node_id in {"gross_margin"}:
        return (
            "毛利率就是净利率，毛利高就一定净利润高。",
            ["gross_net_confusion"],
        )
    if condition == "hidden_transfer":
        return (
            "我会直接看现金有没有变化，所有现金流入都可以理解成收入。",
            ["revenue_cash_confusion"],
        )
    return (
        "我把这类交易都看成现金变化，不太区分利润表和现金流。",
        ["profit_cash_confusion"],
    )


def mock_student_response(
    persona: dict[str, Any],
    node: dict[str, Any],
    condition: str,
    expected_points: list[str],
) -> dict[str, Any]:
    persona_id = persona["id"]

    if persona_id == "novice_closed_book":
        if condition == "no_course_baseline":
            answer = "无法从当前材料推出。"
        elif condition == "hidden_transfer" and node["id"] == "revenue_not_cash_receipt":
            answer = "这月已经赚到这笔业务，但钱还没进来，客户欠款会先挂着，所以现金未必增加。"
        elif condition == "hidden_transfer":
            covered = expected_points[: max(1, len(expected_points) - 1)]
            answer = answer_from_points(covered, "根据已经给出的材料，我能推出：")
        else:
            answer = answer_from_points(expected_points, "根据当前材料，我的推理是：")
        return {
            "student_answer": answer,
            "external_knowledge_suspicion": False,
            "misconception_tags": [],
        }

    if persona_id == "rote_memorizer":
        if condition == "no_course_baseline":
            answer = "没有可背的材料，我无法从当前材料推出。"
        elif condition == "hidden_transfer":
            answer = (
                f"规则说：{node['rule_summary']}。照规则说，我只需要背规则，"
                "但这个新案例我不能完整判断。"
            )
        else:
            answer = f"规则说：{node['rule_summary']}。所以答案就是把规则复述出来。"
        return {
            "student_answer": answer,
            "external_knowledge_suspicion": False,
            "misconception_tags": ["rote_repetition"] if condition != "no_course_baseline" else [],
        }

    if persona_id == "misconception_prone":
        answer, tags = misconception_answer(node, condition)
        return {
            "student_answer": answer,
            "external_knowledge_suspicion": False,
            "misconception_tags": tags,
        }

    if condition == "no_course_baseline":
        answer = "无法从当前材料推出。"
    else:
        answer = answer_from_points(expected_points[:1], "我只能说：")
    return {
        "student_answer": answer,
        "external_knowledge_suspicion": False,
        "misconception_tags": [],
    }


def llm_student_response(
    client: OpenAICompatibleClient,
    persona: dict[str, Any],
    condition: str,
    question: str,
    materials: list[dict[str, Any]],
    prompt_path: Path,
) -> dict[str, Any]:
    system_prompt = prompt_path.read_text(encoding="utf-8")
    user_payload = {
        "persona": persona,
        "condition": condition,
        "question": question,
        "course_materials": materials,
        "output_contract": {
            "student_answer": "string",
            "used_node_ids": ["node_id"],
            "external_knowledge_suspicion": False,
            "misconception_tags": ["string"],
        },
    }
    raw = client.chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
        json_mode=True,
    )
    parsed = parse_json_object(raw)
    return {
        "student_answer": str(parsed.get("student_answer", "")),
        "used_node_ids": parsed.get("used_node_ids", []),
        "external_knowledge_suspicion": bool(parsed.get("external_knowledge_suspicion", False)),
        "misconception_tags": parsed.get("misconception_tags", []),
    }


def build_question_and_expectations(
    node: dict[str, Any],
    condition: str,
    cases_by_node: dict[str, list[dict[str, Any]]],
) -> tuple[str, list[str], list[str], str]:
    if condition == "hidden_transfer":
        case = transfer_case_for_node(node, cases_by_node)
        question = f"{case.get('case', '')}\n{case.get('question', '')}".strip()
        expected_points = [str(point) for point in case.get("expected_reasoning_points", [])]
        traps = [str(trap) for trap in case.get("misconception_traps", [])]
        return question, expected_points, traps, str(case.get("id", ""))
    return (
        str(node.get("mastery_question", node.get("core_question", ""))),
        [str(point) for point in node.get("expected_reasoning_points", [])],
        [str(item) for item in node.get("common_misconceptions", [])],
        "",
    )


def run_simulation(config_path: str | None = None) -> Path:
    config = load_config(config_path)
    graph_nodes, graph_version_value = load_graph(config["graph_path"])
    chain_nodes, fallback_used = select_chain_nodes(
        graph_nodes,
        config["chain_id"],
        bool(config.get("allow_graph_fallback", True)),
    )
    files = config.get("files", {})
    personas = load_personas(files.get("personas", "experiments/synthetic_student_lab/personas.yaml"))
    cases_by_node = load_transfer_cases(
        files.get("transfer_cases", "experiments/synthetic_student_lab/transfer_cases.yaml")
    )
    conditions = [str(condition) for condition in config.get("conditions", [])]
    mock_mode = bool(config.get("mock_mode", True))

    student_settings = config.get("student_client", {})
    student_client_enabled = bool(student_settings.get("enabled", False)) and not mock_mode
    student_model = (
        str(student_settings.get("model"))
        if student_client_enabled
        else MOCK_STUDENT_MODEL
    )
    judge_settings = config.get("judge_client", {})
    judge_model = (
        str(judge_settings.get("model"))
        if bool(judge_settings.get("enabled", False)) and not mock_mode
        else MOCK_JUDGE_MODEL
    )
    student_client = OpenAICompatibleClient(student_settings) if student_client_enabled else None
    prompt_path = CURRENT_DIR / "prompts" / "student_prompt.md"

    records: list[dict[str, Any]] = []
    experiment_id = str(config.get("experiment_id", "ssl_v0_3_minimal"))
    created_at = now_iso()

    for persona in personas:
        persona_id = str(persona["id"])
        for node_index, node in enumerate(chain_nodes):
            for condition in conditions:
                materials, allowed_used_node_ids = materials_for_condition(
                    chain_nodes,
                    node_index,
                    condition,
                )
                question, expected_points, traps, case_id = build_question_and_expectations(
                    node,
                    condition,
                    cases_by_node,
                )
                run_id = deterministic_run_id(
                    experiment_id,
                    graph_version_value,
                    persona_id,
                    node["id"],
                    condition,
                )
                error_message = ""
                if student_client:
                    try:
                        response = llm_student_response(
                            student_client,
                            persona,
                            condition,
                            question,
                            materials,
                            prompt_path,
                        )
                    except Exception as exc:  # noqa: BLE001 - recorded in experiment output.
                        response = {
                            "student_answer": "",
                            "used_node_ids": [],
                            "external_knowledge_suspicion": False,
                            "misconception_tags": [],
                        }
                        error_message = f"student_llm_error: {exc}"
                else:
                    response = mock_student_response(persona, node, condition, expected_points)

                used_node_ids = response.get("used_node_ids", allowed_used_node_ids)
                if not isinstance(used_node_ids, list):
                    used_node_ids = allowed_used_node_ids
                if not student_client:
                    used_node_ids = allowed_used_node_ids
                else:
                    allowed = set(allowed_used_node_ids)
                    used_node_ids = [str(node_id) for node_id in used_node_ids if str(node_id) in allowed]

                record = complete_output_fields(
                    {
                        "run_id": run_id,
                        "graph_version": graph_version_value,
                        "chain_id": config["chain_id"],
                        "node_id": node["id"],
                        "node_title": node["title"],
                        "condition": condition,
                        "student_persona": persona_id,
                        "student_model": student_model,
                        "judge_model": judge_model,
                        "question": question,
                        "student_answer": str(response.get("student_answer", "")),
                        "used_node_ids": used_node_ids,
                        "expected_reasoning_points": expected_points,
                        "misconception_traps": traps,
                        "misconception_tags": response.get("misconception_tags", []),
                        "external_knowledge_suspicion": bool(
                            response.get("external_knowledge_suspicion", False)
                        ),
                        "case_id": case_id,
                        "graph_fallback_used": fallback_used,
                        "error_message": error_message,
                        "created_at": created_at,
                    }
                )
                records.append(record)

    simulation_path = output_path(config, "simulation_runs")
    write_jsonl(simulation_path, records)
    return simulation_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Synthetic Student Lab simulations.")
    parser.add_argument(
        "--config",
        default=str(CURRENT_DIR / "config.yaml"),
        help="Path to config.yaml",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = run_simulation(args.config)
    print(f"Wrote simulation runs: {path}")


if __name__ == "__main__":
    main()
