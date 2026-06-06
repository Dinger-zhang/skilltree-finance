# skilltree-finance

AI 技能树财务报表学习实验系统 —— 一个用于课堂或自学的本地 Python + Streamlit 教学 MVP。帮助零基础学生通过“前测 → 技能树学习 → 后测 → 学习报告”流程掌握基础财务报表知识，并记录完整学习日志。

## 亮点

- 基于技能树的逐步解锁学习路径（20 个节点）
- 前测 / 后测题库与答题记录
- 本地 SQLite 数据库（不依赖外部服务）
- 学习日志与学习报告导出查看

## 快速开始（推荐）
注意：下面给出两种方式：Conda（项目中提到的）和 Python venv。

1. 克隆并进入项目根目录（假设你已将仓库克隆到本地）：
   ```powershell
   cd E:\program\skilltree-finance
   ```

2A. 使用 Conda（项目默认）
   ```powershell
   conda create -n skilltree python=3.10 -y
   conda activate skilltree
   pip install -r requirements.txt
   streamlit run app.py
   ```

2B. 使用 Python venv（无 Conda）
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   streamlit run app.py
   ```

3. 在浏览器打开（通常）：
   ```text
   http://localhost:8501
   ```

## 项目功能

- 学生信息登记（姓名、学号、班级）
- 前测与后测答题（记录得分）
- 基于前置关系的技能树（20 节点）逐步解锁学习
- 学习日志（进入系统、提交测试、完成节点、保存笔记等）
- 学习报告：前后测成绩对比、节点完成进度、答题明细、日志导出

## 项目结构（简要）
```
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── knowledge_graph.yaml
+│   ├── questions.yaml
│   └── skilltree_finance.sqlite3      # 运行后生成
├── pages/
│   └── 1_Pretest.py
└── src/
    ├── __init__.py
    ├── assessment.py
    ├── content.py
    ├── database.py
    └── knowledge_graph.py
```

说明：
- `app.py`：Streamlit 主入口
- `src/content.py`：解析并加载 YAML 内容（题库、知识图谱）
- `src/database.py`：SQLite 初始化与数据读写封装
- `src/assessment.py`：前测/后测题目逻辑与评分
- `src/knowledge_graph.py`：技能树节点与前置关系处理
- `data/knowledge_graph.yaml`：20 个财务报表学习节点定义
- `data/questions.yaml`：前测与后测题库

## 数据存储

- 使用本地 SQLite，首次运行会在 `data/` 下生成 `skilltree_finance.sqlite3`。
- 默认不追踪该文件（.gitignore），属于本地实验数据。
- 主要表：
  - `students`：学生信息
  - `answers`：答题记录（前测/后测）
  - `node_status`：每个节点的学习状态
  - `learning_logs`：学习行为日志

## 开发与调试
- 安装依赖：`pip install -r requirements.txt`
- 本地运行：`streamlit run app.py`
- 想快速清空/重置数据库（开发时常用，请先备份）：
  - 备份数据库文件（PowerShell）：
    ```powershell
    Copy-Item -Path .\data\skilltree_finance.sqlite3 -Destination .\data\skilltree_finance.sqlite3.bak
    ```
  - 删除数据库（下一次启动会重新创建）：
    ```powershell
    Remove-Item -Path .\data\skilltree_finance.sqlite3
    ```

## 配置与扩展
- 教学内容（节点、题目）用 YAML 管理，位于 `data/knowledge_graph.yaml` 与 `data/questions.yaml`，易于扩展。
- 如果要新增节点或调整前置关系，请编辑 `data/knowledge_graph.yaml`，并同步调整 `src/knowledge_graph.py` 中的解析/校验逻辑（如有必要）。

## 测试与质量
- 当前为教学 MVP，未包含自动化测试用例。建议按需添加单元测试（例如针对 `src/database.py` 与 `src/assessment.py` 的核心函数）。

## 贡献
欢迎提交 issue 或 pull request。请尽量：
- 提供重现步骤或复现数据（不含真实个人隐私）
- 对新增功能写明设计意图并附上简单示例
- 如果修改数据结构（DB 或 YAML），在 PR 描述中说明迁移步骤

## 许可与免责声明
本项目用于教学与实验目的。请勿在未经许可的情况下上传包含敏感或真实个人信息的数据到公共仓库。

