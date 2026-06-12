# SkillTree Finance 文档维护说明

最后更新：2026-06-12

## 1. 为什么要维护这些文档

本项目不是一次性代码项目，而是一个持续演化的创业验证项目。它会不断产生新的产品设想、学习理论判断、实验结果、技术实现、商业路线和阶段性纠偏。如果只依赖连续对话，上下文迟早会超出，且容易遗忘早期关键判断。

因此建议把项目沉淀为一组 Markdown 文档。后续每次和 AI 继续讨论时，优先上传这些文档中的相关文件，使 AI 快速恢复上下文。

## 2. 推荐维护的文档体系

建议维护 9 个核心文档：

1. `01_PROJECT_CONTEXT.md`  
   项目总览文档，记录项目愿景、当前阶段、核心假设、已形成的关键结论。每次对话前最值得上传。

2. `02_PRODUCT_AND_LEARNING_DESIGN.md`  
   产品与学习机制设计文档，记录技能树、原子知识点、推理链、掌握验证、学生模型等核心产品设计。

3. `03_MVP_DEVELOPMENT_PLAN.md`  
   MVP 与 Codex 开发计划文档，记录当前系统架构、目录结构、Codex 使用规范、版本路线、开发优先级。

4. `04_EXPERIMENT_PLAN.md`  
   实验验证文档，记录财务报表学习实验、前后测、延迟测试、对照组、指标设计、样本招募和数据分析方法。

5. `05_BUSINESS_ROADMAP.md`  
   商业化路线文档，记录商业潜力、切入路径、阶段目标、商业模式、风险和护城河。

6. `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`  
   决策日志与待解决问题文档，记录每次重大调整、被否定的方向、已确认结论、当前问题池。

7. `07_V0_2_ACCEPTANCE_REPORT.md`  
   v0.2 验收报告文档，记录功能验收标准、实际验收结果、验收结论、遗留问题和 v0.2.1 内部试用目标。

8. `08_LLM_API_ENHANCEMENT_PLAN.md`  
   大模型 API 增强计划文档，记录 LLM Shadow Evaluator、个性化反馈、报告总结、题目生成、图谱审查等增强方向。

9. `09_SYNTHETIC_STUDENT_LAB_PLAN.md`  
   模拟学生学习实验室文档，记录多模型模拟学生、课程压力测试、自博弈优化、后台运行门禁和验收标准。

## 3. 每次对话如何使用这些文档

### 情况 A：讨论总体方向
上传：
- `01_PROJECT_CONTEXT.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

### 情况 B：讨论学习机制、知识图谱、推理链
上传：
- `01_PROJECT_CONTEXT.md`
- `02_PRODUCT_AND_LEARNING_DESIGN.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

### 情况 C：讨论 Codex 开发和项目管理
上传：
- `01_PROJECT_CONTEXT.md`
- `03_MVP_DEVELOPMENT_PLAN.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

### 情况 C+：讨论 v0.2 验收结果和 v0.2.1 试用
上传：
- `01_PROJECT_CONTEXT.md`
- `03_MVP_DEVELOPMENT_PLAN.md`
- `04_EXPERIMENT_PLAN.md`
- `07_V0_2_ACCEPTANCE_REPORT.md`

### 情况 D：讨论实验设计和数据分析
上传：
- `01_PROJECT_CONTEXT.md`
- `04_EXPERIMENT_PLAN.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

### 情况 E：讨论商业化和创业推进
上传：
- `01_PROJECT_CONTEXT.md`
- `05_BUSINESS_ROADMAP.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`

### 情况 F：讨论大模型 API、DeepSeek 接入、AI 助教或自动生成内容
上传：
- `01_PROJECT_CONTEXT.md`
- `02_PRODUCT_AND_LEARNING_DESIGN.md`
- `03_MVP_DEVELOPMENT_PLAN.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`
- `08_LLM_API_ENHANCEMENT_PLAN.md`

### 情况 G：讨论模拟学生、课程自博弈、知识图谱自动质检或后台优化
上传：
- `01_PROJECT_CONTEXT.md`
- `02_PRODUCT_AND_LEARNING_DESIGN.md`
- `03_MVP_DEVELOPMENT_PLAN.md`
- `04_EXPERIMENT_PLAN.md`
- `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`
- `08_LLM_API_ENHANCEMENT_PLAN.md`
- `09_SYNTHETIC_STUDENT_LAB_PLAN.md`

### 情况 H：讨论 Codex 自主化、自动推进和长期工程协作

建议上传或让 Codex 优先读取：

1. `AGENTS.md`
2. `docs/10_CODEX_AUTONOMOUS_WORKFLOW.md`
3. `docs/11_CURRENT_STAGE.md`
4. `docs/03_MVP_DEVELOPMENT_PLAN.md`
5. `docs/09_SYNTHETIC_STUDENT_LAB_PLAN.md`

用途：

- 判断当前 Codex 是否应该继续自动推进；
- 判断哪些动作需要人工批准；
- 判断当前阶段是否完成；
- 判断实验输出是否足够进入下一阶段。

## 4. 每次对话结束后如何更新

建议在每轮重要对话结束时，让 AI 做三件事：

1. 更新相关文档中的“新增结论”；
2. 更新 `06_DECISION_LOG_AND_OPEN_QUESTIONS.md`；
3. 如果涉及开发变更，更新 `03_MVP_DEVELOPMENT_PLAN.md`。

推荐提示词：

```text
请根据本轮对话，更新我上传的项目文档。要求：
1. 保留原有结构；
2. 只修改与本轮对话相关的部分；
3. 把新增决策写入决策日志；
4. 把仍未解决的问题写入 Open Questions；
5. 输出更新后的 Markdown 文件。
```

## 5. 文档维护原则

1. 文档要服务于行动，不要写成空泛战略文。
2. 每个重要判断都要记录“为什么这样判断”。
3. 被否定的方向也要记录，避免后续反复绕回。
4. 每次版本变化都要写清楚：从什么变成什么，原因是什么。
5. 以 `01_PROJECT_CONTEXT.md` 作为项目上下文入口。
6. 以 `06_DECISION_LOG_AND_OPEN_QUESTIONS.md` 作为项目记忆和问题池。

## 6. 2026-06-12 文档同步说明

本次同步的核心变化：

```text
1. Synthetic Student Lab repaired baseline 已验收通过；
2. enhanced rule scorer v2 已验收通过；
3. 当前阶段从“完整 B 链真实实验”推进为“课程三点小修补”；
4. 下一步只允许修改 accrual_vs_cash、net_profit、gross_margin；
5. after_patch 实验必须等待人工审核 diff 后再运行。
```

下次继续对话时，优先上传或参考：

```text
AGENTS.md
docs/11_CURRENT_STAGE.md
docs/10_CODEX_AUTONOMOUS_WORKFLOW.md
docs/09_SYNTHETIC_STUDENT_LAB_PLAN.md
```
