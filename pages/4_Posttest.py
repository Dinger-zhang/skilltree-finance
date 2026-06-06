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
PHASE = "posttest"


@st.cache_resource
def get_connection() -> Any:
    conn = db.connect(DB_PATH)
    db.init_db(conn)
    return conn


@st.cache_data
def get_questions() -> dict[str, list[dict[str, Any]]]:
    return content.load_questions(DATA_DIR / "questions.yaml")


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
        submitted = st.form_submit_button("进入后测")

    if submitted:
        if not name.strip():
            st.sidebar.error("请先填写姓名。")
            return None

        student_id = db.get_or_create_student(conn, name, student_code, class_name)
        st.session_state["student_id"] = student_id
        db.log_event(conn, student_id, "student_enter", detail="进入后测页面")
        st.rerun()

    return None


def question_type_label(question: dict[str, Any]) -> str:
    labels = {
        asm.QUESTION_SINGLE: "单选题",
        asm.QUESTION_MULTIPLE: "多选题",
        asm.QUESTION_SHORT: "简答题",
    }
    return labels.get(asm.question_type(question), "未知题型")


def render_question(question: dict[str, Any], index: int) -> Any:
    st.markdown(f"**{index}. {question['question']}**")
    st.caption(f"题型：{question_type_label(question)} | 分值：{format_score(asm.question_score(question))}")

    q_type = asm.question_type(question)
    if q_type == asm.QUESTION_SINGLE:
        return st.radio(
            "选择一个答案",
            asm.option_labels(question),
            index=None,
            key=f"posttest_{question['id']}",
            label_visibility="collapsed",
        )

    if q_type == asm.QUESTION_MULTIPLE:
        return st.multiselect(
            "选择一个或多个答案",
            asm.option_labels(question),
            key=f"posttest_{question['id']}",
            label_visibility="collapsed",
        )

    if q_type == asm.QUESTION_SHORT:
        return st.text_area(
            "填写简答题答案",
            key=f"posttest_{question['id']}",
            label_visibility="collapsed",
        )

    st.error(f"不支持的题型：{q_type}")
    return None


def is_missing_answer(value: Any) -> bool:
    return value is None or value == [] or (isinstance(value, str) and not value.strip())


def normalize_student_answer(question: dict[str, Any], value: Any) -> Any:
    q_type = asm.question_type(question)
    if q_type == asm.QUESTION_SINGLE:
        return asm.selected_key(str(value))
    if q_type == asm.QUESTION_MULTIPLE:
        return [asm.selected_key(str(item)) for item in value]
    return value


def node_title_map(nodes: list[dict[str, Any]]) -> dict[str, str]:
    return {node["id"]: node["title"] for node in nodes}


def node_map(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {node["id"]: node for node in nodes}


def validate_posttest_nodes(
    pretest_questions: list[dict[str, Any]],
    posttest_questions: list[dict[str, Any]],
) -> None:
    pre_nodes = {question.get("node_id", "") for question in pretest_questions}
    post_nodes = {question.get("node_id", "") for question in posttest_questions}
    if pre_nodes != post_nodes:
        st.warning("后测题目当前未覆盖与前测完全相同的知识节点，请检查 data/questions.yaml。")

    pre_pairs = {(question.get("node_id", ""), question.get("question", "")) for question in pretest_questions}
    post_pairs = {(question.get("node_id", ""), question.get("question", "")) for question in posttest_questions}
    if pre_pairs & post_pairs:
        st.warning("检测到后测中存在与前测完全相同的题干，请检查题库。")


def save_posttest_results(
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
        db.save_answer_result(conn, student_id, PHASE, result, delayed_test=False)

    for node_id in asm.weak_node_ids(results):
        db.set_node_status(conn, student_id, node_id, kg.STATUS_REVIEW)

    db.log_event(conn, student_id, "posttest_submitted", detail="提交后测")
    return results


def latest_results(conn: Any, student_id: int, phase: str) -> list[dict[str, Any]]:
    rows = db.get_latest_answers(conn, student_id, phase)
    return asm.results_from_answer_rows(rows)


def score_summary(results: list[dict[str, Any]]) -> dict[str, float]:
    if not results:
        return {"total_score": 0.0, "max_score": 0.0, "pending_manual": 0.0}
    return asm.summarize_results(results)


def score_text(summary: dict[str, float]) -> str:
    text = f"{format_score(summary['total_score'])} / {format_score(summary['max_score'])}"
    if summary["pending_manual"]:
        text += f"（{int(summary['pending_manual'])} 题待人工评分）"
    return text


def score_delta_text(delta: float) -> str:
    sign = "+" if delta >= 0 else ""
    return f"{sign}{format_score(delta)}"


def node_score_map(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["node_id"]: item for item in asm.knowledge_point_scores(results)}


def node_is_weak(item: dict[str, Any] | None) -> bool:
    if not item:
        return False
    return float(item["score"]) < float(item["max_score"])


def compare_node_scores(
    pre_results: list[dict[str, Any]],
    post_results: list[dict[str, Any]],
    title_map: dict[str, str],
) -> pd.DataFrame:
    pre_scores = node_score_map(pre_results)
    post_scores = node_score_map(post_results)
    all_node_ids = sorted(set(pre_scores) | set(post_scores))
    rows = []

    for node_id in all_node_ids:
        pre_item = pre_scores.get(node_id)
        post_item = post_scores.get(node_id)
        pre_score = float(pre_item["score"]) if pre_item else 0.0
        post_score = float(post_item["score"]) if post_item else 0.0
        max_score = float(post_item["max_score"] if post_item else pre_item["max_score"])
        rows.append(
            {
                "知识节点": title_map.get(node_id, node_id),
                "前测": f"{format_score(pre_score)} / {format_score(float(pre_item['max_score']) if pre_item else max_score)}",
                "后测": f"{format_score(post_score)} / {format_score(float(post_item['max_score']) if post_item else max_score)}",
                "提升": score_delta_text(post_score - pre_score),
                "仍薄弱": "是" if node_is_weak(pre_item) and node_is_weak(post_item) else "否",
                "后测待人工评分": int(post_item["pending_manual"]) if post_item else 0,
            }
        )

    return pd.DataFrame(rows)


def still_weak_node_ids(
    pre_results: list[dict[str, Any]],
    post_results: list[dict[str, Any]],
) -> list[str]:
    pre_scores = node_score_map(pre_results)
    post_scores = node_score_map(post_results)
    weak_nodes = []
    for node_id, post_item in post_scores.items():
        if node_is_weak(pre_scores.get(node_id)) and node_is_weak(post_item):
            weak_nodes.append(node_id)
    return weak_nodes


def recommended_review_nodes(
    weak_node_ids: list[str],
    nodes: list[dict[str, Any]],
) -> list[str]:
    graph = node_map(nodes)
    recommendations = []
    for node_id in weak_node_ids:
        recommendations.append(node_id)
        recommendations.extend(graph.get(node_id, {}).get("prerequisites", []))

    seen = set()
    unique = []
    for node_id in recommendations:
        if node_id and node_id not in seen:
            seen.add(node_id)
            unique.append(node_id)
    return unique


def render_result_summary(
    pre_results: list[dict[str, Any]],
    post_results: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> None:
    title_map = node_title_map(nodes)
    pre_summary = score_summary(pre_results)
    post_summary = score_summary(post_results)
    total_delta = post_summary["total_score"] - pre_summary["total_score"]

    col1, col2, col3 = st.columns(3)
    col1.metric("前测总分", score_text(pre_summary))
    col2.metric("后测总分", score_text(post_summary), delta=score_delta_text(total_delta))
    col3.metric("总分提升", score_delta_text(total_delta))

    if post_summary["pending_manual"] or pre_summary["pending_manual"]:
        st.info("简答题第一版为待人工评分，当前对比中待人工评分题暂按 0 分计算。")

    st.markdown("**各节点提升**")
    st.dataframe(
        compare_node_scores(pre_results, post_results, title_map),
        hide_index=True,
        use_container_width=True,
    )

    weak_nodes = still_weak_node_ids(pre_results, post_results)
    st.markdown("**仍然薄弱的节点**")
    if weak_nodes:
        st.dataframe(
            pd.DataFrame(
                [
                    {"node_id": node_id, "知识节点": title_map.get(node_id, node_id)}
                    for node_id in weak_nodes
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.success("根据当前自动评分结果，暂未发现前后测都薄弱的节点。")

    review_nodes = recommended_review_nodes(weak_nodes or asm.weak_node_ids(post_results), nodes)
    st.markdown("**建议复习节点**")
    if review_nodes:
        st.dataframe(
            pd.DataFrame(
                [
                    {"node_id": node_id, "知识节点": title_map.get(node_id, node_id)}
                    for node_id in review_nodes
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.success("当前没有额外建议复习节点。")


def render_answer_details(
    questions: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> None:
    question_map = {question["id"]: question for question in questions}
    rows = []
    for result in results:
        question = question_map.get(result["question_id"], {})
        options = question.get("options", {})
        rows.append(
            {
                "题号": result["question_id"],
                "题型": question_type_label(question) if question else result["question_type"],
                "知识节点": result.get("node_id", ""),
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

    with st.expander("后测答题明细", expanded=False):
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="后测", layout="wide")
    st.title("后测")
    st.caption("支持与前测一致的三种题型。单选/多选自动评分，简答题第一版保存答案并等待人工评分。")

    conn = get_connection()
    questions = get_questions()
    pretest_questions = questions["pretest"]
    posttest_questions = questions["posttest"]
    nodes = get_nodes()
    validate_posttest_nodes(pretest_questions, posttest_questions)
    student_id = register_student_sidebar(conn)

    if student_id is None:
        st.info("请先在左侧填写学生信息，再开始后测。")
        return

    pre_results = latest_results(conn, student_id, "pretest")
    if not pre_results:
        st.warning("尚未检测到前测结果。可以先完成后测，但无法展示前后测提升。")

    raw_answers: dict[str, Any] = {}
    with st.form("posttest_form"):
        for index, question in enumerate(posttest_questions, start=1):
            raw_answers[question["id"]] = render_question(question, index)
            st.divider()

        submitted = st.form_submit_button("提交后测", type="primary")

    if submitted:
        missing = [
            question["id"]
            for question in posttest_questions
            if is_missing_answer(raw_answers.get(question["id"]))
        ]
        if missing:
            st.warning("还有题目未作答，请完成所有题目后再提交。")
            return

        post_results = save_posttest_results(conn, student_id, posttest_questions, raw_answers)
        st.success("后测已提交，结果已写入 SQLite。")
        if pre_results:
            render_result_summary(pre_results, post_results, nodes)
        else:
            render_result_summary([], post_results, nodes)
        render_answer_details(posttest_questions, post_results)
        return

    latest_post_results = latest_results(conn, student_id, PHASE)
    if latest_post_results:
        st.markdown("### 最近一次后测结果")
        render_result_summary(pre_results, latest_post_results, nodes)
        render_answer_details(posttest_questions, latest_post_results)


if __name__ == "__main__":
    main()
