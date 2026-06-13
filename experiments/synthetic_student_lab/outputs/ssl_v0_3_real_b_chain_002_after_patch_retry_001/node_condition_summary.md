# Node And Condition Summary

## Focus Nodes

### `accrual_vs_cash`
- judge_passed: 2/12 (16.7%)
- conflict_type: {'both_fail': 10, 'rule_fail_llm_pass': 2}
- top_misconception_tags: {'rote_repetition': 3, 'expense_payment_confusion': 3, 'revenue_cash_confusion': 3, 'insufficient_materials': 1, 'weak_transfer': 1}
- chain_so_far: 1/3 (33.3%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 0/3 (0.0%)

### `expense_recognition`
- judge_passed: 5/12 (41.7%)
- conflict_type: {'both_fail': 7, 'rule_fail_llm_pass': 5}
- top_misconception_tags: {'rote_repetition': 2, '只看现金流出不看费用归属期间': 2, '没付款就没有费用': 2, 'insufficient_materials': 1, 'expense_payment_confusion': 1}
- chain_so_far: 2/3 (66.7%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 2/3 (66.7%)

### `net_profit`
- judge_passed: 3/12 (25.0%)
- conflict_type: {'both_fail': 9, 'rule_fail_llm_pass': 3}
- top_misconception_tags: {'profit_cash_confusion': 3, 'rote_repetition': 1, '净利润为正就一定不缺钱。': 1, '净利润为正就一定现金充足': 1}
- chain_so_far: 1/3 (33.3%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 1/3 (33.3%)

### `revenue_recognition`
- judge_passed: 1/12 (8.3%)
- conflict_type: {'both_fail': 11, 'rule_fail_llm_pass': 1}
- top_misconception_tags: {'rote_repetition': 3, 'insufficient_materials': 1}
- chain_so_far: 1/3 (33.3%)
- hidden_transfer: 0/3 (0.0%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 0/3 (0.0%)

## Hidden Transfer High Pass Rate
- overall hidden_transfer judge_passed: 6/24 (25.0%)
- `gross_margin`: 2/3 (66.7%) [normal]
- `net_profit`: 1/3 (33.3%) [normal]
- `expense_recognition`: 1/3 (33.3%) [normal]
- `depreciation_amortization`: 1/3 (33.3%) [normal]
- `accrual_vs_cash`: 1/3 (33.3%) [normal]
- `revenue_recognition`: 0/3 (0.0%) [normal]
- `revenue_not_cash_receipt`: 0/3 (0.0%) [normal]
- `income_statement_boundary`: 0/3 (0.0%) [normal]

## node_only 0/3 Nodes
- `accrual_vs_cash`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `depreciation_amortization`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `gross_margin`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'rule_pass_llm_fail': 2, 'both_fail': 1}
- `revenue_recognition`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
