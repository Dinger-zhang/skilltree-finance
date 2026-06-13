# Scorer v3 False Pass Patch Report

- generated_at: 2026-06-13
- scope: enhanced rule scorer only
- source_after_dir: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/`
- status: `PASS_SCORER_HYGIENE`

## Summary

This patch addresses the 8 enhanced-rule false pass cases found in the valid after_patch retry_002 run.

Changes made:

- Added false-pass regression tests for `gross_margin`, `revenue_recognition`, `revenue_not_cash_receipt`, and `depreciation_amortization`.
- Extended contradiction patterns for observed revenue/cash and depreciation/cash misconceptions.
- Tightened broad semantic matching that allowed conclusion-only or contradictory answers to receive full credit.
- Added a `gross_margin` formula-evidence cap so answers without both 毛利 and 毛利率 formula evidence cannot pass.

No course content, persona, judge prompt, transfer cases, or real API outputs were changed.

## Verification

```text
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
11 passed, 1 warning

python -m compileall -q app.py pages src tests experiments
PASS
```

The valid after_patch retry_002 output was rescored locally with the patched enhanced scorer:

```text
rows: 96
enhanced_rule_passed: 29/96 (30.2%)
enhanced false pass: 8 -> 0
enhanced false fail: 11 -> 18
old_rule_fail_llm_pass: 42
enhanced_rule_fail_llm_pass: 18
sanity_tests_passed: True
```

## Known Tradeoff

The scorer is now more conservative. It eliminated known false passes, but false fails increased. This is acceptable for scorer hygiene because the original failure mode was risky false acceptance of wrong answers.

This patch does not change the course-validation conclusion:

```text
after_patch course validation remains FAIL
```

The after_patch run still does not prove that the three course patches improved learning quality.

## Files Changed

```text
experiments/synthetic_student_lab/common.py
experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/enhanced_rule_score_report.md
```

## Next Gate

Recommended next step:

```text
manual review of new false fail cases before any additional scorer tightening
```

Do not run another real API experiment until the user explicitly approves it.
