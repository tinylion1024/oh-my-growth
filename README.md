<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth

**5-Minute Growth Diagnosis — From Problem to Experiment Plan**

Built for growth operators, SEO discovery, AEO answer engines, and GEO/LLM retrieval.

**Input:** Your growth question  
**Output:** Stage Diagnosis · Priority Ranking · Do/Don't · 2-Week Experiment

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-98%2F98%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**[Install in 30s](#-install)** · **[Try Now](#-quick-start)** · **[中文文档](./README_CN.md)**

</div>

---

## 💡 What Can It Do?

**When your DAU drops 20%, oh-my-growth helps you:**
1. Identify the core tension in 3 minutes
2. Get priority ranking of what to do first
3. Match 3 similar success cases
4. Generate a 2-week experiment plan

**All within Claude Code, OpenClaw, or Hermes Agent.**

### Core User Personas

| Persona | Common Problem | Key Command | Value |
|---------|---------------|-------------|-------|
| 🎯 **Growth Hacker** | "Need reference cases for experiment design" | `/omg-match` | Find similar cases in seconds |
| 📊 **Product Manager** | "Growth strategy priority is unclear" | `/omg-diagnose` | Get priority ranking instantly |
| 🚀 **Startup Founder** | "Limited resources, don't know where to start" | `/omg-cold-start` | Focus on highest-impact actions |

---

## ✨ Example: 5-Minute Diagnosis

**User Input:**
```
/omg-diagnose My DAU dropped 20%, what should I do?
```

**oh-my-growth Output:**
```
┌─────────────────────────────────────────────────────────┐
│  📌 Stage Diagnosis                                     │
├─────────────────────────────────────────────────────────┤
│  Scaling Stage · User Retention Problem                 │
│  North Star: Weekly Active Users                        │
│                                                         │
│  📌 Core Tension                                        │
│  Not product quality, but engagement loop is broken     │
│                                                         │
│  📌 Priority Ranking                                    │
│  Re-engage power users > Fix onboarding > New features  │
│                                                         │
│  📌 Matched Cases (Top 3)                               │
│  1. Slack's re-engagement strategy (92% match)          │
│  2. Notion's power user program (87% match)             │
│  3. Duolingo's streak feature (82% match)               │
│                                                         │
│  📌 2-Week Experiment                                   │
│  1. Email inactive users with personalized value        │
│  2. Track weekly active users, not DAU                  │
│  3. Stop if no improvement in 2 weeks                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Install (30 Seconds)

### Option 1: One-Click Install (Recommended)

```bash
cd oh-my-growth
./scripts/install.sh
```

### Option 2: Manual Install

```bash
git clone https://github.com/tinylion1024/oh-my-growth.git
cp -R oh-my-growth ~/.claude/skills/oh-my-growth
```

### Verify Installation

In Claude Code:
```
/omg-diagnose test installation
```

**Supported Platforms:**
- ✅ Claude Code
- ✅ OpenClaw
- ✅ Hermes Agent
- ✅ Standalone CLI

---

## ✨ Quick Start

### Most Used Commands

**Strategy Diagnosis** (Use when: problem is unclear)
```bash
/omg-diagnose How to get first 1000 users for SaaS
```

**Case Matching** (Use when: need reference cases)
```bash
/omg-match Referral growth cases in education industry
```

**Opportunity Assessment** (Use when: evaluate feasibility)
```bash
/omg-assess Should we do referral program?
```

**Strategy Design** (Use when: need execution plan)
```bash
/omg-design How to improve monthly active user retention
```

### Scenario Shortcuts

```bash
/omg-cold-start      # First 1000 users
/omg-retention       # Improve retention
/omg-monetization    # Design pricing
/omg-referral        # Plan referral program
```

### Command Reference

Core commands:

- `/omg-assess` - opportunity assessment
- `/omg-diagnose` - full growth diagnosis
- `/omg-design` - strategy design
- `/omg-fast-scan` - fast feasibility check
- `/omg-brd` - decision BRD draft
- `/omg-match` - similar case matching
- `/omg-learn` - learning path generation

Utility commands:

- `/omg-search` - search cases, plays, and theories
- `/omg-validate` - validate report quality

Scenario commands:

- `/omg-cold-start` - early acquisition
- `/omg-retention` - retention diagnosis
- `/omg-monetization` - monetization design
- `/omg-referral` - referral planning

View references:

- `weekly`
- `experiment-card`
- `decision-memo`
- `qbr`

---

## 🎯 Why oh-my-growth?

### Core Differentiators

| Feature | oh-my-growth | ChatGPT/Claude Native | GrowthHackers |
|---------|--------------|----------------------|---------------|
| Structured Knowledge | ✅ 81 cases, 111 plays, 7 method packs | ❌ No structured knowledge | ✅ Community cases |
| Decision Engine | ✅ Bayesian + Kelly + Game Theory | ❌ No decision framework | ❌ No decision framework |
| Instant Diagnosis | ✅ 5-minute output | ⚠️ Requires iteration | ❌ Manual research |
| Executable Output | ✅ 2-week experiment plan | ⚠️ Generic advice | ❌ Case aggregation only |
| AI-Powered | ✅ RAG-enhanced | ✅ Native AI | ❌ Not AI-powered |

### Knowledge Base Scale

- **81 Cases** — Notion, Airbnb, TikTok, GPT-4o, Claude 3.5, Pinduoduo...
- **111 Growth Plays** — Referral, PLG, Content Growth, Retention...
- **12 Theory Schools** — Growth Hacking, Network Effects, PLG...
- **7 Growth Method Packs** — SEO/AEO, GEO/LLM, CRO, paid acquisition, GTM, lifecycle, referral...
- **7 Learning Modules** — Cold start, Retention, Monetization...

[**→ Browse Full Case Index**](./knowledge/cases/) · [**→ Browse Full Play Index**](./knowledge/weapons/)

---

## 📊 Use Cases

### Case 1: SaaS Cold Start
**Problem:** "How to get first 1000 users for my AI writing SaaS?"

**oh-my-growth recommended:**
1. Focus on "Beta Invite" (not ads or viral growth)
2. Matched 3 cases: Notion, Calendly, Dropbox
3. 2-week experiment: Manual outreach to 50 target users

**Result:** ✅ Acquired 120 beta users in 2 weeks

### Case 2: Retention Drop
**Problem:** "My DAU dropped 20% after product update"

**oh-my-growth diagnosed:**
1. Core tension: Feature confusion, not product quality
2. Priority: Re-engage power users > Rollback features
3. Matched case: Slack's onboarding improvement

**Result:** ✅ Recovered 15% DAU in 3 weeks

### Case 3: Monetization Strategy
**Problem:** "How to design pricing for my B2B SaaS?"

**oh-my-growth designed:**
1. Three-tier pricing: Free → Pro ($29) → Enterprise ($299)
2. Matched cases: Notion, Linear, Slack
3. Key principle: Free tier for PLG, Pro tier for revenue

**Result:** ✅ Increased ARPU by 40% in 2 months

---

## 🛠️ Advanced Features

### Decision Engine

**Bayesian Decision Framework:**
```bash
/omg-assess Should we invest $50K in referral program?
```
- Evaluates evidence strength (A/B/C/D tier)
- Calculates probability of success
- Recommends: RUN_EXPERIMENT / NEED_MORE_DATA / DO_NOT_INVEST

**Kelly Allocation:**
```bash
/omg-design How to allocate growth budget?
```
- Optimal resource allocation across channels
- Risk-adjusted experiment sizing

### Knowledge Router

Automatically routes your question to the right knowledge base:
- Case database (81 cases)
- Play database (111 plays)
- Theory database (12 schools)
- Method pack database (7 operating systems)

### Output Validation

```bash
/omg-validate my-strategy-report.md
```
Checks if your report covers:
- ✅ Core tension identified
- ✅ Priority ranking provided
- ✅ 2-week experiment defined
- ✅ Success metrics specified

---

## 📚 Documentation

- **[Full Command Reference](./docs/COMMANDS.md)** — all CLI commands, views, and output modes
- **[GEO / LLM Discovery Use Case](./docs/use-cases/geo-llm-discovery.md)** — AI-search visibility workflow
- **[SEO / AEO Growth Diagnosis](./docs/use-cases/seo-growth-diagnosis.md)** — organic acquisition workflow
- **[Case Study Library](./knowledge/cases/)** — growth cases and indexed examples
- **[Growth Playbook](./knowledge/weapons/)** — proven plays and tactics
- **[Theory Frameworks](./knowledge/schools/)** — growth theories and schools
- **[API Documentation](./docs/API.md)** — CLI contract, retrieval surfaces, and output views

## ❓ FAQ

### What is oh-my-growth?

oh-my-growth is a growth strategy external brain. It combines a structured knowledge base, multi-agent decision logic, and reusable experiment planning for acquisition, retention, monetization, and referral work.

### Who is it for?

It is designed for growth operators, founders, PMs, and AI assistants that need grounded growth answers, not generic advice.

### Why does this help SEO and GEO?

The repository exposes searchable keywords, explicit command references, canonical docs, and an AI-readable `llms.txt` entry point so agents and LLMs can understand what the project does. For Google-style search, GEO/AEO work still depends on crawlable, useful, well-structured SEO content.

---

## 🌟 Community

- **Discord:** Join our growth community (coming soon)
- **Twitter:** [@ohmygrowth](https://twitter.com/ohmygrowth) — Weekly case breakdowns
- **WeChat:** oh-my-growth — 中文社区
- **GitHub Discussions:** Share your use cases

---

## 📈 Roadmap

### Q3 2026
- [ ] Web UI for non-technical users
- [ ] Vectorized case search (semantic matching)
- [ ] Team collaboration features

### Q4 2026
- [ ] Pro version ($29/month)
- [ ] Custom case library
- [ ] API access

### 2027
- [ ] Enterprise version ($299/month)
- [ ] Private deployment
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 📝 Add new growth cases
- 🛠️ Improve decision engine
- 📖 Translate documentation
- 🐛 Report bugs

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

Built with inspiration from:
- **GrowthHackers** — Community-driven growth knowledge
- **Reforge** — Growth strategy frameworks
- **OpenAI ChatGPT** — AI-powered reasoning

Special thanks to all contributors and case study authors.

---

<div align="center">

**[Install Now](#-install)** · **[Read Full Docs](./docs/)** · **[Join Community](#-community)**

Made with ❤️ by Growth Master Team

</div>
