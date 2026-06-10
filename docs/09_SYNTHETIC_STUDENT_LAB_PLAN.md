# Synthetic Student Lab：模拟学生学习实验室计划

最后更新：2026-06-07

## 1. 结论

可以通过多个大模型模拟学生学习过程，让它们和 SkillTree Finance 学习系统形成长期对抗/自博弈式反馈闭环。

但该模块的准确定位不是“训练大模型参数”，也不是“让 AI 自动无限改课程”，而是：

> 用多类模拟学生持续压力测试知识图谱、推理链、引导问题、掌握验证题和评分规则，帮助课程设计者发现并修复学习路径中的结构性问题。

推荐名称：

```text
Synthetic Student Lab
模拟学生学习实验室
课程自博弈优化模块
```

## 2. 为什么需要这个模块

当前系统已经从“前测 → 做题 → 后测 → 报告”的测评形态，升级为“原子知识点 → 推理链 → 引导式问题 → 学生自我解释 → 掌握验证”的学习形态。

新的关键问题是：

```text
知识点是否真的足够原子？
前置关系是否完整？
推理链是否自然？
引导问题是否真的能引导学生推出结论？
掌握验证题是否能区分真理解和背诵？
评分规则是否容易被关键词欺骗？
学生失败后推荐的补救路径是否有效？
```

真实学生实验是最终标准，但真实实验成本高、周期慢。模拟学生可以先作为低成本课程质检器，在真实学生试用前提前发现明显问题。

## 3. 与真实学生实验的关系

模拟学生不能替代真实学生。

正确关系是：

```text
模拟学生：提前发现候选问题，生成课程改进建议。
真实学生：验证这些问题是否真实存在，判断改进是否真的提升学习效果。
```

如果模拟学生发现的问题能在真实学生试跑中被观察到，说明该模拟画像有价值。反之，如果模拟学生结果长期和真实学生不一致，就必须调整或降低该模拟画像/评估器的权重。

## 4. 与 LLM Shadow Evaluator 的区别

```text
LLM Shadow Evaluator：评估真实学生的回答。
Synthetic Student Lab：生成模拟学生的学习过程并评估课程结构。
```

二者可以共享部分底层模块，例如：

```text
llm_client.py
llm_prompts.py
llm_schema.py
评分 rubric
expected_reasoning_points
JSON schema 校验
prompt_version 记录
```

但它们的实验目的不同，不能混为一谈。

## 5. 模拟学生画像

第一版建议至少包含 3 类画像：

```text
零基础学生：只依赖课程材料，材料不足时应回答“无法推出”。
死记硬背型学生：容易复述 rule_summary，但迁移题表现差。
误解型学生：容易混淆收入/收款、利润/现金流、资产/现金、资产/费用。
```

后续扩展到 5—8 类：

```text
跳步型学生：直接给结论，中间推理缺失。
聪明但急躁型学生：能猜对答案，但解释不完整。
迁移困难型学生：原案例会做，新案例不会。
反例挑战型学生：专门找规则边界和例外。
关键词堆砌型学生：堆出关键词但逻辑不成立。
```

## 6. 可以发现的问题类型

Synthetic Student Lab 应至少识别以下问题：

```text
node_too_coarse：节点过粗，包含多个认知问题。
missing_prerequisite：缺少前置节点或前置边。
derivation_gap：derives 关系跳步，学生难以自然推出下一节点。
weak_guiding_question：引导问题不能引出关键推理点。
weak_mastery_question：掌握题只测试复述，不测试迁移。
missing_misconception：常见误区没有覆盖。
false_pass：错误答案因关键词命中被误判通过。
poor_remediation：补救路径推荐无效。
external_knowledge_suspicion：模拟学生可能使用了课程外知识。
```

## 7. 推荐系统闭环

```text
当前 knowledge_graph.yaml
→ Synthetic Student Runner
→ 多类模拟学生按节点学习并回答
→ Judge 评估推理完整度
→ Failure Analyzer 归因失败原因
→ Graph Patch Generator 生成候选修改
→ Regression Eval 检查是否破坏其他节点
→ 输出 node_failure_report.md 与 patch_suggestions.yaml
→ 人工审核
→ 合并到正式知识图谱
```

注意：正式知识图谱不能被后台程序直接自动覆盖。

## 8. 如何降低大模型使用自身知识的影响

通用大模型本身可能已经知道财务知识，因此不能简单把“模型答对了”视为“课程教会了它”。

建议采用以下方法降低影响：

### 8.1 封闭知识模式

模拟学生 prompt 中要求：

```text
只能使用系统提供的节点材料。
如果材料不足，必须回答“无法从当前材料推出”。
不得使用自身已有知识补全课程缺口。
```

### 8.2 要求引用依据

模拟学生回答时必须标注：

```text
使用了哪些 node_id
依据了哪些 rule_summary
覆盖了哪些 expected_reasoning_points
哪些地方无法从材料推出
```

如果回答中出现课程材料没有提供的高级概念，应标记为 `external_knowledge_suspicion=true`。

### 8.3 无课程 baseline

同一任务先让模拟学生不看课程直接答题，再让它学习课程后答题。

比较：

```text
baseline_score
learned_score
transfer_score
```

如果 baseline 已经很高，说明该题不能证明课程贡献。

### 8.4 隐藏迁移题

不能只用模型刚看过的题。需要准备新案例，用来测试是否能迁移。

### 8.5 虚构知识体系

必要时构造现实不存在的伪领域，例如：

```text
蓝石账户
红叶资源
银线负债
三角现金流
```

如果系统能让模型在伪领域完成推理，才更能说明“原子知识点 + 推理链 + 掌握验证”机制本身有效。

## 9. 后台长期运行原则

可以长期后台运行，但必须是受控运行。

允许：

```text
定时运行模拟学习
生成失败报告
生成候选修改建议
进行回归测试
提交待审核 patch
统计 API 成本
比较修改前后效果
```

不允许：

```text
无限循环调用 API
自动覆盖正式 knowledge_graph.yaml
用模拟学生通过率替代真实学习效果
同一个模型同时当学生、judge 和优化器
没有隐藏测试集就合并修改
没有人工审核就上线课程内容
```

推荐运行策略：

```text
v0.3：手动运行，只测试 1 条链。
v0.4：每次知识图谱大改后运行，测试 5 条链。
v0.5：每周或每次 PR 后自动运行，生成候选报告。
v1.0：结合真实学生数据校准模拟学生画像和 judge 权重。
```

## 10. 推荐技术目录

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

## 11. 核心数据字段

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

## 12. 核心指标

```text
Mastery Pass Rate：掌握题通过率
Transfer Score：迁移题得分
Reasoning Coverage：推理要点覆盖率
Prerequisite Failure Rate：前置知识失败率
Misconception Rate：误解率
False Pass Rate：错误答案被误判通过比例
Patch Improvement：修改前后提升幅度
Regression Damage：修改后其他节点是否变差
Cost per Improvement：每次有效改进的 API 成本
```

其中最重要的是：

```text
False Pass Rate
Transfer Score
Regression Damage
```

## 13. v0.3 最小可行实验

建议从最小实验开始，不要一开始做复杂后台系统。

范围：

```text
1 条推理链
3 类模拟学生
1 个 student_model
1 个 judge_model
规则评分 + LLM 评分
只输出报告，不修改正式图谱
```

流程：

```text
第 1 轮：模拟学生学习并答题。
第 2 轮：judge 评估失败原因。
第 3 轮：failure analyzer 归因。
第 4 轮：生成 node_failure_report.md。
第 5 轮：人工挑选 3 条建议修改知识图谱。
第 6 轮：重新运行模拟并比较修改前后。
```

最小验收标准：

```text
1. 能稳定跑完 1 条链 × 3 类学生画像。
2. 能输出每个节点的失败率、缺失推理点和失败原因。
3. 能识别至少 3 个有参考价值的课程问题。
4. 修改建议不直接覆盖正式 knowledge_graph.yaml。
5. 人工认为报告对课程迭代有帮助。
```

## 14. v0.4 扩展实验

扩展目标：

```text
5 条核心财报推理链
5—8 类模拟学生画像
多模型学生模拟
隐藏迁移题
候选 patch_suggestions.yaml
回归测试报告
```

验收标准：

```text
1. 能发现节点过粗、前置缺失、推理链跳步、评分误判等问题。
2. 修改候选图谱后，模拟失败率下降。
3. 隐藏迁移题表现不下降。
4. 至少部分模拟发现的问题能在真实学生试跑中被观察到。
5. API 成本、失败率、运行时间可统计。
```

## 15. 与商业化的关系

该模块如果验证有效，可以成为 SkillTree Builder 的重要差异化能力。

对外表达：

> 系统不仅能帮老师把课程变成技能树，还能在课程发布前用多类模拟学生自动试学，生成课程质量报告和改进建议。

商业价值：

```text
降低课程设计试错成本
帮助机构发现内容跳步
提高课程发布前质量
沉淀课程质量评估数据
形成学习路径优化闭环
```

它使 SkillTree 从“AI 课程生成工具”升级为：

> 可诊断、可验证、可迭代的学习路径引擎。

## 16. 当前建议

当前不应因为这个想法打断 v0.2.1 内部试用。

推荐顺序：

```text
第一步：完成 v0.2.1 真实用户内部试跑。
第二步：收集真实学生卡点和评分误判样本。
第三步：用这些真实样本设计 3 类模拟学生画像。
第四步：在 v0.3 中做 1 条链的离线模拟实验。
第五步：验证模拟报告是否真的能帮助修改课程。
第六步：确认有效后，再扩展到长期后台运行。
```

一句话：

> Synthetic Student Lab 是很有潜力的中期核心模块，但当前应先作为离线课程质检器，而不是立即做成无限后台自治优化系统。
