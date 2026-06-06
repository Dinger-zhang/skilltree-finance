# skilltree-finance

AI 技能树财务报表学习实验系统。本项目是一个本地运行的 Python + Streamlit 教育实验 MVP，用于帮助零基础学生学习基础财务报表知识，并记录前测、学习过程、后测和学习报告。

## 环境约定

本项目使用的 conda 环境名称为：

```bash
skilltree
```

如果本地还没有该环境，可以创建：

```bash
conda create -n skilltree python=3.10
conda activate skilltree
pip install -r requirements.txt
```

如果环境已经存在，直接激活并安装依赖：

```bash
conda activate skilltree
pip install -r requirements.txt
```

## 功能

- 学生信息登记：姓名、学号、班级
- 前测答题：记录学生基础水平
- 技能树学习：按前置关系逐步解锁 20 个财务报表学习节点
- 学习日志：记录进入系统、提交测试、完成节点、保存笔记等行为
- 后测答题：记录学习后的测评结果
- 学习报告：展示前后测成绩、节点完成进度、答题明细和学习日志

## 项目结构

```text
skilltree-finance/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── knowledge_graph.yaml
│   └── questions.yaml
└── src/
    ├── __init__.py
    ├── content.py
    └── database.py
```

说明：

- `app.py`：Streamlit 主入口
- `src/content.py`：加载 YAML 内容
- `src/database.py`：SQLite 初始化和数据读写
- `data/knowledge_graph.yaml`：20 个财务报表学习节点
- `data/questions.yaml`：前测和后测题目

## 本地运行

在项目根目录执行：

```bash
conda activate skilltree
pip install -r requirements.txt
streamlit run app.py
```

然后在浏览器中打开 Streamlit 提供的本地地址，通常是：

```text
http://localhost:8501
```

## 数据存储

项目使用本地 SQLite，不接入真实登录、支付、云服务或外部数据库。

首次运行后会自动生成本地数据库文件：

```text
data/skilltree_finance.sqlite3
```

该数据库文件属于本地运行数据，默认不会提交到 GitHub。

SQLite 表包括：

- `students`：学生信息
- `answers`：前测和后测答题记录
- `node_status`：学习节点状态
- `learning_logs`：学习过程日志

## 学习节点

当前版本包含 20 个财务报表学习节点，覆盖：

- 财务报表三件套
- 会计恒等式
- 资产、负债、所有者权益
- 收入、费用、净利润
- 现金流量表
- 权责发生制与现金制
- 折旧与摊销
- 营运资本
- 毛利率、流动比率、资产负债率、ROE
- 三张报表勾稽关系
- 基础分析流程和风险信号

## 开发原则

- 保持本地优先，便于课堂实验和快速迭代
- 保持代码简单、可读、可扩展
- 教学内容使用 YAML 管理，便于后续扩充节点和题目
- 数据层集中在 SQLite 模块中，便于后续替换或迁移
