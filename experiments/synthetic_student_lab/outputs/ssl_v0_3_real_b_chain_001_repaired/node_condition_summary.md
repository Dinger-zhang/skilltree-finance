# Node And Condition Summary

## Focus Nodes

### `accrual_vs_cash`
- judge_passed: 5/12 (41.7%)
- conflict_type: {'both_fail': 7, 'rule_fail_llm_pass': 5}
- top_misconception_tags: {'expense_payment_confusion': 3, 'revenue_cash_confusion': 3, 'rote_repetition': 2, '权责发生制更关注现金是否实际收付。': 2, '没付款就没有费用。': 2}
- chain_so_far: 2/3 (66.7%)
- hidden_transfer: 3/3 (100.0%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 0/3 (0.0%)

### `expense_recognition`
- judge_passed: 7/12 (58.3%)
- conflict_type: {'both_fail': 5, 'rule_fail_llm_pass': 7}
- top_misconception_tags: {'rote_repetition': 4, 'expense_payment_confusion': 4, '没付款就没有费用。': 2, 'insufficient_materials': 1, '不明确': 1}
- chain_so_far: 2/3 (66.7%)
- hidden_transfer: 2/3 (66.7%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 3/3 (100.0%)

### `net_profit`
- judge_passed: 6/12 (50.0%)
- conflict_type: {'both_fail': 6, 'rule_fail_llm_pass': 6}
- top_misconception_tags: {'rote_repetition': 4, 'profit_cash_confusion': 4, 'insufficient_materials': 1, '净利润为正就一定不缺钱。': 1, '净利润为正就一定现金充足': 1}
- chain_so_far: 2/3 (66.7%)
- hidden_transfer: 3/3 (100.0%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 1/3 (33.3%)

### `revenue_recognition`
- judge_passed: 6/12 (50.0%)
- conflict_type: {'both_fail': 6, 'rule_fail_llm_pass': 6}
- top_misconception_tags: {'revenue_cash_confusion': 4, 'rote_repetition': 3, '没收到现金就一定不能确认收入。': 2, 'insufficient_materials': 1, '把收款作为收入确认的唯一条件': 1}
- chain_so_far: 2/3 (66.7%)
- hidden_transfer: 2/3 (66.7%)
- no_course_baseline: 0/3 (0.0%)
- node_only: 2/3 (66.7%)

## Hidden Transfer High Pass Rate
- overall hidden_transfer judge_passed: 22/24 (91.7%)
- `revenue_not_cash_receipt`: 3/3 (100.0%) [high]
- `net_profit`: 3/3 (100.0%) [high]
- `income_statement_boundary`: 3/3 (100.0%) [high]
- `gross_margin`: 3/3 (100.0%) [high]
- `depreciation_amortization`: 3/3 (100.0%) [high]
- `accrual_vs_cash`: 3/3 (100.0%) [high]
- `revenue_recognition`: 2/3 (66.7%) [normal]
- `expense_recognition`: 2/3 (66.7%) [normal]

## node_only 0/3 Nodes
- `accrual_vs_cash`: 0/3, failing_personas=novice_closed_book, rote_memorizer, misconception_prone, conflict_type={'both_fail': 3}
