# Node And Condition Summary

## Focus Nodes

### `accrual_vs_cash`
- judge_passed: 1/12 (8.3%)
- conflict_type: {'both_fail': 11, 'rule_fail_llm_pass': 1}
- top_misconception_tags: {'insufficient_materials': 1, 'rote_repetition': 1}
- chain_so_far: 0/3 (0.0%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 0/3 (0.0%)

### `expense_recognition`
- judge_passed: 4/12 (33.3%)
- conflict_type: {'both_fail': 8, 'rule_fail_llm_pass': 4}
- top_misconception_tags: {'rote_repetition': 2, 'expense_payment_confusion': 2}
- chain_so_far: 1/3 (33.3%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 2/3 (66.7%)

### `net_profit`
- judge_passed: 2/12 (16.7%)
- conflict_type: {'both_fail': 10, 'rule_fail_llm_pass': 2}
- top_misconception_tags: {'rote_repetition': 2, 'insufficient_materials': 1, '无法推理': 1, 'weak_transfer': 1, 'profit_cash_confusion': 1}
- chain_so_far: 1/3 (33.3%)
- hidden_transfer: 0/3 (0.0%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 1/3 (33.3%)

### `revenue_recognition`
- judge_passed: 2/12 (16.7%)
- conflict_type: {'both_fail': 10, 'rule_fail_llm_pass': 2}
- top_misconception_tags: {'revenue_cash_confusion': 3, 'insufficient_materials': 1, 'rote_repetition': 1, 'weak_transfer': 1, '没收到现金就一定不能确认收入。': 1}
- chain_so_far: 0/3 (0.0%)
- hidden_transfer: 1/3 (33.3%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 1/3 (33.3%)

## Hidden Transfer High Pass Rate
- overall hidden_transfer judge_passed: 8/24 (33.3%)
- `revenue_not_cash_receipt`: 2/3 (66.7%) [normal]
- `income_statement_boundary`: 2/3 (66.7%) [normal]
- `revenue_recognition`: 1/3 (33.3%) [normal]
- `gross_margin`: 1/3 (33.3%) [normal]
- `expense_recognition`: 1/3 (33.3%) [normal]
- `accrual_vs_cash`: 1/3 (33.3%) [normal]
- `net_profit`: 0/3 (0.0%) [normal]
- `depreciation_amortization`: 0/3 (0.0%) [normal]

## node_only 0/3 Nodes
- `accrual_vs_cash`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `depreciation_amortization`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `gross_margin`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `income_statement_boundary`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
- `revenue_not_cash_receipt`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
