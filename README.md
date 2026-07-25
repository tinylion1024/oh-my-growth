<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# oh-my-growth — Open-Source Growth Decision Engine

**An open-source AI growth strategy tool for SEO, AEO, GEO, product growth, and AI-agent teams.**

Turn a growth question into a ranked, evidence-linked **2-week experiment** with a success signal and a stop condition—not a generic list of tactics.

**For:** growth leads, founders, product teams, and AI agents using Claude Code, OpenClaw, Hermes, or the local `growth` CLI.

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](./VERSION)
[![PyPI](https://img.shields.io/pypi/v/oh-my-growth?label=PyPI)](https://pypi.org/project/oh-my-growth/)
[![Tests](https://img.shields.io/badge/tests-99%2F99%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**[Install from PyPI](#-install)** · **[See a real command](#-quick-start)** · **[Star or fork on GitHub](https://github.com/tinylion1024/oh-my-growth)** · **[中文文档](./README_CN.md)**

</div>

---

## What is oh-my-growth?

oh-my-growth is a **growth decision-support system**, not an analytics dashboard or an autonomous ad-buying tool. It combines a versioned growth knowledge base with decision logic to help a team choose a small, testable next move.

| If you need to… | oh-my-growth returns… |
|---|---|
| Decide what to test first | A ranked set of actions with rationale and risks |
| Diagnose acquisition, retention, monetization, or referral | The stage, core tension, metric, and missing context |
| Improve SEO, AEO, or GEO / LLM discovery | A search-visibility experiment tied to a conversion goal |
| Reuse a decision in a team or agent workflow | Operator, executive, JSON, decision-memo, or public-safe share views |

**Use it when the question is “what should we validate next?”—not when you only need a dashboard of existing metrics.**

## When to use it

**When your DAU drops 20%, oh-my-growth helps you:**
1. Identify the core tension in 3 minutes
2. Get priority ranking of what to do first
3. Match 3 similar success cases
4. Generate a 2-week experiment plan

Use it inside Claude Code, OpenClaw, or Hermes Agent, or from any terminal with the standalone CLI.

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

## 📦 Install

Choose the host you already use. Each command installs the same knowledge base and decision engine.

**Fastest standalone install from PyPI:**

```bash
uv tool install oh-my-growth
growth --help
```

### Claude Code

```bash
git clone https://github.com/tinylion1024/oh-my-growth.git && cd oh-my-growth && ./scripts/install.sh --platform claude
```

### OpenClaw

```bash
git clone https://github.com/tinylion1024/oh-my-growth.git && cd oh-my-growth && ./scripts/install.sh --platform openclaw
```

### Hermes Agent

```bash
git clone https://github.com/tinylion1024/oh-my-growth.git && cd oh-my-growth && ./scripts/install.sh --platform hermes
```

### Standalone CLI

**Recommended for macOS and other developer machines — isolated install with `uv`:**

```bash
brew install uv
uv tool install oh-my-growth
growth --help
```

**Install with `pip` in a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install oh-my-growth
growth --help
```

Homebrew Python intentionally blocks global `pip install` commands (PEP 668). Use `uv` above, `pipx install oh-my-growth`, or a virtual environment instead of `--break-system-packages`.

**Get your first recommendation:**

```bash
growth diagnose "How can my SaaS get its first 1,000 users?" \
  --industry saas \
  --stage 0-1 \
  --problem acquisition
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

### Standalone CLI

Use `growth` from any terminal after installation. Add only the context you know; the tool will identify missing inputs and suggest the next experiment.

```bash
growth fast-scan "Should we test a referral loop?" \
  --industry saas \
  --stage 1-10 \
  --problem referral
```

For a complete decision report, use `growth diagnose ...`; run `growth --help` to see all commands.

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
- `share`
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

## 📊 Representative Outputs

The following are illustrative scenarios that show the expected output shape. They are **not customer outcome claims**. We are collecting anonymized, reproducible user case studies; see [how to contribute a case](./CONTRIBUTING.md#添加新案例).

### Case 1: SaaS Cold Start
**Problem:** "How to get first 1000 users for my AI writing SaaS?"

**oh-my-growth recommended:**
1. Focus on "Beta Invite" (not ads or viral growth)
2. Matched 3 cases: Notion, Calendly, Dropbox
3. 2-week experiment: Manual outreach to 50 target users

**Success signal:** acquire 3 paid customers from 50 founder-led outreach attempts

### Case 2: Retention Drop
**Problem:** "My DAU dropped 20% after product update"

**oh-my-growth diagnosed:**
1. Core tension: Feature confusion, not product quality
2. Priority: Re-engage power users > Rollback features
3. Matched case: Slack's onboarding improvement

**Success signal:** improve D7 retention before scaling acquisition

### Case 3: Monetization Strategy
**Problem:** "How to design pricing for my B2B SaaS?"

**oh-my-growth designed:**
1. Three-tier pricing: Free → Pro ($29) → Enterprise ($299)
2. Matched cases: Notion, Linear, Slack
3. Key principle: Free tier for PLG, Pro tier for revenue

**Success signal:** validate willingness to pay and retention guardrails before rollout

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

### Does it replace product analytics, a BI tool, or a growth team?

No. Bring the metrics, constraints, and prior experiment history you already have. oh-my-growth helps turn that context into a decision, an experiment design, and explicit success and stop signals.

### Can I use it without an AI-agent host?

Yes. Install the PyPI package and use `growth diagnose`, `growth design`, `growth fast-scan`, or `growth search` from a terminal. Claude Code, OpenClaw, and Hermes are additional integration surfaces, not prerequisites.

### Why does this help SEO and GEO?

The repository exposes searchable keywords, explicit command references, canonical docs, and an AI-readable `llms.txt` entry point so agents and LLMs can understand what the project does. For Google-style search, GEO/AEO work still depends on crawlable, useful, well-structured SEO content.

---

## 🌟 Community

- **Star the repository** if evidence-backed growth decisions are useful to your team; it makes the project easier for other builders to discover.
- **Fork it** if you want to add a vertical knowledge base, adapt the decision logic, or integrate a new agent host; the project is MIT-licensed.
- **GitHub Issues:** report a bug, request a case, or propose an improvement.
- **GitHub Discussions:** share a use case or compare implementation notes.
- **Case contributions:** add an anonymized, evidence-backed case via the [contribution guide](./CONTRIBUTING.md).
- **Twitter/X:** [@ohmygrowth](https://twitter.com/ohmygrowth).

---

## 📈 Roadmap

For current priorities and how to influence them, see the [public roadmap](./docs/ROADMAP.md).

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

**[Install from PyPI](#-install)** · **[Read Full Docs](./docs/)** · **[Contribute a case](./CONTRIBUTING.md)** · **[Star or fork on GitHub](https://github.com/tinylion1024/oh-my-growth)**

Made with ❤️ by Growth Master Team

</div>
