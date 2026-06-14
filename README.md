<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth

**Growth Strategy External Brain — Claude Code, OpenClaw & Hermes Agent Plugin**

Integrating **81 Cases** · **111 Growth Plays** · **12 Schools** · **Complete Decision Framework**

Input a growth question, output: `Stage Diagnosis` · `Core Tension` · `Priority Ranking` · `Do/Don't` · `2-Week Experiment`

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-84%2F84%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[Install](#-install) · [Quick Start](#-quick-start) · [Core Frameworks](#-core-frameworks) · [Documentation](#-documentation)

**[中文文档](./README_CN.md)**

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

**Shortcut**: Use `/omg` instead of `/oh-my-growth`

```
/omg diagnose My DAU dropped 20%, what should I do?
/omg assess We're planning referral, evaluate feasibility first
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
cd oh-my-growth
./scripts/install.sh
```

### Option 2: Manual Install

```bash
# Clone repository
git clone https://github.com/tinylion1024/oh-my-growth.git

# Install to Claude Code skills directory
cp -R oh-my-growth ~/.claude/skills/oh-my-growth
```

### Verify Installation

In Claude Code, type:
```
/oh-my-growth diagnose test installation
```

### Install to OpenClaw

oh-my-growth also supports **OpenClaw**:

```bash
# Clone repository
git clone https://github.com/tinylion1024/oh-my-growth.git

# Install to OpenClaw skills directory
cp -R oh-my-growth/openclaw ~/.openclaw/skills/oh-my-growth
cp -R oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.openclaw/skills/oh-my-growth/

# Install Python dependencies
pip install -r oh-my-growth/requirements.txt
```

See [openclaw/INSTALL.md](./openclaw/INSTALL.md) for detailed OpenClaw installation guide.

### Install to Hermes Agent

oh-my-growth also supports **Hermes Agent**:

```bash
# Clone repository
git clone https://github.com/tinylion1024/oh-my-growth.git

# Install to Hermes skills directory
mkdir -p ~/.hermes/skills/oh-my-growth
cp -R oh-my-growth/hermes/SKILL.md ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/knowledge ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.hermes/skills/oh-my-growth/

# Install Python dependencies
pip install -r oh-my-growth/requirements.txt
```

See [hermes/INSTALL.md](./hermes/INSTALL.md) for detailed Hermes Agent installation guide.

---

## ✨ Quick Start

### Use in Claude Code

**Core Commands:**

```bash
# Strategy diagnosis - diagnose growth problems with priority ranking
/omg diagnose How to get first 1000 users for SaaS product
/omg diagnose My DAU dropped 20%, what should I do?

# Opportunity assessment - evaluate if worth deeper analysis
/omg assess Should we do referral program
/omg assess We're planning viral growth, evaluate feasibility first

# Strategy design - actionable strategy with execution path
/omg design How to improve monthly active user retention
/omg design SaaS monetization strategy

# Case matching - find success cases
/omg match Gamification to boost user activity
/omg match Referral growth cases in education industry

# Learning path - systematic learning roadmap
/omg learn How to systematically learn referral growth
/omg learn Retention strategy for B2B SaaS
```

**Quick Judgment:**

```bash
# Fast scan - quick feasibility check
/omg fast-scan Is TikTok ads worth trying for our SaaS?

# Decision BRD - full decision document for budget approval
/omg brd Should we invest $50K in referral program
```

**Utility Commands:**

```bash
# Search knowledge base directly
/omg search viral growth
/omg search PLG onboarding

# Validate output document
/omg validate report.md
```

**Scenario Shortcuts:**

```bash
# Cold start scenario
/omg cold-start How to get first 100 seed users for AI writing SaaS

# Retention scenario
/omg retention How to improve 30-day retention rate

# Monetization scenario
/omg monetization How to design pricing for SaaS product

# Referral scenario
/omg referral Should we do invitation referral
```

### Command Reference

| Command | Description | Use Case |
|---------|-------------|----------|
| `diagnose` | Diagnosis + Priority + Experiment | Growth lead needs quick judgment |
| `assess` | Evaluate if worth deeper analysis | Current state unclear, need clarity first |
| `design` | Actionable strategy | Know what to do, need execution path |
| `fast-scan` | Quick judgment | Is this idea worth pursuing? |
| `brd` | Full decision document | Need budget/resource approval |
| `match` | Find success cases | Want to see how others did it |
| `learn` | Systematic learning path | Want to deep dive into a growth area |
| `search` | Search knowledge base | Direct lookup of cases/plays/theories |
| `validate` | Validate output document | Check report completeness |
| `cold-start` | Cold start scenario | First users acquisition |
| `retention` | Retention scenario | Improve user retention |
| `monetization` | Monetization scenario | Design monetization strategy |
| `referral` | Referral scenario | Plan referral program |

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

## 🎯 Knowledge Base Scale

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

<div align="center">

**Built with ❤️ by Growth Master Team**

[⬆ Back to Top](#-oh-my-growth)

</div>
