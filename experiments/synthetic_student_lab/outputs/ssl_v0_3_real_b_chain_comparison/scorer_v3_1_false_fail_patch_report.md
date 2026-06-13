# Enhanced Scorer v3.1 False Fail 小修报告

日期：2026-06-13

## 本阶段目标

基于人工审核后的 18 条 false fail，只处理高置信 `scorer_too_strict` 样本，避免广泛放松 scorer。

本阶段明确不做：

```text
不修改课程内容。
不修改 persona。
不修改 judge prompt。
不修改 transfer_cases。
不运行真实 API。
不改动主产品流程。
```

## 人工审核决定

人工审核后确认：

| 处理方向 | 样本 | 决定 |
|---|---|---|
| 放行进入 v3.1 | `4e12cea729ecaa0a` | `revenue_recognition` 有完整“服务完成/未收款/可确认收入”证据。 |
| 放行进入 v3.1 | `585ba193316e1153` | `revenue_not_cash_receipt` 能说明收入与收款的时间差。 |
| 放行进入 v3.1 | `4ab92215771f559d` | 与上一条同类，表达充分且无反向误解。 |
| 保持失败 | `gross_margin` 相关样本 | 多数缺公式或含“毛利=净利”风险，不放松。 |
| 保持失败 | `net_profit` 相关样本 | 多数缺机制或带“净利润为正现金充足”风险，不放松。 |
| 保持失败 | `depreciation_amortization` 相关样本 | 含“折旧不应算费用”等反向结论，不放松。 |
| 人工保留 | `income_statement_boundary` 混合样本 | 暂不修改 scorer，等待更细 rubric。 |

## 修改内容

修改文件：

```text
experiments/synthetic_student_lab/common.py
experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py
```

scorer v3.1 改动：

```text
1. 为 revenue_recognition 增加窄范围语义匹配：
   完成服务/商品交付 + 未收款/下月收款 + 可确认收入。

2. 为 revenue_not_cash_receipt 增加窄范围语义匹配：
   收入记录赚到的经营成果 + 收款记录现金进入 + 赊销造成时间差。

3. 增加 revenue/cash 反向误解保护：
   没收钱就不应算收入、现金没增加时确认收入不合理、收入增加就应现金增加。

4. 修复 v3.1 初稿引入的 accrual_vs_cash 回归：
   只在明确“6 月服务完成/7 月收款仍确认 6 月收入”和“6 月房租/7 月付款仍确认 6 月费用”时补充匹配。
```

新增测试：

```text
test_accrual_vs_cash_completed_service_and_unpaid_expense_should_pass
test_revenue_recognition_completion_and_no_cash_paraphrase_should_pass
test_revenue_not_cash_timing_gap_paraphrase_should_pass
test_revenue_not_cash_timing_gap_with_cash_misconception_should_fail
```

## 本地验证

已运行：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
python experiments/synthetic_student_lab/rescore_with_enhanced_rules.py --input-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
```

检查结果：

```text
compileall: PASS
pytest enhanced scorer: 15 passed, 1 dependency deprecation warning
local rescore sanity_tests_passed: True
```

## v3 到 v3.1 指标变化

| 指标 | v3 | v3.1 |
|---|---:|---:|
| total rows | 96 | 96 |
| judge_passed | 47 | 47 |
| enhanced_rule_passed | 29 | 32 |
| enhanced false pass | 0 | 0 |
| enhanced false fail | 18 | 15 |
| enhanced_rule_score_avg | 0.3906 | 0.3984 |

v3.1 后 false fail 分布：

| node_id | false_fail_count |
|---|---:|
| net_profit | 4 |
| gross_margin | 3 |
| revenue_not_cash_receipt | 3 |
| income_statement_boundary | 2 |
| depreciation_amortization | 2 |
| revenue_recognition | 1 |

相对 v3 的关键变化：

| run_id | node_id | 变化 |
|---|---|---|
| `4e12cea729ecaa0a` | revenue_recognition | false fail -> both pass |
| `585ba193316e1153` | revenue_not_cash_receipt | false fail -> both pass |
| `4ab92215771f559d` | revenue_not_cash_receipt | false fail -> both pass |
| `57d885de1199748c` | revenue_not_cash_receipt | 仍失败，新增 `cash_required_for_revenue` contradiction tag |
| `1b8d3d51286c162a` | revenue_not_cash_receipt | 仍失败，新增 `revenue_implies_cash` contradiction tag |

## 风险评估

false pass 风险：

```text
低。v3.1 后 enhanced false pass 仍为 0。
```

false fail 风险：

```text
中等。false fail 从 18 降到 15，但仍保留 15 条，主要集中在 net_profit、gross_margin 和 revenue_not_cash_receipt。
```

过拟合风险：

```text
低到中等。修改只针对概念级表达，不直接匹配 run_id 或完整答案；同时补了反向误解负例。
```

课程验证风险：

```text
仍然存在。scorer hygiene 改善不等于课程 patch 有效。
当前课程验证结论仍为 FAIL。
```

## 结论

```text
scorer_v3_1_false_fail_patch: PASS
false_pass_guard: PASS
false_fail_reduction: PASS
course_validation_status: FAIL
next_gate: 人工审核 v3.1 diff，再决定是否需要新的真实实验或课程二次 patch
```
