from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import assessment as asm
from src import content
from src import database as db
from src import knowledge_graph as kg


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "skilltree_finance.sqlite3"
PHASE = "pretest"


@st.cache_resource
def get_connection() -> Any:
    conn = db.connect(DB_PATH)
    db.init_db(conn)
    return conn


@st.cache_data
def get_pretest_questions() -> list[dict[str, Any]]:
    return content.load_questions(DATA_DIR / "questions.yaml")["pretest"]


@st.cache_data
def get_nodes() -> list[dict[str, Any]]:
    return kg.load_knowledge_graph(DATA_DIR / "knowledge_graph.yaml")


def format_score(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


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
            st.rerun()
        return int(current_id)

    with st.sidebar.form("student_form"):
        name = st.text_input("姓名 *")
        student_code = st.text_input("学号（可选）")
        class_name = st.text_input("班级（可选）")
        submitted = st.form_submit_button("进入前测")

    if submitted:
        if not name.strip():
            st.sidebar.error("请先填写姓名。")
            return None

        student_id = db.get_or_create_student(conn, name, student_code, class_name)
        st.session_state["student_id"] = student_id
        db.log_event(conn, student_id, "student_enter", detail="进入前测页面")
        st.rerun()

    return None


def render_question(question: dict[str, Any], index: int) -> Any:
    st.markdown(f"**{index}. {question['question']}**")
    st.caption(f"题型：{question_type_label(question)} | 分值：{format_score(asm.question_score(question))}")

    q_type = asm.question_type(question)
    if q_type == asm.QUESTION_SINGLE:
        return st.radio(
            "选择一个答案",
            asm.option_labels(question),
            index=None,
            key=f"pretest_{question['id']}",
            label_visibility="collapsed",
        )

    if q_type == asm.QUESTION_MULTIPLE:
        return st.multiselect(
            "选择一个或多个答案",
            asm.option_labels(question),
            key=f"pretest_{question['id']}",
            label_visibility="collapsed",
        )

    if q_type == asm.QUESTION_SHORT:
        return st.text_area(
            "填写简答题答案",
            key=f"pretest_{question['id']}",
            label_visibility="collapsed",
        )

    st.error(f"不支持的题型：{q_type}")
    return None


def question_type_label(question: dict[str, Any]) -> str:
    labels = {
        asm.QUESTION_SINGLE: "单选题",
        asm.QUESTION_MULTIPLE: "多选题",
        asm.QUESTION_SHORT: "简答题",
    }
    return labels.get(asm.question_type(question), "未知题型")


def is_missing_answer(value: Any) -> bool:
    return value is None or value == [] or (isinstance(value, str) and not value.strip())


def normalize_student_answer(question: dict[str, Any], value: Any) -> Any:
    q_type = asm.question_type(question)
    if q_type == asm.QUESTION_SINGLE:
        return asm.selected_key(str(value))
    if q_type == asm.QUESTION_MULTIPLE:
        return [asm.selected_key(str(item)) for item in value]
    return value


def node_titles(nodes: list[dict[str, Any]]) -> dict[str, str]:
    return {node["id"]: node["title"] for node in nodes}


def save_pretest_results(
    conn: Any,
    student_id: int,
    questions: list[dict[str, Any]],
    raw_answers: dict[str, Any],
) -> list[dict[str, Any]]:
    results = []
    for question in questions:
        answer = normalize_student_answer(question, raw_answers[question["id"]])
        result = asm.grade_question(question, answer)
        results.append(result)
        db.save_answer_result(conn, student_id, PHASE, result)

    weak_nodes = asm.weak_node_ids(results)
    for node_id in weak_nodes:
        db.set_node_status(conn, student_id, node_id, kg.STATUS_WEAK)

    db.log_event(
        conn,
        student_id,
        "pretest_submitted",
        detail=f"提交前测，薄弱节点数：{len(weak_nodes)}",
    )
    return results


def render_total_score(results: list[dict[str, Any]]) -> None:
    summary = asm.summarize_results(results)
    st.metric(
        "总分",
        f"{format_score(summary['total_score'])} / {format_score(summary['max_score'])}",
    )
    if summary["pending_manual"]:
        st.info(f"{int(summary['pending_manual'])} 道简答题待人工评分，当前总分暂按 0 分计入。")


def render_knowledge_scores(
    results: list[dict[str, Any]],
    title_map: dict[str, str],
) -> None:
    rows = []
    for item in asm.knowledge_point_scores(results):
        node_id = item["node_id"]
        rows.append(
            {
                "知识节点": title_map.get(node_id, node_id),
                "得分": f"{format_score(item['score'])} / {format_score(item['max_score'])}",
                "自动错题数": item["wrong_count"],
                "待人工评分": item["pending_manual"],
            }
        )

    st.markdown("**各知识点得分**")
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def render_weak_nodes(results: list[dict[str, Any]], title_map: dict[str, str]) -> None:
    weak_node_ids = asm.weak_node_ids(results)
    st.markdown("**初步薄弱节点**")
    if not weak_node_ids:
        st.success("自动评分题暂未识别出薄弱节点。简答题需人工评分后再进一步判断。")
        return

    rows = [
        {
            "node_id": node_id,
            "知识节点": title_map.get(node_id, node_id),
            "已写入状态": kg.STATUS_LABELS[kg.STATUS_WEAK],
        }
        for node_id in weak_node_ids
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def render_answer_details(
    questions: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> None:
    question_map = {question["id"]: question for question in questions}
    rows = []
    for result in results:
        question = question_map[result["question_id"]]
        options = question.get("options", {})
        rows.append(
            {
                "题号": result["question_id"],
                "题型": question_type_label(question),
                "知识节点": question.get("node_id", ""),
                "你的答案": asm.format_answer(result["selected_answer"], options),
                "参考答案": asm.format_answer(result["correct_answer"], options),
                "得分": f"{format_score(result['score'])} / {format_score(result['max_score'])}",
                "状态": (
                    "待人工评分"
                    if result["needs_manual_grading"]
                    else "正确"
                    if result["is_correct"]
                    else "错误"
                ),
            }
        )

    with st.expander("答题明细", expanded=False):
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def render_results(
    questions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> None:
    title_map = node_titles(nodes)
    render_total_score(results)
    render_knowledge_scores(results, title_map)
    render_weak_nodes(results, title_map)
    render_answer_details(questions, results)


def latest_pretest_results(conn: Any, student_id: int) -> list[dict[str, Any]]:
    rows = db.get_latest_answers(conn, student_id, PHASE)
    return asm.results_from_answer_rows(rows)


def main() -> None:
    st.set_page_config(page_title="前测", layout="wide")
    st.title("前测")
    st.caption("支持单选题、多选题和简答题。单选/多选自动评分，简答题第一版仅保存答案，后续人工评分。")

    conn = get_connection()
    questions = get_pretest_questions()
    nodes = get_nodes()
    student_id = register_student_sidebar(conn)

    if student_id is None:
        st.info("请先在左侧填写学生信息，再开始前测。")
        return

    raw_answers: dict[str, Any] = {}
    with st.form("pretest_form"):
        for index, question in enumerate(questions, start=1):
            raw_answers[question["id"]] = render_question(question, index)
            st.divider()

        submitted = st.form_submit_button("提交前测", type="primary")

    if submitted:
        missing = [
            question["id"]
            for question in questions
            if is_missing_answer(raw_answers.get(question["id"]))
        ]
        if missing:
            st.warning("还有题目未作答，请完成所有题目后再提交。")
            return

        results = save_pretest_results(conn, student_id, questions, raw_answers)
        st.success("前测已提交，结果已写入 SQLite。")
        render_results(questions, results, nodes)
        return

    latest_results = latest_pretest_results(conn, student_id)
    if latest_results:
        st.markdown("### 最近一次前测结果")
        render_results(questions, latest_results, nodes)


if __name__ == "__main__":
    main()
