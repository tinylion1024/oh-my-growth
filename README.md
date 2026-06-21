<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth

**Growth Strategy External Brain — Claude Code, OpenClaw & Hermes Agent Plugin**

Integrating **194 Cases** · **111 Growth Plays** · **12 Schools** · **Complete Decision Framework**

Input a growth question, output: `Stage Diagnosis` · `Core Tension` · `Priority Ranking` · `Do/Don't` · `2-Week Experiment`

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-96%2F96%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[Install](#-install) · [Quick Start](#-quick-start) · [Core Frameworks](#-core-frameworks) · [Documentation](#-documentation)

**[中文文档](./README_CN.md)**

</div>

---

## 💡 What is This?

**oh-my-growth** is a **growth strategy plugin for Claude Code, OpenClaw, and Hermes Agent**.

Use it directly in your Claude Code session:

```
/omg-diagnose My DAU dropped 20%, what should I do?
/omg-assess We're planning referral, evaluate feasibility first
/omg-design How to design monetization strategy for SaaS?
```

**Shortcut**: Use `/omg` instead of `/oh-my-growth`

```
/omg-diagnose My DAU dropped 20%, what should I do?
/omg-assess We're planning referral, evaluate feasibility first
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
/omg-diagnose test installation
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
/omg-diagnose How to get first 1000 users for SaaS product
/omg-diagnose My DAU dropped 20%, what should I do?

# Opportunity assessment - evaluate if worth deeper analysis
/omg-assess Should we do referral program
/omg-assess We're planning viral growth, evaluate feasibility first

# Strategy design - actionable strategy with execution path
/omg-design How to improve monthly active user retention
/omg-design SaaS monetization strategy

# Case matching - find success cases
/omg-match Gamification to boost user activity
/omg-match Referral growth cases in education industry

# Learning path - systematic learning roadmap
/omg-learn How to systematically learn referral growth
/omg-learn Retention strategy for B2B SaaS
```

**Quick Judgment:**

```bash
# Fast scan - quick feasibility check
/omg-fast-scan Is TikTok ads worth trying for our SaaS?

# Decision BRD - full decision document for budget approval
/omg-brd Should we invest $50K in referral program
```

**Utility Commands:**

```bash
# Search knowledge base directly
/omg-search viral growth
/omg-search PLG onboarding

# Validate output document
/omg-validate report.md
```

**Scenario Shortcuts:**

```bash
# Cold start scenario
/omg-cold-start How to get first 100 seed users for AI writing SaaS

# Retention scenario
/omg-retention How to improve 30-day retention rate

# Monetization scenario
/omg-monetization How to design pricing for SaaS product

# Referral scenario
/omg-referral Should we do invitation referral
```

### Command Reference

| Command | Description | Use Case |
|---------|-------------|----------|
| `/omg-diagnose` | Diagnosis + Priority + Experiment | Growth lead needs quick judgment |
| `/omg-assess` | Evaluate if worth deeper analysis | Current state unclear, need clarity first |
| `/omg-design` | Actionable strategy | Know what to do, need execution path |
| `/omg-fast-scan` | Quick judgment | Is this idea worth pursuing? |
| `/omg-brd` | Full decision document | Need budget/resource approval |
| `/omg-match` | Find success cases | Want to see how others did it |
| `/omg-learn` | Systematic learning path | Want to deep dive into a growth area |
| `/omg-search` | Search knowledge base | Direct lookup of cases/plays/theories |
| `/omg-validate` | Validate output document | Check report completeness |
| `/omg-cold-start` | Cold start scenario | First users acquisition |
| `/omg-retention` | Retention scenario | Improve user retention |
| `/omg-monetization` | Monetization scenario | Design monetization strategy |
| `/omg-referral` | Referral scenario | Plan referral program |

### Output Views

The standalone CLI supports `operator`, `executive`, `report`, `json`, `weekly`,
`experiment-card`, `decision-memo`, and `qbr` views through `--view`.

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
| 📚 Cases | **194** | Pinduoduo, TikTok, Notion, Airbnb, GPT-4o, Claude 3.5... |
| 🛠️ Plays | **111** | Referral, PLG, Content Growth, Retention... |
| 📖 Theories | **12 Schools** | Growth Hacking, Network Effects, PLG... |

### Case Index

<!-- AUTO-CASE-INDEX:START -->
<details>
<summary>China Cases (118)</summary>

**AI Products 2025 (25)**
- [Manus AI - AI Agent Platform](<./knowledge/cases/china/ai-products-2025/manus-ai.md>) · AI Agent · Productivity
- [Monica AI - All-in-one AI Assistant](<./knowledge/cases/china/ai-products-2025/monica-ai.md>) · AI Assistant · Browser Extension
- [Tongyi Qianwen (Alibaba) - Enterprise AI](<./knowledge/cases/china/ai-products-2025/tongyi-qianwen.md>) · LLM · Enterprise AI
- [Wenxin Yiyan (Baidu) - Chinese AI Assistant](<./knowledge/cases/china/ai-products-2025/wenxin-yiyan.md>) · AI Assistant · Search
- [Kimi (Moonshot) - Long-context AI](<./knowledge/cases/china/ai-products-2025/moonshot-kimi.md>) · AI Assistant · Long Context
- [DeepSeek - Open Source AI Model](<./knowledge/cases/china/deepseek.md>) · B-tier Evidence · Open Source · Low Cost Training
- [Baichuan AI - Chinese LLM](<./knowledge/cases/china/ai-products-2025/baichuan-ai.md>) · LLM · Chinese AI
- [Zhipu AI (GLM) - Chinese LLM Unicorn](<./knowledge/cases/china/zhipu-ai.md>) · LLM · Enterprise AI
- [MiniMax - AI Product Growth](<./knowledge/cases/china/minimax-ai.md>) · AI · Video Generation
- [Doubao (ByteDance) - AI Assistant](<./knowledge/cases/china/doubao-bytedance.md>) · B-tier Evidence · AI Assistant · ByteDance Ecosystem

**New Business Models 2025 (25)**
- [TEMU Overseas - Cross-border E-commerce](<./knowledge/cases/china/new-models-2025/temu-overseas.md>) · E-commerce · Cross-border
- [TikTok Shop - Social Commerce](<./knowledge/cases/china/new-models-2025/tiktok-shop.md>) · E-commerce · Short Video
- [NIO Battery Swap - EV Innovation](<./knowledge/cases/china/new-models-2025/nio-battery-swap.md>) · EV · Battery Swap
- [Li Auto - Extended-range EV](<./knowledge/cases/china/new-models-2025/lixiang-auto.md>) · EV · Extended Range
- [XPeng Motors - Smart EV](<./knowledge/cases/china/new-models-2025/xiaopeng-auto.md>) · EV · Autonomous Driving

**Fintech (16)**
- [WeBank - Internet Bank](<./knowledge/cases/china/fintech/webank.md>) · Internet Bank · WeChat Ecosystem
- [MyBank - SME Banking](<./knowledge/cases/china/fintech/mybank.md>) · Internet Bank · SME
- [Lufax - Wealth Management](<./knowledge/cases/china/fintech/lufax.md>) · Wealth Management · P2P Transformation
- [JD Digits - Fintech Platform](<./knowledge/cases/china/fintech/jd-digits.md>) · Fintech · Digital Finance
- [Alipay - Payment Platform](<./knowledge/cases/china/alipay.md>) · B-tier Evidence · Payment · Finance

**Gaming & Entertainment (10)**
- [Genshin Impact - Open World Game](<./knowledge/cases/china/gaming/genshin-impact.md>) · Open World · Cross-platform
- [Honor of Kings - MOBA Game](<./knowledge/cases/china/gaming/honor-of-kings.md>) · MOBA · Mobile Game
- [Peace Elite - Battle Royale](<./knowledge/cases/china/gaming/peace-elite.md>) · Battle Royale · Mobile Game
- [Black Myth: Wukong - AAA Game](<./knowledge/cases/china/gaming/black-myth-wukong.md>) · AAA · Action RPG

**Healthcare (10)**
- [Ping An Doctor - Internet Healthcare](<./knowledge/cases/china/healthcare/pingan-doctor.md>) · Internet Healthcare · Telemedicine
- [JD Health - Pharmaceutical E-commerce](<./knowledge/cases/china/healthcare/jd-health.md>) · Pharmaceutical E-commerce
- [Ali Health - Pharmaceutical Platform](<./knowledge/cases/china/healthcare/ali-health.md>) · Pharmaceutical Platform

**E-commerce & Retail (9)**
- [Pinduoduo - Group Buy Growth](<./knowledge/cases/china/pinduoduo-group-buy.md>) · E-commerce · Social Referral
- [Douyin E-commerce - Live Streaming](<./knowledge/cases/china/douyin-ecommerce.md>) · E-commerce · Live Streaming
- [Xiaohongshu - Community Seeding](<./knowledge/cases/china/xiaohongshu.md>) · E-commerce · Community

**Social & Community (6)**
- [Bilibili - Community Growth](<./knowledge/cases/china/bilibili.md>) · C-tier Evidence · Social · Community · Gen Z
- [Zhihu - Knowledge Sharing](<./knowledge/cases/china/zhihu.md>) · B-tier Evidence · Social · Knowledge · Q&A

**Local Life (5)**
- [Meituan - Local Life Platform](<./knowledge/cases/china/meituan.md>) · C-tier Evidence · Local Life · Platform
- [Didi - Ride-hailing Platform](<./knowledge/cases/china/didi.md>) · B-tier Evidence · Transportation · Platform

</details>

<details>
<summary>Overseas Cases (66)</summary>

**AI Products 2025 (29)**
- [Claude 3.5 (Anthropic) - AI Assistant](<./knowledge/cases/overseas/ai-products-2025/claude-3-5.md>) · AI Assistant · Enterprise AI
- [GPT-4o (OpenAI) - Multimodal AI](<./knowledge/cases/overseas/ai-products-2025/gpt-4o.md>) · Multimodal AI · Voice
- [Gemini 2 (Google) - Multimodal AI](<./knowledge/cases/overseas/ai-products-2025/gemini-2.md>) · Multimodal AI · Search
- [Llama 3 (Meta) - Open Source LLM](<./knowledge/cases/overseas/ai-products-2025/llama-3.md>) · Open Source · LLM
- [ChatGPT (OpenAI) - Generative AI Product](<./knowledge/cases/overseas/openai-chatgpt.md>) · B-tier Evidence · AI · LLM · Consumer App
- [Midjourney - Community-driven Growth](<./knowledge/cases/overseas/midjourney.md>) · C-tier Evidence · AI · Image Generation · Discord
- [Perplexity - Answer Engine Growth](<./knowledge/cases/overseas/perplexity.md>) · B-tier Evidence · AI · Search Engine
- [Character.AI - Community Viral Growth](<./knowledge/cases/overseas/character-ai.md>) · B-tier Evidence · AI · Chatbot · Community
- [Cursor - AI Coding Tool Explosive Growth](<./knowledge/cases/overseas/cursor-ai-editor.md>) · B-tier Evidence · AI Coding · SaaS · Tool

**New Business Models 2025 (15)**
- [Figma Design - Design Collaboration](<./knowledge/cases/overseas/new-models-2025/figma-design.md>) · Design Tool · Collaboration
- [Canva Design - Design Democratization](<./knowledge/cases/overseas/new-models-2025/canva-design.md>) · Design Tool · Freemium
- [Webflow No-code - Website Builder](<./knowledge/cases/overseas/new-models-2025/webflow-nocode.md>) · No-code · Website Builder
- [Notion - Community-driven Growth](<./knowledge/cases/overseas/notion.md>) · B-tier Evidence · SaaS · Collaboration · Community

**SaaS Tools (7)**
- [Zoom - Viral Growth](<./knowledge/cases/overseas/zoom.md>) · B-tier Evidence · SaaS · Video Conference · Viral
- [Slack - Product-led Growth](<./knowledge/cases/overseas/slack.md>) · C-tier Evidence · SaaS · Collaboration · Tool
- [Dropbox - Referral Viral Growth](<./knowledge/cases/overseas/dropbox.md>) · B-tier Evidence · SaaS · Storage · Referral

**Consumer Brands (4)**
- [Glossier - Social E-commerce](<./knowledge/cases/overseas/glossier.md>) · B-tier Evidence · Beauty · DTC · Community
- [Allbirds - Word-of-mouth Growth](<./knowledge/cases/overseas/allbirds.md>) · B-tier Evidence · Shoes · DTC · Sustainable

**Transportation (3)**
- [Airbnb - Trust Mechanism Growth](<./knowledge/cases/overseas/airbnb.md>) · B-tier Evidence · Accommodation · Platform · Two-sided Market
- [Uber - Two-sided Market Growth](<./knowledge/cases/overseas/uber.md>) · B-tier Evidence · Transportation · Platform · Two-sided Market

</details>

<details>
<summary>Vertical Industry Cases (10)</summary>

- [Coursera - Online Education Growth](<./knowledge/cases/vertical/coursera.md>) · C-tier Evidence · Education · Online · MOOC
- [Duolingo - Gamified Learning Growth](<./knowledge/cases/vertical/duolingo.md>) · B-tier Evidence · Education · Gamification · Learning
- [SHAREit - Tool Overseas Expansion](<./knowledge/cases/vertical/shareit.md>) · C-tier Evidence · Tool · Overseas · Pre-install
- [SHEIN - Fast Fashion Overseas](<./knowledge/cases/vertical/shein.md>) · B-tier Evidence · Fast Fashion · Overseas · Supply Chain
- [TikTok - Overseas Growth](<./knowledge/cases/vertical/tiktok.md>) · C-tier Evidence · Short Video · Overseas · Algorithm

</details>
<!-- AUTO-CASE-INDEX:END -->


---

### Play Index

<!-- AUTO-WEAPON-INDEX:START -->
<details>
<summary>Cold Start Growth (10)</summary>

- [Manual Seed User Acquisition](<./knowledge/weapons/01-cold-start/weapons/001-手动拉种子用户.md>) · Low effort · Medium impact · C-tier Evidence
- [Cold Email/DM](<./knowledge/weapons/01-cold-start/weapons/002-冷邮件-私信.md>) · Low effort · Medium impact · C-tier Evidence
- [Deep Community Engagement](<./knowledge/weapons/01-cold-start/weapons/003-社区深度参与.md>) · Low effort · Medium impact · C-tier Evidence
- [Manual Service for First 100 Users](<./knowledge/weapons/01-cold-start/weapons/004-手动服务前100用户.md>) · Low effort · Medium impact · C-tier Evidence
- [Founder Personal IP](<./knowledge/weapons/01-cold-start/weapons/005-创始人个人IP.md>) · Medium effort · High impact · C-tier Evidence
- [Waitlist](<./knowledge/weapons/01-cold-start/weapons/006-Waitlist候补名单.md>) · Low effort · Medium impact · B-tier Evidence
- [Beta Invitation](<./knowledge/weapons/01-cold-start/weapons/007-Beta邀请制.md>) · Low effort · High impact · B-tier Evidence
- [Landing Page Registration](<./knowledge/weapons/01-cold-start/weapons/008-Landing Page注册.md>) · Medium effort · High impact · C-tier Evidence
- [Product Hunt Launch](<./knowledge/weapons/01-cold-start/weapons/009-Product Hunt发布.md>) · Medium effort · High impact · C-tier Evidence
- [Seed User Community](<./knowledge/weapons/01-cold-start/weapons/010-种子用户群.md>) · Low effort · Medium impact · C-tier Evidence

</details>

<details>
<summary>Viral & Referral (15)</summary>

- [Referral Reward System](<./knowledge/weapons/02-viral-referral/weapons/011-邀请奖励机制.md>) · Medium effort · High impact · B-tier Evidence
- [Two-sided Rewards](<./knowledge/weapons/02-viral-referral/weapons/012-双边奖励.md>) · Medium effort · High impact · A-tier Evidence
- [Share-to-Unlock Feature](<./knowledge/weapons/02-viral-referral/weapons/013-分享解锁功能.md>) · Low effort · Medium impact · C-tier Evidence
- [Share-to-Unlock Content](<./knowledge/weapons/02-viral-referral/weapons/014-分享解锁内容.md>) · High effort · High impact · A-tier Evidence
- [Referral Poster Generation](<./knowledge/weapons/02-viral-referral/weapons/015-裂变海报生成.md>) · High effort · High impact · B-tier Evidence
- [Leaderboard Sharing](<./knowledge/weapons/02-viral-referral/weapons/016-排行榜分享.md>) · Medium effort · Medium impact · C-tier Evidence
- [Group Buy Mechanism](<./knowledge/weapons/02-viral-referral/weapons/017-拼团机制.md>) · Medium effort · High impact · A-tier Evidence
- [Price Bargain Game](<./knowledge/weapons/02-viral-referral/weapons/018-砍价玩法.md>) · High effort · High impact · B-tier Evidence
- [Social Challenge](<./knowledge/weapons/02-viral-referral/weapons/019-社交挑战赛.md>) · Low effort · Medium impact · C-tier Evidence
- [Template Share Referral](<./knowledge/weapons/02-viral-referral/weapons/020-模板分享裂变.md>) · High effort · High impact · B-tier Evidence
- [AI-generated Content Sharing](<./knowledge/weapons/02-viral-referral/weapons/021-AI生成内容分享.md>) · Low effort · Medium impact · B-tier Evidence
- [Remove Watermark After Sharing](<./knowledge/weapons/02-viral-referral/weapons/022-分享后去水印.md>) · Medium effort · High impact · B-tier Evidence
- [Referral Code System](<./knowledge/weapons/02-viral-referral/weapons/023-推荐码体系.md>) · Low effort · Medium impact · C-tier Evidence
- [Invitation Leaderboard](<./knowledge/weapons/02-viral-referral/weapons/024-邀请排行榜.md>) · Medium effort · Medium impact · C-tier Evidence
- [Friend Help Unlock](<./knowledge/weapons/02-viral-referral/weapons/025-好友助力解锁.md>) · Medium effort · High impact · B-tier Evidence

</details>

<details>
<summary>Content Growth (15)</summary>

- [SEO Keyword Matrix](<./knowledge/weapons/03-content-growth/weapons/026-SEO关键词矩阵.md>) · Medium effort · High impact · B-tier Evidence
- [Programmatic SEO Pages](<./knowledge/weapons/03-content-growth/weapons/027-程序化SEO页面.md>) · Medium effort · High impact · B-tier Evidence
- [Long-tail Keyword Articles](<./knowledge/weapons/03-content-growth/weapons/028-长尾关键词文章.md>) · Medium effort · Medium impact · C-tier Evidence
- [Tutorial Content](<./knowledge/weapons/03-content-growth/weapons/029-教程型内容.md>) · High effort · High impact · C-tier Evidence
- [Industry Reports](<./knowledge/weapons/03-content-growth/weapons/030-行业报告.md>) · Medium effort · Medium impact · C-tier Evidence
- [Free Tools](<./knowledge/weapons/03-content-growth/weapons/031-免费工具.md>) · Low effort · Medium impact · C-tier Evidence
- [YouTube Tutorials](<./knowledge/weapons/03-content-growth/weapons/032-YouTube教程.md>) · High effort · High impact · B-tier Evidence
- [TikTok Matrix](<./knowledge/weapons/03-content-growth/weapons/033-TikTok矩阵.md>) · Medium effort · High impact · C-tier Evidence
- [Newsletter](<./knowledge/weapons/03-content-growth/weapons/034-Newsletter.md>) · Low effort · Medium impact · C-tier Evidence
- [Podcast](<./knowledge/weapons/03-content-growth/weapons/035-播客.md>) · High effort · High impact · B-tier Evidence
- [Guest Blogging](<./knowledge/weapons/03-content-growth/weapons/036-客座博客.md>) · Low effort · Medium impact · C-tier Evidence
- [Free E-books](<./knowledge/weapons/03-content-growth/weapons/037-免费电子书.md>) · Medium effort · Medium impact · C-tier Evidence
- [Case Studies](<./knowledge/weapons/03-content-growth/weapons/038-案例研究.md>) · Medium effort · High impact · B-tier Evidence
- [Template Library](<./knowledge/weapons/03-content-growth/weapons/039-模板资源库.md>) · Low effort · Medium impact · C-tier Evidence
- [Content Redistribution](<./knowledge/weapons/03-content-growth/weapons/040-内容再分发.md>) · Low effort · Medium impact · C-tier Evidence

</details>

<details>
<summary>Community Growth (10)</summary>

- [Discord Community](<./knowledge/weapons/04-community/weapons/041-Discord社区.md>) · High effort · High impact · C-tier Evidence
- [Slack Community](<./knowledge/weapons/04-community/weapons/042-Slack社区.md>) · Medium effort · High impact · B-tier Evidence
- [User Ambassador Program](<./knowledge/weapons/04-community/weapons/043-用户大使计划.md>) · Medium effort · Medium impact · C-tier Evidence
- [User Co-creation](<./knowledge/weapons/04-community/weapons/044-用户共创.md>) · Medium effort · High impact · B-tier Evidence
- [Offline Meetup](<./knowledge/weapons/04-community/weapons/045-线下Meetup.md>) · Medium effort · Medium impact · C-tier Evidence
- [Public User Interviews](<./knowledge/weapons/04-community/weapons/046-用户访谈公开化.md>) · Low effort · Medium impact · C-tier Evidence
- [User Story Column](<./knowledge/weapons/04-community/weapons/047-用户故事栏目.md>) · Medium effort · Medium impact · C-tier Evidence
- [Community Challenge](<./knowledge/weapons/04-community/weapons/048-社区挑战赛.md>) · Medium effort · High impact · B-tier Evidence
- [Super User Program](<./knowledge/weapons/04-community/weapons/049-超级用户计划.md>) · Low effort · Medium impact · C-tier Evidence
- [User UGC Campaign](<./knowledge/weapons/04-community/weapons/050-用户UGC活动.md>) · High effort · Medium impact · C-tier Evidence

</details>

<details>
<summary>Product-led Growth (15)</summary>

- [Freemium Model](<./knowledge/weapons/05-plg/weapons/051-Freemium模式.md>) · Medium effort · High impact · A-tier Evidence
- [Free Trial](<./knowledge/weapons/05-plg/weapons/052-免费试用.md>) · Low effort · Medium impact · B-tier Evidence
- [No-login Experience](<./knowledge/weapons/05-plg/weapons/053-无需登录体验.md>) · Medium effort · High impact · B-tier Evidence
- [Fast Onboarding](<./knowledge/weapons/05-plg/weapons/054-快速Onboarding.md>) · Medium effort · High impact · B-tier Evidence
- [In-product Guidance](<./knowledge/weapons/05-plg/weapons/055-产品内引导.md>) · Low effort · Medium impact · B-tier Evidence
- [Template Library](<./knowledge/weapons/05-plg/weapons/056-模板库.md>) · High effort · High impact · B-tier Evidence
- [Empty State Design](<./knowledge/weapons/05-plg/weapons/057-空状态设计.md>) · Low effort · Medium impact · C-tier Evidence
- [In-product Sharing](<./knowledge/weapons/05-plg/weapons/058-产品内分享.md>) · Medium effort · Medium impact · C-tier Evidence
- [Product Watermark](<./knowledge/weapons/05-plg/weapons/059-产品水印.md>) · High effort · High impact · B-tier Evidence
- [Team Collaboration](<./knowledge/weapons/05-plg/weapons/060-团队协作.md>) · High effort · High impact · B-tier Evidence
- [Usage Limit Trigger](<./knowledge/weapons/05-plg/weapons/061-使用量限制触发.md>) · Medium effort · Medium impact · C-tier Evidence
- [Result Export Viral](<./knowledge/weapons/05-plg/weapons/062-成果导出传播.md>) · Low effort · High impact · A-tier Evidence
- [Usage Report](<./knowledge/weapons/05-plg/weapons/063-使用报告.md>) · Medium effort · High impact · B-tier Evidence
- [Built-in Community Entry](<./knowledge/weapons/05-plg/weapons/064-内置社区入口.md>) · Low effort · Medium impact · C-tier Evidence
- [In-product Referral](<./knowledge/weapons/05-plg/weapons/065-产品内推荐.md>) · Medium effort · Medium impact · C-tier Evidence

</details>

<details>
<summary>Retention Growth (10)</summary>

- [Email Lifecycle](<./knowledge/weapons/06-retention/weapons/066-邮件生命周期.md>) · Low effort · Medium impact · C-tier Evidence
- [Push Notification](<./knowledge/weapons/06-retention/weapons/067-推送通知.md>) · Low effort · Medium impact · C-tier Evidence
- [Streak Rewards](<./knowledge/weapons/06-retention/weapons/068-连续使用奖励.md>) · Medium effort · High impact · B-tier Evidence
- [Milestone Notification](<./knowledge/weapons/06-retention/weapons/069-里程碑提示.md>) · Low effort · Medium impact · B-tier Evidence
- [Data Report Email](<./knowledge/weapons/06-retention/weapons/070-数据报告邮件.md>) · Medium effort · Medium impact · B-tier Evidence
- [Weekly/Monthly Report](<./knowledge/weapons/06-retention/weapons/071-周报-月报.md>) · Medium effort · Medium impact · B-tier Evidence
- [New Feature Alert](<./knowledge/weapons/06-retention/weapons/072-新功能提醒.md>) · Low effort · Medium impact · C-tier Evidence
- [User Achievement System](<./knowledge/weapons/06-retention/weapons/073-用户成就系统.md>) · Low effort · Medium impact · C-tier Evidence
- [Habit Building](<./knowledge/weapons/06-retention/weapons/074-习惯培养.md>) · Low effort · Low impact · C-tier Evidence
- [Churn Recall](<./knowledge/weapons/06-retention/weapons/075-流失召回.md>) · High effort · High impact · A-tier Evidence

</details>

<details>
<summary>Monetization Growth (10)</summary>

- [Tiered Pricing](<./knowledge/weapons/07-monetization/weapons/076-分层定价.md>) · Medium effort · Medium impact · B-tier Evidence
- [Usage-based Billing](<./knowledge/weapons/07-monetization/weapons/077-使用量计费.md>) · Medium effort · High impact · B-tier Evidence
- [Annual Discount](<./knowledge/weapons/07-monetization/weapons/078-年付折扣.md>) · Medium effort · High impact · B-tier Evidence
- [Limited-time Offer](<./knowledge/weapons/07-monetization/weapons/079-限时优惠.md>) · Medium effort · High impact · B-tier Evidence
- [Feature Upgrade Prompt](<./knowledge/weapons/07-monetization/weapons/080-功能升级提示.md>) · High effort · High impact · B-tier Evidence
- [Bundle Package](<./knowledge/weapons/07-monetization/weapons/081-捆绑套餐.md>) · Medium effort · High impact · B-tier Evidence
- [Enterprise Upgrade](<./knowledge/weapons/07-monetization/weapons/082-企业版升级.md>) · Low effort · Medium impact · C-tier Evidence
- [Add-on Plugin Market](<./knowledge/weapons/07-monetization/weapons/083-增值插件市场.md>) · Low effort · Medium impact · C-tier Evidence
- [Paid Template Market](<./knowledge/weapons/07-monetization/weapons/084-付费模板市场.md>) · Medium effort · High impact · B-tier Evidence
- [Upsell Email](<./knowledge/weapons/07-monetization/weapons/085-Upsell邮件.md>) · Medium effort · High impact · A-tier Evidence

</details>

<details>
<summary>Paid Advertising (10)</summary>

- [Google Ads](<./knowledge/weapons/08-paid-ads/weapons/086-Google Ads.md>) · Medium effort · Medium impact · B-tier Evidence
- [Facebook Ads](<./knowledge/weapons/08-paid-ads/weapons/087-Facebook Ads.md>) · Medium effort · Medium impact · B-tier Evidence
- [TikTok Ads](<./knowledge/weapons/08-paid-ads/weapons/088-TikTok Ads.md>) · High effort · High impact · B-tier Evidence
- [YouTube Ads](<./knowledge/weapons/08-paid-ads/weapons/089-YouTube Ads.md>) · High effort · High impact · B-tier Evidence
- [Retargeting Ads](<./knowledge/weapons/08-paid-ads/weapons/090-再营销广告.md>) · Low effort · Medium impact · B-tier Evidence
- [Lookalike Audience](<./knowledge/weapons/08-paid-ads/weapons/091-Lookalike人群.md>) · Low effort · Medium impact · C-tier Evidence
- [App Store Ads](<./knowledge/weapons/08-paid-ads/weapons/092-App Store Ads.md>) · Low effort · Medium impact · C-tier Evidence
- [KOL Advertising](<./knowledge/weapons/08-paid-ads/weapons/093-KOL投放.md>) · Medium effort · Medium impact · B-tier Evidence
- [Affiliate Marketing](<./knowledge/weapons/08-paid-ads/weapons/094-联盟营销.md>) · Medium effort · Medium impact · B-tier Evidence
- [Influencer Partnership](<./knowledge/weapons/08-paid-ads/weapons/095-Influencer合作.md>) · Medium effort · Medium impact · B-tier Evidence

</details>

<details>
<summary>Brand Growth (8)</summary>

- [Brand Story](<./knowledge/weapons/09-brand/weapons/096-品牌故事.md>) · Medium effort · High impact · C-tier Evidence
- [Founder IP](<./knowledge/weapons/09-brand/weapons/097-创始人IP.md>) · Low effort · High impact · B-tier Evidence
- [PR Media](<./knowledge/weapons/09-brand/weapons/098-PR媒体.md>) · Medium effort · Medium impact · C-tier Evidence
- [Industry Conference](<./knowledge/weapons/09-brand/weapons/099-行业大会.md>) · High effort · Medium impact · C-tier Evidence
- [Brand Visual Consistency](<./knowledge/weapons/09-brand/weapons/100-品牌视觉统一.md>) · Medium effort · Medium impact · B-tier Evidence
- [Signature Event](<./knowledge/weapons/09-brand/weapons/101-标志性活动.md>) · High effort · Medium impact · C-tier Evidence
- [Value-driven Marketing](<./knowledge/weapons/09-brand/weapons/102-价值观营销.md>) · High effort · Medium impact · C-tier Evidence
- [Social Issues](<./knowledge/weapons/09-brand/weapons/103-社会议题.md>) · Low effort · Medium impact · C-tier Evidence

</details>

<details>
<summary>B2B Sales (8)</summary>

- [Cold Calling](<./knowledge/weapons/10-b2b-sales/weapons/104-冷启动外呼.md>) · Medium effort · High impact · C-tier Evidence
- [LinkedIn Outreach](<./knowledge/weapons/10-b2b-sales/weapons/105-LinkedIn外联.md>) · Low effort · Medium impact · C-tier Evidence
- [Webinar](<./knowledge/weapons/10-b2b-sales/weapons/106-Webinar.md>) · Medium effort · Medium impact · C-tier Evidence
- [Demo Presentation](<./knowledge/weapons/10-b2b-sales/weapons/107-Demo演示.md>) · Medium effort · High impact · C-tier Evidence
- [Whitepaper Download](<./knowledge/weapons/10-b2b-sales/weapons/108-白皮书下载.md>) · Medium effort · Medium impact · C-tier Evidence
- [Sales Automation](<./knowledge/weapons/10-b2b-sales/weapons/109-销售自动化.md>) · Low effort · High impact · B-tier Evidence
- [Customer Success](<./knowledge/weapons/10-b2b-sales/weapons/110-客户成功.md>) · High effort · High impact · B-tier Evidence
- [Referral Program](<./knowledge/weapons/10-b2b-sales/weapons/111-转介绍计划.md>) · Low effort · High impact · B-tier Evidence

</details>

<!-- AUTO-WEAPON-INDEX:END -->


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
| Scripted Main Tests | 96/96 | ✅ |
| CLI Integration Tests | diagnose / assess / match / validate / learn | ✅ |
| Golden Scenario Regression | Wrong stage / Wrong constraint / Wrong direction | ✅ |
| Agent/Index Validation | Structure and knowledge integrity | ✅ |

---

## 🚀 Productization Status

See [`docs/optimization-status.md`](./docs/optimization-status.md) for current high-ROI optimization status and active backlog.

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
