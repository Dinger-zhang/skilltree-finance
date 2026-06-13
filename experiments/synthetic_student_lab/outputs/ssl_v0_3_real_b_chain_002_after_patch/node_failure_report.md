# Synthetic Student Lab v0.3 Minimal Report

## 实验范围

- experiment_id: `ssl_v0_3_minimal`
- graph_version: `sha256:acf19f846747`
- chain_id: `B. 从交易到利润表`
- nodes: 8
- personas: 3 (misconception_prone, novice_closed_book, rote_memorizer)
- conditions: 4 (chain_so_far, hidden_transfer, no_course_baseline, node_only)
- total_runs: 96
- graph_fallback_used_runs: 0

## 总体指标

| metric | value |
| --- | --- |
| rule_pass_rate | 4.2% |
| judge_pass_rate | 16.7% |
| hidden_transfer_judge_pass_rate | 33.3% |
| false_pass_count | 1 |
| false_fail_count | 13 |
| manual_review_count | 73 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `accrual_vs_cash` | 权责发生制与现金制 | 12 | 91.7% | 66.7% | 0 | 1 | 0.17 |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 12 | 100.0% | 100.0% | 0 | 0 | 0.00 |
| `expense_recognition` | 费用确认 | 12 | 66.7% | 66.7% | 0 | 4 | 0.31 |
| `gross_margin` | 毛利形成 | 12 | 83.3% | 66.7% | 0 | 0 | 0.17 |
| `income_statement_boundary` | 交易进入利润表的边界 | 12 | 75.0% | 33.3% | 0 | 3 | 0.28 |
| `net_profit` | 净利润推导 | 12 | 83.3% | 100.0% | 0 | 2 | 0.11 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 12 | 83.3% | 33.3% | 1 | 1 | 0.17 |
| `revenue_recognition` | 收入确认 | 12 | 83.3% | 66.7% | 0 | 2 | 0.14 |

## 评分冲突样本


### rule_fail_llm_pass

1. node_id: `income_statement_boundary`
   condition: `hidden_transfer`
   student_persona: `novice_closed_book`
   question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
   student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。
   rule_score / judge_score: 0.3333 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: 利润表记录一段期间的经营成果
   missing_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入

2. node_id: `revenue_recognition`
   condition: `node_only`
   student_persona: `novice_closed_book`
   question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
   student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务，即使客户下月付款，也可能确认收入。
   rule_score / judge_score: 0.0 / 0.67
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账

3. node_id: `expense_recognition`
   condition: `hidden_transfer`
   student_persona: `novice_closed_book`
   question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
   student_answer: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付。材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用。因此，本月可以确认工资费用，费用发生与现金付款是两回事。
   rule_score / judge_score: 0.0 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润

4. node_id: `net_profit`
   condition: `node_only`
   student_persona: `novice_closed_book`
   question: 为什么净利润为正仍不一定代表现金充足？
   student_answer: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金。所以净利润为正不一定代表现金充足。
   rule_score / judge_score: 0.0 / 0.67
   review_label: possible_rule_false_fail
   matched_reasoning_points: -
   missing_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金

5. node_id: `accrual_vs_cash`
   condition: `hidden_transfer`
   student_persona: `novice_closed_book`
   question: 咨询公司 6 月完成服务，7 月收款；6 月发生房租但 7 月付款。 权责发生制下 6 月应如何看收入和费用？它和现金制的关注点有什么不同？
   student_answer: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间。所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用。现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用。
   rule_score / judge_score: 0.25 / 1.0
   review_label: possible_rule_false_fail
   matched_reasoning_points: 权责发生制关注交易归属期间
   missing_reasoning_points: 满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间
   初步归因: 规则评分的同义表达覆盖不足，学生用自然语言覆盖了核心推理但未触发关键词。
   课程或评分规则修改建议: 为未命中的评分点补充同义表达 aliases，并用该样本回归验证。当前未命中：满足条件时未收款也可能确认 6 月收入；已发生费用即使未付款也可能归入 6 月；现金制关注现金实际收付时间

### rule_pass_llm_fail

1. node_id: `revenue_not_cash_receipt`
   condition: `chain_so_far`
   student_persona: `novice_closed_book`
   question: 赊销商品时，为什么可能确认收入但现金没有增加？
   student_answer: 根据材料，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以可能确认收入但现金没有增加。
   rule_score / judge_score: 0.6667 / 0.0
   matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加
   missing_reasoning_points: 可能形成应收账款而不是现金流入
   初步归因: 规则评分只看局部关键词，未校验题干所需的案例计算或因果链是否完整。
   课程或评分规则修改建议: 将题干中的关键数值、对象或期间判断拆为 required points；对只复述规则、拒绝迁移判断的回答加入 blocker 或降分。

## hidden transfer 表现

| node_id | title | judge_passes | avg_judge_score | failing_personas |
| --- | --- | --- | --- | --- |
| `accrual_vs_cash` | 权责发生制与现金制 | 1/3 | 0.33 | misconception_prone, rote_memorizer |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 0/3 | 0.00 | misconception_prone, novice_closed_book, rote_memorizer |
| `expense_recognition` | 费用确认 | 1/3 | 0.33 | misconception_prone, rote_memorizer |
| `gross_margin` | 毛利形成 | 1/3 | 0.33 | misconception_prone, rote_memorizer |
| `income_statement_boundary` | 交易进入利润表的边界 | 2/3 | 0.67 | misconception_prone |
| `net_profit` | 净利润推导 | 0/3 | 0.00 | misconception_prone, novice_closed_book, rote_memorizer |
| `revenue_not_cash_receipt` | 收入不等于收款 | 2/3 | 0.67 | misconception_prone |
| `revenue_recognition` | 收入确认 | 1/3 | 0.22 | misconception_prone, novice_closed_book |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 0.762 | 100.0% | 100.0% | 0 | profit_cash_confusion:2, insufficient_materials:1 |
| `net_profit` | 净利润推导 | 0.708 | 83.3% | 100.0% | 0 | rote_repetition:2, insufficient_materials:1, 无法推理:1 |
| `accrual_vs_cash` | 权责发生制与现金制 | 0.625 | 91.7% | 66.7% | 0 | insufficient_materials:1, rote_repetition:1 |
| `revenue_recognition` | 收入确认 | 0.612 | 83.3% | 66.7% | 0 | revenue_cash_confusion:3, insufficient_materials:1, rote_repetition:1 |
| `gross_margin` | 毛利形成 | 0.583 | 83.3% | 66.7% | 0 | insufficient_materials:1, profit_cash_confusion:1 |
| `expense_recognition` | 费用确认 | 0.533 | 66.7% | 66.7% | 0 | rote_repetition:2, expense_payment_confusion:2 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 0.512 | 83.3% | 33.3% | 1 | rote_repetition:2, revenue_cash_confusion:2, 收入增加就等于现金增加。:1 |
| `income_statement_boundary` | 交易进入利润表的边界 | 0.488 | 75.0% | 33.3% | 0 | 把所有收到的钱都当成收入。:3, 把借款或股东投入当成利润。:2, rote_repetition:2 |

## 课程修改建议

本节区分课程内容建议和评分规则建议；存在 false fail 时，优先补强评分规则或 aliases。

### 评分规则修改建议
以下节点存在 `rule_fail_llm_pass`：LLM judge 认为答案覆盖了要点，但规则评分未命中。这里应优先理解为评分规则或 aliases 需要增强，不能直接判定课程内容错误。

- node_id: `accrual_vs_cash` 权责发生制与现金制
- 失败样本数量: 1
- 未命中的 expected_reasoning_points: 满足条件时未收款也可能确认 6 月收入:1；已发生费用即使未付款也可能归入 6 月:1；现金制关注现金实际收付时间:1
- 学生答案中的同义表达（对应 `满足条件时未收款也可能确认 6 月收入`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用
- 建议增加的 aliases（对应 `满足条件时未收款也可能确认 6 月收入`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用
- 学生答案中的同义表达（对应 `已发生费用即使未付款也可能归入 6 月`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用
- 建议增加的 aliases（对应 `已发生费用即使未付款也可能归入 6 月`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用
- 学生答案中的同义表达（对应 `现金制关注现金实际收付时间`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用
- 建议增加的 aliases（对应 `现金制关注现金实际收付时间`）: 根据材料，权责发生制关注交易归属期间，而不是现金实际收付时间；所以6月完成服务，即使7月收款，6月也应确认收入；6月发生房租，即使7月付款，6月也应确认费用；现金制则关注现金实际收付时间，所以6月没有收款和付款，就不确认收入和费用

- node_id: `expense_recognition` 费用确认
- 失败样本数量: 4
- 未命中的 expected_reasoning_points: 费用是为取得收入或维持经营发生的耗费:4；费用发生不一定等于当期已经付款:4；工资费用会减少本期利润:4
- 学生答案中的同义表达（对应 `费用是为取得收入或维持经营发生的耗费`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款；规则说费用是为取得收入或维持经营发生的资源耗费
- 建议增加的 aliases（对应 `费用是为取得收入或维持经营发生的耗费`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款；规则说费用是为取得收入或维持经营发生的资源耗费
- 学生答案中的同义表达（对应 `费用发生不一定等于当期已经付款`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；因此，本月可以确认工资费用，费用发生与现金付款是两回事；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款
- 建议增加的 aliases（对应 `费用发生不一定等于当期已经付款`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；因此，本月可以确认工资费用，费用发生与现金付款是两回事；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款
- 学生答案中的同义表达（对应 `工资费用会减少本期利润`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；因此，本月可以确认工资费用，费用发生与现金付款是两回事；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款
- 建议增加的 aliases（对应 `工资费用会减少本期利润`）: 根据课程材料，费用确认关注的是耗费是否服务于本期经营，而不是现金是否支付；材料中明确提到“费用发生不一定等于当期现金付款”，并且以“员工已经完成本月工作，但工资下月发放”为例，说明本月可以确认工资费用；因此，本月可以确认工资费用，费用发生与现金付款是两回事；规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款

- node_id: `income_statement_boundary` 交易进入利润表的边界
- 失败样本数量: 3
- 未命中的 expected_reasoning_points: 销售商品或服务形成收入或费用边界内的交易:2；银行借款是筹资活动不是营业收入:2；利润表记录一段期间的经营成果:2；销售商品或提供服务才通常形成收入:1；借款是筹资活动不是营业收入:1
- 学生答案中的同义表达（对应 `销售商品或服务形成收入或费用边界内的交易`）: 咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表；贷款不是销售商品或提供服务，所以不是营业收入
- 建议增加的 aliases（对应 `销售商品或服务形成收入或费用边界内的交易`）: 出售咖啡属于销售商品；不是销售商品或提供服务
- 学生答案中的同义表达（对应 `银行借款是筹资活动不是营业收入`）: 咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表；贷款不是销售商品或提供服务，所以不是营业收入
- 建议增加的 aliases（对应 `银行借款是筹资活动不是营业收入`）: 出售咖啡属于销售商品；不是营业收入；不是销售商品或提供服务
- 学生答案中的同义表达（对应 `利润表记录一段期间的经营成果`）: 规则说利润表记录经营成果，不是所有现金流入；规则说利润表记录经营成果，看收入、成本、费用，不是所有现金流入
- 建议增加的 aliases（对应 `利润表记录一段期间的经营成果`）: 利润表记录经营成果
- 学生答案中的同义表达（对应 `销售商品或提供服务才通常形成收入`）: 银行借款不是来自销售商品或提供服务，所以不应作为营业收入
- 建议增加的 aliases（对应 `销售商品或提供服务才通常形成收入`）: 不是来自销售商品或提供服务；银行借款不是来自销售商品或提供服务
- 学生答案中的同义表达（对应 `借款是筹资活动不是营业收入`）: 银行借款不是来自销售商品或提供服务，所以不应作为营业收入
- 建议增加的 aliases（对应 `借款是筹资活动不是营业收入`）: 不是来自销售商品或提供服务；银行借款不是来自销售商品或提供服务；不应作为营业收入

- node_id: `net_profit` 净利润推导
- 失败样本数量: 2
- 未命中的 expected_reasoning_points: 净利润大致等于收入扣除成本费用和税费:2；净利润可能包含未收现收入:2；净利润可能包含非现金费用所以不等于现金:2
- 学生答案中的同义表达（对应 `净利润大致等于收入扣除成本费用和税费`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足
- 建议增加的 aliases（对应 `净利润大致等于收入扣除成本费用和税费`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足
- 学生答案中的同义表达（对应 `净利润可能包含未收现收入`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足
- 建议增加的 aliases（对应 `净利润可能包含未收现收入`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足
- 学生答案中的同义表达（对应 `净利润可能包含非现金费用所以不等于现金`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足
- 建议增加的 aliases（对应 `净利润可能包含非现金费用所以不等于现金`）: 根据材料，净利润是收入扣除成本、费用和税费后的结果，但净利润不等于现金；所以净利润为正不一定代表现金充足；规则说净利润不等于现金，所以净利润为正不一定代表现金充足

- node_id: `revenue_not_cash_receipt` 收入不等于收款
- 失败样本数量: 1
- 未命中的 expected_reasoning_points: 未收现金时现金不一定增加:1；可能形成应收账款而不是现金流入:1
- 学生答案中的同义表达（对应 `未收现金时现金不一定增加`）: 规则说收入记录赚到的经营成果，收款记录现金进入；赊销会让收入和现金流入出现时间差；所以本月利润表收入增加8000元，现金不变；收入不等于收款是因为收入确认不一定等于收到现金
- 建议增加的 aliases（对应 `未收现金时现金不一定增加`）: 现金不变；收入确认不一定等于收到现金
- 学生答案中的同义表达（对应 `可能形成应收账款而不是现金流入`）: 规则说收入记录赚到的经营成果，收款记录现金进入；赊销会让收入和现金流入出现时间差；所以本月利润表收入增加8000元，现金不变；收入不等于收款是因为收入确认不一定等于收到现金
- 建议增加的 aliases（对应 `可能形成应收账款而不是现金流入`）: 现金不变；收入确认不一定等于收到现金

- node_id: `revenue_recognition` 收入确认
- 失败样本数量: 2
- 未命中的 expected_reasoning_points: 收入来自销售商品或提供服务:2；完成交付或服务后可能满足收入确认条件:2；收入确认不一定依赖现金已经到账:2
- 学生答案中的同义表达（对应 `收入来自销售商品或提供服务`）: 根据材料，收入确认不一定等于收到现金；本月完成服务，即使客户下月付款，也可能确认收入；规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入
- 建议增加的 aliases（对应 `收入来自销售商品或提供服务`）: 根据材料，收入确认不一定等于收到现金；本月完成服务，即使客户下月付款，也可能确认收入；规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入
- 学生答案中的同义表达（对应 `完成交付或服务后可能满足收入确认条件`）: 根据材料，收入确认不一定等于收到现金；本月完成服务，即使客户下月付款，也可能确认收入；规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入
- 建议增加的 aliases（对应 `完成交付或服务后可能满足收入确认条件`）: 根据材料，收入确认不一定等于收到现金；本月完成服务，即使客户下月付款，也可能确认收入；规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入
- 学生答案中的同义表达（对应 `收入确认不一定依赖现金已经到账`）: 根据材料，收入确认不一定等于收到现金；本月完成服务，即使客户下月付款，也可能确认收入；规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入
- 建议增加的 aliases（对应 `收入确认不一定依赖现金已经到账`）: 收入确认不一定等于收到现金

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

### 1. `depreciation_amortization` 折旧与摊销是成本分配
- 问题证据: hidden_transfer 通过率 0/3 (0.0%)；失败 persona: misconception_prone, novice_closed_book, rote_memorizer；top_tags: profit_cash_confusion:2；insufficient_materials:1；典型 missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊:3；折旧费用会减少当期利润:3；折旧通常不是当期现金流出:3；典型学生回答片段: novice_closed_book: ；rote_memorizer: 
- 问题归因: 前置知识中长期资产和费用的连接不够显性；guiding_questions 没有强制区分历史购置现金流、本期折旧费用和今年是否再次付款；mastery_question 偏概念解释，未要求学生把“成本分配、利润减少、非本期现金流出”三点同时写出。
- 新增 guiding_question: 烤箱购买付款发生在哪个期间？今年计提折旧是不是再次付现金？
- 新增 guiding_question: 折旧把哪项长期资产成本分配到哪些受益期间？
- 新增 guiding_question: 今年计提折旧时，利润表费用和资产账面价值分别可能怎样变化？
- 修改 mastery_question 的具体方向: 改为给出“去年买烤箱、今年继续使用并计提折旧”的场景，要求学生说明折旧为何减少今年利润，以及为什么通常不代表今年再次现金流出。
- 修改 expected_reasoning_points: 购买烤箱的现金流通常发生在购置期间
- 修改 expected_reasoning_points: 今年折旧是把长期资产成本分配到受益期间
- 修改 expected_reasoning_points: 折旧费用减少今年利润，但通常不是今年再次现金流出
- 增加 common_misconceptions: 折旧没有现金流出，所以不应进入利润表。
- 增加 common_misconceptions: 每期折旧等于企业每期重新支付一笔现金。
- 新增变式案例: 新增一个软件摊销案例：去年一次性购买软件，今年按月摊销，要求判断本期利润、现金和资产账面价值的不同变化。

### 2. `gross_margin` 毛利形成
- 问题证据: hidden_transfer 通过率 1/3 (33.3%)；失败 persona: misconception_prone, rote_memorizer；top_tags: insufficient_materials:1；profit_cash_confusion:1；典型 missing_reasoning_points: {'aliases': ['毛利是3500', '毛利为3500', '毛利3500元', '10000减6500得到3500'], 'required': True, 'text': '本例毛利等于 10000 - 6500 = 3500 元'}:1；{'aliases': ['毛利率是35%', '毛利率为35%', '毛利率35%', '3500除以10000'], 'required': True, 'text': '本例毛利率等于 3500 / 10000 = 35%'}:1；{'aliases': ['还没扣销售费用', '还没扣管理费用', '还没扣期间费用', '未扣除期间费用', '还不是净利润'], 'required': True, 'text': '毛利还没有扣除销售管理研发财务等期间费用'}:1；典型学生回答片段: rote_memorizer: ；misconception_prone: 
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

### 3. `expense_recognition` 费用确认
- 问题证据: hidden_transfer 通过率 1/3 (33.3%)；失败 persona: misconception_prone, rote_memorizer；top_tags: rote_repetition:2；expense_payment_confusion:2；典型 missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费:2；费用发生不一定等于当期已经付款:2；工资费用会减少本期利润:2；典型学生回答片段: rote_memorizer: ；misconception_prone: 
- 问题归因: 引导问题跳过了“员工已经完成本月工作”这一归属期间判断；mastery_question 只问为什么下月发也可能算本月费用，没有要求同时说明费用发生、未付款和利润影响；常见误区覆盖了“没付款就没有费用”，但缺少把工资场景拆成利润表和现金变化的练习。
- 新增 guiding_question: 员工本月已经完成工作，这个耗费服务于哪个会计期间？
- 新增 guiding_question: 工资下月支付会不会改变本月费用归属？为什么？
- 新增 guiding_question: 如果本月确认工资费用，本月利润表和现金分别怎样变化？
- 修改 mastery_question 的具体方向: 改为给出“本月工作、下月付款”的工资场景，要求学生判断本月是否确认工资费用，并分别说明费用发生、现金付款时间和本期利润影响。
- 修改 expected_reasoning_points: 员工已完成本月工作，工资耗费服务于本期经营
- 修改 expected_reasoning_points: 下月付款不阻止本月确认工资费用
- 修改 expected_reasoning_points: 确认工资费用会减少本期利润，但本月现金可能暂不减少
- 增加 common_misconceptions: 工资费用只有在实际发现金时才发生。
- 增加 common_misconceptions: 费用确认只影响现金，不影响利润表期间归属。
- 新增变式案例: 新增一个房租案例：门店本月已使用房屋但下月支付租金，要求区分费用归属、本月利润影响和现金付款时间。

## 需要人工复核的样本

- run_id: `f599d9bb1b2418b3`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `node_only`
- rule/judge: 0.0 -> 0.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是销售商品或提供服务产生的，所以不应作为营业收入进入利润表。
- missing: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- error: judge_llm_error: The read operation timed out

- run_id: `1d2f4a510281905d`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `chain_so_far`
- rule/judge: 0.0 -> 0.0
- question: 为什么银行借款通常不应作为营业收入进入利润表？
- answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款是资金来源的变化，不是销售商品或提供服务产生的收入，所以不应作为营业收入进入利润表。
- missing: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- error: judge_llm_error: The read operation timed out

- run_id: `a15875025c353cca`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.3333 -> 1.0
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能形成收入进入利润表；而银行借款只是资金来源变化，不是营业收入，所以不应进入利润表。
- missing: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入

- run_id: `4e12cea729ecaa0a`
- node: `revenue_recognition` 收入确认
- persona/condition: `novice_closed_book` / `node_only`
- rule/judge: 0.0 -> 0.67
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- answer: 根据材料，收入确认不一定等于收到现金。本月完成服务，即使客户下月付款，也可能确认收入。
- missing: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件

- run_id: `9f925b57d5ef9706`
- node: `revenue_recognition` 收入确认
- persona/condition: `novice_closed_book` / `chain_so_far`
- rule/judge: 0.0 -> 0.0
- question: 客户下月付款时，本月完成服务为什么仍可能确认收入？
- answer: 根据材料，收入确认关注的是赚到收入而不是收到现金。材料中的设计公司本月完成并交付海报，即使客户下月付款，本月仍可能确认收入，因为服务已经完成。
- missing: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- error: judge_llm_error: The read operation timed out

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 本报告由 real-mode 生成；student_model: `deepseek-v4-flash`；judge_model: `deepseek-v4-flash`。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
