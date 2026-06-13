# Enhanced Rule Score Report

- output_jsonl: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_001/judge_results.enhanced.jsonl`
- total_rows: 96

## Overall

- old_rule_score_avg: 0.1050
- enhanced_rule_score_avg: 0.3315
- judge_score_avg: 0.2416
- old_rule_passed: 7/96 (7.3%)
- enhanced_rule_passed: 28/96 (29.2%)
- old_rule_fail_llm_pass: 18
- enhanced_rule_fail_llm_pass: 5
- old_rule_pass_llm_fail: 2
- old_rule_pass_llm_fail_with_contradiction_detected: 0/2
- reported_issue_baseline_enhanced_rule_pass_llm_fail: 8
- current_enhanced_rule_pass_llm_fail: 10
- enhanced_conflict_type: {'both_fail': 63, 'both_pass': 18, 'rule_pass_llm_fail': 10, 'rule_fail_llm_pass': 5}
- conclusion_status: FAIL

## Targeted Fix Checks

### expense_recognition
- reported_issue_baseline_enhanced_avg: 0.0000
- reported_issue_baseline_enhanced_rule_fail_llm_pass: 7
- previous_file_enhanced_avg: n/a
- previous_file_enhanced_rule_fail_llm_pass: n/a
- current_enhanced_avg: 0.3889
- current_enhanced_rule_fail_llm_pass: 0

### net_profit
- generic_run_id: `787b5003cc442550`
- reported_issue_baseline_score: 1.0000
- reported_issue_baseline_net_profit_rule_pass_llm_fail: 3
- previous_file_score: n/a
- current_score: n/a
- current_passed: n/a
- previous_file_net_profit_rule_pass_llm_fail: n/a
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
| `accrual_vs_cash` | 12 | 0.3125 | 0.3467 | +0.0342 | 0 | 1 | 2 | 2 |
| `depreciation_amortization` | 12 | 0.0000 | 0.3333 | +0.3333 | 0 | 4 | 2 | 0 |
| `expense_recognition` | 12 | 0.0000 | 0.3889 | +0.3889 | 0 | 5 | 5 | 0 |
| `gross_margin` | 12 | 0.3333 | 0.5000 | +0.1667 | 5 | 6 | 0 | 0 |
| `income_statement_boundary` | 12 | 0.0278 | 0.4722 | +0.4445 | 0 | 6 | 4 | 0 |
| `net_profit` | 12 | 0.0278 | 0.1667 | +0.1389 | 0 | 1 | 3 | 2 |
| `revenue_not_cash_receipt` | 12 | 0.1389 | 0.1944 | +0.0556 | 2 | 2 | 1 | 1 |
| `revenue_recognition` | 12 | 0.0000 | 0.2500 | +0.2500 | 0 | 3 | 1 | 0 |

## Enhanced Rule Pass LLM Fail Samples (10)

### 1. `a15875025c353cca`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.3333 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录一段期间的经营成果，重点看收入、成本、费用，而不是所有现金流入。咖啡店向顾客出售咖啡属于销售商品，可能进入利润表作为收入。而银行借款只是资金来源变化，不是经营收入，所以不应进入利润表。

### 2. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。

### 3. `ff04d3360d229fb1`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以折旧减少利润是因为成本分摊，但不需要当期付出现金。

### 4. `a8027fffd436418b`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

### 5. `c8a1cd8fb15a26c6`
- node_id / condition / persona: `gross_margin` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.6667 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。材料没有提到净利润的计算，所以无法从当前课程材料推出完整答案。

### 6. `71fa0e4523ba0495`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.33 / False
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说：收入确认不一定等于收到现金。

### 7. `cec6e305439237b9`
- node_id / condition / persona: `gross_margin` / `node_only` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.6667 -> 1.0
- judge_score / judge_passed: 0.67 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说：毛利等于收入减销售成本，毛利率等于毛利除以收入，但毛利还不是净利润。所以毛利率高不等于净利润一定高。

### 8. `6f9da756a4a58197`
- node_id / condition / persona: `accrual_vs_cash` / `hidden_transfer` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.5 -> 0.75
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 权责发生制关注交易归属期间；满足条件时未收款也可能确认 6 月收入；现金制关注现金实际收付时间
- enhanced_missing_reasoning_points: 已发生费用即使未付款也可能归入 6 月
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说：权责发生制关注交易归属期间，现金制关注现金实际收付时间。所以6月完成服务，收入属于6月；6月发生房租，费用属于6月。现金制下，7月收款才算收入，7月付款才算费用。

### 9. `bee48c2ac1d6d055`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 0.6667
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: 利润表记录一段期间的经营成果
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 咖啡店卖咖啡的收入应该进利润表，因为那是经营成果。贷款不是营业收入，因为材料说不是所有现金流入都代表经营收入，借款只是资金来源变化。但是，我觉得贷款收到的钱也是钱，应该也算收入吧？不过材料说不能算，那就不算吧。

### 10. `5e8f09219a82b69d`
- node_id / condition / persona: `gross_margin` / `chain_so_far` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 毛利率高说明收入减去销售成本后剩下的比例大，但净利润还要扣掉很多其他费用，比如工资、房租、折旧这些。不过我觉得如果毛利率高，那净利润应该也不会太差吧，毕竟收入多成本少，利润肯定高。

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
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 2. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.8 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 3. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。

### 4. `1cfaba10d861f9c4`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.75 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工已经完成本月工作，耗费服务于本期经营，因此应作为本月费用。

### 5. `79c64d2597f89e85`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。员工已经完成本月工作，但工资下月发放，耗费服务于本期经营，所以应记入本期费用。

### 6. `ff04d3360d229fb1`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以折旧减少利润是因为成本分摊，但不需要当期付出现金。

### 7. `ef006d458bad3b49`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 8. `a8027fffd436418b`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

### 9. `d2ba14e5050c1df2`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.95 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收款，费用发生不等于现金支付，折旧和摊销会减少利润但不代表现金流出。所以，净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。

### 10. `bf2dc9120ce2ddfd`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务，所以不应作为营业收入。

## Contradiction Detected Samples

1. `b3cd9f655a514dd1` | `expense_recognition` | `hidden_transfer` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.0 | tags=payment_required_for_expense
   - answer: 没收到钱所以不算费用，工资下月才发，本月不应该确认工资费用。费用发生和现金付款是一回事，没付款就没有费用。
2. `b498fa1bf5bd5471` | `accrual_vs_cash` | `node_only` | `misconception_prone` | old=0.5 enhanced=0.16 judge=0.0 | tags=cash_required_for_revenue；payment_required_for_expense
   - answer: 权责发生制和现金制的核心区别是：权责发生制关注交易归属期间，现金制关注现金实际收付时间。但我觉得，没收到钱就不算收入，没付款就没有费用，所以权责发生制其实也是看现金的。

## Conclusion

- enhanced scorer 未满足关键修复条件，需要继续收紧或补充语义规则。
- 建议先修评分器再进入课程修改；当前差异主要来自同义表达识别和矛盾答案惩罚，而不是课程内容本身已经被证伪。
