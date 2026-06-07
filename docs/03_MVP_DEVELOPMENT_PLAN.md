# MVP 开发计划与 Codex 项目管理

最后更新：2026-06-07

## 1. 当前开发目标

当前开发目标已经从“实现 v0.2 推理式学习页面”转为：

> 在 v0.2 功能验收通过的基础上，进入 v0.2.1 内部试用，验证推理式学习是否真正产生学习效果。

本次代码审查确认：

1. v0.1 基础测试流程仍存在：前测、旧节点学习页、后测、报告、CSV 导出。
2. v0.2 核心结构已经存在：40 个微节点、5 条推理链、`src/graph.py`、`pages/3_ReasoningLesson.py`。
3. v0.2 功能验收已经通过，当前不应继续扩功能，而应先做版本固化、README 同步、内部试用准备和学习效果观察。

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
    ├── 06_DECISION_LOG_AND_OPEN_QUESTIONS.md
    ├── 07_V0_2_ACCEPTANCE_REPORT.md
    ├── 08_LLM_API_ENHANCEMENT_PLAN.md
    └── 09_SYNTHETIC_STUDENT_LAB_PLAN.md
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

### v0.2：推理式学习重构版（功能验收已通过）

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

验收结果：已通过。

已确认：

1. 系统可以正常启动。
2. 5 条推理链都可以在页面中打开。
3. 每条链 8 个节点都能正常展示。
4. 学生可以提交解释，系统能保存到 `node_learning_records`。
5. 通过/未通过能正确更新 `node_status`。
6. 报告页能读取学习记录，不报错。
7. CSV 能正常导出。
8. 一个测试学生可以完整完成前测 → 推理式学习 → 后测 → 报告。
9. 本轮未发现页面 bug、内容跳步、评分误判。

### v0.2.1：内部试用版（当前阶段）

目标：不继续堆功能，而是用 1—3 名真实用户验证学习体验和学习效果。

重点任务：

```text
固化 v0.2 版本
同步 README 与 docs
准备内部试用记录表
收集前测/后测/学习时长/薄弱节点/主观反馈
记录解释不清、节点跳步、评分误判等内容问题
```

验收标准：

1. 至少 1 名真实用户完整完成学习流程。
2. 用户能独立完成前测 → 推理式学习 → 后测 → 报告。
3. 后测分数相比前测有提升，或能解释未提升原因。
4. 至少收集 5 条用户反馈。
5. 至少发现并记录 3 个可改进点，优先是内容层面问题而不是功能堆叠需求。
6. 能根据学习记录指出用户的薄弱节点。
7. 报告页对用户有解释价值，而不只是展示数据。

### v0.3：实验稳定版（v0.2.1 试用后再进入）

目标：让 1—3 名同学稳定完成内部试跑，再扩展到 6—12 人小规模验证。

下一阶段重点功能：

```text
数据完整性检查
反馈问卷
学习流程说明页或实验手册
数据完整性检查
反馈问卷
学习流程说明页或实验手册
知识图谱结构测试
推理评分函数测试
题目 node_id 映射测试
README 与 docs 同步
必要时弱化或隐藏旧 LearnNode 页面
离线 Synthetic Student Lab 最小实验：只测试 1 条推理链、3 类模拟学生，不进入学生主流程
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
Synthetic Student Lab 扩展到 5 条推理链并输出课程质量报告
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

由于 v0.2 功能验收已通过，建议现在即可打版本标签：

```bash
git tag v0.2
git push origin v0.2
```

完成 1—3 人内部试跑后，再视情况打：

```bash
git tag v0.2.1-internal-trial
```

## 8. 当前最应该给 Codex 的任务

```text
任务：v0.2.1 内部试用准备与 README/docs 同步

背景：v0.2 功能验收已经通过：系统启动、5 条推理链、40 个节点、推理回答提交、数据库写入、状态更新、报告页和 CSV 导出均已确认可用。现在不要继续扩功能，先把项目状态固化，并准备 1—3 人内部试用。

目标：把当前项目从“功能验收通过”推进到“可让真实用户试用并收集学习效果数据”。

具体要求：
1. 更新 README 中明显过时的部分：节点数量、目录结构、3_ReasoningLesson.py、src/graph.py、v0.2 验收状态。
2. 新增或同步 v0.2 验收报告文档。
3. 准备一份内部试用记录模板，至少包含：学生编号、前测分数、后测分数、学习链、学习时长、薄弱节点、主观反馈、发现的问题。
4. 不改变现有业务逻辑，除非发现阻塞内部试用的 bug。
5. 保留现有前测、推理学习、后测、报告、CSV 导出流程。
6. 补充最小测试时优先覆盖：图谱加载、边指向、题目 node_id 映射、推理评分通过/不通过案例。

不能做：
1. 不接入 OpenAI API。
2. 不做复杂 UI。
3. 不新增登录、支付、云部署。
4. 不扩大知识图谱规模。
5. 不把 v0.3/v0.4 功能混入本次任务。

验收标准：
1. README 与 docs 均明确写明：v0.2 功能验收已通过，当前进入 v0.2.1 内部试用。
2. python tests/test_diagnosis.py 通过。
3. python -m compileall -q app.py pages src tests 通过。
4. 至少一个测试学生仍可完整完成前测 → 推理式学习 → 后测 → 报告。
5. 内部试用记录模板可以直接用于 1—3 人试跑。
6. 完成后列出修改文件、已验证项目、仍存在限制。
```

当前 Codex 任务的核心不是“继续做更多功能”，而是“把已经验收通过的 v0.2 转成可试用、可记录、可复盘的 v0.2.1”。

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
后台无限自治改图谱
全学科扩展
K12 正式商业化
```

原因：当前最关键的是验证学习机制，而不是扩展功能。

## 11. 大模型 API 增强层开发计划

当前系统不需要依赖大模型 API 才能运行。DeepSeek/其他大模型 API 应作为可关闭、可回退、可审计的增强层接入。

### 11.1 推荐新增模块

如果进入 LLM Shadow Evaluator 开发，建议新增：

```text
src/llm_client.py          # 统一封装 DeepSeek/OpenAI 等 API 调用
src/llm_evaluator.py       # 解释题语义评分、错因分类、反馈生成
src/llm_prompts.py         # prompt 模板与版本管理
src/llm_schema.py          # JSON schema 校验与默认回退值
.env.example               # DEEPSEEK_API_KEY=，USE_LLM_EVALUATOR=false
```

### 11.2 推荐新增数据表

```text
llm_evaluation_records
```

建议字段：

```text
id
student_id
node_id
student_answer
rule_passed
llm_score
llm_passed
llm_matched_points
llm_missed_points
llm_misconception
llm_feedback
llm_confidence
model_name
prompt_version
raw_response
error_message
created_at
```

### 11.3 v0.2.1 最小实现范围

```text
1. 没有 API Key 时系统照常运行。
2. USE_LLM_EVALUATOR=false 时完全不调用外部 API。
3. 学生提交解释后，规则评分照常执行。
4. 如果开启 LLM，则额外生成影子评分。
5. 影子评分只写入 llm_evaluation_records，不改变 node_status。
6. API 失败、超时、JSON 解析失败时，记录错误并回退，不影响学生流程。
```

### 11.4 Codex 实现约束

给 Codex 的开发要求应明确：

```text
不要让 LLM 结果直接决定 mastered / weak。
不要把学生姓名、学号、班级等敏感信息发送给外部 API。
不要让模型自由输出非 JSON 内容。
不要把学生回答当成指令执行。
必须有 timeout、fallback、schema validation、prompt_version 记录。
必须能在无网络、无 API Key 条件下运行全部原有功能。
```

### 11.5 LLM Shadow Evaluator 验收标准

```text
1. 关闭 LLM 时，系统行为与当前 v0.2 完全一致。
2. 开启 LLM 且 API Key 有效时，每次解释题提交可生成一条影子评分记录。
3. LLM 返回结果能解析为固定 JSON。
4. 影子评分记录包含 node_id、student_answer、rule_result、llm_result、model_name、prompt_version。
5. API 调用失败不会阻断学生学习。
6. 至少收集 20 条回答，比较规则评分与 LLM 评分差异。
7. 人工复核冲突样本后，再决定是否在 v0.3 中启用正式 LLM 反馈。
```


## 12. Synthetic Student Lab 开发计划

本模块来自新的产品设想：用几个大模型模拟学生学习过程，并长期对学习系统进行压力测试，把失败样本反馈给课程结构和推理链设计。

### 12.1 当前阶段定位

当前不建议把它并入 v0.2.1 主流程。v0.2.1 的最高优先级仍是：

```text
1—3 名真实用户内部试跑
验证前后测提升
发现真实内容跳步和评分误判
```

Synthetic Student Lab 应作为 v0.3 起的离线开发者工具，先用于内容质检，而不是面向学生的功能。

### 12.2 推荐目录结构

```text
experiments/
└── synthetic_student_lab/
    ├── personas.yaml
    ├── run_simulation.py
    ├── run_adversarial_loop.py
    ├── judge.py
    ├── failure_analyzer.py
    ├── graph_patch_generator.py
    ├── regression_eval.py
    ├── prompts/
    │   ├── student_prompt.md
    │   ├── adversarial_student_prompt.md
    │   ├── judge_prompt.md
    │   ├── failure_analyzer_prompt.md
    │   └── graph_optimizer_prompt.md
    └── outputs/
        ├── simulation_runs.jsonl
        ├── node_failure_report.md
        ├── patch_suggestions.yaml
        └── regression_report.md
```

### 12.3 数据记录字段

```text
run_id
graph_version
chain_id
node_id
student_persona
student_model
judge_model
given_materials
student_answer
self_explanation
used_node_ids
matched_reasoning_points
missing_reasoning_points
judge_score
failure_type
suggested_fix
external_knowledge_suspicion
passed
cost_tokens
created_at
```

### 12.4 v0.3 最小实现范围

```text
1. 读取 data/knowledge_graph.yaml。
2. 读取 experiments/synthetic_student_lab/personas.yaml。
3. 支持至少 3 类模拟学生：零基础、死记硬背、误解型。
4. 只跑 1 条推理链，例如“利润不等于现金流”相关链条。
5. 每个节点生成学生回答和自我解释。
6. 使用规则评分 + LLM judge 评估推理覆盖。
7. 输出 node_failure_report.md。
8. 不自动修改正式 knowledge_graph.yaml。
```

### 12.5 v0.4 扩展范围

```text
1. 扩展到 5 条核心推理链。
2. 支持 5—8 类模拟学生画像。
3. 输出节点质量分、推理链自然度、迁移题难度和误判样本。
4. 生成 patch_suggestions.yaml，但仍需人工审核。
5. 修改候选图谱后自动跑回归测试。
```

### 12.6 不允许做的事

```text
不要让模拟学生结果直接覆盖正式知识图谱。
不要让同一个模型同时当学生、老师、裁判和优化器。
不要只看模拟学生通过率作为课程质量指标。
不要无成本上限地后台调用 API。
不要用模拟结果替代真实学生实验。
```

### 12.7 验收标准

最小验收：

```text
1. 能稳定跑完 1 条链 × 3 类学生画像。
2. 能输出每个节点的失败率和缺失推理点。
3. 能识别至少 3 类问题：节点过粗、前置缺失、验证题太浅、评分误判中的任意 3 类。
4. 生成的修改建议以候选报告形式保存，不直接改正式数据。
5. 人工判断至少 3 条建议具有参考价值。
```

更强验收：

```text
1. 修改候选图谱后，模拟失败率下降。
2. 隐藏迁移题表现不下降。
3. 真实学生试跑中至少能观察到部分模拟学生提前发现的问题。
4. 每次有效改进的 API 成本可统计、可控制。
```
