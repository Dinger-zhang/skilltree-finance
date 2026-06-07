from __future__ import annotations

import math
import re
import time
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import database as db
from src import graph as reasoning_graph
from src import knowledge_graph as kg


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "skilltree_finance.sqlite3"
PASS_RATIO = 0.6


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
            st.session_state.pop("reasoning_active_node", None)
            st.session_state.pop("reasoning_start_time", None)
            st.rerun()
        return int(current_id)

    with st.sidebar.form("student_form"):
        name = st.text_input("姓名 *")
        student_code = st.text_input("学号（可选）")
        class_name = st.text_input("班级（可选）")
        submitted = st.form_submit_button("进入推理学习")

    if submitted:
        if not name.strip():
            st.sidebar.error("请先填写姓名。")
            return None

        student_id = db.get_or_create_student(conn, name, student_code, class_name)
        st.session_state["student_id"] = student_id
        db.log_event(conn, student_id, "student_enter", detail="进入推理式学习页面")
        st.rerun()

    return None


def chain_state_key(chain: str) -> str:
    prefix = chain.split(".", maxsplit=1)[0].strip() or "chain"
    return f"reasoning_chain_index_{prefix}"


def ensure_timer(node_id: str) -> None:
    if st.session_state.get("reasoning_active_node") != node_id:
        st.session_state["reasoning_active_node"] = node_id
        st.session_state["reasoning_start_time"] = time.time()
    elif "reasoning_start_time" not in st.session_state:
        st.session_state["reasoning_start_time"] = time.time()


def elapsed_seconds() -> int:
    started_at = float(st.session_state.get("reasoning_start_time", time.time()))
    return max(int(time.time() - started_at), 0)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def point_matches(answer: str, point: str) -> bool:
    normalized_answer = normalize_text(answer)
    normalized_point = normalize_text(point)
    if normalized_point and normalized_point in normalized_answer:
        return True

    tokens = [
        normalize_text(token)
        for token in re.split(r"[/,，、；;\s]+", point)
        if len(normalize_text(token)) >= 2
    ]
    return any(token in normalized_answer for token in tokens)


def evaluate_answer(
    answer: str,
    expected_points: list[str],
) -> dict[str, Any]:
    matched = [point for point in expected_points if point_matches(answer, point)]
    missing = [point for point in expected_points if point not in matched]
    required_count = max(1, math.ceil(len(expected_points) * PASS_RATIO))
    passed = len(matched) >= required_count
    return {
        "passed": passed,
        "matched": matched,
        "missing": missing,
        "required_count": required_count,
    }


def render_node(node: dict[str, Any], index: int, total: int) -> None:
    st.markdown(f"### 第 {index + 1} / {total} 节：{node['title']}")
    st.caption(f"类型：{node['type']} | 层级：{node['layer']} | 节点 ID：{node['id']}")

    st.markdown("**核心问题**")
    st.write(node["core_question"])

    st.markdown("**情境案例**")
    st.write(node["scenario"])

    st.markdown("**引导问题**")
    for question in node["guiding_questions"]:
        st.write(f"- {question}")

    st.markdown("**规则总结**")
    st.info(node["rule_summary"])

    with st.expander("常见误区", expanded=False):
        for item in node["common_misconceptions"]:
            st.write(f"- {item}")

    st.markdown("**掌握验证题**")
    st.write(node["mastery_question"])


def save_reasoning_answer(
    conn: Any,
    student_id: int,
    node: dict[str, Any],
    answer: str,
    evaluation: dict[str, Any],
    duration_seconds: int,
) -> None:
    next_ids = node.get("derives", [])
    fallback_ids = node.get("prerequisites", [])
    recommended_node_id = (
        next_ids[0]
        if evaluation["passed"] and next_ids
        else fallback_ids[-1]
        if fallback_ids
        else ""
    )
    correct_answer = "；".join(node["expected_reasoning_points"])
    error_type = "" if evaluation["passed"] else "推理要点不足"

    db.save_node_learning_record(
        conn,
        student_id,
        node["id"],
        "reasoning_mastery",
        "reasoning",
        node["mastery_question"],
        answer,
        correct_answer,
        bool(evaluation["passed"]),
        duration_seconds,
        error_type,
        recommended_node_id,
    )
    db.set_node_status(
        conn,
        student_id,
        node["id"],
        kg.STATUS_MASTERED if evaluation["passed"] else kg.STATUS_WEAK,
    )
    db.log_event(
        conn,
        student_id,
        "reasoning_lesson_submitted",
        node_id=node["id"],
        detail=(
            f"{node['title']} -> "
            f"{'通过' if evaluation['passed'] else '未通过'}; "
            f"命中 {len(evaluation['matched'])}/{len(node['expected_reasoning_points'])} 个要点"
        ),
    )


def render_evaluation_result(
    nodes: list[dict[str, Any]],
    node: dict[str, Any],
    evaluation: dict[str, Any],
) -> None:
    matched = evaluation["matched"]
    missing = evaluation["missing"]
    st.write(f"命中要点：{len(matched)} / {len(node['expected_reasoning_points'])}")

    if matched:
        st.caption("已命中：" + "、".join(matched))
    if missing:
        st.caption("待补充：" + "、".join(missing))

    if not evaluation["passed"]:
        st.warning("暂未通过。请补充关键推理点后再次提交。")
        return

    derived_nodes = kg.get_derived_nodes(nodes, node["id"])
    if not derived_nodes:
        st.success("已通过。本条推理链已到达最后一个节点。")
        return

    st.success("已通过。你可以推出的下一个节点：")
    for derived in derived_nodes:
        st.write(f"- {derived['title']}：{derived['core_question']}")


def render_history(conn: Any, student_id: int, node_id: str) -> None:
    rows = [
        row
        for row in db.get_node_learning_records(conn, student_id, node_id)
        if row["item_type"] == "reasoning"
    ]
    if not rows:
        return

    history = [
        {
            "时间": row["created_at"],
            "答案": row["student_answer"],
            "结果": "通过" if row["is_correct"] else "未通过",
            "用时秒": row["duration_seconds"],
            "推荐节点": row["recommended_node_id"] or "",
        }
        for row in rows
    ]
    with st.expander("本节点推理作答记录", expanded=False):
        st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)


def render_navigation(chain_items: list[dict[str, Any]], chain_key: str, current_index: int) -> None:
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("上一节点", disabled=current_index <= 0):
            st.session_state[chain_key] = current_index - 1
            st.rerun()
    with col2:
        if st.button("下一节点", disabled=current_index >= len(chain_items) - 1):
            st.session_state[chain_key] = current_index + 1
            st.rerun()
    with col3:
        selected_id = st.selectbox(
            "跳转到链内节点",
            [node["id"] for node in chain_items],
            index=current_index,
            format_func=lambda node_id: next(
                node["title"] for node in chain_items if node["id"] == node_id
            ),
        )
        selected_index = next(
            index for index, node in enumerate(chain_items) if node["id"] == selected_id
        )
        if selected_index != current_index:
            st.session_state[chain_key] = selected_index
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="推理式学习", layout="wide")
    st.title("推理式学习")
    st.caption("v0.2 最小示例：按推理链学习原子知识点，提交答案后用关键词进行第一版判断。")

    conn = get_connection()
    nodes = get_nodes()
    student_id = register_student_sidebar(conn)
    chains = reasoning_graph.group_nodes_by_chain(nodes)

    selected_chain = st.selectbox("选择推理链", list(chains.keys()))
    chain_items = chains[selected_chain]
    state_key = chain_state_key(selected_chain)
    current_index = int(st.session_state.get(state_key, 0))
    current_index = min(max(current_index, 0), len(chain_items) - 1)
    st.session_state[state_key] = current_index

    st.progress(
        (current_index + 1) / len(chain_items),
        text=f"当前进度：{current_index + 1} / {len(chain_items)}",
    )
    render_navigation(chain_items, state_key, current_index)

    node = chain_items[current_index]
    ensure_timer(node["id"])
    render_node(node, current_index, len(chain_items))

    if student_id is None:
        st.info("请先在左侧填写学生信息。未登记学生时可以浏览推理链，但不能保存答案。")
        return

    with st.form(f"reasoning_form_{node['id']}"):
        answer = st.text_area("你的推理回答", key=f"reasoning_answer_{node['id']}")
        submitted = st.form_submit_button("提交并判断", type="primary")

    if submitted:
        if not answer.strip():
            st.warning("请先填写你的推理回答。")
            return

        duration_seconds = elapsed_seconds()
        evaluation = evaluate_answer(answer, node["expected_reasoning_points"])
        save_reasoning_answer(conn, student_id, node, answer, evaluation, duration_seconds)
        st.session_state["reasoning_start_time"] = time.time()
        render_evaluation_result(nodes, node, evaluation)

    render_history(conn, student_id, node["id"])


if __name__ == "__main__":
    main()
