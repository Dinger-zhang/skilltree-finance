# 当前阶段状态

## 1. 当前阶段

当前阶段：Synthetic Student Lab 完整 B 链真实实验。

## 2. 已完成事项

已完成：

1. Synthetic Student Lab 最小框架开发；
2. mock 或前置验证阶段；
3. 阶段 1—6；
4. 准备进入完整 B 链真实实验。

## 3. 当前目标

运行完整 B 链真实实验，生成可审计实验包。

目标输出目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001/
```

## 4. 当前实验范围

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

最低预期记录数：

```text
8 个节点 × 3 个 persona × 4 个 condition = 96 条
```

如果实际 B 链节点数不是 8，以实际节点数为准，但必须在报告中说明。

## 5. 下一步任务

Codex 下一步应执行：

1. 检查当前脚本支持哪些 CLI 参数；
2. 确认输出目录不会覆盖旧结果；
3. 确认 API Key 只从环境变量读取；
4. 运行 compileall；
5. 如果未做 smoke test，先做 1 个节点真实 smoke test；
6. 请求用户批准后，运行完整 B 链真实 simulation；
7. 运行真实 judge；
8. 生成 node_failure_report.md；
9. 运行 check_outputs.py；
10. 抽取 human_review_samples.jsonl；
11. 输出阶段报告；
12. 暂停等待人工复核。

## 6. 本阶段完成标准

本阶段完成必须满足：

1. `simulation_runs.jsonl` 存在；
2. `judge_results.jsonl` 存在；
3. `node_failure_report.md` 存在；
4. `check_summary.txt` 存在；
5. `human_review_samples.jsonl` 存在；
6. 记录数达到预期；
7. simulation 与 judge 能按 run_id 对齐；
8. 报告能指出至少 3 个具体课程问题或评分问题；
9. 没有自动修改正式知识图谱；
10. 需要人工复核的样本已抽出。

## 7. 当前禁止事项

在本阶段，Codex 不得：

1. 修改 `data/knowledge_graph.yaml`；
2. 修改正式学习页面；
3. 删除旧输出；
4. 覆盖 mock 输出；
5. 改 judge 标准；
6. commit / push；
7. 打印 API Key；
8. 自动进入后台长期运行。

## 8. 阶段记录

### 记录 001

状态：待执行完整 B 链真实实验。

输出目录：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_001/
```

当前结论：等待 Codex 检查脚本和运行环境。