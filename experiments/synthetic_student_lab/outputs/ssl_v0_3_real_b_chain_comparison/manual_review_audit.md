# Manual Review Audit

- generated_at: 2026-06-13
- after_dir: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/`
- comparison_report: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/comparison_report.md`
- current_status: `FAIL`

## Executive Summary

The retry_002 after_patch run is structurally valid, but it does not validate the three-node course patch.

Key reasons:

- Overall LLM judge pass rate declined from 55/96 (57.3%) to 47/96 (49.0%).
- Hidden transfer LLM judge pass rate declined from 22/24 (91.7%) to 18/24 (75.0%).
- Enhanced-rule false pass count increased from 3 to 8.
- `accrual_vs_cash` declined sharply under LLM judge, from 5/12 to 1/12.
- `gross_margin` still has serious false pass risk under enhanced rule scoring.

This should be treated as a valid negative result, not as proof that the course patch helped.

## Main Findings

### 1. `accrual_vs_cash` Patch Did Not Transfer Reliably

Observed after_patch pattern:

- overall judge: 5/12 -> 1/12
- hidden_transfer judge: 3/3 -> 1/3
- enhanced rule: 1/12 -> 1/12

The common failure mode is not usually definition reversal anymore for all students. Instead, many answers only repeat:

```text
权责发生制关注交易归属期间，现金制关注现金实际收付时间。
```

They often omit the two concrete mechanisms required by the node:

```text
未收款也可能确认收入
未付款也可能确认费用
```

Interpretation: the patch made the definition clearer, but the learning material still does not reliably force students to apply both sides of the accrual/cash distinction in examples.

### 2. `net_profit` Is Stable But Not Clearly Improved

Observed after_patch pattern:

- overall judge: 6/12 -> 6/12
- hidden_transfer judge: 3/3 -> 3/3
- enhanced rule: 2/12 -> 3/12

This is the least worrying of the three patched nodes. It preserved hidden_transfer, and some answers now mention both accrual timing and non-cash expenses.

Remaining failure mode:

- rote answers still say only “净利润不等于现金”
- some answers mention未收现收入 but omit non-cash expenses
- some answers mention mechanisms but do not compute or anchor the example

Interpretation: the patch may have helped slightly, but the evidence is mixed and not strong enough to claim improvement.

### 3. `gross_margin` Still Has False Pass Risk

Observed after_patch pattern:

- overall judge: 7/12 -> 5/12
- hidden_transfer judge: 3/3 -> 3/3
- enhanced rule: 8/12 -> 8/12
- after false pass samples involving `gross_margin`: 4

The enhanced scorer still passes weak or contradictory answers, for example answers that only say:

```text
毛利还不是净利润。
```

or answers that mention expenses but omit formula-level reasoning.

Interpretation: the course material may be partly okay for hidden transfer, but the enhanced scorer is too permissive on `gross_margin`. This is not a good target for another course patch until the false pass behavior is understood.

### 4. Scorer/Judge Alignment Got Worse

Enhanced false pass increased:

```text
3 -> 8
```

After false pass nodes:

```text
gross_margin: 4
revenue_recognition: 2
revenue_not_cash_receipt: 1
depreciation_amortization: 1
```

Several false pass examples contain explicit misconception tags or contradictory statements. This suggests a scoring weakness, especially around partial keyword matches and contradiction handling.

### 5. The Negative Result May Reflect LLM Stochasticity, But Should Not Be Dismissed

Because the before and after runs are separate real LLM runs, some movement may come from model variance. However, the decline is too broad to ignore:

- hidden_transfer judge dropped by 16.7pp
- node_only judge dropped by 20.8pp
- `accrual_vs_cash` dropped by 33.3pp
- enhanced false pass increased materially

Interpretation: a small targeted rerun can help distinguish noise from real regression, but the current run should remain recorded as FAIL.

## Recommended Next Steps

1. Do not apply another course patch immediately.
2. Manually review the 8 enhanced false pass samples first.
3. Decide whether the enhanced scorer needs a narrow contradiction/partial-answer fix, especially for `gross_margin`, `revenue_recognition`, and `revenue_not_cash_receipt`.
4. For `accrual_vs_cash`, inspect whether the node needs an explicit two-case mini example rather than more definition text.
5. If rerunning, run a targeted confirmatory retry on the 3 patched nodes plus false-pass-heavy nodes, not the full B chain.

## Current Gate Recommendation

Recommended gate result:

```text
PARTIAL_PASS_ENGINEERING
FAIL_COURSE_VALIDATION
```

Engineering side passed after the timeout fix: the experiment now produces complete, structurally valid outputs.

Course validation failed: the after_patch comparison does not show reliable improvement and raises new scorer-alignment risks.
