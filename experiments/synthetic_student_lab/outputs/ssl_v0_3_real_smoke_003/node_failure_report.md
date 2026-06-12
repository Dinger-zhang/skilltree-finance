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
| rule_pass_rate | 83.3% |
| judge_pass_rate | 91.7% |
| hidden_transfer_judge_pass_rate | 100.0% |
| false_pass_count | 0 |
| false_fail_count | 1 |
| manual_review_count | 1 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `revenue_not_cash_receipt` | 收入不等于收款 | 12 | 8.3% | 0.0% | 0 | 1 | 0.86 |

## 评分冲突样本


### rule_fail_llm_pass

1. node_id: `revenue_not_cash_receipt`
   condition: `chain_so_far`
   student_persona: `rote_memorizer`
   question: 赊销商品时，为什么可能确认收入但现金没有增加？
   student_answer: 因为收入确认遵循权责发生制，只要商品已经卖出或服务已经完成，就可以确认收入，而不一定收到现金。赊销时，商品已经交付，所以确认收入，但现金要等到客户付款时才增加。
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
| `revenue_not_cash_receipt` | 收入不等于收款 | 3/3 | 1.00 | - |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `revenue_not_cash_receipt` | 收入不等于收款 | 0.075 | 8.3% | 0.0% | 0 | rote_repetition:4, weak_transfer:2, insufficient_materials:1 |

## 课程修改建议

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

高风险前三个节点中有节点缺少预设诊断模板，请先补充该节点的失败样本归因再改课程。

## 需要人工复核的样本

- run_id: `044c94e22425d6e7`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `rote_memorizer` / `chain_so_far`
- rule/judge: 0.3333 -> 1.0
- question: 赊销商品时，为什么可能确认收入但现金没有增加？
- answer: 因为收入确认遵循权责发生制，只要商品已经卖出或服务已经完成，就可以确认收入，而不一定收到现金。赊销时，商品已经交付，所以确认收入，但现金要等到客户付款时才增加。
- missing: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- tags: rote_repetition

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 当前 mock judge 用于验证数据流和报告结构，不等价于真实语义评分。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
