# 当前阶段状态

最后更新：2026-06-13

## 1. 当前阶段

当前阶段：**Synthetic Student Lab repaired baseline + enhanced scorer v2 已验收通过，课程三点小修补已完成并进入 after_patch；retry_002 已生成结构有效输出与 comparison_report，当前结论为 FAIL，等待人工审核。**

产品主线仍是 SkillTree Finance / AI 学习树的财务报表学习 MVP。Synthetic Student Lab 的定位仍然是离线课程质检工具，不进入正式学习主流程，不替代真实学生实验。

当前阶段的核心判断：

```text
Enhanced scorer v2：PASS
SSL repaired baseline：VALID
课程三点小修补：DONE
after_patch retry_002：STRUCTURALLY_VALID
comparison_report：GENERATED
当前结论：FAIL
下一步：人工审核 comparison_report 与 human_review_samples
后续：人工决定是否做 targeted retry、课程修订、scorer 审查或停止本轮课程 patch
```

## 2. 已完成事项

### 2.1 Synthetic Student Lab 工程与实验闭环

已完成：

1. `experiments/synthetic_student_lab/` 最小实验框架；
2. 3 类模拟学生画像：
   - `novice_closed_book`
   - `rote_memorizer`
   - `misconception_prone`
3. 4 类测试条件：
   - `no_course_baseline`
   - `node_only`
   - `chain_so_far`
   - `hidden_transfer`
4. B 链真实完整实验；
5. bad records targeted retry；
6. repaired baseline 输出目录；
7. human review 样本抽取；
8. enhanced rule scorer v1/v2；
9. enhanced scorer sanity tests；
10. 人工复核与课程问题候选归因。

### 2.2 repaired baseline 验收结果

当前有效 baseline 目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

`check_ssl_outputs.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired` 已确认：

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

该 repaired 目录应作为后续 before/after 对比实验的 before baseline，不再使用原始 `ssl_v0_3_real_b_chain_001/` 作为对比基线。

### 2.3 enhanced rule scorer v2 验收结果

已运行：

```bash
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

结果：

```text
5 passed in 0.24s
```

`enhanced_rule_score_report.md` 当前核心指标：

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

仍需记录的残留问题：

```text
1. gross_margin 仍有局部 false pass；
2. expense_recognition 仍有 1 条 enhanced_rule_pass_llm_fail；
3. 后续 after_patch 判断不能只看 enhanced_rule_score，仍需结合 LLM judge 与人工抽查。
```

## 3. 当前目标

当前目标从“跑完整 B 链真实实验”转为：

> 基于 repaired baseline + enhanced scorer v2，只对 3 个课程节点做小范围 patch，并运行 after_patch 对比实验，判断 Synthetic Student Lab 是否能指导课程改进。

当前不再继续大修 scorer，除非 after_patch 暴露新的明显评分漏洞。

当前 after_patch retry_002 已完成。输出结构有效，但 comparison 结果未验证课程 patch 有效性：总体 LLM judge 通过率下降，hidden_transfer LLM judge 通过率下降，enhanced-rule false pass 风险上升。

## 4. 当前建议修改的 3 个课程节点

### 4.1 `accrual_vs_cash`

问题：

```text
学生容易把权责发生制和现金制定义反过来；
认为没收款就不能确认收入；
认为没付款就没有费用。
```

修改方向：

```text
增加同一业务在权责发生制和现金制下的对照案例；
明确权责发生制看交易归属期间，现金制看现金实际收付；
强化未收款也可能确认收入、未付款也可能确认费用。
```

### 4.2 `net_profit`

问题：

```text
学生容易只背“净利润不等于现金”，但解释不出机制；
也容易认为净利润为正就现金充足。
```

修改方向：

```text
补充净利润形成链条：收入 - 成本 - 费用 - 税费；
解释未收现收入与非现金费用如何造成净利润与现金不一致；
加入利润为正但现金紧张的小案例。
```

### 4.3 `gross_margin`

问题：

```text
学生容易认为毛利率高就等于净利润高；
甚至进一步认为毛利高就现金多。
```

修改方向：

```text
强化毛利与净利润的边界；
说明毛利只扣销售成本，尚未扣期间费用、折旧摊销、税费等；
说明毛利高不等于净利润高，也不等于现金充足。
```

## 5. 下一步任务

Codex 下一步应执行：

1. 读取本文件、`docs/10_CODEX_AUTONOMOUS_WORKFLOW.md`、`docs/09_SYNTHETIC_STUDENT_LAB_PLAN.md`；
2. 只修改 `data/knowledge_graph.yaml` 中以下 3 个节点：
   - `accrual_vs_cash`
   - `net_profit`
   - `gross_margin`
3. 不修改实验工具代码；
4. 不调用 API；
5. 不运行 after_patch；
6. 只运行基础检查：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

7. 输出：

```bash
git diff --stat
git diff data/knowledge_graph.yaml
```

8. 暂停等待人工审核。

## 6. 本阶段完成标准

课程三点小修补阶段完成标准：

1. 只修改 3 个指定节点；
2. 每个节点只做小范围、可解释内容增强；
3. 不改变 B 链结构；
4. 不改变 persona、judge prompt、transfer_cases；
5. 不修改 Synthetic Student Lab 工具代码；
6. `compileall` 通过；
7. enhanced scorer tests 通过；
8. `git diff data/knowledge_graph.yaml` 能清楚展示每个修改点；
9. 人工审核确认修改与 baseline 暴露的问题一致。

## 7. 当前禁止事项

在本阶段，Codex 不得：

1. 自动运行完整真实 API 实验；
2. 自动进入 after_patch；
3. 自动修改除 3 个指定节点以外的课程内容；
4. 修改 `app.py`、`pages/`、正式学习页面；
5. 修改 persona、judge prompt、transfer_cases；
6. 删除或覆盖历史实验输出；
7. 安装新依赖；
8. commit / push；
9. 打印、保存或上传 API Key。

## 8. 下一阶段预告：after_patch 对比实验

课程三点小修补经人工审核通过后，再进入 after_patch 实验：

```text
输出目录：experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
对比基线：experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

对比指标：

```text
judge_passed 通过率变化
enhanced_rule_passed 通过率变化
hidden_transfer 是否下降
accrual_vs_cash / net_profit / gross_margin 是否改善
是否引入新高风险节点
是否出现新的 false pass / false fail
```

## 9. 阶段记录

### 记录 001

状态：原始完整 B 链真实实验已完成，但存在 bad records。

原始目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001/
```

问题：

```text
error_message non-empty count: 5
student_answer empty count: 3
```

处理：已通过 targeted retry 修复。

### 记录 002

状态：repaired baseline 验收通过。

有效目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

结论：该目录作为后续 before baseline。

### 记录 003

状态：enhanced scorer v2 验收通过。

证据：

```text
pytest: 5 passed
enhanced_rule_score_report.md: conclusion_status = PASS
```

结论：可以进入课程三点小修补阶段。

### 记录 004

状态：课程三点小修补已完成，等待人工审核。

修改范围：

```text
data/knowledge_graph.yaml
- accrual_vs_cash
- net_profit
- gross_margin
```

本次只对上述 3 个节点的解释、常见误区和掌握题答案做小范围、可解释增强；未修改其他课程节点，未修改 persona、judge prompt、transfer_cases、Synthetic Student Lab 工具代码、`app.py`、`pages/` 或主产品流程。

已运行检查：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

检查结果：

```text
compileall: PASS
pytest enhanced scorer: 5 passed, 1 dependency deprecation warning
```

当前结论：需要人工审核 `git diff data/knowledge_graph.yaml`。尚未运行 after_patch，也未进入 `experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/`。

### 记录 005

状态：after_patch retry_002 已完成，结构有效，但 comparison 结论为 FAIL。

背景：

```text
第一次 after_patch 与 retry_001 均因外部 API read timeout 产生大量 bad records，不能作为有效 before/after 对比。
随后将 experiments/synthetic_student_lab/config.yaml 中 student_client 与 judge_client 的 timeout_seconds 从 60 提高到 180。
```

有效 after_patch 输出目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/
```

comparison 输出目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/
```

已运行命令：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
python experiments/synthetic_student_lab/run_simulation.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/judge.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/failure_analyzer.py --real-mode --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python check_ssl_outputs.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/inspect_ssl_issues.py --output-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
python experiments/synthetic_student_lab/rescore_with_enhanced_rules.py --input-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
```

结构检查结果：

```text
simulation_runs.jsonl rows: 96
judge_results.jsonl rows: 96
run_id one_to_one: True
error_message non-empty count: 0
student_answer empty count: 0
required field check: none
severe structural problems: none
```

comparison 核心结果：

```text
overall judge_passed: 55/96 (57.3%) -> 47/96 (49.0%)
overall enhanced_rule_passed: 45/96 (46.9%) -> 44/96 (45.8%)
hidden_transfer judge_passed: 22/24 (91.7%) -> 18/24 (75.0%)
hidden_transfer enhanced_rule_passed: 16/24 (66.7%) -> 18/24 (75.0%)
enhanced false pass count: 3 -> 8
```

3 个 patch 节点结果：

```text
accrual_vs_cash: judge 5/12 -> 1/12; enhanced 1/12 -> 1/12
net_profit: judge 6/12 -> 6/12; enhanced 2/12 -> 3/12
gross_margin: judge 7/12 -> 5/12; enhanced 8/12 -> 8/12
```

结论：

```text
current conclusion: FAIL
```

说明：

```text
after_patch retry_002 是结构有效实验输出，但不能证明 3 个课程 patch 改善课程质量。
主要风险是 LLM judge 总体通过率下降、hidden_transfer 下降，以及 enhanced-rule false pass 增加。
当前必须暂停，等待人工审核 comparison_report、stage_report 与 human_review_samples。
```

### 记录 006

状态：enhanced scorer v3 false-pass 小修已完成，等待人工审核。

触发原因：

```text
有效 after_patch retry_002 中 enhanced-rule false pass 从 3 增加到 8。
人工复核发现主要集中在 gross_margin、revenue_recognition、revenue_not_cash_receipt、depreciation_amortization。
```

修改范围：

```text
experiments/synthetic_student_lab/common.py
experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py
```

修改内容：

```text
1. 为 8 条 false pass 类型补充回归测试；
2. 扩展 revenue/cash 与 depreciation/cash 的 contradiction patterns；
3. 收紧 revenue_recognition、revenue_not_cash_receipt、depreciation_amortization 的过宽语义匹配；
4. 为 gross_margin 增加公式证据门槛，避免“毛利还不是净利润”类弱答案打满分。
```

已运行检查：

```bash
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
python -m compileall -q app.py pages src tests experiments
python experiments/synthetic_student_lab/rescore_with_enhanced_rules.py --input-dir experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180
```

检查结果：

```text
pytest enhanced scorer: 11 passed, 1 dependency deprecation warning
compileall: PASS
rescore sanity_tests_passed: True
```

v3 rescore 结果：

```text
enhanced false pass: 8 -> 0
enhanced false fail: 11 -> 18
enhanced_rule_passed: 29/96 (30.2%)
enhanced_rule_score_avg: 0.3906
```

结论：

```text
scorer hygiene: PASS
course validation: still FAIL
```

说明：

```text
v3 小修降低了 false pass 风险，但 scorer 变得更保守，false fail 增加。
当前不应继续自动调 scorer，也不应宣称课程 patch 有效。
下一步需要人工审核新增 false fail 样本，再决定是否进行更细的 scorer 调整或课程二次 patch。
```

### 记录 007

状态：enhanced scorer v3 false fail 审核已完成，等待人工判断是否进入 v3.1。

审核范围：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
筛选条件：judge_passed=true 且 enhanced_rule_passed=false
样本数量：18
```

新增报告：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/enhanced_false_fail_review.md
```

审核分布：

```text
by node:
  revenue_not_cash_receipt: 5
  net_profit: 4
  gross_margin: 3
  revenue_recognition: 2
  income_statement_boundary: 2
  depreciation_amortization: 2

by condition:
  chain_so_far: 7
  node_only: 6
  hidden_transfer: 5

by persona:
  misconception_prone: 10
  rote_memorizer: 5
  novice_closed_book: 3
```

归因结论：

```text
scorer_too_strict: 3
acceptable_conservative_fail: 5
judge_too_lenient: 7
needs_human_review: 3
```

主要发现：

```text
1. revenue_recognition 与 revenue_not_cash_receipt 存在少量高置信 scorer 过严样本，主要是有效改写没有命中 v3 证据模式。
2. gross_margin、depreciation_amortization、net_profit 中多条样本包含明确反向结论或残留误解，enhanced fail 更像合理保守。
3. misconception_prone 样本占 10/18，是 false fail 增加的主要来源；其中多条更接近 judge_too_lenient。
4. 当前不建议广泛放松 scorer v3。若进入 v3.1，应只处理高置信 paraphrase，并保留反向误解回归测试。
```

本阶段约束：

```text
未修改课程。
未修改 scorer。
未修改 persona / judge prompt / transfer_cases。
未运行真实 API。
未进入 scorer v3.1 实现。
当前课程验证结论仍为 FAIL。
```

当前闸门：

```text
false_fail_review: COMPLETE
recommended_status: PARTIAL_PASS
course_validation_status: FAIL
next_gate: human review before scorer v3.1 implementation
```

### 记录 008

状态：false fail 人工审核已完成，enhanced scorer v3.1 小修已完成，等待人工审核 diff。

人工审核决定：

```text
批准只处理 3 条高置信 scorer_too_strict 样本：
  4e12cea729ecaa0a / revenue_recognition
  585ba193316e1153 / revenue_not_cash_receipt
  4ab92215771f559d / revenue_not_cash_receipt

继续保持以下边界不放松：
  gross_margin 公式与净利边界
  net_profit 与现金充足边界
  depreciation_amortization 非现金费用边界
  income_statement_boundary 借款非收入边界
```

修改范围：

```text
experiments/synthetic_student_lab/common.py
experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/enhanced_false_fail_review.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_comparison/scorer_v3_1_false_fail_patch_report.md
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/judge_results.enhanced.jsonl
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch_retry_002_timeout_180/enhanced_rule_score_report.md
```

scorer v3.1 修改内容：

```text
1. revenue_recognition:
   覆盖“服务完成/商品交付 + 未收款/下月收款 + 可确认收入”的有效改写。

2. revenue_not_cash_receipt:
   覆盖“收入记录赚到的经营成果 + 收款记录现金进入 + 赊销造成时间差”的有效改写。

3. contradiction guard:
   补充“没收钱就不应算收入”“现金没增加时确认收入不合理”“收入增加就应现金增加”等反向误解识别。

4. accrual_vs_cash:
   修复 v3.1 初稿引入的一条回归，保证明确说明 6 月收入/费用归属的答案仍可通过。
```

已运行命令：

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

v3 到 v3.1 指标变化：

```text
enhanced_rule_passed: 29/96 -> 32/96
enhanced false pass: 0 -> 0
enhanced false fail: 18 -> 15
enhanced_rule_score_avg: 0.3906 -> 0.3984
```

结论：

```text
scorer_v3_1_false_fail_patch: PASS
false_pass_guard: PASS
course_validation_status: still FAIL
```

说明：

```text
v3.1 是 scorer hygiene 小修，不能改写课程验证结论。
本阶段没有修改课程，没有运行真实 API。
当前应暂停，等待人工审核 v3.1 diff 与中文报告，再决定是否需要新的真实实验或课程二次 patch。
```
