from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

from src import assessment as asm
from src import database as db
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


def format_score(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} 秒"
    minutes, remain_seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} 分 {remain_seconds} 秒"
    hours, remain_minutes = divmod(minutes, 60)
    return f"{hours} 小时 {remain_minutes} 分"


def row_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def student_label(student: dict[str, Any]) -> str:
    code = student["student_code"] or "-"
    class_name = student["class_name"] or "-"
    return f"{student['name']} | 学号：{code} | 班级：{class_name} | id={student['id']}"


def select_student(conn: Any) -> Optional[int]:
    students = row_dicts(db.get_students(conn))
    if not students:
        st.info("暂无学生记录。请先完成前测或节点学习。")
        return None

    students_by_id = {int(student["id"]): student for student in students}
    student_ids = list(students_by_id)
    current_id = st.session_state.get("student_id")
    default_index = 0
    if current_id:
        try:
            default_index = student_ids.index(int(current_id))
        except ValueError:
            default_index = 0

    selected_id = st.selectbox(
        "选择学生",
        student_ids,
        index=default_index,
        format_func=lambda student_id: student_label(students_by_id[int(student_id)]),
    )
    st.session_state["student_id"] = int(selected_id)
    return int(selected_id)


def latest_phase_results(conn: Any, student_id: int, phase: str) -> list[dict[str, Any]]:
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


def node_title_map(nodes: list[dict[str, Any]]) -> dict[str, str]:
    return {node["id"]: node["title"] for node in nodes}


def node_score_map(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["node_id"]: item for item in asm.knowledge_point_scores(results)}


def node_is_weak(item: dict[str, Any] | None) -> bool:
    if not item:
        return False
    return float(item["score"]) < float(item["max_score"])


def node_status_dataframe(
    statuses: dict[str, str],
    nodes: list[dict[str, Any]],
) -> pd.DataFrame:
    titles = node_title_map(nodes)
    rows = []
    for node in nodes:
        node_id = node["id"]
        rows.append(
            {
                "node_id": node_id,
                "知识节点": titles.get(node_id, node_id),
                "层级": node["level"],
                "状态": kg.status_label(statuses.get(node_id)),
            }
        )
    return pd.DataFrame(rows)


def node_comparison_dataframe(
    pre_results: list[dict[str, Any]],
    post_results: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
) -> pd.DataFrame:
    titles = node_title_map(nodes)
    pre_scores = node_score_map(pre_results)
    post_scores = node_score_map(post_results)
    all_node_ids = sorted(set(pre_scores) | set(post_scores))
    rows = []

    for node_id in all_node_ids:
        pre_item = pre_scores.get(node_id)
        post_item = post_scores.get(node_id)
        pre_score = float(pre_item["score"]) if pre_item else 0.0
        post_score = float(post_item["score"]) if post_item else 0.0
        rows.append(
            {
                "node_id": node_id,
                "知识节点": titles.get(node_id, node_id),
                "前测得分": pre_score,
                "后测得分": post_score,
                "提升": post_score - pre_score,
                "前测满分": float(pre_item["max_score"]) if pre_item else 0.0,
                "后测满分": float(post_item["max_score"]) if post_item else 0.0,
                "仍薄弱": "是" if node_is_weak(pre_item) and node_is_weak(post_item) else "否",
                "待人工评分": int((pre_item or {}).get("pending_manual", 0))
                + int((post_item or {}).get("pending_manual", 0)),
            }
        )

    return pd.DataFrame(rows)


def weak_nodes_dataframe(
    statuses: dict[str, str],
    comparison_df: pd.DataFrame,
    nodes: list[dict[str, Any]],
) -> pd.DataFrame:
    titles = node_title_map(nodes)
    weak_ids = set()
    for node_id, status in statuses.items():
        if kg.normalize_status(status) in {kg.STATUS_WEAK, kg.STATUS_REVIEW}:
            weak_ids.add(node_id)

    if not comparison_df.empty:
        weak_ids.update(comparison_df.loc[comparison_df["仍薄弱"] == "是", "node_id"].tolist())

    rows = [
        {
            "node_id": node_id,
            "知识节点": titles.get(node_id, node_id),
            "当前状态": kg.status_label(statuses.get(node_id)),
        }
        for node_id in sorted(weak_ids)
    ]
    return pd.DataFrame(rows)


def recommended_review_dataframe(
    weak_df: pd.DataFrame,
    nodes: list[dict[str, Any]],
    learning_df: pd.DataFrame,
) -> pd.DataFrame:
    graph = {node["id"]: node for node in nodes}
    titles = node_title_map(nodes)
    recommended_ids = []

    if not learning_df.empty and "recommended_node_id" in learning_df.columns:
        recommended_ids.extend(
            item for item in learning_df["recommended_node_id"].dropna().tolist() if item
        )

    if not weak_df.empty:
        for node_id in weak_df["node_id"].tolist():
            recommended_ids.append(node_id)
            recommended_ids.extend(graph.get(node_id, {}).get("prerequisites", []))

    seen = set()
    rows = []
    for node_id in recommended_ids:
        if node_id in seen:
            continue
        seen.add(node_id)
        rows.append(
            {
                "node_id": node_id,
                "推荐复习节点": titles.get(node_id, node_id),
                "原因": "薄弱节点或其前置节点",
            }
        )
    return pd.DataFrame(rows)


def error_stats_dataframe(learning_df: pd.DataFrame) -> pd.DataFrame:
    if learning_df.empty or "error_type" not in learning_df.columns:
        return pd.DataFrame(columns=["错误类型", "次数"])

    filtered = learning_df[learning_df["error_type"].fillna("") != ""]
    if filtered.empty:
        return pd.DataFrame(columns=["错误类型", "次数"])

    return (
        filtered.groupby("error_type")
        .size()
        .reset_index(name="次数")
        .rename(columns={"error_type": "错误类型"})
        .sort_values("次数", ascending=False)
    )


def total_learning_seconds(learning_df: pd.DataFrame) -> int:
    if learning_df.empty or "duration_seconds" not in learning_df.columns:
        return 0
    return int(pd.to_numeric(learning_df["duration_seconds"], errors="coerce").fillna(0).sum())


def answers_dataframe(rows: list[Any]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(row_dicts(rows))


def learning_dataframe(rows: list[Any]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(row_dicts(rows))


def build_summary_text(
    student: Any,
    mastered_count: int,
    weak_df: pd.DataFrame,
    recommended_df: pd.DataFrame,
    nodes: list[dict[str, Any]],
) -> str:
    titles = node_title_map(nodes)
    mastered_phrase = f"已掌握 {mastered_count} 个知识节点"

    if weak_df.empty:
        return f"该学生{mastered_phrase}，当前自动记录中未发现持续薄弱节点，可进入综合复盘和延迟测试阶段。"

    weak_titles = weak_df["知识节点"].head(3).tolist()
    weak_phrase = "、".join(weak_titles)
    review_titles = (
        recommended_df["推荐复习节点"].head(3).tolist()
        if not recommended_df.empty
        else weak_titles
    )
    review_phrase = "、".join(review_titles)
    student_name = student["name"] if student else "该学生"

    return (
        f"{student_name}{mastered_phrase}，但在{weak_phrase}上仍存在薄弱点。"
        f"建议优先复习{review_phrase}，并结合错题记录重新完成节点掌握验证。"
    )


def csv_download_button(label: str, df: pd.DataFrame, file_name: str) -> None:
    if df.empty:
        return
    st.download_button(
        label,
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name=file_name,
        mime="text/csv",
    )


def render_metrics(
    pre_summary: dict[str, float],
    post_summary: dict[str, float],
    total_seconds: int,
    mastered_count: int,
    weak_count: int,
) -> None:
    delta = post_summary["total_score"] - pre_summary["total_score"]
    col1, col2, col3 = st.columns(3)
    col1.metric("前测分数", score_text(pre_summary))
    col2.metric("后测分数", score_text(post_summary), delta=format_score(delta))
    col3.metric("分数提升", format_score(delta))

    col4, col5, col6 = st.columns(3)
    col4.metric("总学习时长", format_duration(total_seconds))
    col5.metric("已掌握节点数", mastered_count)
    col6.metric("薄弱节点数", weak_count)


def main() -> None:
    st.set_page_config(page_title="学习报告", layout="wide")
    st.title("学习报告")
    st.caption("读取学生完整学习记录，汇总前测、后测、节点学习、错误诊断和复习建议。")

    conn = get_connection()
    nodes = get_nodes()
    student_id = select_student(conn)
    if student_id is None:
        return

    student = db.get_student(conn, student_id)
    db.ensure_node_statuses(conn, student_id, nodes)
    statuses = db.get_node_statuses(conn, student_id)

    pre_results = latest_phase_results(conn, student_id, "pretest")
    post_results = latest_phase_results(conn, student_id, "posttest")
    pre_summary = score_summary(pre_results)
    post_summary = score_summary(post_results)

    all_answers_df = answers_dataframe(db.get_all_answers(conn, student_id))
    learning_df = learning_dataframe(db.get_all_node_learning_records(conn, student_id))
    comparison_df = node_comparison_dataframe(pre_results, post_results, nodes)
    status_df = node_status_dataframe(statuses, nodes)
    weak_df = weak_nodes_dataframe(statuses, comparison_df, nodes)
    recommended_df = recommended_review_dataframe(weak_df, nodes, learning_df)
    error_df = error_stats_dataframe(learning_df)

    mastered_count = sum(
        1 for status in statuses.values() if kg.normalize_status(status) == kg.STATUS_MASTERED
    )
    total_seconds = total_learning_seconds(learning_df)

    if student:
        st.write(
            f"学生：{student['name']}  "
            f"学号：{student['student_code'] or '-'}  "
            f"班级：{student['class_name'] or '-'}"
        )

    render_metrics(pre_summary, post_summary, total_seconds, mastered_count, len(weak_df))

    st.markdown("### 节点得分对比")
    st.dataframe(comparison_df, hide_index=True, use_container_width=True)
    csv_download_button("导出节点得分对比 CSV", comparison_df, f"student_{student_id}_node_scores.csv")

    st.markdown("### 节点状态")
    st.dataframe(status_df, hide_index=True, use_container_width=True)
    csv_download_button("导出节点状态 CSV", status_df, f"student_{student_id}_node_status.csv")

    st.markdown("### 薄弱节点")
    if weak_df.empty:
        st.success("当前没有识别到薄弱节点。")
    else:
        st.dataframe(weak_df, hide_index=True, use_container_width=True)
        csv_download_button("导出薄弱节点 CSV", weak_df, f"student_{student_id}_weak_nodes.csv")

    st.markdown("### 常见错误类型统计")
    if error_df.empty:
        st.write("暂无错误诊断记录。")
    else:
        st.dataframe(error_df, hide_index=True, use_container_width=True)
        csv_download_button("导出错误类型统计 CSV", error_df, f"student_{student_id}_error_stats.csv")

    st.markdown("### 推荐复习节点")
    if recommended_df.empty:
        st.success("当前没有额外推荐复习节点。")
    else:
        st.dataframe(recommended_df, hide_index=True, use_container_width=True)
        csv_download_button("导出推荐复习节点 CSV", recommended_df, f"student_{student_id}_review_nodes.csv")

    with st.expander("完整答题记录", expanded=False):
        st.dataframe(all_answers_df, hide_index=True, use_container_width=True)
        csv_download_button("导出完整答题记录 CSV", all_answers_df, f"student_{student_id}_answers.csv")

    with st.expander("完整节点学习记录", expanded=False):
        st.dataframe(learning_df, hide_index=True, use_container_width=True)
        csv_download_button(
            "导出完整节点学习记录 CSV",
            learning_df,
            f"student_{student_id}_node_learning.csv",
        )

    st.markdown("### 自然语言总结")
    st.info(build_summary_text(student, mastered_count, weak_df, recommended_df, nodes))


if __name__ == "__main__":
    main()
