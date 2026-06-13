# Synthetic Student Lab Before/After Comparison

- generated_at: 2026-06-13T02:36:03Z
- before_dir: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/`
- after_dir: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/`
- conclusion_status: `FAIL`

## Data Quality

- after simulation_runs rows: 96
- after judge_results rows: 96
- structural_pass: True
- after check_summary: no error_message rows, no empty student_answer rows, no severe structural problems detected.

## Overall Metrics

| metric | before | after | delta |
| --- | --- | --- | --- |
| judge_passed | 55/96 (57.3%) | 47/96 (49.0%) | -8.3pp |
| enhanced_rule_passed | 45/96 (46.9%) | 44/96 (45.8%) | -1.0pp |
| judge_score_avg | 0.5553 | 0.4811 | -0.0742 |
| enhanced_rule_score_avg | 0.5380 | 0.5269 | -0.0111 |

## Condition Metrics

| condition | judge_passed before | enhanced_rule_passed before | judge_passed after | enhanced_rule_passed after | judge_passed delta | enhanced_rule_passed delta |
| --- | --- | --- | --- | --- | --- | --- |
| chain_so_far | 17/24 (70.8%) | 15/24 (62.5%) | 18/24 (75.0%) | 15/24 (62.5%) | +4.2pp | +0.0pp |
| hidden_transfer | 22/24 (91.7%) | 16/24 (66.7%) | 18/24 (75.0%) | 18/24 (75.0%) | -16.7pp | +8.3pp |
| no_course_baseline | 0/24 (0.0%) | 0/24 (0.0%) | 0/24 (0.0%) | 0/24 (0.0%) | +0.0pp | +0.0pp |
| node_only | 16/24 (66.7%) | 14/24 (58.3%) | 11/24 (45.8%) | 11/24 (45.8%) | -20.8pp | -12.5pp |

## Patched Node Metrics

| node_id | judge before | judge after | judge delta | enhanced before | enhanced after | enhanced delta | hidden judge before | hidden judge after | hidden judge delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| accrual_vs_cash | 5/12 (41.7%) | 1/12 (8.3%) | -33.3pp | 1/12 (8.3%) | 1/12 (8.3%) | +0.0pp | 3/3 (100.0%) | 1/3 (33.3%) | -66.7pp |
| net_profit | 6/12 (50.0%) | 6/12 (50.0%) | +0.0pp | 2/12 (16.7%) | 3/12 (25.0%) | +8.3pp | 3/3 (100.0%) | 3/3 (100.0%) | +0.0pp |
| gross_margin | 7/12 (58.3%) | 5/12 (41.7%) | -16.7pp | 8/12 (66.7%) | 8/12 (66.7%) | +0.0pp | 3/3 (100.0%) | 3/3 (100.0%) | +0.0pp |

## All Node Judge Metrics

| node_id | judge_passed before | enhanced_rule_passed before | judge_passed after | enhanced_rule_passed after | judge_passed delta | enhanced_rule_passed delta |
| --- | --- | --- | --- | --- | --- | --- |
| accrual_vs_cash | 5/12 (41.7%) | 1/12 (8.3%) | 1/12 (8.3%) | 1/12 (8.3%) | -33.3pp | +0.0pp |
| depreciation_amortization | 9/12 (75.0%) | 9/12 (75.0%) | 8/12 (66.7%) | 9/12 (75.0%) | -8.3pp | +0.0pp |
| expense_recognition | 7/12 (58.3%) | 7/12 (58.3%) | 5/12 (41.7%) | 5/12 (41.7%) | -16.7pp | -16.7pp |
| gross_margin | 7/12 (58.3%) | 8/12 (66.7%) | 5/12 (41.7%) | 8/12 (66.7%) | -16.7pp | +0.0pp |
| income_statement_boundary | 7/12 (58.3%) | 7/12 (58.3%) | 9/12 (75.0%) | 7/12 (58.3%) | +16.7pp | +0.0pp |
| net_profit | 6/12 (50.0%) | 2/12 (16.7%) | 6/12 (50.0%) | 3/12 (25.0%) | +0.0pp | +8.3pp |
| revenue_not_cash_receipt | 8/12 (66.7%) | 5/12 (41.7%) | 8/12 (66.7%) | 4/12 (33.3%) | +0.0pp | -8.3pp |
| revenue_recognition | 6/12 (50.0%) | 6/12 (50.0%) | 5/12 (41.7%) | 7/12 (58.3%) | -8.3pp | +8.3pp |

## False Pass / False Fail Risk

- enhanced_rule_passed=true while judge_passed=false: 3 -> 8
- enhanced_rule_passed=false while judge_passed=true: 13 -> 11
- after false pass by node: depreciation_amortization: 1, gross_margin: 4, revenue_not_cash_receipt: 1, revenue_recognition: 2
- after false fail by node: gross_margin: 1, income_statement_boundary: 2, net_profit: 3, revenue_not_cash_receipt: 5
- before enhanced_conflict_type: both_fail: 38, both_pass: 42, rule_fail_llm_pass: 13, rule_pass_llm_fail: 3
- after enhanced_conflict_type: both_fail: 41, both_pass: 36, rule_fail_llm_pass: 11, rule_pass_llm_fail: 8

## High Risk / Regression Signals

- accrual_vs_cash: judge_passed 5/12 (41.7%) -> 1/12 (8.3%) (-33.3pp)
- expense_recognition: judge_passed 7/12 (58.3%) -> 5/12 (41.7%) (-16.7pp)
- gross_margin: judge_passed 7/12 (58.3%) -> 5/12 (41.7%) (-16.7pp)

## Overfitting Check

- hidden_transfer judge_passed changed from 22/24 (91.7%) to 18/24 (75.0%) (-16.7pp).
- hidden_transfer enhanced_rule_passed changed from 16/24 (66.7%) to 18/24 (75.0%) (+8.3pp).
- Because hidden_transfer judge performance declined while enhanced hidden_transfer improved, there is a risk that rule-score movement is not aligned with LLM judge quality. This should be reviewed manually before claiming patch effectiveness.

## Conclusion

- conclusion_status: `FAIL`
- The run is structurally valid, but the course patch is not validated by this after_patch result.
- Main reasons: overall judge_passed declined, hidden_transfer judge_passed declined, and enhanced-rule false pass risk increased.
