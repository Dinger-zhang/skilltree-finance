# skilltree-finance

`skilltree-finance` 是一个基于 Python + Streamlit + SQLite 的本地教育实验 MVP，主题为“AI 技能树财务报表学习实验系统”。

系统面向财务报表零基础或初学者，通过知识图谱、推理链、前后测、节点学习、诊断反馈和学习报告，记录学生从基础概念到报表理解的学习过程。当前版本只面向本地实验运行，不接入真实登录、支付、云服务、外部数据库或大模型 API。

默认推荐的 conda 环境名称：

```powershell
skilltree
```

## 当前状态

当前代码实现的是本地单机 MVP：

- 技术栈：Python、Streamlit、SQLite、pandas、PyYAML。
- 知识图谱：`data/knowledge_graph.yaml` 中维护 40 个财务报表原子知识节点。
- 推理链：节点按 5 条推理链组织，用于从概念、规则、分类到报表关系逐步推导。
- 测评题库：`data/questions.yaml` 中包含前测 10 题、后测 10 题。
- 数据存储：首次运行自动创建 `data/skilltree_finance.sqlite3`。
- 诊断方式：本地规则和关键词判断，不调用大模型。

## 功能

当前版本包含以下功能：

- 学生登记：记录姓名、学号、班级，并在 Streamlit session 中保持当前学生。
- 知识图谱展示：按层级展示节点、状态、前置节点和核心问题。
- 节点状态管理：支持“未学习、学习中、已掌握、薄弱、需要复习”。
- 前测：支持单选题、多选题、简答题；单选和多选自动评分，简答题保存为待人工评分。
- 普通节点学习：展示学习目标、解释、例题、常见误区、练习题和掌握验证题。
- 推理式学习：按推理链学习节点，提交推理回答后通过关键词命中情况判断是否通过。
- 错误诊断：答错后使用本地规则识别错误类型，并推荐回退或复习节点。
- 后测：覆盖与前测相同知识范围，题目与前测不完全重复。
- 前后测对比：展示总分、各节点提升、仍薄弱节点和复习建议。
- 学习报告：汇总学生信息、节点状态、答题记录、学习记录、错误统计和 CSV 导出。
- 数据导出：报告页支持导出多个 CSV 表，使用 `utf-8-sig` 编码便于 Excel 打开中文。
- 延迟测试字段预留：`answers.delayed_test` 已在数据库中预留，但页面流程尚未正式实现。

## 项目结构

```text
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── knowledge_graph.yaml
│   ├── questions.yaml
│   └── skilltree_finance.sqlite3      # 运行后自动生成，本地数据，不提交 Git
├── docs/
│   ├── 00_README_文档维护说明.md
│   ├── 01_PROJECT_CONTEXT.md
│   ├── 02_PRODUCT_AND_LEARNING_DESIGN.md
│   ├── 03_MVP_DEVELOPMENT_PLAN.md
│   ├── 04_EXPERIMENT_PLAN.md
│   ├── 05_BUSINESS_ROADMAP.md
│   └── 06_DECISION_LOG_AND_OPEN_QUESTIONS.md
├── pages/
│   ├── 1_Pretest.py
│   ├── 3_LearnNode.py
│   ├── 3_ReasoningLesson.py
│   ├── 4_Posttest.py
│   └── 5_Report.py
├── src/
│   ├── __init__.py
│   ├── assessment.py
│   ├── content.py
│   ├── database.py
│   ├── diagnosis.py
│   ├── graph.py
│   └── knowledge_graph.py
└── tests/
    └── test_diagnosis.py
```

主要文件说明：

- `app.py`：Streamlit 主入口，包含学生登记、技能树概览、简版测评和报告入口。
- `pages/1_Pretest.py`：前测页面，负责提交前测和写入薄弱节点状态。
- `pages/3_LearnNode.py`：普通节点学习页面，保存练习和掌握验证记录。
- `pages/3_ReasoningLesson.py`：推理式学习页面，按推理链推进节点学习。
- `pages/4_Posttest.py`：后测页面，包含前后测覆盖范围校验和对比展示。
- `pages/5_Report.py`：学习报告页面，支持查看学生报告和导出 CSV。
- `src/assessment.py`：题型识别、答案序列化、自动评分和得分统计。
- `src/content.py`：YAML 内容加载。
- `src/database.py`：SQLite 初始化、轻量迁移和数据读写。
- `src/diagnosis.py`：本地规则诊断系统。
- `src/graph.py`：v0.2 知识图谱 schema、推理链分组和图结构校验。
- `src/knowledge_graph.py`：兼容旧页面字段的知识图谱适配层和节点状态定义。
- `docs/`：项目上下文、产品设计、实验计划、商业路线和决策日志。

## 安装

### 使用 conda

```powershell
conda create -n skilltree python=3.10 -y
conda activate skilltree
pip install -r requirements.txt
```

如果环境已经存在：

```powershell
conda activate skilltree
pip install -r requirements.txt
```

### 使用 venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

依赖项见 `requirements.txt`：

- `streamlit`
- `pandas`
- `PyYAML`

## 运行

在项目根目录执行：

```powershell
conda activate skilltree
streamlit run app.py
```

浏览器打开 Streamlit 输出的地址，通常是：

```text
http://localhost:8501
```

首次运行会自动创建本地 SQLite 数据库：

```text
data/skilltree_finance.sqlite3
```

该文件保存本地实验数据，已通过 `.gitignore` 排除，不应提交到 Git。

## 建议实验流程

1. 登记学生信息。
2. 进入 `Pretest` 页面完成前测。
3. 在首页查看知识图谱、节点状态和薄弱节点。
4. 进入 `LearnNode` 页面进行普通节点学习与掌握验证。
5. 进入 `ReasoningLesson` 页面按推理链完成推理式学习。
6. 答错或未通过时，根据诊断反馈回到推荐节点复习。
7. 进入 `Posttest` 页面完成后测。
8. 进入 `Report` 页面查看学习报告并导出 CSV。

## 数据与导出

SQLite 主要表：

- `students`：学生信息。
- `answers`：前测、后测答题记录，以及延迟测试预留字段。
- `node_status`：每个学生在每个节点上的状态。
- `node_learning_records`：普通学习、掌握验证、推理式学习的作答记录。
- `learning_logs`：学生进入页面、提交测评、更新节点状态等行为日志。

报告页当前可导出：

- 节点得分对比 CSV。
- 节点状态 CSV。
- 薄弱节点 CSV。
- 常见错误类型统计 CSV。
- 推荐复习节点 CSV。
- 完整答题记录 CSV。
- 完整节点学习记录 CSV。

重置本地实验数据：

```powershell
Remove-Item -Path .\data\skilltree_finance.sqlite3
```

下次运行应用时数据库会自动重建。

## 测试

运行诊断模块测试：

```powershell
conda activate skilltree
python tests/test_diagnosis.py
```

也可以运行诊断模块自检：

```powershell
python src/diagnosis.py
```

当前测试重点覆盖本地诊断规则。数据库迁移、评分逻辑、页面流程尚未形成完整自动化测试，应作为后续补充方向。

## 文档维护

`docs/` 是项目长期上下文入口，建议按任务类型优先阅读：

- 总体方向：`docs/01_PROJECT_CONTEXT.md`。
- 学习机制和知识图谱：`docs/02_PRODUCT_AND_LEARNING_DESIGN.md`。
- 开发计划和技术实现：`docs/03_MVP_DEVELOPMENT_PLAN.md`。
- 实验设计：`docs/04_EXPERIMENT_PLAN.md`。
- 商业路线：`docs/05_BUSINESS_ROADMAP.md`。
- 决策记录和待解决问题：`docs/06_DECISION_LOG_AND_OPEN_QUESTIONS.md`。

文档维护规则见：`docs/00_README_文档维护说明.md`。

## 后续扩展方向

- 增加教师端人工评分页面，用于批改简答题。
- 实现一周后延迟测试流程，复用已预留的 `delayed_test` 字段。
- 增加更丰富题型，例如判断题、案例分析题和报表阅读题。
- 扩展知识图谱，从基础财务报表延伸到财务分析、估值和经营诊断。
- 优化推理式学习的答案判断，从关键词命中升级为更稳定的本地规则或可选模型评估。
- 增加可视化图表，例如推理链路径图、节点掌握热力图、前后测雷达图。
- 增加批量导出，支持按班级导出全部学生报告。
- 增加自动化测试，覆盖数据库迁移、评分逻辑、诊断逻辑和核心页面流程。
- 将本地 SQLite 替换为可选数据库后端，例如 PostgreSQL。
- 在合规前提下接入大模型，用于个性化解释、错因分析和复习计划。

## 免责声明

本项目用于教学实验和 MVP 验证，不应直接用于正式教学评价或高风险决策。请不要将包含真实隐私信息的数据库文件上传到公共仓库。
