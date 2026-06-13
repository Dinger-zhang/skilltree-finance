# Enhanced Rule Score Report

- output_jsonl: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/judge_results.enhanced.jsonl`
- total_rows: 96

## Overall

- old_rule_score_avg: 0.0582
- enhanced_rule_score_avg: 0.2656
- judge_score_avg: 0.1664
- old_rule_passed: 4/96 (4.2%)
- enhanced_rule_passed: 24/96 (25.0%)
- old_rule_fail_llm_pass: 13
- enhanced_rule_fail_llm_pass: 3
- old_rule_pass_llm_fail: 1
- old_rule_pass_llm_fail_with_contradiction_detected: 0/1
- reported_issue_baseline_enhanced_rule_pass_llm_fail: 8
- current_enhanced_rule_pass_llm_fail: 11
- enhanced_conflict_type: {'both_fail': 69, 'rule_pass_llm_fail': 11, 'both_pass': 13, 'rule_fail_llm_pass': 3}
- conclusion_status: FAIL

## Targeted Fix Checks

### expense_recognition
- reported_issue_baseline_enhanced_avg: 0.0000
- reported_issue_baseline_enhanced_rule_fail_llm_pass: 7
- previous_file_enhanced_avg: n/a
- previous_file_enhanced_rule_fail_llm_pass: n/a
- current_enhanced_avg: 0.4445
- current_enhanced_rule_fail_llm_pass: 0

### net_profit
- generic_run_id: `787b5003cc442550`
- reported_issue_baseline_score: 1.0000
- reported_issue_baseline_net_profit_rule_pass_llm_fail: 3
- previous_file_score: n/a
- current_score: n/a
- current_passed: n/a
- previous_file_net_profit_rule_pass_llm_fail: n/a
- current_net_profit_rule_pass_llm_fail: 1

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
| `accrual_vs_cash` | 12 | 0.1042 | 0.1250 | +0.0208 | 0 | 0 | 1 | 1 |
| `depreciation_amortization` | 12 | 0.0000 | 0.0833 | +0.0833 | 0 | 1 | 0 | 0 |
| `expense_recognition` | 12 | 0.0000 | 0.4445 | +0.4445 | 0 | 6 | 4 | 0 |
| `gross_margin` | 12 | 0.1389 | 0.2500 | +0.1111 | 2 | 3 | 0 | 0 |
| `income_statement_boundary` | 12 | 0.0278 | 0.4167 | +0.3889 | 0 | 5 | 3 | 0 |
| `net_profit` | 12 | 0.0000 | 0.1111 | +0.1111 | 0 | 1 | 2 | 2 |
| `revenue_not_cash_receipt` | 12 | 0.1944 | 0.2778 | +0.0833 | 2 | 3 | 1 | 0 |
| `revenue_recognition` | 12 | 0.0000 | 0.4167 | +0.4167 | 0 | 5 | 2 | 0 |

## Enhanced Rule Pass LLM Fail Samples (11)

### 1. `f599d9bb1b2418b3`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是销售商品或提供服务产生的，所以不应作为营业收入进入利润表。

### 2. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款是资金来源的变化，不是销售商品或提供服务产生的收入，所以不应作为营业收入进入利润表。

### 3. `9f925b57d5ef9706`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认关注的是赚到收入而不是收到现金。材料中的设计公司本月完成并交付海报，即使客户下月付款，本月仍可能确认收入，因为服务已经完成。

### 4. `5597cb7ad2db9ba6`
- node_id / condition / persona: `revenue_not_cash_receipt` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.6667 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 赊销可能先确认收入；未收现金时现金不一定增加；可能形成应收账款而不是现金流入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以可能确认收入但现金没有增加。

### 5. `1cfaba10d861f9c4`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，不一定等于当期现金付款。本月工资虽然下月才发，但它是本月员工工作产生的耗费，服务于本月经营，所以可能作为本月费用。

### 6. `79c64d2597f89e85`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但因为它服务于本月经营，所以可以作为本月费用。

### 7. `d2ba14e5050c1df2`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收到现金（如赊销），费用发生也不等于现金支付（如工资下月发放），折旧和摊销会减少利润但通常不代表当期现金流出。所以净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。

### 8. `4b6cc7d618879fba`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 因为收入确认看的是服务完成，不是收到现金，所以本月完成服务就可以确认收入，但客户下月才付款，所以现金还没收到，收入已经确认了。不过我觉得没收到钱就确认收入有点奇怪，毕竟钱还没到账。

### 9. `3982efb926a2baf0`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.3 / False
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 因为收入确认看的是服务是否完成，不是看有没有收到钱。但是，如果客户下月才付款，那这个月其实还没收到现金，所以我觉得严格来说不应该算收入，因为没收到钱就不算赚到。

### 10. `801b3238e4c0630e`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 折旧会减少利润，因为折旧是费用，但折旧不是现金流出，因为折旧是长期资产成本的分摊，不是真的付钱。不过，折旧减少利润，那现金应该也会减少吧？因为利润少了，现金肯定也少了。

### 11. `84591106c3523017`
- node_id / condition / persona: `gross_margin` / `node_only` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 毛利率高说明收入减去销售成本后剩下的钱多，那净利润应该也高啊。材料说毛利还不是净利润，但我觉得毛利高的话，净利润肯定也高，因为剩下的钱多嘛。

## Top 10 Score Changes

### 1. `f599d9bb1b2418b3`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款属于资金来源变化，不是销售商品或提供服务产生的，所以不应作为营业收入进入利润表。

### 2. `1d2f4a510281905d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款是资金来源的变化，不是销售商品或提供服务产生的收入，所以不应作为营业收入进入利润表。

### 3. `4e12cea729ecaa0a`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.67 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务，即使客户下月付款，也可能确认收入。

### 4. `9f925b57d5ef9706`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认关注的是赚到收入而不是收到现金。材料中的设计公司本月完成并交付海报，即使客户下月付款，本月仍可能确认收入，因为服务已经完成。

### 5. `1cfaba10d861f9c4`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，不一定等于当期现金付款。本月工资虽然下月才发，但它是本月员工工作产生的耗费，服务于本月经营，所以可能作为本月费用。

### 6. `79c64d2597f89e85`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但因为它服务于本月经营，所以可以作为本月费用。

### 7. `d2ba14e5050c1df2`
- node_id / condition / persona: `net_profit` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.0 / False
- old_conflict_type -> enhanced_conflict_type: `both_fail` -> `rule_pass_llm_fail`
- enhanced_matched_reasoning_points: 净利润大致等于收入扣除成本费用和税费；净利润可能包含未收现收入；净利润可能包含非现金费用所以不等于现金
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，净利润为正不一定代表现金充足，因为利润表记录的是经营成果，而不是现金流入。材料中提到，收入确认不等于收到现金（如赊销），费用发生也不等于现金支付（如工资下月发放），折旧和摊销会减少利润但通常不代表当期现金流出。所以净利润为正时，可能因为赊销、未付款的费用或折旧等原因，现金并没有同步增加。

### 8. `7839880dba2edf96`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说利润表记录经营成果，不是所有现金流入。银行借款不是来自销售商品或提供服务，所以不应作为营业收入。

### 9. `75e013c030b465ac`
- node_id / condition / persona: `income_statement_boundary` / `hidden_transfer` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或服务形成收入或费用边界内的交易；银行借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说利润表记录经营成果，看收入、成本、费用，不是所有现金流入。贷款不是销售商品或提供服务，所以不是营业收入。

### 10. `bcb84f9ceba8fce9`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.667 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说收入确认不一定等于收到现金，所以本月完成服务就可以确认收入。

## Contradiction Detected Samples

- none

## Conclusion

- enhanced scorer 未满足关键修复条件，需要继续收紧或补充语义规则。
- 建议先修评分器再进入课程修改；当前差异主要来自同义表达识别和矛盾答案惩罚，而不是课程内容本身已经被证伪。
