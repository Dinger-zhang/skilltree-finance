# After Patch + Scorer v3.1 阶段报告

生成日期：2026-06-13

当前结论：

```text
conclusion_status: FAIL
```

## 本阶段目标

在已经完成 after_patch retry_002 和 enhanced scorer v3/v3.1 小修后，刷新主阶段报告，使当前 comparison 输出与最新 v3.1 本地 rescore 状态一致。

本次继续动作只做报告同步：

```text
不修改课程。
不修改 persona / judge prompt / transfer_cases。
不运行真实 API。
不新增实验目录。
不覆盖 simulation_runs.jsonl 或 judge_results.jsonl。
```

## 已执行的关键命令

真实 after_patch retry_002 阶段已执行：

```bash
python experiments/synthetic_student_lab/run_simulation.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/judge.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/failure_analyzer.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python check_ssl_outputs.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/inspect_ssl_issues.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
```

scorer v3.1 阶段已执行：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
python experiments/synthetic_student_lab/rescore_with_enhanced_rules.py --input-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
```

## 生成和更新的输出

主报告：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/comparison_report.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/stage_report.md
```

专项报告：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/enhanced_false_pass_review.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/enhanced_false_fail_review.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/scorer_v3_false_pass_patch_report.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/scorer_v3_1_false_fail_patch_report.md
```

本地 rescore 输出：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/enhanced_rule_score_report.md
```

## 检查结果

```text
compileall: PASS
pytest enhanced scorer: 15 passed, 1 dependency deprecation warning
local rescore sanity_tests_passed: True
```

after retry_002 结构检查：

```text
simulation_runs.jsonl rows: 96
judge_results.jsonl rows: 96
run_id one_to_one: True
error_message non-empty count: 0
student_answer empty count: 0
severe structural problems: none
```

## 当前 comparison 摘要

真实 judge 指标：

```text
overall judge_passed: 55/96 (57.3%) -> 47/96 (49.0%) (-8.3pp)
hidden_transfer judge_passed: 22/24 (91.7%) -> 18/24 (75.0%) (-16.7pp)
```

v3.1 enhanced 指标：

```text
enhanced_rule_passed: 45/96 (46.9%) -> 32/96 (33.3%)
enhanced false pass: 3 -> 0
enhanced false fail: 13 -> 15
```

说明：

```text
enhanced after 已经是 v3.1 本地 rescore。
enhanced 指标主要用于 scorer hygiene，不应当作课程 patch 的直接效果证据。
```

## 三个 patch 节点

```text
accrual_vs_cash:
  judge 5/12 (41.7%) -> 1/12 (8.3%)
  enhanced 1/12 (8.3%) -> 1/12 (8.3%)

net_profit:
  judge 6/12 (50.0%) -> 6/12 (50.0%)
  enhanced 2/12 (16.7%) -> 2/12 (16.7%)

gross_margin:
  judge 7/12 (58.3%) -> 5/12 (41.7%)
  enhanced 8/12 (66.7%) -> 2/12 (16.7%)
```

## 风险

```text
1. course_patch_validation 仍为 FAIL。
2. hidden_transfer judge 下降明显，迁移效果没有成立。
3. accrual_vs_cash 是最高风险课程节点。
4. gross_margin 在 v3.1 下暴露出公式和净利边界风险。
5. scorer v3.1 已改善 false pass，但 false fail 仍需人工理解。
```

## 当前闸门

```text
structural_validity: PASS
scorer_v3_1_hygiene: PASS
course_patch_validation: FAIL
next_gate: 人工审核课程失败样本，决定是否做第二轮课程 patch
```

## 下一步建议

建议先做离线人工分析，不要直接运行新的真实 API：

```text
1. 聚焦 accrual_vs_cash、gross_margin、net_profit 三个 patch 节点的 judge fail 样本。
2. 区分课程内容问题、学生 persona 随机波动、judge 偏差和 scorer 过严。
3. 若确认课程仍需修改，再提出第二轮小范围课程 patch 计划。
4. 只有课程 patch 或实验方案经人工批准后，再考虑新的真实 API 对比实验。
```
