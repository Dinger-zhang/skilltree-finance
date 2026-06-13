# Enhanced Scorer v3 False Fail 审核报告

日期：2026-06-13

数据来源：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
```

审核范围：

```text
仅审核 judge_passed=true 且 enhanced_rule_passed=false 的样本。
本次审核未修改课程内容、scorer、persona、judge prompt、transfer_cases，也未调用真实 API。
```

## 总览结论

scorer v3 已消除上一轮重点关注的 false pass 风险，但评分变得更保守。当前有效 after_patch retry_002 结果中共有 18 条 false fail。

分类汇总：

| 分类 | 数量 | 含义 |
|---|---:|---|
| scorer_too_strict | 3 | 学生答案在概念上基本充分，v3 可能漏掉了有效改写。 |
| acceptable_conservative_fail | 5 | judge 判为通过，但答案证据不完整或表达偏薄，v3 保守失败可以接受。 |
| judge_too_lenient | 7 | 答案包含明确误解或自相矛盾，enhanced fail 更可能是正确结果。 |
| needs_human_review | 3 | 答案混合了正确理解和风险表述，需要人工 rubric 决定。 |

建议闸门：

```text
不要广泛放松 scorer v3。
仅考虑在 v3.1 中对 revenue_recognition 与 revenue_not_cash_receipt 做小范围、高置信 paraphrase 补强。
保留对明确反向误解答案的失败判定。
课程验证结论仍保持 FAIL。
```

## 分布统计

按节点：

| node_id | false_fail_count |
|---|---:|
| revenue_not_cash_receipt | 5 |
| net_profit | 4 |
| gross_margin | 3 |
| revenue_recognition | 2 |
| income_statement_boundary | 2 |
| depreciation_amortization | 2 |

按 condition：

| condition | false_fail_count |
|---|---:|
| chain_so_far | 7 |
| node_only | 6 |
| hidden_transfer | 5 |

按 persona：

| student_persona | false_fail_count |
|---|---:|
| misconception_prone | 10 |
| rote_memorizer | 5 |
| novice_closed_book | 3 |

## 逐条审核

| # | run_id | node_id | condition | persona | judge/enhanced | 分类 | v3.1 建议 |
|---:|---|---|---|---|---|---|---|
| 1 | 4e12cea729ecaa0a | revenue_recognition | node_only | novice_closed_book | 1.0 / 0.0 | scorer_too_strict | 增加正例 paraphrase 测试：已完成服务或交付商品，未收款也可能确认收入。 |
| 2 | 585ba193316e1153 | revenue_not_cash_receipt | node_only | novice_closed_book | 0.6667 / 0.3333 | scorer_too_strict | 增加正例测试：收入记录赚到的经营成果，收款记录现金进入，赊销造成时间差。 |
| 3 | 49702d7924a64a2f | gross_margin | chain_so_far | novice_closed_book | 0.8 / 0.5 | acceptable_conservative_fail | 暂不放松。答案解释了毛利率和期间费用，但缺少“毛利=收入-销售成本”。 |
| 4 | bcb84f9ceba8fce9 | revenue_recognition | hidden_transfer | rote_memorizer | 0.6667 / 0.0 | acceptable_conservative_fail | 除非答案出现完成服务或交付证据，否则保持失败。该答案只说收入不等于现金。 |
| 5 | 4ab92215771f559d | revenue_not_cash_receipt | node_only | rote_memorizer | 1.0 / 0.3333 | scorer_too_strict | 可与样本 2 一起作为候选正例，前提是没有现金认知反向误解。 |
| 6 | e4e4b528edb49ba4 | revenue_not_cash_receipt | chain_so_far | rote_memorizer | 0.7 / 0.3333 | acceptable_conservative_fail | 保持保守。答案方向正确，但缺少“现金未增加”或“应收账款”等明确证据。 |
| 7 | 1101b9b1a3e1bef6 | net_profit | chain_so_far | rote_memorizer | 0.67 / 0.3333 | acceptable_conservative_fail | 不建议 v3.1 修改。答案只说净利润不等于现金，缺少未收现收入或非现金费用机制。 |
| 8 | 4e0aad17637d82ae | net_profit | hidden_transfer | rote_memorizer | 0.6667 / 0.3333 | acceptable_conservative_fail | 不建议 v3.1 修改。答案缺少本题 8000 元计算，也缺少具体利润和现金差异机制。 |
| 9 | 8bff312837528c9a | income_statement_boundary | node_only | misconception_prone | 0.6 / 0.3333 | judge_too_lenient | 保持失败。答案最后仍把借款视为收入的一种。 |
| 10 | 16d7b0406bfc8948 | income_statement_boundary | chain_so_far | misconception_prone | 0.67 / 0.3333 | needs_human_review | 混合答案。开头有“收到现金应算收入”的直觉，后文又修正为资金来源，需人工决定容忍度。 |
| 11 | 57d885de1199748c | revenue_not_cash_receipt | node_only | misconception_prone | 0.6667 / 0.3333 | judge_too_lenient | 保持失败。答案明确说没收到钱就不应确认收入。 |
| 12 | 1b8d3d51286c162a | revenue_not_cash_receipt | chain_so_far | misconception_prone | 0.6 / 0.3333 | judge_too_lenient | 保持失败。答案明确认为收入增加就应意味着现金增加。 |
| 13 | 801b3238e4c0630e | depreciation_amortization | chain_so_far | misconception_prone | 0.6667 / 0.0 | needs_human_review | 混合答案。意识到没有现金流出，但对费用机制仍明显困惑，修改 scorer 前需人工判断。 |
| 14 | 99080fad5a427dab | depreciation_amortization | hidden_transfer | misconception_prone | 1.0 / 0.0 | judge_too_lenient | 保持失败。答案前半正确，但最后说折旧不应算费用。 |
| 15 | 84591106c3523017 | gross_margin | node_only | misconception_prone | 0.6667 / 0.3333 | judge_too_lenient | 保持失败。答案声称毛利高最终肯定赚钱，与目标概念冲突。 |
| 16 | a40ddd549a31f9ec | gross_margin | hidden_transfer | misconception_prone | 0.6667 / 0.5 | judge_too_lenient | 保持失败。答案把毛利率等同于净利率，并把毛利等同于净利润。 |
| 17 | a3c7062b5c479e04 | net_profit | chain_so_far | misconception_prone | 0.6667 / 0.3333 | needs_human_review | 基本机制较正确，但又泛化为现金短缺只是暂时的，需人工判断。 |
| 18 | f6001906a04e3a51 | net_profit | hidden_transfer | misconception_prone | 1.0 / 0.3333 | judge_too_lenient | 保持失败。答案完成计算和部分解释，但最后说净利润为正公司应不缺钱。 |

## 节点级发现

### revenue_recognition

false fail 数量：2。

样本 1 是高置信 scorer 过严案例。答案明确提到服务完成、区分收款，并得出本月可确认收入的结论。v3 没命中，主要是因为学生用完整句子表达了语义证据，而没有命中当前 expected point 的具体模式。

样本 4 较弱。它只说收入确认不等于收到现金，没有明确把确认收入锚定到服务完成或商品交付。因此更适合作为 acceptable_conservative_fail。

v3.1 候选规则：

```text
当答案明确说明“服务完成/商品交付可满足收入确认条件，且不依赖现金到账”时，应允许通过。
仅说“收入不是现金”但没有完成服务或交付证据时，不应通过。
```

### revenue_not_cash_receipt

false fail 数量：5。

样本 2 和样本 5 是最强的 scorer 过严证据。它们区分了“收入记录赚到的经营成果”和“收款记录现金进入”，并说明赊销会造成收入与现金流入的时间差。虽然没有使用“应收账款”字样，但已经能解释为什么确认收入时现金可能没有增加。

样本 6 方向正确但证据较薄，所以 v3 fail 可以接受。样本 11 和样本 12 含有明确现金收入误解，应继续失败。

v3.1 候选规则：

```text
如果答案同时说明：
1. 收入是已赚取或经营成果的确认；
2. 收款或现金流入可能发生在以后，赊销会造成时间差；
则可以考虑通过。

如果答案声称没收现金就不能确认收入，或收入增加必须意味着现金增加，则仍应失败。
```

### gross_margin

false fail 数量：3。

不建议广泛放松 scorer。样本 3 是合理的概念性答案，但缺少“毛利=收入-销售成本”。由于 v3 正是为了避免 gross_margin 中公式证据不足的 false pass，除非人工明确认可按题目类型放宽，否则该样本更适合保留为 acceptable_conservative_fail。

样本 15 和样本 16 应保持失败。两者都包含与目标概念冲突的结论：毛利高最终肯定赚钱，或毛利率等于净利率。

v3.1 候选规则：

```text
只有在人工确认“为什么毛利率高不等于净利润高”类问题可以不重复毛利公式时，才考虑题目感知型放宽。
保留公式证据和反向误解回归测试。
```

### net_profit

false fail 数量：4。

样本 7 和样本 8 是合理保守失败。它们说明净利润不等于现金，但没有给出未收现收入、非现金费用等具体机制；样本 8 还缺少本题要求的 8000 元计算。

样本 17 是混合答案。它正确提到未收现收入和非现金费用，但又把现金短缺泛化为暂时问题。样本 18 在计算和机制上较充分，但最后明确说净利润为正公司应该不缺钱。这更像 judge_too_lenient，而不是 scorer_too_strict。

v3.1 候选规则：

```text
在人工决定如何处理“先正确解释，最后又给出矛盾结论”的答案之前，不建议放松 net_profit。
```

### depreciation_amortization

false fail 数量：2。

不建议放松 scorer。两个样本都在“折旧是否可以不伴随当期现金流出而影响利润”上有混合或矛盾表述。样本 14 尤其不应通过，因为它最后说今年没付现金所以折旧不应算费用。

v3.1 候选规则：

```text
保持当前保守策略。
如果未来调整，应增加明确测试：答案末尾的反向结论应覆盖前面的正确片段。
```

### income_statement_boundary

false fail 数量：2。

样本 9 应失败，因为它在简短解释正确区别之后，仍把借款视为收入。样本 10 较混合：开头有“收到现金应算收入”的直觉，但后文修正为借款只是资金来源，不是经营收入。

v3.1 候选规则：

```text
暂不修改 scorer。是否允许“先误解、后自我修正且最终结论正确”的答案通过，需要人工 rubric 决定。
```

## 建议的 v3.1 测试清单

高置信正例：

| 目标 | 来源样本 | 期望 |
|---|---|---|
| revenue_recognition 中“完成服务且未收款也可确认收入”的改写 | 4e12cea729ecaa0a | enhanced_rule_passed=true |
| revenue_not_cash_receipt 中没有“应收账款”字样但能说明时间差 | 585ba193316e1153 | enhanced_rule_passed=true |
| rote persona 下相同时间差解释 | 4ab92215771f559d | enhanced_rule_passed=true |

高置信负例：

| 目标 | 来源样本 | 期望 |
|---|---|---|
| 没收现金就不能确认收入 | 57d885de1199748c | enhanced_rule_passed=false |
| 收入增加必须意味着现金增加 | 1b8d3d51286c162a | enhanced_rule_passed=false |
| 将借款视为收入 | 8bff312837528c9a | enhanced_rule_passed=false |
| 认为没有当期现金支付所以折旧不应算费用 | 99080fad5a427dab | enhanced_rule_passed=false |
| 将毛利率等同于净利率或净利润 | a40ddd549a31f9ec | enhanced_rule_passed=false |
| 认为净利润为正就说明现金充足 | f6001906a04e3a51 | enhanced_rule_passed=false |

人工复核候选：

| 目标 | 来源样本 | 原因 |
|---|---|---|
| income_statement_boundary 中的自我修正答案 | 16d7b0406bfc8948 | 最终结论基本正确，但开头带有误解。 |
| depreciation_amortization 中的无现金困惑 | 801b3238e4c0630e | 认识到没有现金流出，但没有清楚解释成本分摊。 |
| net_profit 中正确机制加风险泛化 | a3c7062b5c479e04 | 核心概念存在，但最后关于现金短缺的判断偏危险。 |

## 风险评估

false fail 风险：

```text
中等。v3 比 v2 更严格，尤其在收入与现金时间差相关节点上漏掉了少数有效改写。
```

如果放松 v3 的 false pass 风险：

```text
高。许多 false fail 样本包含明确误解，尤其集中在 misconception_prone persona。
如果不做窄范围规则和负例测试，容易重新引入 false pass。
```

过拟合风险：

```text
低到中等。当前问题更像证据匹配过窄，而不是 mastery question 记忆化。
若进入 v3.1，应采用概念级、窄范围补强，并配套反向误解负例测试。
```

## 人工审核后的执行结果

人工审核结论：

```text
批准进入窄范围 scorer v3.1。
仅处理 3 条高置信 scorer_too_strict 样本。
不放松 gross_margin、net_profit、depreciation_amortization、income_statement_boundary 的保守边界。
不修改课程，不运行真实 API。
```

v3.1 已完成的修正：

```text
1. revenue_recognition:
   覆盖“服务完成/商品交付 + 未收款/下月收款 + 可确认收入”的有效改写。

2. revenue_not_cash_receipt:
   覆盖“收入记录赚到的经营成果 + 收款记录现金进入 + 赊销造成时间差”的有效改写。

3. contradiction guard:
   补充“没收钱就不应算收入”“收入增加就应现金增加”等反向误解识别。

4. accrual_vs_cash:
   修复 v3.1 初稿造成的一条回归，确保明确的权责发生制收入/费用归属答案仍可通过。
```

v3.1 本地 rescore 结果：

```text
enhanced_rule_passed: 29/96 -> 32/96
enhanced false pass: 0 -> 0
enhanced false fail: 18 -> 15
enhanced_rule_score_avg: 0.3906 -> 0.3984
sanity_tests_passed: True
```

对应报告：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/scorer_v3_1_false_fail_patch_report.md
```

## 结论

```text
false_fail_review: COMPLETE
human_review_gate: APPROVED_NARROW_V3_1
scorer_v3_1_false_fail_patch: COMPLETE
recommended_status: PARTIAL_PASS
course_validation_status: FAIL
next_gate: human review of v3.1 diff before any new real API experiment
```

本审核已支持并完成一个小范围 v3.1 计划：针对 `revenue_recognition` 和 `revenue_not_cash_receipt` 的高置信有效改写补充覆盖，同时保留反向误解失败保护。当前仍不支持广泛放松 scorer，不支持课程修改，也不支持立刻重新运行真实 API。
