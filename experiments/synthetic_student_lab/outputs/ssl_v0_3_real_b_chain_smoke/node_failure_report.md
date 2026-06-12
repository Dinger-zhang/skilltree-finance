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
| judge_pass_rate | 58.3% |
| hidden_transfer_judge_pass_rate | 100.0% |
| false_pass_count | 0 |
| false_fail_count | 7 |
| manual_review_count | 7 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `income_statement_boundary` | 交易进入利润表的边界 | 12 | 41.7% | 0.0% | 0 | 7 | 0.64 |

## 评分冲突样本


### rule_fail_llm_pass

1. node_id: `income_statement_boundary`
   condition: `node_only`
   student_persona: `novice_closed_book`
   question: 为什么银行借款通常不应作为营业收入进入利润表？
   student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。
   rule_score / judge_score: 0.0 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

2. node_id: `income_statement_boundary`
   condition: `chain_so_far`
   student_persona: `novice_closed_book`
   question: 为什么银行借款通常不应作为营业收入进入利润表？
   student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入进入利润表。
   rule_score / judge_score: 0.0 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

3. node_id: `income_statement_boundary`
   condition: `hidden_transfer`
   student_persona: `novice_closed_book`
   question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
   student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为经营成果。而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。
   rule_score / judge_score: 0.3333 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: 利润表记录一段期间的经营成果
   missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入

4. node_id: `income_statement_boundary`
   condition: `node_only`
   student_persona: `rote_memorizer`
   question: 为什么银行借款通常不应作为营业收入进入利润表？
   student_answer: 规则说，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。
   rule_score / judge_score: 0.3333 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: 利润表记录一段期间的经营成果
   missing_reasoning_points: 销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

5. node_id: `income_statement_boundary`
   condition: `chain_so_far`
   student_persona: `rote_memorizer`
   question: 为什么银行借款通常不应作为营业收入进入利润表？
   student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入。
   rule_score / judge_score: 0.0 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

### rule_pass_llm_fail

本次没有样本。
若后续出现样本，将逐条输出：node_id、condition、student_persona、question、student_answer、rule_score / judge_score、matched_reasoning_points、missing_reasoning_points、初步归因、课程或评分规则修改建议。

## hidden transfer 表现

| node_id | title | judge_passes | avg_judge_score | failing_personas |
| --- | --- | --- | --- | --- |
| `income_statement_boundary` | 交易进入利润表的边界 | 3/3 | 0.90 | - |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `income_statement_boundary` | 交易进入利润表的边界 | 0.267 | 41.7% | 0.0% | 0 | revenue_cash_confusion:4, rote_repetition:3, 把所有收到的钱都当成收入。:2 |

## 课程修改建议

本节区分课程内容建议和评分规则建议；存在 false fail 时，优先补强评分规则或 aliases。

### 评分规则修改建议
以下节点存在 `rule_fail_llm_pass`：LLM judge 认为答案覆盖了要点，但规则评分未命中。这里应优先理解为评分规则或 aliases 需要增强，不能直接判定课程内容错误。

- node_id: `income_statement_boundary` 交易进入利润表的边界
- 失败样本数量: 7
- 未命中的 expected_reasoning_points: 利润表记录一段期间的经营成果:4；销售商品或提供服务才通常形成收入:4；借款是筹资活动不是营业收入:4；销售商品或服务形成收入或费用边界内的交易:3；银行借款是筹资活动不是营业收入:3
- 学生答案中的同义表达（对应 `利润表记录一段期间的经营成果`）: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入；银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入进入利润表；规则说利润表记录经营成果，不是所有现金流入；咖啡店卖咖啡的收入应该进利润表，因为材料说利润表记录经营成果，卖咖啡是销售商品
- 建议增加的 aliases（对应 `利润表记录一段期间的经营成果`）: 利润表记录的是经营成果；重点看收入、成本、费用；利润表记录经营成果
- 学生答案中的同义表达（对应 `销售商品或提供服务才通常形成收入`）: 银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款不是来自销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入
- 建议增加的 aliases（对应 `销售商品或提供服务才通常形成收入`）: 不是来自销售商品或提供服务；不是销售商品或提供服务；银行借款不是来自销售商品或提供服务
- 学生答案中的同义表达（对应 `借款是筹资活动不是营业收入`）: 银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款不是来自销售商品或提供服务，所以不应作为营业收入进入利润表；银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入
- 建议增加的 aliases（对应 `借款是筹资活动不是营业收入`）: 不是来自销售商品或提供服务；银行借款是资金来源变化；借款是资金来源变化；不应作为营业收入；不是销售商品或提供服务；银行借款不是来自销售商品或提供服务
- 学生答案中的同义表达（对应 `销售商品或服务形成收入或费用边界内的交易`）: 咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为经营成果；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表；所以咖啡店卖咖啡的收入可能进入利润表，但贷款不是营业收入，因为材料说不是所有现金流入都代表经营收入，贷款只是资金来源变化；咖啡店卖咖啡的收入应该进利润表，因为材料说利润表记录经营成果，卖咖啡是销售商品；贷款不是营业收入，因为材料说借款不是经营收入，只是资金来源变化
- 建议增加的 aliases（对应 `销售商品或服务形成收入或费用边界内的交易`）: 出售咖啡属于销售商品；销售商品，可能进入利润表；卖咖啡的收入可能进入利润表；卖咖啡是销售商品
- 学生答案中的同义表达（对应 `银行借款是筹资活动不是营业收入`）: 咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为经营成果；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表；所以咖啡店卖咖啡的收入可能进入利润表，但贷款不是营业收入，因为材料说不是所有现金流入都代表经营收入，贷款只是资金来源变化；咖啡店卖咖啡的收入应该进利润表，因为材料说利润表记录经营成果，卖咖啡是销售商品；贷款不是营业收入，因为材料说借款不是经营收入，只是资金来源变化
- 建议增加的 aliases（对应 `银行借款是筹资活动不是营业收入`）: 出售咖啡属于销售商品；销售商品，可能进入利润表；不是营业收入；卖咖啡的收入可能进入利润表；贷款只是资金来源变化；贷款不是营业收入；卖咖啡是销售商品；借款不是经营收入

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

## 需要人工复核的样本

- run_id: `bd4d2df63ecbbc29`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `node_only`
- rule/judge: 0.0 -> 1.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。
- missing: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

- run_id: `6ac87983201c5f3d`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `chain_so_far`
- rule/judge: 0.0 -> 1.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入进入利润表。
- missing: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入

- run_id: `8a26a66f246d453f`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.3333 -> 1.0
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为经营成果。而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。
- missing: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入

- run_id: `b02afd18f3003d2f`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `rote_memorizer` / `node_only`
- rule/judge: 0.3333 -> 1.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 规则说，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。
- missing: 销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- tags: rote_repetition

- run_id: `06359d3e2905e151`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `rote_memorizer` / `chain_so_far`
- rule/judge: 0.0 -> 1.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入。
- missing: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- tags: rote_repetition

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 本报告由 real-mode 生成；student_model: `deepseek-v4-flash`；judge_model: `deepseek-v4-flash`。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
