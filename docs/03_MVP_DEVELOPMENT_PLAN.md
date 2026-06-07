# MVP 开发计划与 Codex 项目管理

最后更新：2026-06-07

## 1. 当前开发目标

使用 Codex 开发一个本地运行的 Python + Streamlit MVP，用于验证技能树学习系统是否能帮助零基础学习者掌握基础财务报表阅读。

当前目标已从“基础测试系统”升级为：

> 原子知识点 + 推理链 + 引导式学习 + 掌握验证的学习实验系统。

## 2. 技术栈

建议技术栈：

```text
Python 3.10+
Streamlit
SQLite
YAML / JSON
pandas
PyYAML
pytest
可选 OpenAI API
```

第一版不做：

```text
用户登录
支付
云部署
移动端 App
复杂前端框架
多租户系统
复杂权限系统
```

## 3. 初始项目目录建议

```text
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_PLAN.md
├── data/
│   ├── knowledge_graph.yaml
│   ├── questions.yaml
│   └── students.db
├── pages/
│   ├── 1_Pretest.py
│   ├── 2_SkillTree.py
│   ├── 3_ReasoningLesson.py
│   ├── 4_Posttest.py
│   ├── 5_Report.py
│   └── 6_Admin.py
├── src/
│   ├── db.py
│   ├── graph.py
│   ├── diagnosis.py
│   ├── scoring.py
│   ├── report.py
│   └── reasoning.py
├── analysis/
│   ├── analyze_results.py
│   └── output/
├── exports/
│   └── experiment_results.csv
└── docs/
    └── experiment_manual.md
```

## 4. 版本路线

### v0.1：基础实验原型

目标：系统能跑通基础流程。

功能：

```text
学生注册
前测
粗粒度技能树
节点学习
规则诊断
后测
报告
CSV 导出
```

验收标准：

1. 可以本地运行。
2. 一个学生能完整完成注册、前测、学习、后测、报告。
3. 数据写入 SQLite。
4. 能导出 CSV。

### v0.2：推理式学习重构版

目标：从测试系统升级为真正学习系统。

重点功能：

```text
重构 knowledge_graph.yaml
从 20 个粗节点变成约 40 个微节点
加入 5 条推理链
新增节点字段：core_question、scenario、guiding_questions、rule_summary、expected_reasoning_points
新增 ReasoningLesson 页面
记录学生自我解释
基于 expected_reasoning_points 简单判断掌握情况
```

验收标准：

1. 至少 5 条推理链可展示。
2. 每条链至少 6 个微节点。
3. 学生可以按节点学习并提交解释。
4. 系统能保存解释和判断结果。
5. 学生通过一个节点后能看到可推出的下一节点。

### v0.3：实验稳定版

目标：能让 3—10 名同学稳定完成实验。

重点功能：

```text
管理员页面
数据完整性检查
反馈问卷
学习时长统计
错因统计
导出完整实验数据
pytest 基础测试
```

验收标准：

1. 同学使用过程中不容易卡死。
2. 数据不丢失。
3. 管理员可查看所有学生进度。
4. 能导出完整分析数据。

### v0.4：数据分析与演示版

目标：支持实验分析和展示。

重点功能：

```text
分析脚本
前后测提升统计
错因统计
薄弱节点统计
学习报告示例
轻量 UI 优化
Demo 数据
```

验收标准：

1. 能生成实验总结报告。
2. 能展示系统价值。
3. 能支持创业路演或项目介绍。

## 5. Codex 使用原则

你负责：

```text
产品目标
实验设计
知识质量判断
开发任务拆分
验收标准
商业判断
```

Codex 负责：

```text
代码实现
修复 bug
重构模块
生成测试
写 README
生成分析脚本
解释代码 diff
```

Codex 不应该负责：

```text
决定商业方向
随意扩大功能范围
自动修改实验设计
自行更改知识内容逻辑
引入复杂架构
```

## 6. 每次给 Codex 的任务格式

每个任务应包含：

```text
任务标题
背景
目标
具体要求
不能做什么
验收标准
完成后需要说明什么
```

示例：

```text
任务：新增推理式学习页面 pages/3_ReasoningLesson.py

背景：当前系统更像测评系统，学习过程不足。需要让学生围绕核心问题、情境案例和引导问题进行推理式学习。

目标：实现一条完整推理链的学习流程。

要求：
1. 从 knowledge_graph.yaml 读取 chain 数据；
2. 学生选择推理链；
3. 按节点展示 core_question、scenario、guiding_questions、rule_summary、mastery_question；
4. 学生提交回答后保存；
5. 基于 expected_reasoning_points 进行简单关键词判断；
6. 通过后显示 derives 指向的下一节点。

不能做：
1. 不要删除原有前测后测功能；
2. 不要引入复杂前端；
3. 不要接入 OpenAI API；
4. 不要大规模重构数据库，除非先说明迁移方案。

验收标准：
1. 系统可以运行；
2. 能完整学习一条推理链；
3. 学生回答被保存；
4. 节点通过状态可以更新；
5. 控制台无明显报错。
```

## 7. Git 工作流

每次 Codex 修改前先 checkpoint：

```bash
git status
git add .
git commit -m "checkpoint before reasoning lesson refactor"
```

Codex 修改后：

```bash
git diff
streamlit run app.py
pytest
```

验收通过后：

```bash
git add .
git commit -m "add reasoning lesson page"
```

建议打版本 tag：

```bash
git tag v0.1
git tag v0.2
```

## 8. 当前最应该给 Codex 的任务

```text
当前项目 skilltree-finance 已经可以完成基础测试流程，但学习过程不足，知识点过粗，更像测评系统而不是真正的推理式学习系统。

现在请进行 v0.2 重构，目标是：
把知识图谱从“粗粒度知识点列表”升级为“原子知识点 + 推理链”的结构。

请先不要修改所有页面，先完成数据结构和一个最小可运行示例。

具体要求：
1. 重构 data/knowledge_graph.yaml
   - 将原来的 20 个粗节点改为更细的微知识节点。
   - 第一版先实现 5 条推理链：
     A. 从资源到资产负债表
     B. 从交易到利润表
     C. 从收付款到现金流量表
     D. 从赊销到应收账款风险
     E. 从综合数据到公司健康判断
   - 每条链至少包含 6 个微节点。
   - 总节点数量控制在 40 个左右。

2. 每个节点必须包含以下字段：
   - id
   - title
   - layer
   - chain
   - type
   - prerequisites
   - derives
   - contrasts
   - core_question
   - scenario
   - guiding_questions
   - rule_summary
   - common_misconceptions
   - mastery_question
   - expected_reasoning_points

3. 修改 src/graph.py
   - 支持读取新的节点字段。
   - 支持根据 prerequisites 查询前置节点。
   - 支持根据 derives 查询可推出的后续节点。
   - 支持按 chain 展示推理链。

4. 新增 pages/3_ReasoningLesson.py
   - 学生选择一条推理链。
   - 系统按节点顺序展示学习内容。
   - 每个节点显示：核心问题、情境案例、引导问题、规则总结、掌握验证题。
   - 学生提交回答后，保存回答。
   - 第一版使用关键词或 expected_reasoning_points 做简单判断。
   - 通过后显示“你可以推出的下一个节点”。

5. 暂时不要删除原来的测试功能。
   - 保留前测、后测、报告功能。
   - 新增推理式学习页面即可。

6. 不要做复杂 UI。
   - 重点是数据结构正确、推理链清晰、流程可跑通。

完成后请说明：
1. 修改了哪些文件；
2. 如何运行；
3. 如何测试一条完整推理链；
4. 当前实现还有哪些限制。
```

## 9. 暂缓开发事项

以下事项暂缓：

```text
复杂 UI 美化
排行榜
游戏商城
移动端 App
云部署
用户注册登录
支付
大模型深度 Agent
全学科扩展
K12 正式商业化
```

原因：当前最关键的是验证学习机制，而不是扩展功能。
