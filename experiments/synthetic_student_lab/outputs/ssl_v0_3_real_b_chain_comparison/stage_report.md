# After Patch Stage Report

- generated_at: 2026-06-13T02:36:03Z
- conclusion_status: `FAIL`

## Goal

Run a structurally valid after_patch comparison for the three reviewed course patches: `accrual_vs_cash`, `net_profit`, and `gross_margin`.

## Commands

- `python -m compileall -q app.py pages src tests experiments`
- `python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q`
- `python experiments/synthetic_student_lab/run_simulation.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`
- `python experiments/synthetic_student_lab/judge.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`
- `python experiments/synthetic_student_lab/failure_analyzer.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`
- `python check_ssl_outputs.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`
- `python experiments/synthetic_student_lab/inspect_ssl_issues.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`
- `python experiments/synthetic_student_lab/rescore_with_enhanced_rules.py --input-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180`

## Modified Files

- `experiments/synthetic_student_lab/config.yaml`: increased student and judge API request timeout from 60 seconds to 180 seconds.
- `docs/11_CURRENT_STAGE.md`: updated after this report generation to record the retry_002 result.

## New Outputs

- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/simulation_runs.jsonl`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.jsonl`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/node_failure_report.md`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/check_summary.txt`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/human_review_samples.jsonl`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/human_review.md`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/enhanced_rule_score_report.md`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/comparison_report.md`
- `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/stage_report.md`

## Check Summary

- simulation_runs.jsonl rows: 96
- judge_results.jsonl rows: 96
- run_id one_to_one: True
- error_message non-empty count: 0
- student_answer empty count: 0
- severe structural problems: none

## Comparison Summary

- overall judge_passed: 55/96 (57.3%) -> 47/96 (49.0%) (-8.3pp)
- overall enhanced_rule_passed: 45/96 (46.9%) -> 44/96 (45.8%) (-1.0pp)
- hidden_transfer judge_passed: 22/24 (91.7%) -> 18/24 (75.0%) (-16.7pp)
- hidden_transfer enhanced_rule_passed: 16/24 (66.7%) -> 18/24 (75.0%) (+8.3pp)
- enhanced false pass count: 3 -> 8
- enhanced false fail count: 13 -> 11

## Patched Nodes

- `accrual_vs_cash`: judge 5/12 (41.7%) -> 1/12 (8.3%) (-33.3pp); enhanced 1/12 (8.3%) -> 1/12 (8.3%) (+0.0pp)
- `net_profit`: judge 6/12 (50.0%) -> 6/12 (50.0%) (+0.0pp); enhanced 2/12 (16.7%) -> 3/12 (25.0%) (+8.3pp)
- `gross_margin`: judge 7/12 (58.3%) -> 5/12 (41.7%) (-16.7pp); enhanced 8/12 (66.7%) -> 8/12 (66.7%) (+0.0pp)

## Risks

- hidden_transfer judge performance declined, so transfer did not hold.
- enhanced-rule false pass count increased, so scorer/judge alignment risk increased.
- `accrual_vs_cash` declined sharply under LLM judge despite being a patched target node.
- This result should not be used to claim course patch effectiveness without manual review.

## Conclusion

- current conclusion: `FAIL`
- The after_patch run is technically valid, but the educational improvement hypothesis is not validated.
- Pause for human review before any targeted retry, course changes, scorer changes, or broader experiment.
