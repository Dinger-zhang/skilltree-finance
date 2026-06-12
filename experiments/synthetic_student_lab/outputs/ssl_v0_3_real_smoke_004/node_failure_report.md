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
| rule_pass_rate | 50.0% |
| judge_pass_rate | 66.7% |
| hidden_transfer_judge_pass_rate | 100.0% |
| false_pass_count | 0 |
| false_fail_count | 2 |
| manual_review_count | 2 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `revenue_not_cash_receipt` | 收入不等于收款 | 12 | 33.3% | 0.0% | 0 | 2 | 0.56 |

## 评分冲突样本


### rule_fail_llm_pass

1. node_id: `revenue_not_cash_receipt`
   condition: `chain_so_far`
   student_persona: `rote_memorizer`
   question: 赊销商品时，为什么可能确认收入但现金没有增加？
   student_answer: 规则说，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。
   rule_score / judge_score: 0.3333 / 0.67
   review_label: possible_rule_false_fail
   matched_reasoning_points: 赊销可能先确认收入
   missing_reasoning_points: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
   初步归因: 规则评分只按原始表述匹配，未识别“已经赚到”“钱还没进来”“客户欠款”等同义表达对应收入确认、未收现和应收款。
   课程或评分规则修改建议: 在 hidden transfer 案例中为三个要点增加 aliases：“已经赚到这笔业务”映射“赊销可能先确认收入”，“钱还没进来/现金未必增加”映射“现金不一定增加”，“客户欠款/先挂应收”映射“应收账款”。

2. node_id: `revenue_not_cash_receipt`
   condition: `hidden_transfer`
   student_persona: `rote_memorizer`
   question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
   student_answer: 规则说收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以本月利润表收入增加8000元，现金不变。收入不等于收款是因为收入确认不一定等于收到现金。
   rule_score / judge_score: 0.3333 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: 赊销可能先确认收入
   missing_reasoning_points: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
   初步归因: 规则评分只按原始表述匹配，未识别“已经赚到”“钱还没进来”“客户欠款”等同义表达对应收入确认、未收现和应收款。
   课程或评分规则修改建议: 在 hidden transfer 案例中为三个要点增加 aliases：“已经赚到这笔业务”映射“赊销可能先确认收入”，“钱还没进来/现金未必增加”映射“现金不一定增加”，“客户欠款/先挂应收”映射“应收账款”。

### rule_pass_llm_fail

本次没有样本。
若后续出现样本，将逐条输出：node_id、condition、student_persona、question、student_answer、rule_score / judge_score、matched_reasoning_points、missing_reasoning_points、初步归因、课程或评分规则修改建议。

## hidden transfer 表现

| node_id | title | judge_passes | avg_judge_score | failing_personas |
| --- | --- | --- | --- | --- |
| `revenue_not_cash_receipt` | 收入不等于收款 | 3/3 | 0.92 | - |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `revenue_not_cash_receipt` | 收入不等于收款 | 0.196 | 33.3% | 0.0% | 0 | revenue_cash_confusion:4, rote_repetition:2, insufficient_materials:1 |

## 课程修改建议

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

### 1. `revenue_not_cash_receipt` 收入不等于收款
- 问题证据: hidden_transfer 通过率 3/3 (100.0%)；失败 persona: -；top_tags: revenue_cash_confusion:4；rote_repetition:2；insufficient_materials:1；false_fail_count: 2；no_course_baseline_fail: 3 (misconception_prone, novice_closed_book, rote_memorizer)；典型 missing_reasoning_points: 可能形成应收账款而不是现金流入:11；未收现金时现金不一定增加:6；赊销可能先确认收入:3；典型学生回答片段: -
- 课程强化: 强化“收入确认”和“现金收款”的对照，并加入典型误解提醒：“没收到钱不代表不能确认收入；收入增加也不代表现金同步增加。”
- 新增 guiding_question: 商品已经卖出、客户尚未付款、利润表收入、现金变化分别对应什么？
- 评分规则建议: 补充 rule aliases：“现金要等到客户付款时才增加”、“现金不变”、“现金还没进来”、“收入确认不一定等于收到现金”、“客户后续付款”、“赊销导致现金流入延后”。
- 课程材料补充: 显式加入“赊销形成应收账款，不是当期现金流入。”
- baseline 解读: no_course_baseline 下封闭学生答不出是预期行为，用于验证学生不会在没有材料时外推；不应直接视为课程失败。

## 需要人工复核的样本

- run_id: `044c94e22425d6e7`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `rote_memorizer` / `chain_so_far`
- rule/judge: 0.3333 -> 0.67
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- answer: 规则说，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。
- missing: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入

- run_id: `3e84ef3c746e97e2`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.3333 -> 1.0
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- answer: 规则说收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以本月利润表收入增加8000元，现金不变。收入不等于收款是因为收入确认不一定等于收到现金。
- missing: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- tags: rote_repetition

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 本报告使用真实 LLM judge，但仍需人工抽查关键冲突样本。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
