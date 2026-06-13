# Enhanced Scorer v3 False Fail Review

Date: 2026-06-13

Source result:

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
```

Scope:

```text
Only rows where judge_passed=true and enhanced_rule_passed=false.
No course content, scorer, persona, judge prompt, transfer_cases, or real API calls were changed in this review.
```

## Executive Summary

The v3 scorer eliminated the previously reviewed false pass risk, but became more conservative. The current after_patch retry_002 result contains 18 false fail rows.

Classification summary:

| classification | count | interpretation |
|---|---:|---|
| scorer_too_strict | 3 | The answer appears conceptually sufficient, and v3 likely missed a valid paraphrase. |
| acceptable_conservative_fail | 5 | The judge passed the answer, but v3 is reasonably conservative because required evidence is partial or underspecified. |
| judge_too_lenient | 7 | The answer contains an explicit misconception or contradiction, so enhanced failure is likely correct. |
| needs_human_review | 3 | The answer is mixed enough that a human rubric decision should precede any scorer change. |

Recommended gate:

```text
Do not broadly relax scorer v3.
Only consider v3.1 for narrow, high-confidence paraphrase coverage in revenue_recognition and revenue_not_cash_receipt.
Keep contradiction-heavy misconception answers failing.
Course validation remains FAIL.
```

## Distribution

By node:

| node_id | false_fail_count |
|---|---:|
| revenue_not_cash_receipt | 5 |
| net_profit | 4 |
| gross_margin | 3 |
| revenue_recognition | 2 |
| income_statement_boundary | 2 |
| depreciation_amortization | 2 |

By condition:

| condition | false_fail_count |
|---|---:|
| chain_so_far | 7 |
| node_only | 6 |
| hidden_transfer | 5 |

By persona:

| student_persona | false_fail_count |
|---|---:|
| misconception_prone | 10 |
| rote_memorizer | 5 |
| novice_closed_book | 3 |

## Per-Case Review

| # | run_id | node_id | condition | persona | judge/enhanced | classification | v3.1 suggestion |
|---:|---|---|---|---|---|---|---|
| 1 | 4e12cea729ecaa0a | revenue_recognition | node_only | novice_closed_book | 1.0 / 0.0 | scorer_too_strict | Add positive paraphrase test: service completed or goods delivered, not cash receipt, may recognize revenue. |
| 2 | 585ba193316e1153 | revenue_not_cash_receipt | node_only | novice_closed_book | 0.6667 / 0.3333 | scorer_too_strict | Add positive paraphrase test for "income records earned result; collection records cash; credit sale creates timing gap." |
| 3 | 49702d7924a64a2f | gross_margin | chain_so_far | novice_closed_book | 0.8 / 0.5 | acceptable_conservative_fail | No immediate relaxation; answer explains gross margin rate and period expenses but omits gross profit formula. |
| 4 | bcb84f9ceba8fce9 | revenue_recognition | hidden_transfer | rote_memorizer | 0.6667 / 0.0 | acceptable_conservative_fail | Keep failing unless completion/delivery evidence is present; answer only says revenue is not cash. |
| 5 | 4ab92215771f559d | revenue_not_cash_receipt | node_only | rote_memorizer | 1.0 / 0.3333 | scorer_too_strict | Same candidate as case 2, if no contradictory cash misconception appears. |
| 6 | e4e4b528edb49ba4 | revenue_not_cash_receipt | chain_so_far | rote_memorizer | 0.7 / 0.3333 | acceptable_conservative_fail | Keep conservative; answer is directionally right but lacks explicit cash-not-increased or receivable evidence. |
| 7 | 1101b9b1a3e1bef6 | net_profit | chain_so_far | rote_memorizer | 0.67 / 0.3333 | acceptable_conservative_fail | No v3.1 change; answer states net profit is not cash but gives no mechanism such as uncollected revenue or non-cash expense. |
| 8 | 4e0aad17637d82ae | net_profit | hidden_transfer | rote_memorizer | 0.6667 / 0.3333 | acceptable_conservative_fail | No v3.1 change; answer misses the case calculation and concrete cash/profit mechanisms. |
| 9 | 8bff312837528c9a | income_statement_boundary | node_only | misconception_prone | 0.6 / 0.3333 | judge_too_lenient | Keep failing; answer ends by treating a loan as a kind of revenue. |
| 10 | 16d7b0406bfc8948 | income_statement_boundary | chain_so_far | misconception_prone | 0.67 / 0.3333 | needs_human_review | Mixed answer: starts with cash-as-income intuition but corrects toward financing source. Human rubric should decide tolerance. |
| 11 | 57d885de1199748c | revenue_not_cash_receipt | node_only | misconception_prone | 0.6667 / 0.3333 | judge_too_lenient | Keep failing; answer explicitly says no cash means revenue should not be recognized. |
| 12 | 1b8d3d51286c162a | revenue_not_cash_receipt | chain_so_far | misconception_prone | 0.6 / 0.3333 | judge_too_lenient | Keep failing; answer explicitly claims revenue increase should mean cash increase. |
| 13 | 801b3238e4c0630e | depreciation_amortization | chain_so_far | misconception_prone | 0.6667 / 0.0 | needs_human_review | Mixed answer recognizes no cash outflow but remains confused about expense mechanics; review before scorer change. |
| 14 | 99080fad5a427dab | depreciation_amortization | hidden_transfer | misconception_prone | 1.0 / 0.0 | judge_too_lenient | Keep failing; answer contains correct setup but ends with "depreciation should not be an expense." |
| 15 | 84591106c3523017 | gross_margin | node_only | misconception_prone | 0.6667 / 0.3333 | judge_too_lenient | Keep failing; answer says high gross profit ultimately means profit, contradicting target concept. |
| 16 | a40ddd549a31f9ec | gross_margin | hidden_transfer | misconception_prone | 0.6667 / 0.5 | judge_too_lenient | Keep failing; answer equates gross margin rate with net margin and net profit. |
| 17 | a3c7062b5c479e04 | net_profit | chain_so_far | misconception_prone | 0.6667 / 0.3333 | needs_human_review | Mostly correct mechanism, but overgeneralizes that cash shortage is only temporary; human rubric should decide. |
| 18 | f6001906a04e3a51 | net_profit | hidden_transfer | misconception_prone | 1.0 / 0.3333 | judge_too_lenient | Keep failing; answer calculates and explains correctly, then contradicts the target by saying positive profit should mean enough cash. |

## Node-Level Findings

### revenue_recognition

False fail count: 2.

One high-confidence scorer strictness case exists. Case 1 is a strong answer: it mentions service completion, distinguishes cash receipt, and concludes revenue may be recognized. v3 missed this because the semantic evidence is phrased as a sentence-level explanation rather than matching its expected point patterns.

Case 4 is weaker. It says revenue recognition is not equal to receiving cash, but does not explicitly anchor recognition to completed service or delivery. Keep it as an acceptable conservative failure.

v3.1 candidate:

```text
PASS when an answer clearly says completed service/goods delivery can satisfy revenue recognition and cash receipt is not required.
Do not PASS when the answer only says "revenue is not cash" without completion/delivery evidence.
```

### revenue_not_cash_receipt

False fail count: 5.

Cases 2 and 5 are the strongest scorer strictness evidence. They distinguish revenue as earned operating result from cash collection, and explain that credit sales create a timing gap. The answer does not use "accounts receivable", but conceptually explains why cash may not increase.

Case 6 is directionally correct but thinner, so the v3 fail is acceptable. Cases 11 and 12 contain explicit cash-revenue misconceptions, so they should remain failing.

v3.1 candidate:

```text
PASS if the answer explains both sides of the distinction:
1. revenue is recognized as earned/operating result, and
2. collection/cash inflow can occur later because a credit sale creates a timing gap.

Still FAIL if the answer says no cash means no revenue, or revenue increase must mean cash increase.
```

### gross_margin

False fail count: 3.

No broad scorer relaxation is recommended. Case 3 is a reasonable conceptual answer, but it omits the gross profit formula. Because v3 was intentionally patched to prevent formula-light gross_margin false passes, this is best treated as an acceptable conservative failure unless a human approves question-aware relaxation.

Cases 15 and 16 should fail. Both include target-conflicting claims: high gross profit ultimately means profit, or gross margin rate equals net margin.

v3.1 candidate:

```text
Only consider question-aware relaxation if human reviewers decide that a "why gross margin is not net profit" question can pass without restating gross profit = revenue - COGS.
Keep formula and contradiction regression tests intact.
```

### net_profit

False fail count: 4.

Cases 7 and 8 are acceptable conservative failures: they state net profit is not cash but omit concrete mechanisms, and case 8 also omits the required 8000 calculation.

Case 17 is mixed. It correctly names uncollected revenue and non-cash expenses, but then overgeneralizes cash shortage as temporary. Case 18 is stronger on calculation and mechanism, but ends with a misconception that positive net profit means the company should not lack money. This looks more like judge leniency than scorer strictness.

v3.1 candidate:

```text
No scorer relaxation until human review decides how to handle answers with a correct explanation followed by a contradictory final sentence.
```

### depreciation_amortization

False fail count: 2.

No scorer relaxation is recommended. Both cases contain mixed or contradictory reasoning about whether depreciation can be an expense without current cash payment. Case 14 in particular should not receive a full pass because it ends by saying depreciation should not count as an expense.

v3.1 candidate:

```text
Keep current conservative handling.
If changed later, add explicit tests that final contradictory statements override earlier correct statements.
```

### income_statement_boundary

False fail count: 2.

Case 9 should fail because it treats a loan as revenue after briefly explaining the correct distinction. Case 10 is mixed: it begins with the same cash-as-income intuition, then corrects itself and states the loan is only a funding source, not operating revenue.

v3.1 candidate:

```text
No immediate scorer change. Human review should decide whether self-correction should pass when the final answer is correct.
```

## Suggested v3.1 Test Cases

High-confidence positive tests:

| target | source case | expected |
|---|---|---|
| revenue_recognition paraphrase with completion and no cash receipt | 4e12cea729ecaa0a | enhanced_rule_passed=true |
| revenue_not_cash_receipt timing-gap explanation without "accounts receivable" wording | 585ba193316e1153 | enhanced_rule_passed=true |
| revenue_not_cash_receipt same timing-gap explanation by rote persona | 4ab92215771f559d | enhanced_rule_passed=true |

High-confidence negative tests:

| target | source case | expected |
|---|---|---|
| no-cash-means-no-revenue misconception | 57d885de1199748c | enhanced_rule_passed=false |
| revenue-increase-means-cash-increase misconception | 1b8d3d51286c162a | enhanced_rule_passed=false |
| loan treated as revenue | 8bff312837528c9a | enhanced_rule_passed=false |
| depreciation should not be an expense without cash payment | 99080fad5a427dab | enhanced_rule_passed=false |
| gross margin equals net margin or net profit | a40ddd549a31f9ec | enhanced_rule_passed=false |
| positive net profit means enough cash | f6001906a04e3a51 | enhanced_rule_passed=false |

Human-review candidate tests:

| target | source case | reason |
|---|---|---|
| income_statement_boundary self-correction | 16d7b0406bfc8948 | Final answer is mostly correct, but starts from a misconception. |
| depreciation no-cash confusion | 801b3238e4c0630e | Recognizes no cash outflow, but does not explain cost allocation cleanly. |
| net_profit correct mechanism plus overgeneralized cash statement | a3c7062b5c479e04 | Core concept is present, final implication is risky. |

## Risk Assessment

False fail risk:

```text
Moderate. v3 is stricter than v2 and misses a few valid paraphrases, especially around revenue/cash timing.
```

False pass risk if v3 is relaxed:

```text
High unless changes are narrow. Many false fail rows contain explicit misconceptions that the judge passed, especially for misconception_prone samples.
```

Overfitting risk:

```text
Low to moderate. The current issue is more exact-evidence matching than mastery-question memorization. Any v3.1 fix should be pattern-light and concept-based, with paired negative tests for contradictions.
```

## Conclusion

```text
false_fail_review: COMPLETE
recommended_status: PARTIAL_PASS
course_validation_status: FAIL
next_gate: human review before any scorer v3.1 implementation
```

This review supports a small v3.1 plan only for high-confidence paraphrase coverage in `revenue_recognition` and `revenue_not_cash_receipt`. It does not support broad scorer relaxation, course edits, or a new real API run at this stage.
