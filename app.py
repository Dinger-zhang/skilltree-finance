from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import content
from src import database as db


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "skilltree_finance.sqlite3"

STATUS_LABELS = {
    "locked": "未解锁",
    "available": "可学习",
    "completed": "已完成",
}

PHASE_LABELS = {
    "pretest": "前测",
    "posttest": "后测",
}


@st.cache_resource
def get_connection() -> Any:
    conn = db.connect(DB_PATH)
    db.init_db(conn)
    return conn


@st.cache_data
def get_nodes() -> list[dict[str, Any]]:
    return content.load_knowledge_graph(DATA_DIR / "knowledge_graph.yaml")


@st.cache_data
def get_questions() -> dict[str, list[dict[str, Any]]]:
    return content.load_questions(DATA_DIR / "questions.yaml")


def apply_unlock_rules(
    conn: Any,
    student_id: int,
    nodes: list[dict[str, Any]],
) -> dict[str, str]:
    db.ensure_node_statuses(conn, student_id, nodes)
    statuses = db.get_node_statuses(conn, student_id)
    completed = {
        node_id for node_id, status in statuses.items() if status == "completed"
    }

    for node in nodes:
        node_id = str(node["id"])
        if statuses.get(node_id) == "completed":
            continue

        prerequisites = node.get("prerequisites", [])
        next_status = (
            "available"
            if all(prerequisite in completed for prerequisite in prerequisites)
            else "locked"
        )
        if statuses.get(node_id) != next_status:
            db.set_node_status(conn, student_id, node_id, next_status)

    return db.get_node_statuses(conn, student_id)


def register_student_sidebar(conn: Any) -> int | None:
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
        submitted = st.form_submit_button("进入实验")

    if submitted:
        if not name.strip():
            st.sidebar.error("请先填写姓名。")
            return None

        student_id = db.get_or_create_student(conn, name, student_code, class_name)
        st.session_state["student_id"] = student_id
        db.log_event(conn, student_id, "student_enter", detail="进入学习实验")
        st.rerun()

    return None


def option_labels(question: dict[str, Any]) -> list[str]:
    return [
        f"{option_key}. {option_text}"
        for option_key, option_text in question["options"].items()
    ]


def selected_key(label: str) -> str:
    return label.split(".", 1)[0]


def score_summary(answers: list[Any], total: int) -> tuple[int, str]:
    score = sum(int(row["is_correct"]) for row in answers)
    return score, f"{score} / {total}"


def answer_review_dataframe(
    questions: list[dict[str, Any]],
    latest_answers: list[Any],
) -> pd.DataFrame:
    answer_map = {row["question_id"]: row for row in latest_answers}
    rows = []

    for question in questions:
        answer = answer_map.get(question["id"])
        if not answer:
            continue

        selected = answer["selected_answer"]
        correct = answer["correct_answer"]
        rows.append(
            {
                "题号": question["id"],
                "题目": question["question"],
                "你的答案": f"{selected}. {question['options'][selected]}",
                "正确答案": f"{correct}. {question['options'][correct]}",
                "结果": "正确" if answer["is_correct"] else "错误",
            }
        )

    return pd.DataFrame(rows)


def render_quiz(
    conn: Any,
    student_id: int,
    phase: str,
    questions: list[dict[str, Any]],
) -> None:
    label = PHASE_LABELS[phase]
    st.subheader(label)
    st.write("请选择每道题的答案并提交，系统会记录本次答题结果。重复提交会保留历史记录，报告页展示最近一次结果。")

    latest_answers = db.get_latest_answers(conn, student_id, phase)
    if latest_answers:
        score, score_text = score_summary(latest_answers, len(questions))
        st.info(f"最近一次{label}成绩：{score_text}")

    with st.form(f"{phase}_form"):
        selections: dict[str, Optional[str]] = {}
        for index, question in enumerate(questions, start=1):
            st.markdown(f"**{index}. {question['question']}**")
            selections[question["id"]] = st.radio(
                "选择答案",
                option_labels(question),
                index=None,
                key=f"{phase}_{question['id']}",
                label_visibility="collapsed",
            )

        submitted = st.form_submit_button(f"提交{label}")

    if submitted:
        missing = [
            question["id"]
            for question in questions
            if selections.get(question["id"]) is None
        ]
        if missing:
            st.warning("还有题目未作答，请完成所有题目后再提交。")
            return

        for question in questions:
            selected = selected_key(str(selections[question["id"]]))
            db.save_answer(
                conn,
                student_id,
                phase,
                question["id"],
                selected,
                question["answer"],
            )

        db.log_event(conn, student_id, f"{phase}_submitted", detail=f"提交{label}")
        st.success(f"{label}已提交。")
        st.rerun()

    latest_answers = db.get_latest_answers(conn, student_id, phase)
    if latest_answers:
        review_df = answer_review_dataframe(questions, latest_answers)
        with st.expander(f"查看最近一次{label}答题明细", expanded=False):
            st.dataframe(review_df, hide_index=True, use_container_width=True)


def node_label(node: dict[str, Any], statuses: dict[str, str]) -> str:
    status = STATUS_LABELS.get(statuses.get(str(node["id"]), "locked"), "未解锁")
    return f"L{node['level']} | {status} | {node['title']}"


def render_skill_tree(
    conn: Any,
    student_id: int,
    nodes: list[dict[str, Any]],
) -> None:
    st.subheader("技能树学习")
    statuses = apply_unlock_rules(conn, student_id, nodes)
    node_map = {str(node["id"]): node for node in nodes}

    completed_count = sum(
        1 for node in nodes if statuses.get(str(node["id"])) == "completed"
    )
    st.progress(completed_count / len(nodes), text=f"完成进度：{completed_count} / {len(nodes)}")

    overview_rows = []
    for node in nodes:
        prerequisites = node.get("prerequisites", [])
        overview_rows.append(
            {
                "层级": node["level"],
                "节点": node["title"],
                "报表/主题": node["statement"],
                "状态": STATUS_LABELS.get(statuses.get(str(node["id"]), "locked")),
                "前置节点": "、".join(
                    node_map[item]["title"] for item in prerequisites if item in node_map
                )
                or "无",
            }
        )

    st.dataframe(pd.DataFrame(overview_rows), hide_index=True, use_container_width=True)

    selected_node_id = st.selectbox(
        "选择学习节点",
        [str(node["id"]) for node in nodes],
        format_func=lambda node_id: node_label(node_map[node_id], statuses),
    )
    selected_node = node_map[selected_node_id]
    selected_status = statuses.get(selected_node_id, "locked")

    st.markdown(f"### {selected_node['title']}")
    st.caption(f"主题：{selected_node['statement']} | 状态：{STATUS_LABELS[selected_status]}")

    if selected_status == "locked":
        prerequisite_titles = [
            node_map[item]["title"]
            for item in selected_node.get("prerequisites", [])
            if item in node_map
        ]
        st.warning("该节点尚未解锁。请先完成前置节点：" + "、".join(prerequisite_titles))
        return

    st.write(selected_node["summary"])
    st.markdown("**学习目标**")
    for goal in selected_node.get("learning_goals", []):
        st.write(f"- {goal}")

    st.info(f"例子：{selected_node['example']}")

    check = selected_node.get("check_question", {})
    if check:
        with st.expander("自检问题"):
            st.write(check.get("question", ""))
            st.caption(f"参考答案：{check.get('answer', '')}")

    left, right = st.columns([1, 2])
    with left:
        if selected_status == "completed":
            st.success("该节点已完成。")
        elif st.button("标记为已学完", type="primary"):
            db.set_node_status(conn, student_id, selected_node_id, "completed")
            db.log_event(
                conn,
                student_id,
                "node_completed",
                node_id=selected_node_id,
                detail=selected_node["title"],
            )
            st.rerun()

    with right:
        note = st.text_area("学习笔记（可选）", key=f"note_{selected_node_id}")
        if st.button("保存学习笔记"):
            if not note.strip():
                st.warning("学习笔记为空，未保存。")
            else:
                db.log_event(
                    conn,
                    student_id,
                    "note_saved",
                    node_id=selected_node_id,
                    detail=note.strip(),
                )
                st.success("学习笔记已保存。")


def report_metric_columns(
    pre_answers: list[Any],
    post_answers: list[Any],
    pre_total: int,
    post_total: int,
    completed_count: int,
    node_total: int,
) -> None:
    pre_score, pre_text = score_summary(pre_answers, pre_total) if pre_answers else (0, "未完成")
    post_score, post_text = (
        score_summary(post_answers, post_total) if post_answers else (0, "未完成")
    )
    delta_text = None
    if pre_answers and post_answers:
        delta_text = f"{post_score - pre_score:+d}"

    col1, col2, col3 = st.columns(3)
    col1.metric("前测", pre_text)
    col2.metric("后测", post_text, delta=delta_text)
    col3.metric("技能节点", f"{completed_count} / {node_total}")


def render_report(
    conn: Any,
    student_id: int,
    nodes: list[dict[str, Any]],
    questions: dict[str, list[dict[str, Any]]],
) -> None:
    st.subheader("学习报告")

    student = db.get_student(conn, student_id)
    if student:
        st.write(
            f"学生：{student['name']}  "
            f"学号：{student['student_code'] or '-'}  "
            f"班级：{student['class_name'] or '-'}"
        )

    statuses = apply_unlock_rules(conn, student_id, nodes)
    pre_answers = db.get_latest_answers(conn, student_id, "pretest")
    post_answers = db.get_latest_answers(conn, student_id, "posttest")
    completed_count = sum(
        1 for node in nodes if statuses.get(str(node["id"])) == "completed"
    )

    report_metric_columns(
        pre_answers,
        post_answers,
        len(questions["pretest"]),
        len(questions["posttest"]),
        completed_count,
        len(nodes),
    )

    st.markdown("**节点状态**")
    status_df = pd.DataFrame(
        [
            {
                "层级": node["level"],
                "节点": node["title"],
                "主题": node["statement"],
                "状态": STATUS_LABELS.get(statuses.get(str(node["id"]), "locked")),
            }
            for node in nodes
        ]
    )
    st.dataframe(status_df, hide_index=True, use_container_width=True)

    with st.expander("前测最近一次答题", expanded=False):
        if pre_answers:
            st.dataframe(
                answer_review_dataframe(questions["pretest"], pre_answers),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.write("尚未完成前测。")

    with st.expander("后测最近一次答题", expanded=False):
        if post_answers:
            st.dataframe(
                answer_review_dataframe(questions["posttest"], post_answers),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.write("尚未完成后测。")

    st.markdown("**学习日志**")
    logs = db.get_learning_logs(conn, student_id)
    if not logs:
        st.write("暂无学习日志。")
        return

    logs_df = pd.DataFrame([dict(row) for row in logs])
    st.dataframe(logs_df, hide_index=True, use_container_width=True)
    st.download_button(
        "下载学习日志 CSV",
        logs_df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"student_{student_id}_learning_logs.csv",
        mime="text/csv",
    )


def main() -> None:
    st.set_page_config(
        page_title="SkillTree Finance",
        layout="wide",
    )
    st.title("AI 技能树财务报表学习实验系统")
    st.caption("本地 MVP：记录学生信息、前测、技能树学习、后测和学习报告。")

    conn = get_connection()
    nodes = get_nodes()
    questions = get_questions()
    student_id = register_student_sidebar(conn)

    if not student_id:
        st.info("请先在左侧填写学生信息并进入实验。")
        return

    tab_pretest, tab_tree, tab_posttest, tab_report = st.tabs(
        ["前测", "技能树学习", "后测", "学习报告"]
    )

    with tab_pretest:
        render_quiz(conn, student_id, "pretest", questions["pretest"])

    with tab_tree:
        render_skill_tree(conn, student_id, nodes)

    with tab_posttest:
        render_quiz(conn, student_id, "posttest", questions["posttest"])

    with tab_report:
        render_report(conn, student_id, nodes, questions)


if __name__ == "__main__":
    main()
