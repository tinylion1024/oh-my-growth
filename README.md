<div align="center">

# 🚀 oh-my-growth

**Growth Strategy External Brain — Claude Code Plugin**

Integrating **81 Cases** · **111 Growth Plays** · **12 Schools** · **Complete Decision Framework**

Input a growth question, output: `Stage Diagnosis` · `Core Tension` · `Priority Ranking` · `Do/Don't` · `2-Week Experiment`

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-84%2F84%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[Install](#-install) · [Quick Start](#-quick-start) · [Core Frameworks](#-core-frameworks) · [Documentation](#-documentation)

**[中文文档](#-oh-my-growth---增长策略外脑)**

</div>

---

## 💡 What is This?

**oh-my-growth** is a **Claude Code plugin for growth strategy decisions**.

Use it directly in your Claude Code session:

```
/oh-my-growth diagnose My DAU dropped 20%, what should I do?
/oh-my-growth assess We're planning referral, evaluate feasibility first
/oh-my-growth design How to design monetization strategy for SaaS?
```

It first determines:

- Which growth stage you're in (validation / scaling / optimization)
- Whether the problem is user acquisition or user engagement
- What your North Star metric should be
- What to focus on and what to avoid

Then outputs actionable recommendations:

- 🎯 **Diagnose Growth Problems** — Identify core tension, stage constraints, and priorities
- 📋 **Validate Decision Docs** — Check if reports cover key sections, fact markers, and action loops
- 🛠️ **Output Strategy Plans** — What to do, what not to do, which experiment to run first
- 📚 **Match Success Cases** — Who has done similar things? How did they do it?
- 🔢 **Form Executable Judgments** — Backed by evidence, cases, and lightweight decision engines

---

## 📦 Install

### Option 1: One-Click Install (Recommended)

```bash
cd growth-master-skill
./scripts/install.sh
```

### Option 2: Manual Install

```bash
# Clone repository
git clone https://github.com/tinylion1024/growth-master-skill.git

# Install to Claude Code skills directory
cp -R growth-master-skill ~/.claude/skills/oh-my-growth
```

### Verify Installation

In Claude Code, type:
```
/oh-my-growth diagnose test installation
```

---

## ✨ Quick Start

### Use in Claude Code

```
/oh-my-growth diagnose How to get first 1000 users for SaaS product
/oh-my-growth assess Should we do referral program
/oh-my-growth design How to improve monthly active user retention
/oh-my-growth match Gamification to boost user activity
/oh-my-growth learn How to systematically learn referral growth
```

### CLI Mode (Standalone)

```bash
# Strategy brain diagnosis
python scripts/cli.py diagnose "How to get first 1000 users for SaaS" \
  --industry saas --stage 0-1 --problem acquisition

# Scenario shortcut
python scripts/cli.py cold-start "How to get first 100 seed users for AI writing SaaS" \
  --industry saas
```

### Sample Output:

```
┌─────────────────────────────────────────────────────────┐
│  📌 Stage Diagnosis                                     │
├─────────────────────────────────────────────────────────┤
│  Validation Stage · User Acquisition                    │
│  North Star: New high-intent users                      │
│                                                         │
│  📌 One-Liner Judgment                                  │
│  Recommend small experiment: Bet on "Beta Invite"       │
│                                                         │
│  📌 Core Tension                                        │
│  Not lack of channels, but no replicable low-cost path  │
│                                                         │
│  📌 Priority Ranking                                    │
│  Beta Invite > Landing Page > Product Hunt Launch       │
│                                                         │
│  📌 2-Week Experiment                                   │
│  1. Validate one action only                            │
│  2. Track new high-intent users                         │
│  3. Stop if hypothesis fails                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Features

### Seven Entry Points

| Mode | CLI Entry | Description | Use Case |
|------|-----------|-------------|----------|
| **Strategy Brain** | `diagnose` | Diagnosis + Priority + Experiment | Growth lead needs quick judgment |
| **Opportunity Assess** | `assess` | Evaluate if worth deeper analysis | Current state unclear, need clarity first |
| **Strategy Design** | `design` | Actionable strategy | Know what to do, need execution path |
| **Fast Scan** | `fast-scan` | Quick judgment | Is this idea worth pursuing? |
| **Decision BRD** | `brd` | Full decision document | Need budget/resource approval |
| **Case Match** | `match` | Find success cases | Want to see how others did it |
| **Learning Path** | `learn` | Systematic learning path | Want to deep dive into a growth area |

### Knowledge Base Scale

| Type | Count | Description |
|------|-------|-------------|
| 📚 Cases | **81** | Pinduoduo, TikTok, Notion, Airbnb... |
| 🛠️ Plays | **111** | Referral, PLG, Content Growth, Retention... |
| 📖 Theories | **12 Schools** | Growth Hacking, Network Effects, PLG... |

---

## 🧭 Core Frameworks

The project organizes strategy judgment around a complete growth operating framework:

- First determine: `Product Validation / Growth Scaling / Scale Optimization`
- Then determine: `User Acquisition` or `User Engagement`
- Then define: `North Star Metric` and `Constraints`
- Finally: Cases, plays, theories, and experiment recommendations

### Quality Assurance

| Mechanism | Purpose |
|-----------|---------|
| ✅ **Current State Clarity Gate** | Ask follow-up questions when information is insufficient |
| ✅ **Evidence Tier System** | A/B/C/D/E five-level confidence, transparent labeling |
| ✅ **Safety Boundary Detection** | Auto-identify financial/legal/regulatory risks |
| ✅ **Output Contract** | 10 required sections, ensure report completeness |

---

## 🔢 Bayesian Decision Engine

### What is Bayesian Decision?

Converts uncertain growth decisions into an **auditable probabilistic reasoning process**:

```
Initial Hypothesis → Set Prior → Collect Evidence → Update Posterior → Compare Threshold → Recommend Action
```

### Action Thresholds

| Posterior Range | Decision | Description |
|-----------------|----------|-------------|
| ≥ 75% | **Invest Now** | High confidence, actionable |
| 50-75% | **Run Experiment** | Medium confidence, needs validation |
| 30-50% | **Collect Evidence** | Low confidence, insufficient info |
| < 30% | **Stop** | Very low confidence, not recommended |

### Evidence Tiers

| Tier | Definition | Update Magnitude |
|------|------------|------------------|
| A | Meta-analysis, systematic reviews | ±25% |
| B | Peer-reviewed, industry reports | ±15% |
| C | Expert opinions, internal data | ±10% |
| D | LLM suggestions, analogies | ±5% |
| E | Blogs, marketing copy | 0% |

---

## 📊 Kelly Allocation Framework

### What is Kelly Criterion?

Calculate optimal investment ratio, answering "how much resource to invest":

```
f* = (bp - q) / b

f* = Optimal investment fraction
b  = Net odds (profit/loss)
p  = Win probability
q  = Loss probability
```

### Action Package Output

```yaml
kelly_result:
  fraction: "15% budget"
  action: "Launch referral MVP"
  budget: "$15K"
  add_condition: "K-factor > 0.5 → Scale to $30K"
  stop_condition: "CAC > $10 → Stop"
  review: "Review in 30 days"
```

---

## 🏗️ Architecture Overview

```
User Input
    │
    ▼
┌─────────────────┐
│ Lead Agent      │ ← Orchestration, problem classification
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│知识   │ │ 决策  │
│ Agent │ │ Agent │
│ 群    │ │ 群    │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
┌─────────────────┐
│ Narrative Agent │ ← Output generation
└─────────────────┘
```

**Knowledge Agents**: Case · Weapon · Theory · Competitor

**Decision Agents**: Growth · Monetization · ROI · Execution · Skeptic

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](./SKILL.md) | Complete skill definition |
| [Growth Operating Framework](./references/growth-operating-framework.md) | Stage, North Star, Journey, Strategy Loop |
| [Bayesian Decision](./references/bayesian-decision.md) | Probabilistic reasoning framework |
| [Game Theory Framework](./references/gametheory-framework.md) | Competitive analysis, equilibrium prediction |
| [Kelly Allocation](./references/kelly-allocation.md) | Resource investment optimization |

---

## 🧪 Test Coverage

```bash
# Run main test suite
python3 scripts/run_tests.py

# Run CLI integration tests only
python3 -m pytest tests/test_cli_integration.py

# Validate agents and indexes
python3 scripts/validate-agents.py
python3 scripts/validate-indexes.py
```

| Test Type | Coverage | Status |
|-----------|----------|--------|
| Scripted Main Tests | 84/84 | ✅ |
| CLI Integration Tests | diagnose / assess / match / validate / learn | ✅ |
| Golden Scenario Regression | Wrong stage / Wrong constraint / Wrong direction | ✅ |
| Agent/Index Validation | Structure and knowledge integrity | ✅ |

---

## 🤝 Contributing

Contributions welcome!

- 📝 Submit new cases (see `knowledge/cases/` format)
- 🛠️ Add growth plays (see `knowledge/weapons/` format)
- 🐛 Report issues (open an Issue)
- 💡 Feature suggestions (open an Issue or PR)

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

<br/>
<br/>
<hr/>

<div align="center">

# 🚀 oh-my-growth - 增长策略外脑

**Claude Code 专用增长决策插件**

整合 **81个案例** · **111种玩法** · **12大流派** · **完整决策框架**

输入一个增长问题，直接输出：
`阶段判断` · `核心矛盾` · `优先级排序` · `建议做/别做` · `两周实验`

[安装](#-安装) · [快速开始](#-快速开始) · [核心框架](#-核心框架) · [文档](#-文档)

**[English](#-oh-my-growth)**

</div>

---

## 💡 这是什么？

**oh-my-growth** 是一个**Claude Code 专用增长决策插件**。

在 Claude Code 会话中，你可以直接调用专业的增长策略分析能力：

```
/oh-my-growth diagnose 我的产品日活下降20%，该怎么办？
/oh-my-growth assess 我们准备做裂变，先评估可行性
/oh-my-growth design SaaS产品如何设计变现策略？
```

它会先判断：

- 你现在到底处于哪个增长阶段
- 主问题更偏用户获取还是用户深耕
- 当前最该围绕哪个北极星指标
- 应该先做什么，不该分散到什么方向

然后再给出可执行输出：

- 🎯 **诊断增长问题** — 先判断主矛盾、阶段约束和优先级
- 📋 **校验决策文档** — 检查报告是否覆盖关键章节、事实标记和行动闭环
- 🛠️ **输出策略方案** — 建议做什么、先别做什么、先做哪一个实验
- 📚 **匹配成功案例** — 谁做过类似的事？怎么做到的？
- 🔢 **形成可执行判断** — 用证据、案例和轻量决策引擎支撑结论

---

## 📦 安装

### 方式一：一键安装（推荐）

```bash
cd growth-master-skill
./scripts/install.sh
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/growth-master-skill.git

# 安装到 Claude Code skills 目录
cp -R growth-master-skill ~/.claude/skills/oh-my-growth
```

### 验证安装

在 Claude Code 中输入：
```
/oh-my-growth diagnose 测试安装
```

---

## ✨ 快速开始

### 在 Claude Code 中使用

```
/oh-my-growth diagnose SaaS产品如何获取首批用户
/oh-my-growth assess 我们要不要做邀请裂变
/oh-my-growth design 如何提升月活跃用户留存率
/oh-my-growth match 游戏化提升用户活跃
/oh-my-growth learn 如何系统学习裂变增长
```

### CLI 模式（独立使用）

```bash
# 策略外脑诊断
python scripts/cli.py diagnose "SaaS产品如何获取首批1000用户" \
  --industry saas --stage 0-1 --problem acquisition

# 场景化快捷入口
python scripts/cli.py cold-start "AI写作SaaS如何拿到前100个种子用户" \
  --industry saas
```

### 输出示例：

```
┌─────────────────────────────────────────────────────────┐
│  📌 阶段判断                                            │
├─────────────────────────────────────────────────────────┤
│  产品验证期 · 用户获取                                  │
│  北极星：新增高意向用户数                               │
│                                                         │
│  📌 一句话判断                                          │
│  推荐小规模实验：冷启动阶段先押注「Beta邀请制」           │
│                                                         │
│  📌 核心矛盾                                            │
│  不是渠道不够多，而是还没找到可复制的低成本主路径         │
│                                                         │
│  📌 优先级排序                                          │
│  Beta邀请制 > Landing Page注册 > Product Hunt发布       │
│                                                         │
│  📌 两周实验                                            │
│  1. 只验证一个动作                                      │
│  2. 追踪新增高意向用户数                                 │
│  3. 不成立就停止扩预算                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 核心功能

### 七个核心入口

| 模式 | CLI 入口 | 一句话描述 | 适用场景 |
|------|----------|-----------|----------|
| **Strategy Brain** | `diagnose` | 诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| **Opportunity Assess** | `assess` | 先判断能不能进入策略分析 | 现状还不够清楚，先做清晰度与方向评估 |
| **Strategy Design** | `design` | 可落地的策略 | 知道要做什么，但不知道怎么设计执行路径 |
| **Fast Scan** | `fast-scan` | 快速判断 | 这个想法靠谱吗？ |
| **Decision BRD** | `brd` | 完整决策文档 | 需要申请预算/资源 |
| **Case Match** | `match` | 找成功案例 | 想看看别人怎么做的 |
| **Learning Path** | `learn` | 系统学习路径 | 想深入了解某个增长领域 |

### 知识库规模

| 类型 | 数量 | 说明 |
|------|------|------|
| 📚 案例 | **81个** | 拼多多、抖音、Notion、Airbnb... |
| 🛠️ 玩法 | **111种** | 裂变、PLG、内容增长、留存... |
| 📖 理论 | **12流派** | 增长黑客、网络效应、PLG... |

---

## 🧭 核心框架

项目现在默认按一套更完整的增长经营框架组织策略判断：

- 先判断当前处于 `产品验证期 / 增长放大期 / 规模经营期`
- 再判断主问题属于 `用户获取` 还是 `用户深耕`
- 再定义当前最该围绕的 `北极星指标` 与 `约束线`
- 最后才进入案例、玩法、理论和实验建议

### 质量保障

| 机制 | 作用 |
|------|------|
| ✅ **现状清晰度门控** | 信息不足时主动追问，避免盲目诊断 |
| ✅ **证据分级系统** | A/B/C/D/E 五级可信度，透明标注 |
| ✅ **安全边界检测** | 自动识别财务/法律/监管风险 |
| ✅ **输出契约** | 10 个必选章节，确保报告完整 |

---

## 🔢 贝叶斯决策引擎

### 什么是贝叶斯决策？

将不确定的增长决策转化为**可审计的概率推理过程**：

```
初始假设 → 设置先验概率 → 收集证据 → 更新后验概率 → 比较阈值 → 推荐行动
```

### 行动阈值

| 后验范围 | 决策 | 说明 |
|----------|------|------|
| ≥ 75% | **直接投入** | 高置信度，可执行 |
| 50-75% | **小实验** | 中等置信度，需验证 |
| 30-50% | **收集证据** | 低置信度，信息不足 |
| < 30% | **停止** | 极低置信度，不推荐 |

### 证据等级

| 等级 | 定义 | 更新幅度 |
|------|------|---------|
| A | 元分析、系统综述 | ±25% |
| B | 同行评审、行业报告 | ±15% |
| C | 专家意见、内部数据 | ±10% |
| D | LLM建议、类比 | ±5% |
| E | 博客、营销文案 | 0% |

---

## 📊 Kelly 资源分配框架

### 什么是 Kelly 准则？

计算最优投入比例，回答"应该投入多少资源"：

```
f* = (bp - q) / b

f* = 最优投入比例
b  = 净赔率（盈利/亏损）
p  = 胜率
q  = 失败概率
```

### 行动包输出

```yaml
kelly_result:
  fraction: "15% 预算"
  action: "启动邀请裂变 MVP"
  budget: "15万"
  add_condition: "病毒系数 > 0.5 → 加仓到 30万"
  stop_condition: "CAC > 80元 → 停止"
  review: "30天后复盘"
```

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 完整技能定义 |
| [增长操作框架](./references/growth-operating-framework.md) | 阶段、北极星、旅程、策略环 |
| [贝叶斯决策](./references/bayesian-decision.md) | 概率推理框架 |
| [博弈论框架](./references/gametheory-framework.md) | 竞争分析、均衡预测 |
| [Kelly分配](./references/kelly-allocation.md) | 资源投入优化 |

---

## 🧪 测试覆盖

```bash
# 运行主测试集
python3 scripts/run_tests.py

# 单独跑 CLI 集成测试
python3 -m pytest tests/test_cli_integration.py
```

| 测试类型 | 覆盖 | 状态 |
|----------|------|------|
| 脚本化主测试 | 84/84 | ✅ |
| CLI 集成测试 | diagnose / assess / match / validate / learn | ✅ |
| Golden 场景回归 | 错阶段 / 错约束 / 错方向 | ✅ |

---

## 🤝 贡献

欢迎贡献！

- 📝 提交新案例（参考 `knowledge/cases/` 格式）
- 🛠️ 补充增长玩法（参考 `knowledge/weapons/` 格式）
- 🐛 报告问题（提 Issue）
- 💡 功能建议（提 Issue 或 PR）

---

## 📄 License

MIT License - 自由使用、修改、分发

---

<div align="center">

**Built with ❤️ by Growth Master Team**

[⬆ Back to Top](#-oh-my-growth)

</div>
