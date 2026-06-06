from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import assessment as asm
from src import content
from src import database as db
from src import knowledge_graph as kg


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "skilltree_finance.sqlite3"

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
    return kg.load_knowledge_graph(DATA_DIR / "knowledge_graph.yaml")


@st.cache_data
def get_questions() -> dict[str, list[dict[str, Any]]]:
    return content.load_questions(DATA_DIR / "questions.yaml")


def get_statuses(
    conn: Any,
    student_id: Optional[int],
    nodes: list[dict[str, Any]],
) -> dict[str, str]:
    if student_id is None:
        return kg.default_statuses(nodes)

    db.ensure_node_statuses(conn, student_id, nodes)
    stored_statuses = db.get_node_statuses(conn, student_id)
    return {
        node["id"]: kg.normalize_status(stored_statuses.get(node["id"]))
        for node in nodes
    }


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
    return asm.option_labels(question)


def selected_key(label: str) -> str:
    return asm.selected_key(label)


def format_score(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


def score_summary(answers: list[Any], total: int) -> tuple[int, str]:
    results = asm.results_from_answer_rows(answers)
    summary = asm.summarize_results(results)
    score = int(summary["total_score"])
    score_text = (
        f"{format_score(summary['total_score'])} / "
        f"{format_score(summary['max_score'] or float(total))}"
    )
    if summary["pending_manual"]:
        score_text += f"（{int(summary['pending_manual'])} 题待人工评分）"
    return score, score_text


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

        selected = asm.row_value(answer, "selected_answer", "")
        correct = asm.row_value(answer, "correct_answer", "")
        needs_manual_grading = bool(asm.row_value(answer, "needs_manual_grading", 0))
        score = float(asm.row_value(answer, "score", int(answer["is_correct"])))
        max_score = float(asm.row_value(answer, "max_score", 1))
        options = question.get("options", {})
        rows.append(
            {
                "题号": question["id"],
                "题目": question["question"],
                "你的答案": asm.format_answer(selected, options),
                "参考答案": asm.format_answer(correct, options),
                "得分": f"{format_score(score)} / {format_score(max_score)}",
                "结果": (
                    "待人工评分"
                    if needs_manual_grading
                    else "正确"
                    if answer["is_correct"]
                    else "错误"
                ),
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
        _, score_text = score_summary(latest_answers, len(questions))
        st.info(f"最近一次{label}成绩：{score_text}")

    with st.form(f"{phase}_form"):
        selections: dict[str, Any] = {}
        for index, question in enumerate(questions, start=1):
            st.markdown(f"**{index}. {question['question']}**")
            q_type = asm.question_type(question)
            if q_type == asm.QUESTION_SINGLE:
                selections[question["id"]] = st.radio(
                    "选择答案",
                    option_labels(question),
                    index=None,
                    key=f"{phase}_{question['id']}",
                    label_visibility="collapsed",
                )
            elif q_type == asm.QUESTION_MULTIPLE:
                selections[question["id"]] = st.multiselect(
                    "选择答案",
                    option_labels(question),
                    key=f"{phase}_{question['id']}",
                    label_visibility="collapsed",
                )
            elif q_type == asm.QUESTION_SHORT:
                selections[question["id"]] = st.text_area(
                    "填写答案",
                    key=f"{phase}_{question['id']}",
                    label_visibility="collapsed",
                )
            else:
                st.error(f"不支持的题型：{q_type}")
                selections[question["id"]] = None

        submitted = st.form_submit_button(f"提交{label}")

    if submitted:
        missing = []
        for question in questions:
            value = selections.get(question["id"])
            if value is None or value == [] or (isinstance(value, str) and not value.strip()):
                missing.append(question["id"])
        if missing:
            st.warning("还有题目未作答，请完成所有题目后再提交。")
            return

        results = []
        for question in questions:
            value = selections[question["id"]]
            if asm.question_type(question) == asm.QUESTION_SINGLE:
                value = selected_key(str(value))
            elif asm.question_type(question) == asm.QUESTION_MULTIPLE:
                value = [selected_key(str(item)) for item in value]

            result = asm.grade_question(question, value)
            results.append(result)
            db.save_answer_result(conn, student_id, phase, result)

        if phase == "pretest":
            for node_id in asm.weak_node_ids(results):
                db.set_node_status(conn, student_id, node_id, kg.STATUS_WEAK)

        db.log_event(conn, student_id, f"{phase}_submitted", detail=f"提交{label}")
        st.success(f"{label}已提交。")
        st.rerun()

    latest_answers = db.get_latest_answers(conn, student_id, phase)
    if latest_answers:
        review_df = answer_review_dataframe(questions, latest_answers)
        with st.expander(f"查看最近一次{label}答题明细", expanded=False):
            st.dataframe(review_df, hide_index=True, use_container_width=True)


def node_label(node: dict[str, Any], statuses: dict[str, str]) -> str:
    status = kg.status_label(statuses.get(node["id"]))
    return f"L{node['level']} | {status} | {node['title']}"


def prerequisite_text(node: dict[str, Any], node_map: dict[str, dict[str, Any]]) -> str:
    titles = [
        node_map[item]["title"]
        for item in node.get("prerequisites", [])
        if item in node_map
    ]
    return "、".join(titles) if titles else "无"


def render_status_metrics(statuses: dict[str, str]) -> None:
    counts = {status: 0 for status in kg.STATUS_VALUES}
    for status in statuses.values():
        counts[kg.normalize_status(status)] += 1

    columns = st.columns(len(kg.STATUS_VALUES))
    for column, status in zip(columns, kg.STATUS_VALUES):
        column.metric(kg.STATUS_LABELS[status], counts[status])


def render_level_cards(
    grouped_nodes: dict[int, list[dict[str, Any]]],
    statuses: dict[str, str],
    node_map: dict[str, dict[str, Any]],
) -> None:
    for level, level_nodes in grouped_nodes.items():
        st.markdown(f"#### 第 {level} 层")
        columns = st.columns(min(3, len(level_nodes)))
        for index, node in enumerate(level_nodes):
            with columns[index % len(columns)]:
                with st.container(border=True):
                    st.markdown(f"**{node['title']}**")
                    st.caption(f"状态：{kg.status_label(statuses.get(node['id']))}")
                    st.write(node["learning_objective"])
                    st.caption(f"前置节点：{prerequisite_text(node, node_map)}")


def render_dict_or_text_item(item: Any) -> None:
    if isinstance(item, dict):
        if "misconception" in item or "correction" in item:
            st.write(f"- 误区：{item.get('misconception', '')}")
            st.caption(f"纠正：{item.get('correction', '')}")
            return
        if "prompt" in item or "answer" in item:
            st.write(f"- 练习：{item.get('prompt', '')}")
            st.caption(f"参考答案：{item.get('answer', '')}")
            return
        if "question" in item or "answer" in item:
            st.write(f"- 问题：{item.get('question', '')}")
            st.caption(f"参考答案：{item.get('answer', '')}")
            return
    st.write(f"- {item}")


def render_node_detail(
    conn: Any,
    student_id: Optional[int],
    node: dict[str, Any],
    node_map: dict[str, dict[str, Any]],
    current_status: str,
) -> None:
    st.markdown(f"### {node['title']}")
    st.caption(
        f"层级：{node['level']} | 当前状态：{kg.status_label(current_status)} | "
        f"前置节点：{prerequisite_text(node, node_map)}"
    )

    st.markdown("**学习目标**")
    st.write(node["learning_objective"])

    st.markdown("**知识解释**")
    st.write(node["explanation"])

    with st.expander("常见误区", expanded=True):
        for item in node["common_misconceptions"]:
            render_dict_or_text_item(item)

    with st.expander("练习", expanded=False):
        for item in node["exercises"]:
            render_dict_or_text_item(item)

    with st.expander("掌握度问题", expanded=False):
        for item in node["mastery_questions"]:
            render_dict_or_text_item(item)

    st.divider()
    if student_id is None:
        st.info("当前没有学生记录，所有节点默认显示为“未学习”。如需保存节点状态，请先在左侧登记学生信息。")
        return

    labels = list(kg.STATUS_LABELS.values())
    current_label = kg.status_label(current_status)
    selected_label = st.selectbox(
        "更新节点状态",
        labels,
        index=labels.index(current_label),
        key=f"status_{node['id']}",
    )
    note = st.text_area("学习备注（可选）", key=f"note_{node['id']}")

    if st.button("保存节点状态", type="primary"):
        new_status = kg.LABEL_TO_STATUS[selected_label]
        db.set_node_status(conn, student_id, node["id"], new_status)
        db.log_event(
            conn,
            student_id,
            "node_status_updated",
            node_id=node["id"],
            detail=f"{node['title']} -> {selected_label}; {note.strip()}",
        )
        st.success("节点状态已保存。")
        st.rerun()


def render_skill_tree(
    conn: Any,
    student_id: Optional[int],
    nodes: list[dict[str, Any]],
) -> None:
    st.subheader("知识图谱 / 技能树")
    st.write("节点按层级展示。每个节点状态从 SQLite 读取；未选择学生时，默认全部为“未学习”。")

    statuses = get_statuses(conn, student_id, nodes)
    node_map = {node["id"]: node for node in nodes}
    grouped_nodes = kg.group_nodes_by_level(nodes)

    render_status_metrics(statuses)

    mastered_count = sum(
        1 for status in statuses.values() if kg.normalize_status(status) == kg.STATUS_MASTERED
    )
    st.progress(mastered_count / len(nodes), text=f"已掌握进度：{mastered_count} / {len(nodes)}")

    overview_rows = []
    for node in nodes:
        overview_rows.append(
            {
                "层级": node["level"],
                "节点": node["title"],
                "状态": kg.status_label(statuses.get(node["id"])),
                "前置节点": prerequisite_text(node, node_map),
                "学习目标": node["learning_objective"],
            }
        )

    st.dataframe(pd.DataFrame(overview_rows), hide_index=True, use_container_width=True)
    render_level_cards(grouped_nodes, statuses, node_map)

    selected_node_id = st.selectbox(
        "查看节点详情",
        [node["id"] for node in nodes],
        format_func=lambda node_id: node_label(node_map[node_id], statuses),
    )
    render_node_detail(
        conn,
        student_id,
        node_map[selected_node_id],
        node_map,
        statuses.get(selected_node_id, kg.STATUS_NOT_STARTED),
    )


def report_metric_columns(
    pre_answers: list[Any],
    post_answers: list[Any],
    pre_total: int,
    post_total: int,
    mastered_count: int,
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
    col3.metric("已掌握节点", f"{mastered_count} / {node_total}")


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

    statuses = get_statuses(conn, student_id, nodes)
    pre_answers = db.get_latest_answers(conn, student_id, "pretest")
    post_answers = db.get_latest_answers(conn, student_id, "posttest")
    mastered_count = sum(
        1 for status in statuses.values() if kg.normalize_status(status) == kg.STATUS_MASTERED
    )

    report_metric_columns(
        pre_answers,
        post_answers,
        len(questions["pretest"]),
        len(questions["posttest"]),
        mastered_count,
        len(nodes),
    )

    st.markdown("**节点状态**")
    status_df = pd.DataFrame(
        [
            {
                "层级": node["level"],
                "节点": node["title"],
                "状态": kg.status_label(statuses.get(node["id"])),
                "学习目标": node["learning_objective"],
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


def require_student_message(action: str) -> None:
    st.info(f"请先在左侧填写学生信息并进入实验，然后再进行{action}。")


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

    tab_pretest, tab_tree, tab_posttest, tab_report = st.tabs(
        ["前测", "知识图谱", "后测", "学习报告"]
    )

    with tab_pretest:
        if student_id is None:
            require_student_message("前测")
        else:
            render_quiz(conn, student_id, "pretest", questions["pretest"])

    with tab_tree:
        render_skill_tree(conn, student_id, nodes)

    with tab_posttest:
        if student_id is None:
            require_student_message("后测")
        else:
            render_quiz(conn, student_id, "posttest", questions["posttest"])

    with tab_report:
        if student_id is None:
            require_student_message("学习报告查看")
        else:
            render_report(conn, student_id, nodes, questions)


if __name__ == "__main__":
    main()
