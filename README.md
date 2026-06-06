# skilltree-finance

## 1. 项目简介

`skilltree-finance` 是一个基于 Python + Streamlit 的本地教育实验 MVP，主题为“AI 技能树财务报表学习实验系统”。

系统面向零基础学生，围绕基础财务报表知识构建技能树学习路径，记录学生的前测、节点学习、后测、诊断反馈和学习报告。项目第一版只在本地运行，使用 SQLite 存储数据，不接入真实支付、登录、云服务或外部数据库。

项目默认使用的 conda 环境名称为：

```powershell
skilltree
```

## 2. 实验目标

本项目用于支持一个完整的教育实验流程，核心目标包括：

- 评估学生在学习前对基础财务报表知识的掌握情况。
- 通过 20 个知识节点构建财务报表技能树。
- 记录学生在每个节点上的学习行为、练习答案、用时和掌握状态。
- 根据错题和掌握验证结果识别薄弱知识点。
- 使用规则系统诊断错误类型，并推荐回退学习节点。
- 比较前测和后测表现，观察学习效果。
- 生成可导出的学习报告，为教师或研究者提供分析依据。

## 3. 功能列表

当前版本包含以下功能：

- 学生信息登记：姓名、学号、班级。
- 知识图谱 / 技能树：从 YAML 读取 20 个财务报表学习节点。
- 节点状态管理：支持“未学习、学习中、已掌握、薄弱、需要复习”。
- 前测功能：支持单选题、多选题、简答题。
- 自动评分：单选题和多选题自动评分。
- 人工评分预留：简答题第一版保存答案，暂按待人工评分处理。
- 节点学习：展示学习目标、解释、例题、常见误区和练习题。
- 掌握验证：答对掌握验证题后将节点标记为“已掌握”。
- 错误诊断：答错后调用本地规则系统，输出错误类型和推荐回退节点。
- 后测功能：覆盖与前测相同的知识节点，但题目不与前测完全相同。
- 前后测对比：展示总分提升、各节点提升、仍然薄弱的节点和建议复习节点。
- 学习报告：汇总完整学习记录、学习时长、节点状态、错误统计和复习建议。
- CSV 导出：支持导出多类学习数据表。
- 延迟测试预留：`answers.delayed_test` 字段已预留，用于一周后延迟测试。

## 4. 项目目录

```text
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── knowledge_graph.yaml
│   ├── questions.yaml
│   └── skilltree_finance.sqlite3      # 运行后自动生成，本地数据，不提交 Git
├── pages/
│   ├── 1_Pretest.py
│   ├── 3_LearnNode.py
│   ├── 4_Posttest.py
│   └── 5_Report.py
├── src/
│   ├── __init__.py
│   ├── assessment.py
│   ├── content.py
│   ├── database.py
│   ├── diagnosis.py
│   └── knowledge_graph.py
└── tests/
    └── test_diagnosis.py
```

主要文件说明：

- `app.py`：Streamlit 主入口。
- `pages/1_Pretest.py`：独立前测页面。
- `pages/3_LearnNode.py`：独立节点学习页面。
- `pages/4_Posttest.py`：独立后测页面。
- `pages/5_Report.py`：独立学习报告页面。
- `data/knowledge_graph.yaml`：知识图谱和技能树节点数据。
- `data/questions.yaml`：前测和后测题库。
- `src/content.py`：YAML 内容加载。
- `src/knowledge_graph.py`：知识节点校验、分层和状态定义。
- `src/assessment.py`：题型识别、答案序列化、自动评分和得分统计。
- `src/diagnosis.py`：本地规则诊断系统，不调用大模型。
- `src/database.py`：SQLite 初始化、迁移和数据读写。
- `tests/test_diagnosis.py`：诊断规则的简单测试脚本。

## 5. 安装方法

### 方式一：使用 conda 环境

如果尚未创建环境：

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

### 方式二：使用 Python venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

项目依赖写在 `requirements.txt` 中，主要包括：

- Streamlit
- pandas
- PyYAML

## 6. 运行方法

在项目根目录运行：

```powershell
conda activate skilltree
streamlit run app.py
```

启动后在浏览器打开 Streamlit 提供的地址，通常是：

```text
http://localhost:8501
```

首次运行时，系统会自动创建本地 SQLite 数据库：

```text
data/skilltree_finance.sqlite3
```

该数据库文件用于保存本地实验数据，默认不提交到 GitHub。

## 7. 实验流程

建议按以下顺序完成实验：

1. 登记学生信息

   在侧边栏填写学生姓名、学号和班级。系统会将学生信息保存到 SQLite。

2. 完成前测

   进入 `Pretest` 页面，完成前测题目。前测包含单选题、多选题和简答题。单选题、多选题自动评分，简答题保存答案等待人工评分。

3. 查看知识图谱

   在主页面或知识图谱区域查看 20 个财务报表学习节点。每个节点有层级、前置节点、学习目标和当前状态。

4. 进行节点学习

   进入 `LearnNode` 页面，选择一个知识节点，阅读学习目标、解释、例题和常见误区，并完成练习题与掌握验证题。

5. 接收诊断反馈

   如果掌握验证题答错，系统会调用 `src/diagnosis.py` 中的本地规则系统，诊断错误类型并推荐回退学习节点。

6. 完成后测

   进入 `Posttest` 页面，完成后测。后测覆盖与前测相同的一批知识节点，但题目不与前测完全相同。

7. 查看学习报告

   进入 `Report` 页面，选择学生后查看完整学习报告，包括前后测对比、学习时长、掌握节点数、薄弱节点、错误类型统计和推荐复习节点。

## 8. 数据导出说明

报告页使用 pandas 生成表格，并支持导出 CSV。

当前支持导出的数据包括：

- 节点得分对比 CSV
- 节点状态 CSV
- 薄弱节点 CSV
- 常见错误类型统计 CSV
- 推荐复习节点 CSV
- 完整答题记录 CSV
- 完整节点学习记录 CSV

导出的 CSV 使用 `utf-8-sig` 编码，便于在 Excel 中直接打开中文内容。

SQLite 中主要表如下：

- `students`：学生信息。
- `answers`：前测、后测和延迟测试预留答题记录。
- `node_status`：每个学生在每个知识节点上的学习状态。
- `node_learning_records`：节点练习、掌握验证题、学生答案、用时、错误类型和推荐节点。
- `learning_logs`：学习行为日志。

如果需要重置本地实验数据，可以删除数据库文件：

```powershell
Remove-Item -Path .\data\skilltree_finance.sqlite3
```

下次运行系统时会自动重新创建数据库。

## 9. 后续可扩展方向

后续可以从以下方向继续扩展：

- 增加教师端人工评分页面，用于批改简答题。
- 实现一周后延迟测试，使用已预留的 `delayed_test` 字段。
- 增加更丰富的题型，例如判断题、案例分析题和报表阅读题。
- 扩展知识图谱节点，从基础财务报表扩展到财务分析、估值和经营诊断。
- 优化错误诊断规则，引入更细粒度的错误标签和回退路径。
- 增加可视化图表，例如学习路径图、节点掌握热力图、前后测雷达图。
- 增加批量导出功能，支持按班级导出所有学生报告。
- 增加自动化测试，覆盖数据库迁移、评分逻辑、诊断逻辑和页面核心流程。
- 将本地 SQLite 替换为可选数据库后端，例如 PostgreSQL。
- 在合规前提下接入大模型，用于生成个性化解释、错因分析和复习计划。

## 测试

诊断模块包含简单测试脚本：

```powershell
conda activate skilltree
python tests/test_diagnosis.py
```

也可以直接运行模块自检：

```powershell
python src/diagnosis.py
```

## 免责声明

本项目用于教学实验和 MVP 验证，不应直接用于正式教学评价或高风险决策。请不要将包含真实隐私信息的数据库文件上传到公共仓库。
