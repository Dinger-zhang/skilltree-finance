# Synthetic Student Lab Before/After 对比报告

生成日期：2026-06-13

before 目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

after 目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/
```

当前结论：

```text
conclusion_status: FAIL
```

## 重要说明

本报告中的 `judge_*` 指标来自真实 after_patch 实验结果，可用于观察课程 patch 的真实 before/after 变化。

`enhanced_rule_*` 指标当前需要谨慎解释：

```text
before enhanced: repaired baseline 验收时的 enhanced scorer 结果
after enhanced: 已经过本地 enhanced scorer v3.1 重新评分
```

因此 enhanced delta 不是严格同版本 scorer 对比，只能作为 scorer hygiene 与风险信号。课程效果判断仍以 `judge_passed`、hidden_transfer、节点表现和人工审核为主。

## 数据质量

after retry_002 是结构有效输出：

```text
simulation_runs.jsonl rows: 96
judge_results.jsonl rows: 96
run_id one_to_one: True
error_message non-empty count: 0
student_answer empty count: 0
severe structural problems: none
```

本次报告刷新未运行真实 API，只使用本地 `judge_results.enhanced.jsonl` 与 v3.1 rescore 结果。

## 总体指标

| metric | before | after 当前值 | delta |
|---|---:|---:|---:|
| judge_passed | 55/96 (57.3%) | 47/96 (49.0%) | -8.3pp |
| enhanced_rule_passed | 45/96 (46.9%) | 32/96 (33.3%) | -13.5pp |
| judge_score_avg | 0.5553 | 0.4811 | -0.0742 |
| enhanced_rule_score_avg | 0.5380 | 0.3984 | -0.1396 |

解释：

```text
judge_passed 下降，说明课程 patch 尚未被真实实验验证。
enhanced_rule_passed 下降主要受 scorer v3/v3.1 更保守影响，不能直接解释为课程变差。
```

## condition 维度

| condition | judge before | judge after | judge delta | enhanced before | enhanced after | enhanced delta |
|---|---:|---:|---:|---:|---:|---:|
| chain_so_far | 17/24 (70.8%) | 18/24 (75.0%) | +4.2pp | 15/24 (62.5%) | 11/24 (45.8%) | -16.7pp |
| hidden_transfer | 22/24 (91.7%) | 18/24 (75.0%) | -16.7pp | 16/24 (66.7%) | 13/24 (54.2%) | -12.5pp |
| no_course_baseline | 0/24 (0.0%) | 0/24 (0.0%) | +0.0pp | 0/24 (0.0%) | 0/24 (0.0%) | +0.0pp |
| node_only | 16/24 (66.7%) | 11/24 (45.8%) | -20.8pp | 14/24 (58.3%) | 8/24 (33.3%) | -25.0pp |

hidden_transfer 结论：

```text
hidden_transfer judge_passed 从 91.7% 降到 75.0%，这是课程验证的主要风险信号。
v3.1 后 hidden_transfer enhanced_rule_passed 为 54.2%，更保守，不改变课程 FAIL 结论。
```

## 三个课程 patch 节点

| node_id | judge before | judge after | judge delta | enhanced before | enhanced after | enhanced delta |
|---|---:|---:|---:|---:|---:|---:|
| accrual_vs_cash | 5/12 (41.7%) | 1/12 (8.3%) | -33.3pp | 1/12 (8.3%) | 1/12 (8.3%) | +0.0pp |
| net_profit | 6/12 (50.0%) | 6/12 (50.0%) | +0.0pp | 2/12 (16.7%) | 2/12 (16.7%) | +0.0pp |
| gross_margin | 7/12 (58.3%) | 5/12 (41.7%) | -16.7pp | 8/12 (66.7%) | 2/12 (16.7%) | -50.0pp |

节点结论：

```text
accrual_vs_cash: judge 明显下降，是最高风险 patch 节点。
net_profit: judge 持平，但没有证明改善。
gross_margin: judge 下降；enhanced v3.1 更严格后通过数明显下降，说明原先可能存在公式/边界 false pass 风险。
```

## 全部节点概览

| node_id | judge before | judge after | enhanced before | enhanced after | after false fail |
|---|---:|---:|---:|---:|---:|
| accrual_vs_cash | 5/12 | 1/12 | 1/12 | 1/12 | 0 |
| depreciation_amortization | 9/12 | 8/12 | 9/12 | 6/12 | 2 |
| expense_recognition | 7/12 | 5/12 | 7/12 | 5/12 | 0 |
| gross_margin | 7/12 | 5/12 | 8/12 | 2/12 | 3 |
| income_statement_boundary | 7/12 | 9/12 | 7/12 | 7/12 | 2 |
| net_profit | 6/12 | 6/12 | 2/12 | 2/12 | 4 |
| revenue_not_cash_receipt | 8/12 | 8/12 | 5/12 | 5/12 | 3 |
| revenue_recognition | 6/12 | 5/12 | 6/12 | 4/12 | 1 |

## False Pass / False Fail 风险

| risk | before | after v3.1 |
|---|---:|---:|
| enhanced_rule_passed=true 且 judge_passed=false | 3 | 0 |
| enhanced_rule_passed=false 且 judge_passed=true | 13 | 15 |

after v3.1 false pass：

```text
none
```

after v3.1 false fail by node：

```text
gross_margin: 3
net_profit: 4
revenue_not_cash_receipt: 3
income_statement_boundary: 2
depreciation_amortization: 2
revenue_recognition: 1
```

解释：

```text
v3.1 scorer hygiene 明显改善 false pass 风险。
代价是 scorer 更保守，false fail 保持在 15 条，需要人工理解，不应继续盲目放松。
```

## 过拟合检查

hidden_transfer 是最关键的迁移信号：

```text
judge_passed: 22/24 (91.7%) -> 18/24 (75.0%)
enhanced_rule_passed: 16/24 (66.7%) -> 13/24 (54.2%)
```

当前没有证据表明三点课程 patch 带来了更好的 hidden_transfer 表现。相反，judge 迁移表现下降，需要避免把 scorer hygiene 的改善误读为课程质量改善。

## 风险

```text
1. 课程 patch 仍未通过真实 before/after 验证。
2. accrual_vs_cash judge 表现下降明显，需要优先人工复核样本和课程表述。
3. gross_margin 在 v3.1 下 enhanced 通过数下降，说明公式与净利边界仍是高风险点。
4. scorer v3.1 已降低 false pass，但 false fail 仍偏多，后续若继续调 scorer 必须保持窄范围。
```

## 结论

```text
structural_validity: PASS
scorer_v3_1_hygiene: PASS
course_patch_validation: FAIL
recommended_next_step: 人工审核课程失败样本，决定是否做第二轮课程 patch；不要直接运行新的真实 API。
```
