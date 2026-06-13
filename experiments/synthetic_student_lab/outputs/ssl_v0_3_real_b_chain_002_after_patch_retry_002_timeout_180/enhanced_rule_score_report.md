# Enhanced Rule Score Report

## 中文摘要

本报告由本地 `rescore_with_enhanced_rules.py` 生成；本次重算未调用真实 API。

```text
scorer 版本阶段：v3.1 false fail 小修后
total_rows: 96
judge_passed: 47/96
enhanced_rule_passed: 32/96
enhanced false pass: 0
enhanced false fail: 15
enhanced_rule_score_avg: 0.3984
conclusion_status: FAIL
```

核心变化：

```text
v3.1 将 3 条高置信 scorer_too_strict 样本转为通过。
v3.1 未引入新的 enhanced false pass。
课程验证结论仍为 FAIL，本报告不能证明课程 patch 有效。
```

- output_jsonl: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl`
- total_rows: 96

## Overall

- old_rule_score_avg: 0.1207
- enhanced_rule_score_avg: 0.3984
- judge_score_avg: 0.4811
- old_rule_passed: 6/96 (6.2%)
- enhanced_rule_passed: 32/96 (33.3%)
- old_rule_fail_llm_pass: 42
- enhanced_rule_fail_llm_pass: 15
- old_rule_pass_llm_fail: 1
- old_rule_pass_llm_fail_with_contradiction_detected: 1/1
- reported_issue_baseline_enhanced_rule_pass_llm_fail: 8
- current_enhanced_rule_pass_llm_fail: 0
- enhanced_conflict_type: {'both_fail': 49, 'both_pass': 32, 'rule_fail_llm_pass': 15}
- conclusion_status: FAIL

## Targeted Fix Checks

### expense_recognition
- reported_issue_baseline_enhanced_avg: 0.0000
- reported_issue_baseline_enhanced_rule_fail_llm_pass: 7
- previous_file_enhanced_avg: 0.4722
- previous_file_enhanced_rule_fail_llm_pass: 0
- current_enhanced_avg: 0.4722
- current_enhanced_rule_fail_llm_pass: 0

### net_profit
- generic_run_id: `787b5003cc442550`
- reported_issue_baseline_score: 1.0000
- reported_issue_baseline_net_profit_rule_pass_llm_fail: 3
- previous_file_score: n/a
- current_score: n/a
- current_passed: n/a
- previous_file_net_profit_rule_pass_llm_fail: 0
- current_net_profit_rule_pass_llm_fail: 0

## Sanity Tests

- all_sanity_tests_passed: True

| test | passed | score | rule_passed | contradiction_detected | tags | expectation |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `net_profit_generic_answer_should_not_full_pass` | True | 0.0 | False | False | - | enhanced_rule_score <= 0.4 and enhanced_rule_passed is false |
| `net_profit_mechanism_answer_should_pass` | True | 1.0 | True | False | - | enhanced_rule_score >= 0.8 and enhanced_rule_passed is true |
| `expense_recognition_complete_answer_should_pass` | True | 1.0 | True | False | - | enhanced_rule_score >= 0.8 and enhanced_rule_passed is true |
| `expense_recognition_contradiction_should_fail` | True | 0.0 | False | True | payment_required_for_expense | contradiction_detected is true and enhanced_rule_passed is false |
| `accrual_vs_cash_reversed_definition_should_fail` | True | 0.0 | False | True | accrual_cash_basis_confusion；payment_required_for_expense | contradiction_detected is true and enhanced_rule_passed is false |

## By Node

| node_id | rows | old_avg | enhanced_avg | avg_delta | old_pass | enhanced_pass | old_rule_fail_llm_pass | enhanced_rule_fail_llm_pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `accrual_vs_cash` | 12 | 0.2708 | 0.3125 | +0.0417 | 0 | 1 | 1 | 0 |
| `depreciation_amortization` | 12 | 0.0000 | 0.5000 | +0.5000 | 0 | 6 | 8 | 2 |
| `expense_recognition` | 12 | 0.0000 | 0.4722 | +0.4722 | 0 | 5 | 5 | 0 |
| `gross_margin` | 12 | 0.2500 | 0.4028 | +0.1528 | 3 | 2 | 2 | 3 |
| `income_statement_boundary` | 12 | 0.0555 | 0.5556 | +0.5000 | 0 | 7 | 9 | 2 |
| `net_profit` | 12 | 0.0555 | 0.2778 | +0.2222 | 0 | 2 | 6 | 4 |
| `revenue_not_cash_receipt` | 12 | 0.3333 | 0.3606 | +0.0272 | 3 | 5 | 6 | 3 |
| `revenue_recognition` | 12 | 0.0000 | 0.3056 | +0.3056 | 0 | 4 | 5 | 1 |

## Enhanced Rule Pass LLM Fail Samples (0)

- none

## Top 10 Score Changes

### 1. `f599d9bb1b2418b3`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，利润表记录经营成果，重点是收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，因此不应作为营业收入进入利润表。

### 2. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，不反映经营成果，所以不应作为营业收入进入利润表。

### 3. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认通常看服务是否完成或商品是否交付，而不是看是否收到现金。本月服务已完成，所以即使客户下月付款，本月仍可确认收入。

### 4. `9f925b57d5ef9706`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，在权责发生制下，收入确认基于服务是否完成而非款项是否收到。本月已完成服务并交付，满足了收入确认条件，因此即使客户下月付款，本月仍可确认收入。

### 5. `5d70ff16349ce408`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，本月可以确认收入，因为服务已完成并交付，收入确认关注的是是否赚到（即完成服务），而不是是否收到现金。客户下月付款不影响本月的收入确认。

### 6. `1cfaba10d861f9c4`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.6667 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。本月员工已为本月经营工作，耗费发生在本月，即使工资下月发放，也应作为本月费用。

### 7. `79c64d2597f89e85`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.6667 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 材料说，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。员工本月工作服务于本月经营，所以即使下月发工资，也应作为本月费用。

### 8. `ff04d3360d229fb1`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 9. `ef006d458bad3b49`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 10. `a8027fffd436418b`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 折旧是长期资产成本的分摊，会减少利润，但通常不代表当期现金流出，因为现金在购买时已经支付。

## Contradiction Detected Samples

1. `4b6cc7d618879fba` | `revenue_recognition` | `node_only` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.0 | tags=cash_required_for_revenue
   - answer: 客户下月付款，本月没有收到现金，所以不应该确认收入。材料说收入确认不一定等于收到现金，但我觉得那不合理，没收到钱怎么能算收入呢？
2. `3982efb926a2baf0` | `revenue_recognition` | `chain_so_far` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.0 | tags=cash_required_for_revenue
   - answer: 材料说收入确认不一定等于收到现金，但我不太同意。既然客户下个月才付款，这个月根本没收到钱，怎么能算收入呢？我认为收入增加应该对应现金增加，没收到钱就不应该确认收入。
3. `90ffab514a6ce477` | `revenue_recognition` | `hidden_transfer` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.0 | tags=cash_required_for_revenue
   - answer: 不能确认收入，因为还没收到现金。客户下月才付款，所以收入应该在下月收到现金时确认。完成服务不等于收到钱，没收到钱就不能算收入。
4. `57d885de1199748c` | `revenue_not_cash_receipt` | `node_only` | `misconception_prone` | old=0.3333 enhanced=0.0 judge=0.6667 | tags=cash_required_for_revenue
   - answer: 材料说收入记录赚到的经营成果，收款记录现金进入，赊销会有时间差。但我还是觉得没收到钱就不应该算收入，所以现金没增加时确认收入不合理。
5. `1b8d3d51286c162a` | `revenue_not_cash_receipt` | `chain_so_far` | `misconception_prone` | old=0.3333 enhanced=0.0 judge=0.6 | tags=revenue_implies_cash
   - answer: 材料说收入记录赚到的经营成果，收款记录现金进入，赊销时收入确认不等于收到现金。但我还是觉得收入增加就应该意味着现金增加，不然怎么叫赚到呢？
6. `b7c79c56ca63ca4c` | `revenue_not_cash_receipt` | `hidden_transfer` | `misconception_prone` | old=0.6667 enhanced=0.3267 judge=0.33 | tags=cash_required_for_revenue；revenue_implies_cash
   - answer: 本月利润表上不应该确认收入，因为没有收到现金，现金也没变化。收入必须是在收到现金时才能确认，所以收入等于收款。赊销商品没收到钱，所以不能算收入。
7. `83e7249776e6fea2` | `depreciation_amortization` | `node_only` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.33 | tags=depreciation_implies_cash_outflow
   - answer: 折旧减少利润是因为它被计入费用，但折旧实际上就是每个月为资产付出去的钱，所以它也算是现金流出。
8. `a40ddd549a31f9ec` | `gross_margin` | `hidden_transfer` | `misconception_prone` | old=0.6667 enhanced=0.5 judge=0.6667 | tags=gross_margin_implies_net_profit
   - answer: 毛利=10000-6500=3500元，毛利率=3500/10000=35%。材料说毛利率就是净利率，所以净利率也是35%。它们还没有扣除其他费用，但毛利已经包含了所有成本，所以净利润就是3500元。

## Conclusion

- enhanced scorer 未满足关键修复条件，需要继续收紧或补充语义规则。
- 建议先修评分器再进入课程修改；当前差异主要来自同义表达识别和矛盾答案惩罚，而不是课程内容本身已经被证伪。
