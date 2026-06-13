# Enhanced False Pass Review

- generated_at: 2026-06-13
- source_file: `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl`
- reviewed_cases: 8
- scope: analysis only; no scorer, course, persona, prompt, or transfer case changes made

## Summary

The after_patch run has 8 enhanced-rule false pass cases:

```text
gross_margin: 4
revenue_recognition: 2
revenue_not_cash_receipt: 1
depreciation_amortization: 1
```

These are not just random judge disagreement. Most are real scorer weaknesses:

1. Semantic matching is too broad and gives full point coverage for short partial answers.
2. Contradiction detection misses several explicit misconceptions.
3. Some answer fragments are matched without checking whether they appear in a negated or opposing sentence.
4. `gross_margin` can pass even when the answer lacks the formula and only says "毛利还不是净利润".

## Case Review

| run_id | node_id | condition | persona | judge_score | enhanced_score | review |
| --- | --- | --- | --- | --- | --- | --- |
| `c8a1cd8fb15a26c6` | `gross_margin` | node_only | novice_closed_book | 0.333 | 1.0 | Partial answer. Mentions 毛利 = 收入 - 销售成本 and 毛利不是净利润, but omits 毛利率公式 and period-expense mechanism. Enhanced scorer over-expanded "还不是净利润" into full coverage. |
| `71fa0e4523ba0495` | `revenue_recognition` | node_only | rote_memorizer | 0.33 | 1.0 | Conclusion-only answer: "收入确认不一定等于收到现金". It lacks sales/service source and completion/delivery condition. Semantic matcher treats "收入确认" as enough for multiple points. |
| `cec6e305439237b9` | `gross_margin` | node_only | rote_memorizer | 0.0 | 1.0 | Severe false pass. Answer only says "毛利还不是净利润"; no formula or explanation. Should be capped as rote/partial answer. |
| `89a5e43e27ea7c6e` | `gross_margin` | chain_so_far | rote_memorizer | 0.0 | 1.0 | Same as above, with a slightly longer sentence. Still lacks formula and period-expense reasoning. |
| `90ffab514a6ce477` | `revenue_recognition` | hidden_transfer | misconception_prone | 0.0 | 1.0 | Severe contradiction. Says no cash means no revenue. Contradiction detector did not catch this phrasing even though misconception_tags did. |
| `b7c79c56ca63ca4c` | `revenue_not_cash_receipt` | hidden_transfer | misconception_prone | 0.33 | 1.0 | Severe contradiction. Says revenue must wait for cash and revenue equals collection. Scorer matched individual keywords despite the answer denying the expected rule. |
| `83e7249776e6fea2` | `depreciation_amortization` | node_only | misconception_prone | 0.33 | 1.0 | Explicit contradiction. Says depreciation is monthly cash outflow. Contradiction detector missed "折旧实际上就是每个月为资产付出去的钱 / 它也算是现金流出". |
| `5e8f09219a82b69d` | `gross_margin` | chain_so_far | misconception_prone | 0.33 | 1.0 | Partial answer. Correctly says net profit deducts other expenses, but does not state 毛利 or 毛利率 formulas. Enhanced scorer inferred both formulas from vague language. |

## Root Cause By Scorer Area

### 1. Broad Semantic Matching

Relevant implementation:

```text
common.py enhanced_semantic_match_reasons
```

Examples:

- `gross_margin_amount` matches whenever answer contains `毛利` and broad words like `收入减销售成本`.
- `gross_margin_rate` matches whenever answer contains `毛利率`, even without a formula or percentage.
- `sales_or_service_revenue` can match `收入确认` alone because the point contains `收入`.
- `revenue_recognition_not_cash` can match cash-related text without ensuring the answer affirms revenue can be recognized before cash.

Impact:

```text
Short partial answers can be scored as full coverage.
Contradictory answers can still collect enough matched points to pass.
```

### 2. Contradiction Detection Coverage Gaps

Relevant implementation:

```text
common.py CONTRADICTION_PATTERNS
common.py detect_contradictions
```

Missed patterns observed in false pass samples:

```text
收入应该在下月收到现金时确认
完成服务不等于收到钱，没收到钱就不能算收入
收入必须是在收到现金时才能确认
收入等于收款
折旧实际上就是每个月为资产付出去的钱
折旧也算是现金流出
```

Impact:

```text
misconception_tags detect some of these issues, but enhanced_rule_scorer does not use misconception_tags.
The contradiction penalty is therefore not applied.
```

### 3. Missing Minimum Evidence Rules For `gross_margin` And `revenue_recognition`

Existing special gates:

```text
net_profit conclusion-only cap
expense_recognition evidence map
```

Missing special gates:

```text
gross_margin: require formula-level evidence for 毛利 and 毛利率 before full pass.
revenue_recognition: require positive evidence that service/goods completion can support revenue recognition before cash receipt.
revenue_not_cash_receipt: require positive evidence of receivable/timing difference, not just cash keywords.
depreciation_amortization: require no explicit cash-outflow misconception.
```

## Candidate Narrow Fixes

Do not implement all at once without approval. Recommended order:

1. Add regression tests for the 8 false pass cases, expecting `enhanced_rule_passed is False`.
2. Extend `CONTRADICTION_PATTERNS` for the exact observed revenue/cash and depreciation/cash misconceptions.
3. Add a `gross_margin` minimum-evidence gate:
   - pass requires formula evidence for either `毛利 = 收入 - 销售成本` or a concrete calculation;
   - pass requires formula evidence for `毛利率 = 毛利 / 收入` when that point is expected;
   - "毛利还不是净利润" alone cannot match formula points.
4. Tighten `revenue_recognition` matching so `收入确认不一定等于收到现金` alone does not satisfy sales/service and completion/delivery points.
5. Tighten `revenue_not_cash_receipt` matching so an answer that denies revenue recognition before cash cannot receive full credit for the same concept.

## Suggested Gate

Recommended next engineering step:

```text
scorer_v3_false_pass_patch
```

Suggested scope:

```text
Only enhanced_rule_scorer tests and scorer logic.
No course content changes.
No persona changes.
No judge prompt changes.
No transfer case changes.
No real API run until tests pass and user approves.
```

Suggested acceptance:

```text
1. Existing 5 enhanced scorer tests still pass.
2. Add 8 false-pass regression tests; all pass.
3. Rescore the valid after_patch retry_002 output.
4. enhanced false pass count should decrease materially without exploding false fail count.
5. Do not claim course patch success; this is scorer hygiene only.
```
