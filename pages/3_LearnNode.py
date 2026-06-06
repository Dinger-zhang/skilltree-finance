from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import database as db
from src import diagnosis
from src import knowledge_graph as kg


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "skilltree_finance.sqlite3"


@st.cache_resource
def get_connection() -> Any:
    conn = db.connect(DB_PATH)
    db.init_db(conn)
    return conn


@st.cache_data
def get_nodes() -> list[dict[str, Any]]:
    return kg.load_knowledge_graph(DATA_DIR / "knowledge_graph.yaml")


def register_student_sidebar(conn: Any) -> Optional[int]:
    st.sidebar.header("学生信息")

    current_id = st.session_state.get("student_id")
    if current_id:
        student = db.get_student(conn, int(current_id))
        if student:
            st.sidebar.write(f"当前学生：{student['name']}")
            if student["student_code"]:
                st.sidebar.caption(f"学号：{student['student_code']}")
            if student["class_name"]:
                st.sidebar.caption(f"班级：{student['class_name']}")

        if st.sidebar.button("切换学生"):
            st.session_state.pop("student_id", None)
            st.session_state.pop("learn_start_time", None)
            st.session_state.pop("learn_active_node", None)
            st.rerun()
        return int(current_id)

    with st.sidebar.form("student_form"):
        name = st.text_input("姓名 *")
        student_code = st.text_input("学号（可选）")
        class_name = st.text_input("班级（可选）")
        submitted = st.form_submit_button("进入学习")

    if submitted:
        if not name.strip():
            st.sidebar.error("请先填写姓名。")
            return None

        student_id = db.get_or_create_student(conn, name, student_code, class_name)
        st.session_state["student_id"] = student_id
        db.log_event(conn, student_id, "student_enter", detail="进入节点学习页面")
        st.rerun()

    return None


def node_label(node: dict[str, Any], statuses: dict[str, str]) -> str:
    return f"L{node['level']} | {kg.status_label(statuses.get(node['id']))} | {node['title']}"


def get_statuses(
    conn: Any,
    student_id: Optional[int],
    nodes: list[dict[str, Any]],
) -> dict[str, str]:
    if student_id is None:
        return kg.default_statuses(nodes)

    db.ensure_node_statuses(conn, student_id, nodes)
    stored = db.get_node_statuses(conn, student_id)
    return {node["id"]: kg.normalize_status(stored.get(node["id"])) for node in nodes}


def ensure_learning_timer(node_id: str) -> None:
    if st.session_state.get("learn_active_node") != node_id:
        st.session_state["learn_active_node"] = node_id
        st.session_state["learn_start_time"] = time.time()
    elif "learn_start_time" not in st.session_state:
        st.session_state["learn_start_time"] = time.time()


def elapsed_seconds() -> int:
    started_at = float(st.session_state.get("learn_start_time", time.time()))
    return max(int(time.time() - started_at), 0)


def render_list_items(title: str, items: list[Any]) -> None:
    st.markdown(f"**{title}**")
    if not items:
        st.write("暂无。")
        return

    for item in items:
        if isinstance(item, dict) and ("misconception" in item or "correction" in item):
            st.write(f"- 误区：{item.get('misconception', '')}")
            st.caption(f"纠正：{item.get('correction', '')}")
        elif isinstance(item, dict) and ("prompt" in item or "answer" in item):
            st.write(f"- 题目：{item.get('prompt', '')}")
            st.caption(f"参考答案：{item.get('answer', '')}")
        elif isinstance(item, dict) and ("question" in item or "answer" in item):
            st.write(f"- 问题：{item.get('question', '')}")
            st.caption(f"参考答案：{item.get('answer', '')}")
        else:
            st.write(f"- {item}")


def exercise_prompt(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("prompt") or item.get("question") or "")
    return str(item)


def exercise_answer(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("answer") or "")
    return ""


def render_node_content(node: dict[str, Any]) -> None:
    st.markdown(f"### {node['title']}")
    st.caption(f"层级：{node['level']} | 前置节点：{', '.join(node['prerequisites']) or '无'}")

    st.markdown("**学习目标**")
    st.write(node["learning_objective"])

    st.markdown("**解释**")
    st.write(node["explanation"])

    examples = node.get("examples") or node.get("exercises", [])[:1]
    with st.expander("例题", expanded=True):
        render_list_items("例题", examples)

    with st.expander("常见误区", expanded=True):
        render_list_items("常见误区", node.get("common_misconceptions", []))

    with st.expander("练习题", expanded=True):
        render_list_items("练习题", node.get("exercises", []))


def save_exercise_records(
    conn: Any,
    student_id: int,
    node: dict[str, Any],
    exercise_answers: dict[str, str],
    duration_seconds: int,
) -> list[dict[str, Any]]:
    records = []
    for index, item in enumerate(node.get("exercises", []), start=1):
        item_id = f"exercise_{index}"
        prompt = exercise_prompt(item)
        reference_answer = exercise_answer(item)
        student_answer = exercise_answers.get(item_id, "").strip()
        is_correct = diagnosis.is_answer_correct(student_answer, reference_answer)
        record = {
            "item_id": item_id,
            "item_type": "exercise",
            "prompt": prompt,
            "student_answer": student_answer,
            "correct_answer": reference_answer,
            "is_correct": is_correct,
            "error_type": "" if is_correct else "练习题待复盘",
            "recommended_node_id": "",
        }
        records.append(record)
        db.save_node_learning_record(
            conn,
            student_id,
            node["id"],
            item_id,
            "exercise",
            prompt,
            student_answer,
            reference_answer,
            is_correct,
            duration_seconds,
            record["error_type"],
            "",
        )
    return records


def save_mastery_records(
    conn: Any,
    student_id: int,
    node: dict[str, Any],
    node_map: dict[str, dict[str, Any]],
    mastery_answers: dict[str, str],
    duration_seconds: int,
) -> list[dict[str, Any]]:
    records = []
    for index, item in enumerate(node.get("mastery_questions", []), start=1):
        item_id = f"mastery_{index}"
        prompt = exercise_prompt(item)
        reference_answer = exercise_answer(item)
        student_answer = mastery_answers.get(item_id, "").strip()
        is_correct = diagnosis.is_answer_correct(student_answer, reference_answer)
        diagnostic = (
            {
                "error_type": "",
                "suggestion": "",
                "recommended_node_id": "",
                "recommended_node_title": "",
            }
            if is_correct
            else diagnosis.diagnose_answer(node, student_answer, reference_answer, node_map)
        )

        record = {
            "item_id": item_id,
            "item_type": "mastery",
            "prompt": prompt,
            "student_answer": student_answer,
            "correct_answer": reference_answer,
            "is_correct": is_correct,
            "error_type": diagnostic["error_type"],
            "suggestion": diagnostic.get("suggestion", ""),
            "recommended_node_id": diagnostic.get("recommended_node_id") or "",
            "recommended_node_title": diagnostic.get("recommended_node_title", ""),
        }
        records.append(record)
        db.save_node_learning_record(
            conn,
            student_id,
            node["id"],
            item_id,
            "mastery",
            prompt,
            student_answer,
            reference_answer,
            is_correct,
            duration_seconds,
            record["error_type"],
            record["recommended_node_id"],
        )
    return records


def render_submission_result(
    mastery_records: list[dict[str, Any]],
    duration_seconds: int,
) -> None:
    st.metric("本次学习用时", f"{duration_seconds} 秒")
    if mastery_records and all(record["is_correct"] for record in mastery_records):
        st.success("掌握验证题答对，节点状态已更新为“已掌握”。")
        return

    st.warning("掌握验证题存在错误，节点状态已更新为“薄弱”。")
    for record in mastery_records:
        if record["is_correct"]:
            continue
        st.write(f"错误类型：{record['error_type']}")
        if record.get("recommended_node_title"):
            st.write(f"推荐回退节点：{record['recommended_node_title']}")
        else:
            st.write("推荐回退节点：暂无，建议重新阅读当前节点。")
        st.caption(record.get("suggestion", ""))


def render_history(conn: Any, student_id: int, node_id: str) -> None:
    rows = db.get_node_learning_records(conn, student_id, node_id)
    if not rows:
        return

    history = [
        {
            "时间": row["created_at"],
            "类型": "掌握验证" if row["item_type"] == "mastery" else "练习",
            "题目": row["prompt"],
            "答案": row["student_answer"],
            "结果": "正确" if row["is_correct"] else "错误",
            "用时秒": row["duration_seconds"],
            "错误类型": row["error_type"] or "",
            "回退节点": row["recommended_node_id"] or "",
        }
        for row in rows
    ]
    with st.expander("最近学习记录", expanded=False):
        st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)


def render_answer_form(
    conn: Any,
    student_id: Optional[int],
    node: dict[str, Any],
    node_map: dict[str, dict[str, Any]],
) -> None:
    if student_id is None:
        st.info("请先在左侧填写学生信息。未登记学生时可以浏览节点内容，但不能保存练习记录。")
        return

    exercise_answers: dict[str, str] = {}
    mastery_answers: dict[str, str] = {}

    with st.form(f"learn_node_form_{node['id']}"):
        st.markdown("**练习作答**")
        for index, item in enumerate(node.get("exercises", []), start=1):
            item_id = f"exercise_{index}"
            exercise_answers[item_id] = st.text_area(
                exercise_prompt(item),
                key=f"{node['id']}_{item_id}",
            )

        st.markdown("**掌握验证题**")
        for index, item in enumerate(node.get("mastery_questions", []), start=1):
            item_id = f"mastery_{index}"
            mastery_answers[item_id] = st.text_area(
                exercise_prompt(item),
                key=f"{node['id']}_{item_id}",
            )

        submitted = st.form_submit_button("提交答案", type="primary")

    if not submitted:
        render_history(conn, student_id, node["id"])
        return

    missing_mastery = [
        item_id for item_id, answer in mastery_answers.items() if not answer.strip()
    ]
    if missing_mastery:
        st.warning("请先完成掌握验证题。")
        return

    duration_seconds = elapsed_seconds()
    save_exercise_records(conn, student_id, node, exercise_answers, duration_seconds)
    mastery_records = save_mastery_records(
        conn,
        student_id,
        node,
        node_map,
        mastery_answers,
        duration_seconds,
    )

    if mastery_records and all(record["is_correct"] for record in mastery_records):
        db.set_node_status(conn, student_id, node["id"], kg.STATUS_MASTERED)
        status_label = kg.STATUS_LABELS[kg.STATUS_MASTERED]
    else:
        db.set_node_status(conn, student_id, node["id"], kg.STATUS_WEAK)
        status_label = kg.STATUS_LABELS[kg.STATUS_WEAK]

    db.log_event(
        conn,
        student_id,
        "learn_node_submitted",
        node_id=node["id"],
        detail=f"{node['title']} -> {status_label}; 用时 {duration_seconds} 秒",
    )
    st.session_state["learn_start_time"] = time.time()
    render_submission_result(mastery_records, duration_seconds)
    render_history(conn, student_id, node["id"])


def main() -> None:
    st.set_page_config(page_title="节点学习", layout="wide")
    st.title("节点学习")
    st.caption("选择一个知识节点，阅读内容并完成练习。掌握验证题通过后，节点状态会更新为“已掌握”。")

    conn = get_connection()
    nodes = get_nodes()
    node_map = {node["id"]: node for node in nodes}
    student_id = register_student_sidebar(conn)
    statuses = get_statuses(conn, student_id, nodes)

    selected_node_id = st.selectbox(
        "选择知识节点",
        [node["id"] for node in nodes],
        format_func=lambda node_id: node_label(node_map[node_id], statuses),
    )
    ensure_learning_timer(selected_node_id)

    node = node_map[selected_node_id]
    current_status = statuses.get(selected_node_id, kg.STATUS_NOT_STARTED)
    st.caption(f"当前状态：{kg.status_label(current_status)}")

    if student_id is not None and current_status == kg.STATUS_NOT_STARTED:
        db.set_node_status(conn, student_id, selected_node_id, kg.STATUS_LEARNING)

    render_node_content(node)
    render_answer_form(conn, student_id, node, node_map)


if __name__ == "__main__":
    main()
