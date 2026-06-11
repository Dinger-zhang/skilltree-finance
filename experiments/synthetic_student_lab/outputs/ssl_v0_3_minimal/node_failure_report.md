# Synthetic Student Lab v0.3 Minimal Report

## 实验范围

- experiment_id: `ssl_v0_3_minimal`
- graph_version: `sha256:6b95d7ba7ba4`
- chain_id: `B. 从交易到利润表`
- nodes: 8
- personas: 3 (misconception_prone, novice_closed_book, rote_memorizer)
- conditions: 4 (chain_so_far, hidden_transfer, no_course_baseline, node_only)
- total_runs: 96
- graph_fallback_used_runs: 0

## 总体指标

| metric | value |
| --- | --- |
| rule_pass_rate | 26.0% |
| judge_pass_rate | 26.0% |
| hidden_transfer_judge_pass_rate | 29.2% |
| false_pass_count | 0 |
| false_fail_count | 0 |
| manual_review_count | 17 |

## 每个节点的失败率

| node_id | title | runs | judge_failure_rate | hidden_failure_rate | false_pass | false_fail | avg_judge_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `accrual_vs_cash` | 权责发生制与现金制 | 12 | 75.0% | 66.7% | 0 | 0 | 0.35 |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `expense_recognition` | 费用确认 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `gross_margin` | 毛利形成 | 12 | 66.7% | 100.0% | 0 | 0 | 0.34 |
| `income_statement_boundary` | 交易进入利润表的边界 | 12 | 75.0% | 66.7% | 0 | 0 | 0.31 |
| `net_profit` | 净利润推导 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 12 | 75.0% | 66.7% | 0 | 0 | 0.33 |
| `revenue_recognition` | 收入确认 | 12 | 75.0% | 66.7% | 0 | 0 | 0.22 |

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
| `accrual_vs_cash` | 权责发生制与现金制 | 1/3 | 0.38 | misconception_prone, rote_memorizer |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `expense_recognition` | 费用确认 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `gross_margin` | 毛利形成 | 0/3 | 0.24 | misconception_prone, novice_closed_book, rote_memorizer |
| `income_statement_boundary` | 交易进入利润表的边界 | 1/3 | 0.33 | misconception_prone, rote_memorizer |
| `net_profit` | 净利润推导 | 1/3 | 0.22 | misconception_prone, rote_memorizer |
| `revenue_not_cash_receipt` | 收入不等于收款 | 1/3 | 0.44 | misconception_prone, rote_memorizer |
| `revenue_recognition` | 收入确认 | 1/3 | 0.22 | misconception_prone, rote_memorizer |

## 高风险节点排行

| node_id | title | risk_score | judge_failure_rate | hidden_failure_rate | false_pass | top_tags |
| --- | --- | --- | --- | --- | --- | --- |
| `gross_margin` | 毛利形成 | 0.650 | 66.7% | 100.0% | 0 | gross_net_confusion:4, trap_hit:4, rote_repetition:3 |
| `expense_recognition` | 费用确认 | 0.588 | 75.0% | 66.7% | 0 | expense_payment_confusion:4, trap_hit:4, rote_repetition:3 |
| `depreciation_amortization` | 折旧与摊销是成本分配 | 0.575 | 75.0% | 66.7% | 0 | depreciation_payment_confusion:4, rote_repetition:3, completeness_blocker:1 |
| `income_statement_boundary` | 交易进入利润表的边界 | 0.571 | 75.0% | 66.7% | 0 | rote_repetition:3, profit_cash_confusion:3, completeness_blocker:1 |
| `revenue_recognition` | 收入确认 | 0.571 | 75.0% | 66.7% | 0 | revenue_cash_confusion:4, rote_repetition:3, completeness_blocker:1 |
| `revenue_not_cash_receipt` | 收入不等于收款 | 0.571 | 75.0% | 66.7% | 0 | revenue_cash_confusion:4, rote_repetition:3, completeness_blocker:1 |
| `net_profit` | 净利润推导 | 0.571 | 75.0% | 66.7% | 0 | profit_cash_confusion:4, rote_repetition:3, completeness_blocker:1 |
| `accrual_vs_cash` | 权责发生制与现金制 | 0.571 | 75.0% | 66.7% | 0 | profit_cash_confusion:4, rote_repetition:3, completeness_blocker:1 |

## 课程修改建议

以下展开高风险前三个节点，建议文本可直接转写到课程 YAML 字段。

### 1. `gross_margin` 毛利形成
- 问题证据: hidden_transfer 通过率 0/3 (0.0%)；失败 persona: misconception_prone, novice_closed_book, rote_memorizer；top_tags: gross_net_confusion:4；trap_hit:4；rote_repetition:3；典型 missing_reasoning_points: 毛利还没有扣除销售管理研发财务等期间费用:2；本例毛利等于 10000 - 6500 = 3500 元:2；本例毛利率等于 3500 / 10000 = 35%:2；典型学生回答片段: novice_closed_book: 根据已经给出的材料，我能推出：本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%。；rote_memorizer: 规则说：毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
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

### 2. `expense_recognition` 费用确认
- 问题证据: hidden_transfer 通过率 1/3 (33.3%)；失败 persona: misconception_prone, rote_memorizer；top_tags: expense_payment_confusion:4；trap_hit:4；rote_repetition:3；典型 missing_reasoning_points: 费用是为取得收入或维持经营发生的耗费:2；费用发生不一定等于当期已经付款:2；工资费用会减少本期利润:2；典型学生回答片段: rote_memorizer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。。照规则说，我只需要背规则，但这个新案例我不能完整判断。；misconception_prone: 费用就是付款，没付款就没有费用，所以工资下月发就只能下月算费用。
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

### 3. `depreciation_amortization` 折旧与摊销是成本分配
- 问题证据: hidden_transfer 通过率 1/3 (33.3%)；失败 persona: misconception_prone, rote_memorizer；top_tags: depreciation_payment_confusion:4；rote_repetition:3；completeness_blocker:1；典型 missing_reasoning_points: 折旧是长期资产成本在多个期间的分摊:2；折旧费用会减少当期利润:2；折旧通常不是当期现金流出:2；典型学生回答片段: rote_memorizer: 规则说：折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。。照规则说，我只需要背规则，但这个新案例我不能完整判断。；misconception_prone: 折旧就是每月重新付款；如果没有付款，折旧也不影响利润。
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

## 需要人工复核的样本

- run_id: `57b3bc6bbc1b3fd2`
- node: `gross_margin` 毛利形成
- persona/condition: `novice_closed_book` / `hidden_transfer`
- rule/judge: 0.6667 -> 0.4
- question: 服装店销售收入 10000 元，对应售出衣服的进货成本 6500 元。 如何推出毛利和毛利率？它们还没有扣除哪些费用？
- answer: 根据已经给出的材料，我能推出：本例毛利等于 10000 - 6500 = 3500 元；本例毛利率等于 3500 / 10000 = 35%。
- missing: 毛利还没有扣除销售管理研发财务等期间费用

- run_id: `d75354d9b0324031`
- node: `income_statement_boundary` 交易进入利润表的边界
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.3333 -> 0.3333
- question: 一家咖啡店本月向顾客出售咖啡，同时从银行借入一笔一年期贷款。 哪一项更可能进入利润表作为经营成果？请说明为什么贷款不是营业收入。
- answer: 规则说：利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- tags: completeness_blocker, rote_repetition

- run_id: `ee674563f4bc3832`
- node: `revenue_recognition` 收入确认
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.0
- question: 设计公司本月完成并交付一套海报，客户约定下月付款。 本月是否可能确认收入？回答时区分“完成服务”和“收到现金”。
- answer: 规则说：收入通常来自销售商品或提供服务；在权责发生制下，收入确认不一定等于收到现金。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- tags: completeness_blocker, rote_repetition

- run_id: `3e84ef3c746e97e2`
- node: `revenue_not_cash_receipt` 收入不等于收款
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.3333
- question: 批发商本月赊销 8000 元商品，客户 45 天后付款。 本月利润表和现金分别可能怎样变化？请说明收入为什么不等于收款。
- answer: 规则说：收入记录赚到的经营成果；收款记录现金进入。赊销会让收入和现金流入出现时间差。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- tags: completeness_blocker, rote_repetition

- run_id: `1263b89da49fd4bd`
- node: `expense_recognition` 费用确认
- persona/condition: `rote_memorizer` / `hidden_transfer`
- rule/judge: 0.0 -> 0.0
- question: 门店员工已经完成本月工作，工资约定下月发放。 本月是否可能确认工资费用？请区分费用发生和现金付款。
- answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。。照规则说，我只需要背规则，但这个新案例我不能完整判断。
- missing: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- tags: completeness_blocker, rote_repetition

## 备注

- 本报告只读正式 `data/knowledge_graph.yaml`，不会修改正式知识图谱。
- 当前 mock judge 用于验证数据流和报告结构，不等价于真实语义评分。
- `graph_fallback_used_runs` 大于 0 表示 `data/chain_definitions.yaml` 和图谱链字段均不可用，实验才使用内置 fallback。
