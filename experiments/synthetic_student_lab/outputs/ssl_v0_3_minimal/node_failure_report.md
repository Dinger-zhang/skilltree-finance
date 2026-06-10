# Synthetic Student Lab v0.3 Minimal Report

## 实验范围

- experiment_id: `ssl_v0_3_minimal`
- graph_version: `sha256:6b95d7ba7ba4`
- chain_id: `B. 从交易到利润表`
- nodes: 8
- personas: 3 (misconception_prone, novice_closed_book, rote_memorizer)
- conditions: 4 (chain_so_far, hidden_transfer, no_course_baseline, node_only)
- total_runs: 96
- graph_fallback_used_runs: 96

## 总体指标

| metric | value |
| --- | --- |
| rule_pass_rate | 27.1% |
| judge_pass_rate | 27.1% |
| hidden_transfer_judge_pass_rate | 33.3% |
| false_pass_count | 1 |
| false_fail_count | 1 |
| manual_review_count | 17 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `accrual_vs_cash` | 权责发生制与现金制 | 12 | 75.0% | 66.7% | 0 | 0 | 0.35 |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `expense_recognition` | 费用确认 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `gross_margin` | 毛利形成 | 12 | 58.3% | 66.7% | 1 | 0 | 0.37 |
| `income_statement_boundary` | 交易进入利润表的边界 | 12 | 75.0% | 66.7% | 0 | 0 | 0.31 |
| `net_profit` | 净利润推导 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 12 | 75.0% | 66.7% | 0 | 1 | 0.33 |
| `revenue_recognition` | 收入确认 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |

## false_pass / false_fail 样本
## false_pass: rule_pass_llm_fail

- run_id: `b22ecb7c16f19973`
- node: `gross_margin` 毛利形成
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.6667 -> 0.4
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- answer: 规则说：毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 毛利还没有扣除销售管理研发财务等期间费用
- tags: rote_repetition

## false_fail: rule_fail_llm_pass

- run_id: `585942f7bc6db083`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.0 -> 1.0
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- answer: 这月已经赚到这笔业务，但钱还没进来，客户欠款会先挂着，所以现金未必增加。
- missing: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入

## hidden transfer 表现

| node_id | title | judge_passes | avg_judge_score | failing_personas |
| --- | --- | --- | --- | --- |
| `accrual_vs_cash` | 权责发生制与现金制 | 1/3 | 0.38 | misconception_prone, rote_memorizer |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `expense_recognition` | 费用确认 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `gross_margin` | 毛利形成 | 1/3 | 0.36 | misconception_prone, rote_memorizer |
| `income_statement_boundary` | 交易进入利润表的边界 | 1/3 | 0.33 | misconception_prone, rote_memorizer |
| `net_profit` | 净利润推导 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `revenue_not_cash_receipt` | 收入不等于收款 | 1/3 | 0.44 | misconception_prone, rote_memorizer |
| `revenue_recognition` | 收入确认 | 1/3 | 0.22 | misconception_prone, rote_memorizer |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `expense_recognition` | 费用确认 | 0.583 | 75.0% | 66.7% | 0 | expense_payment_confusion:4, trap_hit:4, rote_repetition:3 |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 0.571 | 75.0% | 66.7% | 0 | depreciation_payment_confusion:4, rote_repetition:3, trap_hit:1 |
| `income_statement_boundary` | 交易进入利润表的边界 | 0.567 | 75.0% | 66.7% | 0 | rote_repetition:3, profit_cash_confusion:3, revenue_cash_confusion:1 |
| `revenue_recognition` | 收入确认 | 0.567 | 75.0% | 66.7% | 0 | revenue_cash_confusion:4, rote_repetition:3 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 0.567 | 75.0% | 66.7% | 0 | revenue_cash_confusion:4, rote_repetition:3 |
| `net_profit` | 净利润推导 | 0.567 | 75.0% | 66.7% | 0 | profit_cash_confusion:4, rote_repetition:3 |
| `accrual_vs_cash` | 权责发生制与现金制 | 0.567 | 75.0% | 66.7% | 0 | profit_cash_confusion:4, rote_repetition:3 |
| `gross_margin` | 毛利形成 | 0.525 | 58.3% | 66.7% | 1 | gross_net_confusion:4, trap_hit:4, rote_repetition:3 |

## 课程修改建议

- `expense_recognition` 费用确认: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `expense_payment_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `depreciation_amortization` 折旧与摊销是成本分配: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `depreciation_payment_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `income_statement_boundary` 交易进入利润表的边界: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `rote_repetition`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `revenue_recognition` 收入确认: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `revenue_cash_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `revenue_not_cash_receipt` 收入不等于收款: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `revenue_cash_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `net_profit` 净利润推导: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `profit_cash_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `accrual_vs_cash` 权责发生制与现金制: 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `profit_cash_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

- `gross_margin` 毛利形成: 收紧关键词规则，要求关键因果关系同时出现，降低 false_pass。 增加至少 1 个变式案例和反例，引导学生把规则迁移到新交易。 补充常见误区讲解，优先处理 `gross_net_confusion`。 检查前置节点、引导问题和 mastery_question 是否存在跳步。

## 需要人工复核的样本

- run_id: `585942f7bc6db083`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.0 -> 1.0
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- answer: 这月已经赚到这笔业务，但钱还没进来，客户欠款会先挂着，所以现金未必增加。
- missing: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入

- run_id: `d75354d9b0324031`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.3333 -> 0.3333
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- answer: 规则说：利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- tags: rote_repetition

- run_id: `ee674563f4bc3832`
- node: `revenue_recognition` 收入确认
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.0
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- answer: 规则说：收入通常来自销售商品或提供服务；在权责发生制下，收入确认不一定等于收到现金。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- tags: rote_repetition

- run_id: `3e84ef3c746e97e2`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.3333
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- answer: 规则说：收入记录赚到的经营成果；收款记录现金进入。赊销会让收入和现金流入出现时间差。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- tags: rote_repetition

- run_id: `1263b89da49fd4bd`
- node: `expense_recognition` 费用确认
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.0
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- tags: rote_repetition

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 当前 mock judge 用于验证数据流和报告结构，不等价于真实语义评分。
- `graph_fallback_used_runs` 大于 0 表示当前图谱缺少链字段，实验使用了 B 链内置 fallback。
