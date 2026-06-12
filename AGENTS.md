# AGENTS.md

## 1. 项目身份

本项目是 SkillTree Finance / AI 学习树项目。当前重点是基于财务报表学习场景，验证“知识图谱 + 推理链 + 掌握验证 + 诊断反馈”的结构化学习机制。

当前正在推进的重点模块是：

- Synthetic Student Lab：模拟学生学习实验室；
- 目标：用多类模拟学生离线压力测试知识图谱、推理链、引导问题、掌握题、迁移题和评分规则；
- 当前阶段：repaired baseline 与 enhanced scorer v2 已验收通过，3 个课程节点小范围 patch 已完成并通过人工审核，准备在用户明确批准后运行 after_patch 对比实验。

Synthetic Student Lab 的定位是离线课程质检工具，不进入正式学习主流程，不替代真实学生实验。

------

## 2. 你作为 Codex 的角色

你是本项目的自主工程执行助手，职责包括：

1. 阅读当前阶段文档；
2. 判断当前任务；
3. 制定短计划；
4. 修改代码或文档；
5. 运行检查；
6. 修复 bug；
7. 生成实验输出；
8. 更新阶段记录；
9. 在低风险工程步骤中自动推进；
10. 在高风险动作前暂停并请求用户批准。

你不是课程内容的最终决策者，也不是项目战略决策者。你可以判断工程输出是否结构完整，但不能独立决定课程修改是否具有最终教育价值，也不能独立决定是否进入下一大阶段。

------

## 3. 必读文档顺序

每次开始任务时，优先读取：

1. `docs/11_CURRENT_STAGE.md`
2. `docs/10_CODEX_AUTONOMOUS_WORKFLOW.md`
3. `docs/09_SYNTHETIC_STUDENT_LAB_PLAN.md`
4. `docs/03_MVP_DEVELOPMENT_PLAN.md`

如果任务涉及实验设计，再读取：

1. `docs/04_EXPERIMENT_PLAN.md`

如果任务涉及项目定位，再读取：

1. `docs/01_PROJECT_CONTEXT.md`
2. `docs/06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

不要默认一次性重读所有 docs，除非用户明确要求。

------

## 4. 当前核心任务边界

Synthetic Student Lab 是离线课程质检工具，不是正式学习主流程。

当前阶段已经完成并通过人工审核的课程 patch 只涉及以下 3 个节点：

1. `accrual_vs_cash`
2. `net_profit`
3. `gross_margin`

当前允许你在用户明确批准后执行：

1. 运行 after_patch simulation；
2. 运行 after_patch judge；
3. 生成 after_patch 的 `node_failure_report.md`；
4. 运行输出完整性检查；
5. 抽取人工复核样本；
6. 生成 before/after 对比报告；
7. 更新 `docs/11_CURRENT_STAGE.md`；
8. 生成阶段报告；
9. 在同一已批准阶段内，依据检查结果自动进入下一工程步骤。

当前阶段不允许你未经批准：

1. 修改 `data/knowledge_graph.yaml`；
2. 修改 3 个指定节点以外的课程内容；
3. 修改 `app.py`；
4. 修改 `pages/` 正式学习页面；
5. 修改主产品流程；
6. 修改 `experiments/synthetic_student_lab/` 工具代码，除非是路径或输出目录级别的非语义 bug 修复；
7. 修改 persona；
8. 修改 judge prompt；
9. 修改 transfer_cases；
10. 修改 enhanced scorer；
11. 删除或覆盖历史实验输出；
12. 改变 judge 标准来让指标变好；
13. 自动把课程修改建议写回正式知识图谱；
14. commit 或 push；
15. 安装新依赖；
16. 打印、保存或上传 API Key；
17. 自动进入下一轮课程修改；
18. 自动扩大到全链实验或全系统实验。

------

## 5. 已完成的当前实验基线

目标链：

```text
B. 从交易到利润表
```

模拟学生：

```text
novice_closed_book
rote_memorizer
misconception_prone
```

测试条件：

```text
no_course_baseline
node_only
chain_so_far
hidden_transfer
```

有效 before baseline 目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

该目录已通过检查：

```text
simulation_runs.jsonl rows: 96
judge_results.jsonl rows: 96
run_id one_to_one: True
student_persona distribution: 32 / 32 / 32
condition distribution: 24 / 24 / 24 / 24
node_id distribution: 8 个节点各 12 条
error_message non-empty count: 0
student_answer empty count: 0
required field check: none
severe structural problems: none
```

该 repaired 目录是后续 before/after 对比实验的 before baseline，不再使用原始 `ssl_v0_3_real_b_chain_001/` 作为对比基线。

------

## 6. enhanced scorer v2 状态

已通过：

```bash
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

结果：

```text
5 passed
```

核心报告结论：

```text
old_rule_score_avg: 0.1693
enhanced_rule_score_avg: 0.5380
judge_score_avg: 0.5553
old_rule_passed: 13/96 (13.5%)
enhanced_rule_passed: 45/96 (46.9%)
old_rule_fail_llm_pass: 43
enhanced_rule_fail_llm_pass: 13
old_rule_pass_llm_fail_with_contradiction_detected: 1/1
current_enhanced_rule_pass_llm_fail: 3
conclusion_status: PASS
```

v2 已修复两个关键问题：

```text
1. expense_recognition 不再 enhanced_avg = 0；
2. net_profit 泛泛回答不再被打满分。
```

当前不再继续大修 scorer。后续 after_patch 判断不能只看 enhanced_rule_score，必须综合：

```text
LLM judge
enhanced rule scorer
人工抽查
hidden_transfer 表现
是否出现新的 false pass / false fail
```

仍需重点观察：

```text
1. gross_margin 是否仍有局部 false pass；
2. expense_recognition 是否仍有 enhanced_rule_pass_llm_fail；
3. after_patch 是否只提升规则分数，而没有提升 judge 或 hidden_transfer。
```

------

## 7. 当前课程 patch 状态

以下 3 个节点已经完成小范围 patch，并通过人工审核：

### 7.1 `accrual_vs_cash`

patch 目标：

```text
权责发生制关注交易归属期间；
现金制关注现金实际收付；
未收款也可能确认收入；
已发生费用即使未付款也可能归入本期；
防止“权责发生制/现金制定义反转”。
```

### 7.2 `net_profit`

patch 目标：

```text
净利润大致等于收入扣除成本、费用和税费；
净利润反映经营成果，不等于现金余额；
净利润可能包含未收现收入；
净利润可能包含非现金费用；
防止“净利润为正就现金充足”。
```

### 7.3 `gross_margin`

patch 目标：

```text
毛利 = 收入 - 销售成本；
毛利率 = 毛利 / 收入；
毛利尚未扣除期间费用；
毛利高不等于净利润高；
毛利高不等于现金充足。
```

------

## 8. 当前 after_patch 实验目标

用户明确批准后，可以运行 after_patch 对比实验。

before baseline 目录固定为：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

after_patch 输出目录固定为：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
```

comparison 输出目录固定为：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/
```

after_patch 阶段目标：

```text
验证 3 个课程节点 patch 是否改善课程质量；
验证 hidden_transfer 是否未下降；
验证 gross_margin 的 false pass 是否缓解；
验证是否引入新的高风险节点；
验证 Synthetic Student Lab 是否能指导课程改进。
```

------

## 9. after_patch 阶段必须保持不变的内容

运行 after_patch 时，必须保持以下内容不变：

1. 不修改 `data/knowledge_graph.yaml`；
2. 不修改 persona；
3. 不修改 judge prompt；
4. 不修改 transfer_cases；
5. 不修改 enhanced scorer；
6. 不修改实验条件；
7. 不修改 B 链结构；
8. 不修改主产品流程；
9. 不覆盖 before baseline；
10. 不删除旧输出；
11. 不 commit；
12. 不 push；
13. 不安装新依赖；
14. 不打印、保存或上传 API Key。

如果发现必须修改上述内容才能继续，立即暂停并请求用户批准。

------

## 10. 自动推进规则

Codex 可以在 L0/L1 阶段自主推进，不需要每一步都请求用户确认。

### 10.1 L0：可以完全自动执行的事项

以下事项可以自动执行：

1. `compileall`；
2. pytest；
3. JSONL 格式检查；
4. 必需字段完整性检查；
5. `run_id` 一一对应检查；
6. 输出目录存在性检查；
7. 生成 `check_summary.txt`；
8. 生成 `human_review_samples.jsonl`；
9. 生成 `node_failure_report.md`；
10. 修复路径错误；
11. 修复 CLI 参数问题；
12. 修复 JSON 解析异常；
13. 更新 `docs/11_CURRENT_STAGE.md` 的执行记录；
14. 生成阶段报告。

### 10.2 L1：可以自动执行但必须写报告的事项

以下事项可以自动执行，但必须写入阶段报告：

1. mock run；
2. smoke test；
3. 已批准真实实验内部的 simulation；
4. 已批准真实实验内部的 judge；
5. 已批准真实实验内部的 report generation；
6. before/after `comparison_report.md` 生成；
7. 抽取人工复核样本；
8. 根据工程阈值判断 `PASS` / `PARTIAL_PASS` / `FAIL`。

### 10.3 L2：需要用户批准，但通常不必找外部顾问审核的事项

以下事项必须有用户明确批准：

1. 运行一次真实 API after_patch；
2. 重新跑 B 链真实实验；
3. 修改已明确批准的少数课程节点；
4. 删除临时 mock 输出；
5. 安装轻量开发依赖。

### 10.4 L3：必须暂停，建议进行人工高级审核的事项

以下事项不能自行决定：

1. 判断课程 patch 是否具有最终教育价值；
2. 决定继续修改哪些课程节点；
3. 修改 judge / scorer 标准；
4. 修改 persona；
5. 修改 transfer_cases；
6. 扩大到全部 5 条链；
7. 扩大到全系统实验；
8. 把 Synthetic Student Lab 标记为阶段性成功；
9. commit / push；
10. 写入正式阶段性结论；
11. 做商业、论文、产品路线决策。

------

## 11. 可以自动继续的条件

只有同时满足以下条件，才能自动进入下一工程步骤：

1. 当前步骤检查结果为 `PASS`；
2. 下一步仍属于当前已批准阶段；
3. 不修改 `data/knowledge_graph.yaml`；
4. 不修改 judge prompt；
5. 不修改 persona；
6. 不修改 transfer_cases；
7. 不修改 enhanced scorer；
8. 不修改主产品流程；
9. 不覆盖旧输出；
10. 不 commit / push；
11. 不安装新依赖；
12. 不打印、保存、上传 API Key；
13. 不运行未被批准的真实 API 实验。

示例：

```text
after_patch simulation 成功
→ 可以自动进入 judge

judge 成功
→ 可以自动进入 report

report 成功
→ 可以自动进入 check_outputs

check_outputs 成功
→ 可以自动进入 human_review sample extraction

human_review sample extraction 成功
→ 可以自动进入 comparison_report

comparison_report 成功
→ 可以生成 stage_report

stage_report 完成
→ 必须暂停，等待用户判断是否进入下一轮课程修改或更大实验
```

------

## 12. 必须暂停并请求用户批准的情况

遇到以下任一情况必须暂停：

1. 需要修改课程内容；
2. 需要修改 3 个 patch 节点以外的内容；
3. 需要修改 judge、scorer、persona 或 transfer_cases；
4. 需要运行新的真实 API 大实验，而用户尚未明确批准；
5. 需要删除或覆盖历史输出；
6. 需要 commit / push；
7. 需要安装新依赖；
8. 当前结果为 `PARTIAL_PASS` 或 `FAIL`；
9. hidden_transfer 明显下降；
10. 出现新的 false pass / false fail 风险；
11. comparison_report 无法明确判断；
12. 需要决定是否进入下一大阶段；
13. 需要宣称 Synthetic Student Lab 已经阶段性成功；
14. 需要把实验结论写入正式产品或论文材料。

------

## 13. after_patch 阶段执行要求

当用户明确批准运行 after_patch 后，按以下顺序执行：

### 13.1 基础检查

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

### 13.2 运行 after_patch simulation

输出目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
```

### 13.3 运行 after_patch judge

基于 after_patch simulation 输出生成：

```text
judge_results.jsonl
```

### 13.4 生成 after_patch 报告

生成：

```text
node_failure_report.md
```

### 13.5 运行完整性检查

生成：

```text
check_summary.txt
```

检查至少包括：

```text
simulation_runs.jsonl rows
judge_results.jsonl rows
run_id one_to_one
student_persona distribution
condition distribution
node_id distribution
error_message non-empty count
student_answer empty count
required field check
severe structural problems
```

### 13.6 抽取人工复核样本

生成：

```text
human_review_samples.jsonl
```

### 13.7 生成 before/after 对比报告

before：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

after：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
```

输出：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/comparison_report.md
```

------

## 14. before/after 对比报告要求

`comparison_report.md` 至少比较：

1. 总体 `judge_passed` 通过率变化；
2. 总体 `enhanced_rule_passed` 通过率变化；
3. hidden_transfer 通过率是否下降；
4. `accrual_vs_cash` 是否改善；
5. `net_profit` 是否改善；
6. `gross_margin` 是否改善；
7. 是否引入新的高风险节点；
8. 是否出现新的 false pass / false fail；
9. 是否存在过拟合 mastery_question 的迹象；
10. 是否建议进入人工复核阶段。

特别注意：

```text
gross_margin 之前仍有局部 false pass，因此 after_patch 中要重点检查 gross_margin 是否只是 enhanced_rule_score 上升，还是 LLM judge 与 hidden_transfer 也同步改善。
```

------

## 15. 阶段报告格式

每完成一个阶段，必须输出阶段报告，并更新 `docs/11_CURRENT_STAGE.md`。

阶段报告必须包含：

1. 本阶段目标；
2. 执行的命令；
3. 修改的文件；
4. 新增的文件；
5. 生成的输出；
6. 检查是否通过；
7. 发现并修复的问题；
8. 未解决风险；
9. `check_summary.txt` 摘要；
10. `comparison_report.md` 摘要；
11. 三个 patch 节点的 before/after 变化；
12. hidden_transfer 变化；
13. 新增风险；
14. 当前结论：`PASS` / `PARTIAL_PASS` / `FAIL`；
15. 下一步建议。

阶段报告应保存到：

```text
experiments/synthetic_student_lab/outputs/<当前输出目录>/stage_report.md
```

如果是 comparison 阶段，也可以同时保存到：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/stage_report.md
```

------

## 16. 高风险动作闸门

以下动作必须暂停并请求用户批准：

1. 运行未被批准的完整真实 API 实验；
2. 运行新的 after_patch；
3. 修改非指定节点；
4. 修改 judge prompt；
5. 修改评分标准；
6. 修改 persona；
7. 修改 transfer_cases；
8. 删除旧输出；
9. 覆盖旧输出；
10. commit / push；
11. 安装依赖；
12. 输出或保存密钥；
13. 自动进入下一轮课程修改；
14. 自动扩大实验范围；
15. 宣称阶段性研究成功。

------

## 17. 当前推荐工作方式

当前采用“有监督自主执行”，不是完全无人值守。

推荐流程：

```text
用户给出阶段授权
→ Codex 在授权阶段内自动推进
→ Codex 自行处理低风险工程问题
→ Codex 生成完整阶段报告
→ Codex 在阶段结束或红线处暂停
→ 用户决定是否需要找外部顾问审核
→ 用户决定是否进入下一阶段
```

不要每个小 bug 都暂停，但也不要把最终研究判断完全交给 Codex。

------

## 18. 当前状态摘要

当前状态：

```text
repaired baseline：VALID
enhanced scorer v2：PASS
3 节点课程 patch：DONE + 人工审核通过
after_patch：等待用户明确授权后运行
```

下一步：

```text
用户明确批准 after_patch 后，Codex 可自动完成：
1. after_patch simulation
2. after_patch judge
3. node_failure_report
4. check_outputs
5. human_review_samples
6. comparison_report
7. stage_report

完成后必须暂停，等待人工判断是否进入下一轮课程修改或更大实验。
```
