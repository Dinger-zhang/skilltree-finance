# Codex 自主化工作流

## 1. 目的

本文档定义 Codex 在本项目中的自主推进方式，目标是减少人工复制命令、复制错误、反复询问下一步的成本。

Codex 可以自主完成工程执行、检查、修复和报告，但不能越过人工决策边界。

## 2. 工作模式

Codex 每次开始任务时，应执行以下循环：

``` text
读取当前阶段
→ 判断目标
→ 制定短计划
→ 执行最小修改
→ 运行检查
→ 修复错误
→ 再次检查
→ 生成阶段报告
→ 更新当前阶段文档
→ 在决策闸门处暂停
```

## 3. 自主可执行事项

Codex 可以自主执行：

1. 阅读项目文档；
2. 检查文件结构；
3. 修改实验脚本；
4. 新增 CLI 参数；
5. 新增检查脚本；
6. 新增报告脚本；
7. 新增人工复核样本抽取脚本；
8. 跑 mock / dry-run；
9. 跑 compileall；
10. 修复路径错误；
11. 修复 JSONL 字段缺失；
12. 修复异常处理；
13. 生成阶段报告；
14. 更新 `docs/11_CURRENT_STAGE.md`。

## 4. 需要人工批准事项

以下事项 Codex 必须暂停：

1. 运行完整真实 API 实验；
2. 修改正式知识图谱；
3. 修改正式学习页面；
4. 删除旧实验输出；
5. 安装新依赖；
6. 改变 judge 标准；
7. commit / push；
8. 启动长期后台任务；
9. 打印或保存密钥。

## 5. 当前推荐自动化强度

当前采用“有监督自主执行”：

```text
Codex 自主推进工程任务；
遇到高风险动作请求批准；
用户只审阶段报告和批准关键动作。
```

不采用完全无人值守模式。

## 6. 阶段推进原则

Codex 不应一次性追求大而全。

每个阶段只做一件事：

1. 先跑通数据流；
2. 再跑真实小样本；
3. 再跑完整 B 链；
4. 再生成报告；
5. 再抽人工复核样本；
6. 再等待人工判断；
7. 再决定是否修改课程；
8. 再做 before/after 对比。

## 7. 对 Synthetic Student Lab 的特殊要求

Synthetic Student Lab 只能产生候选问题和候选修改建议。

禁止：

1. 自动修改正式知识图谱；
2. 用模拟学生通过率替代真实学生效果；
3. 为了指标好看调整 judge；
4. 用同一轮结果既调参又证明效果；
5. 删除失败样本；
6. 覆盖历史输出。

## 8. 每轮实验必须保留原始数据

必须保留：

```text
simulation_runs.jsonl
judge_results.jsonl
node_failure_report.md
check_summary.txt
human_review_samples.jsonl
运行日志
```

派生报告可以重新生成，但原始 JSONL 不应修改。

## 9. 当前阶段 Codex 执行边界（2026-06-12）

当前 repaired baseline 与 enhanced scorer v2 已验收通过。Codex 当前任务不再是继续修 scorer，而是根据人工批准，对 3 个课程节点做小范围 patch。

### 9.1 当前允许

```text
1. 只修改 data/knowledge_graph.yaml 中：
   - accrual_vs_cash
   - net_profit
   - gross_margin
2. 运行 compileall；
3. 运行 enhanced scorer 测试；
4. 输出 git diff --stat；
5. 输出 git diff data/knowledge_graph.yaml；
6. 更新 docs/11_CURRENT_STAGE.md 的阶段记录。
```

### 9.2 当前禁止

```text
1. 修改其他课程节点；
2. 修改 app.py / pages / 主流程；
3. 修改 judge prompt、persona、transfer_cases；
4. 调用真实 API；
5. 自动运行 after_patch；
6. 覆盖 ssl_v0_3_real_b_chain_001_repaired；
7. commit / push；
8. 安装新依赖；
9. 输出 API Key。
```

### 9.3 当前完成后必须暂停

Codex 完成 3 个节点 patch 后，必须暂停等待人工审核。只有人工确认 `git diff data/knowledge_graph.yaml` 合格后，才能进入：

```text
experiments/synthetic_student_lab/outputs/ssl_v0_3_real_b_chain_002_after_patch/
```
