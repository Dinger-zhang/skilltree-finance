# Enhanced Rule Score Report

- output_jsonl: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/judge_results.enhanced.jsonl`
- total_rows: 96

## Overall

- old_rule_score_avg: 0.1693
- enhanced_rule_score_avg: 0.5380
- judge_score_avg: 0.5553
- old_rule_passed: 13/96 (13.5%)
- enhanced_rule_passed: 45/96 (46.9%)
- old_rule_fail_llm_pass: 43
- enhanced_rule_fail_llm_pass: 13
- old_rule_pass_llm_fail: 1
- old_rule_pass_llm_fail_with_contradiction_detected: 1/1
- reported_issue_baseline_enhanced_rule_pass_llm_fail: 8
- current_enhanced_rule_pass_llm_fail: 3
- enhanced_conflict_type: {'both_fail': 38, 'both_pass': 42, 'rule_fail_llm_pass': 13, 'rule_pass_llm_fail': 3}
- conclusion_status: PASS

## Targeted Fix Checks

### expense_recognition
- reported_issue_baseline_enhanced_avg: 0.0000
- reported_issue_baseline_enhanced_rule_fail_llm_pass: 7
- previous_file_enhanced_avg: 0.5545
- previous_file_enhanced_rule_fail_llm_pass: 1
- current_enhanced_avg: 0.5545
- current_enhanced_rule_fail_llm_pass: 1

### net_profit
- generic_run_id: `787b5003cc442550`
- reported_issue_baseline_score: 1.0000
- reported_issue_baseline_net_profit_rule_pass_llm_fail: 3
- previous_file_score: 0.0
- current_score: 0.0
- current_passed: False
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
| `accrual_vs_cash` | 12 | 0.2708 | 0.3050 | +0.0342 | 0 | 1 | 5 | 4 |
| `depreciation_amortization` | 12 | 0.0000 | 0.7500 | +0.7500 | 0 | 9 | 9 | 0 |
| `expense_recognition` | 12 | 0.0000 | 0.5545 | +0.5545 | 0 | 7 | 7 | 1 |
| `gross_margin` | 12 | 0.4722 | 0.7083 | +0.2361 | 7 | 8 | 0 | 1 |
| `income_statement_boundary` | 12 | 0.1111 | 0.5833 | +0.4722 | 0 | 7 | 7 | 0 |
| `net_profit` | 12 | 0.0278 | 0.2500 | +0.2222 | 0 | 2 | 6 | 4 |
| `revenue_not_cash_receipt` | 12 | 0.4722 | 0.5278 | +0.0555 | 6 | 5 | 3 | 3 |
| `revenue_recognition` | 12 | 0.0000 | 0.6250 | +0.6250 | 0 | 6 | 6 | 0 |

## Enhanced Rule Pass LLM Fail Samples (3)

### 1. `2428a0798f5f6d5f`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `rote_memorizer`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.0 / False
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 规则说：费用是为取得收入或维持经营发生的资源耗费；费用发生不一定等于当期现金付款。所以本月工资下月才发，也可能作为本月费用。

### 2. `64738d379054303a`
- node_id / condition / persona: `gross_margin` / `node_only` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.3333 -> 1.0
- judge_score / judge_passed: 0.33 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 毛利率高说明收入减去销售成本后剩下的钱多，那净利润应该也高啊，因为剩下的钱多就是赚得多。材料说毛利等于收入减销售成本，但净利润还要扣其他费用，不过我觉得毛利高的话，净利润肯定也高，因为钱多了嘛。

### 3. `c51e61ab690c5041`
- node_id / condition / persona: `gross_margin` / `chain_so_far` / `misconception_prone`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0
- judge_score / judge_passed: 0.3 / False
- enhanced_matched_reasoning_points: 毛利等于收入减销售成本；毛利率等于毛利除以收入；毛利还没有扣除销售管理研发财务等期间费用
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 毛利率高说明收入减去销售成本后剩下的钱多，但净利润还要扣掉其他费用，比如折旧、工资这些。不过我觉得毛利率高的话，净利润应该也不会太差吧，毕竟毛利高说明赚得多，那现金也应该多，净利润肯定也高。

## Top 10 Score Changes

### 1. `bd4d2df63ecbbc29`
- node_id / condition / persona: `income_statement_boundary` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.6667 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，重点看收入、成本、费用，而不是所有现金流入。银行借款是资金来源变化，不是销售商品或提供服务产生的，所以不应作为营业收入进入利润表。

### 2. `6ac87983201c5f3d`
- node_id / condition / persona: `income_statement_boundary` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 利润表记录一段期间的经营成果；销售商品或提供服务才通常形成收入；借款是筹资活动不是营业收入
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，利润表记录的是经营成果，而不是所有现金流入。银行借款属于资金来源变化，不是来自销售商品或提供服务，所以不应作为营业收入进入利润表。

### 3. `07a7bc27537b666b`
- node_id / condition / persona: `revenue_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认不一定等于收到现金。本月完成服务并交付，符合收入确认条件，所以即使客户下月付款，本月仍可能确认收入。

### 4. `8c9eead5abf00753`
- node_id / condition / persona: `revenue_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 0.6 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认关注的是赚到还是收到现金，在权责发生制下，收入确认不一定等于收到现金。所以即使客户下月付款，本月完成服务仍可能确认收入。

### 5. `ae2796aa8b8a9207`
- node_id / condition / persona: `revenue_recognition` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 收入来自销售商品或提供服务；完成交付或服务后可能满足收入确认条件；收入确认不一定依赖现金已经到账
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，收入确认关注的是服务是否完成或商品是否交付，而不是是否收到现金。材料中设计公司本月完成并交付海报，所以本月可能确认收入。但客户下月付款，这属于现金流入的时间差异，不影响收入确认。

### 6. `282b0ca91b15a302`
- node_id / condition / persona: `expense_recognition` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。所以本月工资虽然下月才发，但员工本月已经完成了工作，耗费服务于本期经营，因此可以作为本月费用。

### 7. `2461ec4dfa2f2a24`
- node_id / condition / persona: `expense_recognition` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 费用是为取得收入或维持经营发生的耗费；费用发生不一定等于当期已经付款；工资费用会减少本期利润
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，费用确认关注的是耗费是否服务于本期经营，而不是现金支付时间。员工本月完成工作，工资虽下月发放，但耗费服务于本月，所以应作为本月费用。

### 8. `b488edcce2fd39d2`
- node_id / condition / persona: `depreciation_amortization` / `node_only` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 9. `72309d416d4e32b1`
- node_id / condition / persona: `depreciation_amortization` / `chain_so_far` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。

### 10. `28922aa745eb2000`
- node_id / condition / persona: `depreciation_amortization` / `hidden_transfer` / `novice_closed_book`
- old_rule_score -> enhanced_rule_score: 0.0 -> 1.0 (+1.0000)
- judge_score / judge_passed: 1.0 / True
- old_conflict_type -> enhanced_conflict_type: `rule_fail_llm_pass` -> `both_pass`
- enhanced_matched_reasoning_points: 折旧是长期资产成本在多个期间的分摊；折旧费用会减少当期利润；折旧通常不是当期现金流出
- enhanced_missing_reasoning_points: -
- contradiction_tags: -
- scoring_notes: base exact/alias matching preserved；normalized synonym and semantic matching applied
- student_answer: 根据课程材料，折旧和摊销把长期资产成本分摊到多个期间，会减少当期利润，但通常不代表当期现金流出。所以今年的折旧会影响利润，但通常不代表今年再次付现金。

## Contradiction Detected Samples

1. `fe8aa32a0750e1bc` | `revenue_recognition` | `node_only` | `misconception_prone` | old=0.0 enhanced=0.5 judge=0.0 | tags=cash_required_for_revenue
   - answer: 因为收入确认看的是有没有收到钱，没收到钱就不能算收入，所以本月不能确认收入。
2. `797256b2ab910c9f` | `revenue_recognition` | `chain_so_far` | `misconception_prone` | old=0.0 enhanced=0.5 judge=0.2 | tags=cash_required_for_revenue
   - answer: 因为材料说收入确认不一定等于收到现金，但我觉得没收到钱就不算收入，所以这个题有点矛盾。
3. `7a2d69dfbbeea172` | `revenue_recognition` | `hidden_transfer` | `misconception_prone` | old=0.0 enhanced=0.5 judge=0.0 | tags=cash_required_for_revenue
   - answer: 没收到钱就不能算收入，因为客户下月才付款，所以本月不能确认收入。完成服务不等于收到现金，收入确认必须等到实际收款。
4. `0e9191c369ce91ef` | `revenue_not_cash_receipt` | `chain_so_far` | `misconception_prone` | old=0.6667 enhanced=0.5 judge=0.5 | tags=cash_required_for_revenue；revenue_implies_cash
   - answer: 因为收入确认看的是商品是否卖出，不是看有没有收到钱。赊销时商品已经卖出，所以可以确认收入，但现金还没收到，所以现金没有增加。不过我觉得这有点奇怪，没收到钱怎么能算收入呢？收入增加应该意味着现金也增加才对。
5. `cbf5c3a37f4f3c4b` | `revenue_not_cash_receipt` | `hidden_transfer` | `misconception_prone` | old=1.0 enhanced=0.5 judge=0.6667 | tags=cash_required_for_revenue
   - answer: 材料说收入记录赚到的经营成果，收款记录现金进入。赊销会让收入和现金流入出现时间差。所以本月利润表收入增加8000元，但现金没有增加，因为客户45天后才付款。收入不等于收款是因为收入确认看的是商品卖出，不是收到现金。不过我觉得没收到钱就不算收入，但材料说可以确认收入，那可能还是算收入吧。
6. `e3f49d1cad82ec87` | `expense_recognition` | `node_only` | `misconception_prone` | old=0.0 enhanced=0.3267 judge=0.67 | tags=payment_required_for_expense
   - answer: 因为材料说费用是为取得收入或维持经营发生的资源耗费，所以即使工资下月才发，只要员工本月工作了，就应该算作本月的费用。但是我觉得没付款就没有费用，所以不太明白为什么没付钱也能算费用。
7. `4c33192e51dcb12c` | `expense_recognition` | `hidden_transfer` | `misconception_prone` | old=0.0 enhanced=0.3267 judge=0.3 | tags=payment_required_for_expense
   - answer: 材料说费用是为取得收入或维持经营发生的资源耗费，费用发生不一定等于当期现金付款。但我觉得工资还没付出去，没付款就没有费用，所以本月不应该确认工资费用。
8. `980c60f5d75ad6a1` | `gross_margin` | `hidden_transfer` | `misconception_prone` | old=0.6667 enhanced=0.5 judge=0.7 | tags=revenue_implies_cash
   - answer: 毛利就是收入减销售成本，10000减6500等于3500元，毛利率就是3500除以10000等于35%。这些还没有扣除的费用包括工资、租金、折旧这些。不过，收入增加说明现金也增加了，所以毛利高的话现金应该也多。
9. `139b652418ab1cf8` | `accrual_vs_cash` | `node_only` | `misconception_prone` | old=0.0 enhanced=0.0 judge=0.0 | tags=accrual_cash_basis_confusion；payment_required_for_expense
   - answer: 权责发生制和现金制的核心区别是：权责发生制关注现金是否实际收付，而现金制关注交易归属期间。没付款就没有费用。
10. `87b86a8a5f8e4076` | `accrual_vs_cash` | `chain_so_far` | `misconception_prone` | old=0.5 enhanced=0.16 judge=0.6 | tags=payment_required_for_expense
   - answer: 权责发生制和现金制的核心区别是：权责发生制关注交易归属期间，现金制关注现金实际收付时间。但我觉得权责发生制其实更关注现金是否实际收付，因为没收到钱就不能算收入，没付款就没有费用。

## Conclusion

- enhanced scorer 修复通过：expense_recognition 已改善，net_profit 泛泛结论被压低，矛盾答案未通过。
- 建议先修评分器再进入课程修改；当前差异主要来自同义表达识别和矛盾答案惩罚，而不是课程内容本身已经被证伪。
