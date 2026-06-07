# MVP 开发计划与 Codex 项目管理

最后更新：2026-06-07

## 1. 当前开发目标

当前开发目标已经从“实现 v0.2 推理式学习页面”转为：

> 验收并稳定 v0.2 推理式学习原型，使其能支撑 1—3 人内部试跑。

本次代码审查确认：

1. v0.1 基础测试流程仍存在：前测、旧节点学习页、后测、报告、CSV 导出。
2. v0.2 核心结构已经存在：40 个微节点、5 条推理链、`src/graph.py`、`pages/3_ReasoningLesson.py`。
3. 当前不应继续扩功能，而应先做本地完整流程验收、内容质量检查、测试补齐和试跑准备。

## 2. 技术栈

当前实际技术栈：

```text
Python 3.10+
Streamlit
SQLite
YAML
pandas
PyYAML
```

当前 `requirements.txt` 实际包含：

```text
streamlit>=1.35
pandas>=2.2
PyYAML>=6.0
```

当前已有测试文件：

```text
tests/test_diagnosis.py
```

注意：文档原先提到 `pytest`，但当前 `requirements.txt` 尚未声明 pytest。短期可以继续用：

```bash
python tests/test_diagnosis.py
python -m compileall -q app.py pages src tests
```

如果后续要正式使用 pytest，需要把 `pytest` 加入开发依赖或 requirements。

## 3. 当前实际项目目录

本次代码审查确认的当前目录结构如下：

```text
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── knowledge_graph.yaml          # 40 个微知识节点，5 条推理链
│   ├── questions.yaml                # 前测/后测题库，各 10 题
│   └── skilltree_finance.sqlite3     # 本地 SQLite 数据库
├── pages/
│   ├── 1_Pretest.py
│   ├── 3_LearnNode.py                # 旧节点学习页，依靠兼容字段读取新图谱
│   ├── 3_ReasoningLesson.py          # v0.2 推理式学习页
│   ├── 4_Posttest.py
│   └── 5_Report.py
├── src/
│   ├── assessment.py                 # 题型、评分、统计
│   ├── content.py                    # YAML 加载
│   ├── database.py                   # SQLite 表、迁移和读写
│   ├── diagnosis.py                  # 本地规则诊断
│   ├── graph.py                      # v0.2 推理图谱读取、校验、查询
│   └── knowledge_graph.py            # 对 graph.py 的兼容封装
├── tests/
│   └── test_diagnosis.py
└── docs/
    ├── 00_README_文档维护说明.md
    ├── 01_PROJECT_CONTEXT.md
    ├── 02_PRODUCT_AND_LEARNING_DESIGN.md
    ├── 03_MVP_DEVELOPMENT_PLAN.md
    ├── 04_EXPERIMENT_PLAN.md
    ├── 05_BUSINESS_ROADMAP.md
    └── 06_DECISION_LOG_AND_OPEN_QUESTIONS.md
```

原计划中的 `2_SkillTree.py`、`6_Admin.py`、`analysis/`、`exports/` 当前尚未实现，不应在验收时当作已有功能。

## 4. 版本路线

### v0.1：基础实验原型（已基本完成）

目标：系统能跑通基础测评流程。

已实现功能：

```text
学生登记
前测
旧节点学习页
规则诊断
后测
报告
CSV 导出
SQLite 存储
```

验收状态：代码结构已具备，但仍需要用一个测试学生完整走一遍确认没有页面级错误。

### v0.2：推理式学习重构版（最小原型已完成，待本地验收）

目标：从测试系统升级为真正学习系统。

已实现功能：

```text
knowledge_graph.yaml 已重构为 40 个微节点
5 条核心财报推理链，每条 8 个节点
新增字段：core_question、scenario、guiding_questions、rule_summary、expected_reasoning_points 等
新增 src/graph.py
新增 pages/3_ReasoningLesson.py
记录学生自我解释
基于 expected_reasoning_points 做 60% 命中判定
通过后展示 derives 指向的下一节点
```

待验收标准：

1. 5 条推理链都可以在页面中打开。
2. 每条链 8 个节点都能正常展示。
3. 学生可以提交解释，系统能保存到 `node_learning_records`。
4. 通过/未通过能正确更新 `node_status`。
5. 报告页能展示学习记录，不因新字段或新记录类型报错。
6. 至少一名测试学生可以完整完成前测 → 推理式学习 → 后测 → 报告。

### v0.3：实验稳定版（下一阶段）

目标：让 1—3 名同学稳定完成内部试跑，再扩展到 6—12 人小规模验证。

下一阶段重点功能：

```text
数据完整性检查
反馈问卷
学习流程说明页或实验手册
知识图谱结构测试
推理评分函数测试
题目 node_id 映射测试
README 与 docs 同步
必要时弱化或隐藏旧 LearnNode 页面
```

验收标准：

1. 同学使用过程中不容易卡住。
2. 数据不丢失，关键数据可导出。
3. 实验负责人能判断每个学生完成了哪些链、哪些节点薄弱。
4. 试跑后能形成明确的 bug 清单、内容问题清单和下一轮改进清单。

### v0.4：数据分析与演示版

目标：支持实验分析和展示。

重点功能：

```text
分析脚本
前后测提升统计
错因统计
薄弱节点统计
学习报告示例
轻量 UI 优化
Demo 数据
```

验收标准：

1. 能生成实验总结报告。
2. 能展示系统价值。
3. 能支持创业路演或项目介绍。

## 5. Codex 使用原则

你负责：

```text
产品目标
实验设计
知识质量判断
开发任务拆分
验收标准
商业判断
```

Codex 负责：

```text
代码实现
修复 bug
重构模块
生成测试
写 README
生成分析脚本
解释代码 diff
```

Codex 不应该负责：

```text
决定商业方向
随意扩大功能范围
自动修改实验设计
自行更改知识内容逻辑
引入复杂架构
```

## 6. 每次给 Codex 的任务格式

每个任务应包含：

```text
任务标题
背景
目标
具体要求
不能做什么
验收标准
完成后需要说明什么
```

当前阶段的任务应该尽量围绕“验收、修复、补测试”，不要继续扩大功能范围。

示例：

```text
任务：补充 v0.2 推理式学习原型的最小测试

背景：当前系统已经有 40 个微知识节点、5 条推理链和 ReasoningLesson 页面。为了进入 1—3 人内部试跑，需要先确保数据结构、题目映射和基础评分逻辑稳定。

目标：为当前 v0.2 原型补充最小自动化测试。

要求：
1. 新增知识图谱加载测试：应能加载 40 个节点、5 条链；
2. 新增边校验测试：所有 prerequisites 和 derives 都必须指向存在的节点；
3. 新增题目映射测试：pretest/posttest 中每道题的 node_id 都必须存在于 knowledge_graph.yaml；
4. 新增推理评分测试：至少覆盖一个通过案例和一个不通过案例；
5. 保留原有 tests/test_diagnosis.py。

不能做：
1. 不接入 OpenAI API；
2. 不重构页面 UI；
3. 不改变知识点内容；
4. 不引入复杂测试框架，除非同步更新 requirements 和运行说明。

验收标准：
1. python tests/test_diagnosis.py 通过；
2. python -m compileall -q app.py pages src tests 通过；
3. 新增测试可以在本地稳定运行；
4. 测试失败时能明确指出是哪个节点或题目映射有问题。

完成后需要说明：
1. 新增或修改了哪些测试文件；
2. 每个测试覆盖什么风险；
3. 运行命令是什么；
4. 还有哪些页面级流程必须手动验收。
```

## 7. Git 工作流

每次修改前先 checkpoint：

```bash
git status
git add .
git commit -m "checkpoint before v0.2 acceptance fixes"
```

每次修改后至少运行：

```bash
python tests/test_diagnosis.py
python -m compileall -q app.py pages src tests
python -c "from pathlib import Path; from src import graph; nodes = graph.load_knowledge_graph(Path('data/knowledge_graph.yaml')); print(len(nodes), len(graph.group_nodes_by_chain(nodes)))"
```

如果后续加入 pytest，再运行：

```bash
pytest
```

页面级验收仍需要手动执行：

```bash
streamlit run app.py
```

验收通过后：

```bash
git add .
git commit -m "stabilize v0.2 reasoning lesson prototype"
```

建议在完成 1—3 人内部试跑后再打 tag：

```bash
git tag v0.2-acceptance
```

## 8. 当前最应该给 Codex 的任务

```text
任务：v0.2 推理式学习原型验收与稳定化

背景：当前项目已经完成 v0.2 最小原型：knowledge_graph.yaml 已包含 40 个微知识节点和 5 条推理链，src/graph.py 与 pages/3_ReasoningLesson.py 已存在。现在不要继续扩功能，先确保系统能稳定支持 1—3 人内部试跑。

目标：跑通并加固完整学习闭环：前测 → 推理式学习 → 后测 → 报告 → CSV 导出。

具体要求：
1. 不删除现有前测、后测、报告功能。
2. 检查 3_ReasoningLesson.py 是否能正常展示 5 条链、40 个节点。
3. 检查学生提交推理回答后，node_learning_records 是否保存 answer、correct_answer、is_correct、duration_seconds、recommended_node_id。
4. 检查 node_status 是否能在通过时变为 mastered、未通过时变为 weak。
5. 检查 5_Report.py 是否能展示推理式学习记录，不因 item_type=reasoning 或 step_type=reasoning_mastery 报错。
6. 新增最小测试：
   - graph 加载应得到 40 个节点、5 条链；
   - 每个 prerequisite 和 derives 都指向存在的节点；
   - pretest/posttest 每道题的 node_id 都能在 knowledge_graph.yaml 中找到；
   - expected_reasoning_points 简单匹配函数至少覆盖通过和不通过两个案例。
7. 更新 README 中明显过时的部分：节点数量、目录结构、3_ReasoningLesson.py、src/graph.py。

不能做：
1. 不接入 OpenAI API。
2. 不做复杂 UI。
3. 不新增登录、支付、云部署。
4. 不把 v0.3/v0.4 功能混入本次任务。

验收标准：
1. python tests/test_diagnosis.py 通过。
2. python -m compileall -q app.py pages src tests 通过。
3. graph 加载测试输出 40 个节点、5 条链。
4. 手动新建一个测试学生，可以完成前测、至少一条推理链、后测、报告。
5. 报告页可以导出 CSV。
6. 完成后列出修改文件、已验证项目、仍存在限制。
```

当前 Codex 任务的核心不是“做更多”，而是“把已经做出的 v0.2 变成可验收、可试跑的版本”。

## 9. 暂缓开发事项

以下事项暂缓：

```text
复杂 UI 美化
排行榜
游戏商城
移动端 App
云部署
用户注册登录
支付
大模型深度 Agent
全学科扩展
K12 正式商业化
```

原因：当前最关键的是验证学习机制，而不是扩展功能。
