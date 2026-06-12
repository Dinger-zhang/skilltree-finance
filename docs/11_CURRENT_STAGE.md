# 当前阶段状态

最后更新：2026-06-12

## 1. 当前阶段

当前阶段：**Synthetic Student Lab repaired baseline + enhanced scorer v2 已验收通过，课程三点小修补已完成，等待人工审核 diff；尚未运行 after_patch。**

产品主线仍是 SkillTree Finance / AI 学习树的财务报表学习 MVP。Synthetic Student Lab 的定位仍然是离线课程质检工具，不进入正式学习主流程，不替代真实学生实验。

当前阶段的核心判断：

```text
Enhanced scorer v2：PASS
SSL repaired baseline：VALID
课程三点小修补：DONE
下一步：人工审核 data/knowledge_graph.yaml diff
后续：经人工批准后再运行 after_patch 对比实验，验证修改是否改善课程质量
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

> 基于 repaired baseline + enhanced scorer v2，只对 3 个课程节点做小范围 patch，先等待人工审核 diff；审核通过后再运行 after_patch 对比实验，判断 Synthetic Student Lab 是否能指导课程改进。

当前不再继续大修 scorer，除非 after_patch 暴露新的明显评分漏洞。

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
