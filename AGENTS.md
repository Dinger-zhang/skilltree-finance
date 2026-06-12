# AGENTS.md

## 1. 项目身份

本项目是 SkillTree Finance / AI 学习树项目。当前重点是基于财务报表学习场景，验证“知识图谱 + 推理链 + 掌握验证 + 诊断反馈”的结构化学习机制。

当前正在推进的重点模块是：

- Synthetic Student Lab：模拟学生学习实验室
- 目标：用多类模拟学生离线压力测试知识图谱、推理链、引导问题、掌握题、迁移题和评分规则
- 当前阶段：repaired baseline 与 enhanced scorer v2 已验收通过，准备对 3 个课程节点做小范围 patch

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
9. 在高风险动作前暂停并请求用户批准。

你不是课程内容的最终决策者，也不是项目战略决策者。

## 3. 必读文档顺序

每次开始任务时，优先读取：

1. `docs/11_CURRENT_STAGE.md`
2. `docs/10_CODEX_AUTONOMOUS_WORKFLOW.md`
3. `docs/09_SYNTHETIC_STUDENT_LAB_PLAN.md`
4. `docs/03_MVP_DEVELOPMENT_PLAN.md`

如果任务涉及实验设计，再读取：

5. `docs/04_EXPERIMENT_PLAN.md`

如果任务涉及项目定位，再读取：

6. `docs/01_PROJECT_CONTEXT.md`
7. `docs/06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

不要默认一次性重读所有 docs，除非用户明确要求。

## 4. 当前核心任务边界

Synthetic Student Lab 是离线课程质检工具，不是正式学习主流程。

当前阶段允许你：

1. 在用户明确批准后，只修改 `data/knowledge_graph.yaml` 中指定的 3 个节点：
   - `accrual_vs_cash`
   - `net_profit`
   - `gross_margin`
2. 运行基础检查：
   - `python -m compileall -q app.py pages src tests experiments`
   - `python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q`
3. 输出 `git diff --stat` 与 `git diff data/knowledge_graph.yaml`；
4. 更新 `docs/11_CURRENT_STAGE.md` 或实验记录；
5. 在完成修改后暂停，等待人工审核。

当前阶段不允许你未经批准：

1. 修改 3 个指定节点以外的 `data/knowledge_graph.yaml` 内容；
2. 修改 `app.py`；
3. 修改 `pages/` 正式学习页面；
4. 修改主产品流程；
5. 修改 `experiments/synthetic_student_lab/` 工具代码，除非用户明确要求；
6. 修改 persona、judge prompt、transfer_cases；
7. 删除或覆盖历史实验输出；
8. 改变 judge 标准来让指标变好；
9. 自动把课程修改建议写回正式知识图谱以外的节点；
10. commit 或 push；
11. 安装新依赖；
12. 打印、保存或上传 API Key；
13. 自动运行 after_patch 真实 API 实验。

## 5. 已完成的当前实验基线

目标链：`B. 从交易到利润表`

模拟学生：

- `novice_closed_book`
- `rote_memorizer`
- `misconception_prone`

测试条件：

- `no_course_baseline`
- `node_only`
- `chain_so_far`
- `hidden_transfer`

有效 before baseline 目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001_repaired/
```

该目录已通过检查：

```text
simulation_runs.jsonl rows: 96
judge_results.jsonl rows: 96
run_id one_to_one: True
error_message: 0
empty student_answer: 0
severe structural problems: none
```

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
old_rule_fail_llm_pass: 43
enhanced_rule_fail_llm_pass: 13
conclusion_status: PASS
```

当前不再继续大修 scorer。后续课程 patch 的效果判断应综合：

```text
LLM judge
enhanced rule scorer
人工抽查
hidden_transfer 表现
是否出现新的 false pass / false fail
```

## 7. 当前课程 patch 目标

只允许小范围修改以下 3 个节点：

### 7.1 `accrual_vs_cash`

补充重点：

```text
权责发生制关注交易归属期间；
现金制关注现金实际收付；
未收款也可能确认收入；
已发生费用即使未付款也可能归入本期；
防止“权责发生制/现金制定义反转”。
```

### 7.2 `net_profit`

补充重点：

```text
净利润大致等于收入扣除成本、费用和税费；
净利润反映经营成果，不等于现金余额；
净利润可能包含未收现收入；
净利润可能包含非现金费用；
防止“净利润为正就现金充足”。
```

### 7.3 `gross_margin`

补充重点：

```text
毛利 = 收入 - 销售成本；
毛利率 = 毛利 / 收入；
毛利尚未扣除期间费用；
毛利高不等于净利润高；
毛利高不等于现金充足。
```

## 8. 下一步执行要求

Codex 修改课程 patch 后必须输出：

```bash
git diff --stat
git diff data/knowledge_graph.yaml
```

并运行：

```bash
python -m compileall -q app.py pages src tests experiments
python -m pytest experiments/synthetic_student_lab/tests/test_enhanced_rule_scorer.py -q
```

完成后暂停，等待人工审核是否进入：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
```

## 9. 高风险动作闸门

以下动作必须暂停并请求用户批准：

1. 运行完整真实 API 实验；
2. 运行 after_patch；
3. 修改非指定节点；
4. 修改 judge prompt 或评分标准；
5. 修改实验条件或 persona；
6. 删除旧输出；
7. commit / push；
8. 安装依赖；
9. 输出或保存密钥。
