# Synthetic Student Lab v0.3 Minimal Report

## 实验范围

- experiment_id: `ssl_v0_3_minimal`
- graph_version: `sha256:6b95d7ba7ba4`
- chain_id: `B. 从交易到利润表`
- nodes: 1
- personas: 3 (misconception_prone, novice_closed_book, rote_memorizer)
- conditions: 4 (chain_so_far, hidden_transfer, no_course_baseline, node_only)
- total_runs: 12
- graph_fallback_used_runs: 0

## 总体指标

| metric | value |
| --- | --- |
| rule_pass_rate | 0.0% |
| judge_pass_rate | 0.0% |
| hidden_transfer_judge_pass_rate | 0.0% |
| false_pass_count | 0 |
| false_fail_count | 0 |
| manual_review_count | 12 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gross_margin` | 毛利形成 | 12 | 100.0% | 100.0% | 0 | 0 | 0.00 |

## 评分冲突样本


### rule_fail_llm_pass

本次没有样本。
若后续出现样本，将逐条输出：node_id、condition、student_persona、question、student_answer、rule_score / judge_score、matched_reasoning_points、missing_reasoning_points、初步归因、课程或评分规则修改建议。

### rule_pass_llm_fail

本次没有样本。
若后续出现样本，将逐条输出：node_id、condition、student_persona、question、student_answer、rule_score / judge_score、matched_reasoning_points、missing_reasoning_points、初步归因、课程或评分规则修改建议。

## hidden transfer 表现

| node_id | title | judge_passes | avg_judge_score | failing_personas |
| --- | --- | --- | --- | --- |
| `gross_margin` | 毛利形成 | 0/3 | 0.00 | misconception_prone, novice_closed_book, rote_memorizer |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `gross_margin` | 毛利形成 | 0.750 | 100.0% | 100.0% | 0 | - |

## 课程修改建议

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

### 1. `gross_margin` 毛利形成
- 问题证据: hidden_transfer 通过率 0/3 (0.0%)；失败 persona: misconception_prone, novice_closed_book, rote_memorizer；top_tags: -；典型 missing_reasoning_points: {'aliases': ['毛利是3500', '毛利为3500', '毛利3500元', '10000减6500得到3500'], 'required': True, 'text': '本例毛利等于 10000 - 6500 = 3500 元'}:3；{'aliases': ['毛利率是35%', '毛利率为35%', '毛利率35%', '3500除以10000'], 'required': True, 'text': '本例毛利率等于 3500 / 10000 = 35%'}:3；{'aliases': ['还没扣销售费用', '还没扣管理费用', '还没扣期间费用', '未扣除期间费用', '还不是净利润'], 'required': True, 'text': '毛利还没有扣除销售管理研发财务等期间费用'}:3；典型学生回答片段: novice_closed_book: ；rote_memorizer: 
- 问题归因: expected_reasoning_points 在节点层面只描述公式，未强制本例金额、比例和期间费用三项同时出现；guiding_questions 没有先让学生列收入和销售成本，也没有追问毛利到净利润之间还要扣什么；mastery_question 只问“毛利率高不等于净利润高”，太弱，无法暴露只背公式或漏答期间费用。
- 新增 guiding_question: 本例收入是多少？销售成本是多少？请先写出毛利计算式。
- 新增 guiding_question: 毛利率的分母为什么是收入，而不是成本？
- 新增 guiding_question: 毛利和净利润之间还会扣除哪些期间费用？
- 修改 mastery_question 的具体方向: 改为要求学生同时写出毛利金额、毛利率、毛利尚未扣除的费用类型，例如：服装店收入 10000 元、销售成本 6500 元，请计算毛利和毛利率，并说明毛利距离净利润还少扣哪些费用。
- 修改 expected_reasoning_points: 本例毛利 = 10000 - 6500 = 3500 元
- 修改 expected_reasoning_points: 本例毛利率 = 3500 / 10000 = 35%
- 修改 expected_reasoning_points: 毛利还没有扣除销售、管理、研发、财务等期间费用
- 增加 common_misconceptions: 只写出毛利或毛利率公式，就等于完成案例计算。
- 增加 common_misconceptions: 算出毛利和毛利率后，就已经得到净利润。
- 新增变式案例: 新增一个餐饮店案例：收入 30000 元、食材直接成本 18000 元、另有店租和营销费，要求先算毛利和毛利率，再判断哪些费用尚未扣除。

高风险前三个节点中有节点缺少预设诊断模板，请先补充该节点的失败样本归因再改课程。

## 需要人工复核的样本

- run_id: `7961830d59dde736`
- node: `gross_margin` 毛利形成
- persona/condition: `novice_closed_book` / `no_course_baseline`
- rule/judge: 0.0 -> 0.0
- question: 为什么毛利率高不等于净利润一定高？
- answer: 
- missing: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- error: student_llm_error: LLM client is enabled but model, API key, or base URL is missing; judge_llm_error: LLM client is enabled but model, API key, or base URL is missing

- run_id: `974123e4486eed0f`
- node: `gross_margin` 毛利形成
- persona/condition: `novice_closed_book` / `node_only`
- rule/judge: 0.0 -> 0.0
- question: 为什么毛利率高不等于净利润一定高？
- answer: 
- missing: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- error: student_llm_error: LLM client is enabled but model, API key, or base URL is missing; judge_llm_error: LLM client is enabled but model, API key, or base URL is missing

- run_id: `4c8b7b3136628723`
- node: `gross_margin` 毛利形成
- persona/condition: `novice_closed_book` / `chain_so_far`
- rule/judge: 0.0 -> 0.0
- question: 为什么毛利率高不等于净利润一定高？
- answer: 
- missing: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- error: student_llm_error: LLM client is enabled but model, API key, or base URL is missing; judge_llm_error: LLM client is enabled but model, API key, or base URL is missing

- run_id: `57b3bc6bbc1b3fd2`
- node: `gross_margin` 毛利形成
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.0 -> 0.0
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- answer: 
- missing: {'aliases': ['毛利是3500', '毛利为3500', '毛利3500元', '10000减6500得到3500'], 'required': True, 'text': '本例毛利等于 10000 - 6500 = 3500 元'}；{'aliases': ['毛利率是35%', '毛利率为35%', '毛利率35%', '3500除以10000'], 'required': True, 'text': '本例毛利...
- error: student_llm_error: LLM client is enabled but model, API key, or base URL is missing; judge_llm_error: LLM client is enabled but model, API key, or base URL is missing

- run_id: `7d93bab8bf539651`
- node: `gross_margin` 毛利形成
- persona/condition: `rote_memorizer` / `no_course_baseline`
- rule/judge: 0.0 -> 0.0
- question: 为什么毛利率高不等于净利润一定高？
- answer: 
- missing: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- error: student_llm_error: LLM client is enabled but model, API key, or base URL is missing; judge_llm_error: LLM client is enabled but model, API key, or base URL is missing

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 当前 mock judge 用于验证数据流和报告结构，不等价于真实语义评分。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
