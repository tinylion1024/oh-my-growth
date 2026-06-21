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
<summary>中国案例（43）</summary>

- [B站-社区氛围增长](<./knowledge/cases/china/bilibili.md>) · C级证据 · 社交、社区、Z世代
- [DeepSeek（深度求索）- AI开源突围战](<./knowledge/cases/china/deepseek.md>) · B级证据 · 开源模型、低成本训练、viral增长
- [Kimi（月之暗面）- AI助手爆发式增长](<./knowledge/cases/china/kimi-moonshot-ai.md>) · B级证据 · AI助手、免费获客、内容营销
- [MiniMax（海螺AI/稀宇科技）- AI产品爆发式增长](<./knowledge/cases/china/minimax-ai.md>) · C级证据 · AI陪伴、视频生成、免费获客
- [Soul-匿名社交增长](<./knowledge/cases/china/soul.md>) · C级证据 · 社交、灵魂匹配、匿名
- [云集-社交电商裂变](<./knowledge/cases/china/yunji.md>) · C级证据 · 电商、B2B、跨境
- [京东-用户精细化运营](<./knowledge/cases/china/jd-member-ops.md>) · B级证据 · 电商、会员体系、用户运营
- [京东家具双11投放案例：ROI达到252](<./knowledge/cases/china/jd-furniture-roi252.md>) · C级证据
- [京东金融-金条白条增长](<./knowledge/cases/china/jd-finance.md>) · C级证据 · 金融、白条、金条
- [唯品会-特卖模式增长](<./knowledge/cases/china/vipshop.md>) · C级证据 · 电商、特卖、库存
- [夸克AI（阿里巴巴）- 超级入口的AI突围](<./knowledge/cases/china/quark-ai.md>) · C级证据 · AI助手、超级入口、阿里生态
- [小红书-社区种草转化](<./knowledge/cases/china/xiaohongshu.md>) · C级证据 · 电商、种草、社区
- [少儿英语产品用户洞察案例](<./knowledge/cases/china/child-english-insight.md>) · C级证据 · 教育、用户洞察、增长方法
- [得物-潮流社区增长](<./knowledge/cases/china/dewu.md>) · B级证据 · 电商、潮牌、社区
- [微众银行-互联网银行增长](<./knowledge/cases/china/webank.md>) · C级证据 · 金融、互联网银行、微信生态
- [微信支付-红包裂变](<./knowledge/cases/china/wechat-pay.md>) · B级证据 · 支付、社交、红包
- [微信红包-社交裂变增长](<./knowledge/cases/china/wechat-redpacket.md>) · C级证据 · 支付、社交裂变、红包
- [快手极速版-看视频赚现金](<./knowledge/cases/china/kuaishou-jisu-ban.md>) · C级证据 · 短视频、游戏化、现金激励
- [快手白拿-现金膨胀裂变增长](<./knowledge/cases/china/kuaishou-baina.md>) · C级证据 · 现金激励、邀请裂变、金币暴涨
- [抖音-算法推荐增长](<./knowledge/cases/china/douyin-algorithm.md>) · C级证据 · 社交、算法推荐、短视频
- [抖音支付-电商金融](<./knowledge/cases/china/douyin-pay.md>) · C级证据 · 支付、电商、抖音生态
- [抖音极速版-看视频赚金币](<./knowledge/cases/china/douyin-jisu-ban.md>) · C级证据 · 短视频、游戏化、金币激励
- [抖音电商-直播带货爆发](<./knowledge/cases/china/douyin-ecommerce.md>) · C级证据 · 电商、短视频、兴趣电商
- [拼多多-拼团裂变增长](<./knowledge/cases/china/pinduoduo-group-buy.md>) · C级证据 · 电商、社交裂变、拼团
- [携程-旅游平台增长](<./knowledge/cases/china/ctrip.md>) · C级证据 · 旅游、OTA、平台
- [支付宝-支付增长](<./knowledge/cases/china/alipay.md>) · B级证据 · 支付、金融、场景
- [智谱AI（Z.ai/GLM）——中国大模型独角兽的差异化成长之路](<./knowledge/cases/china/zhipu-ai.md>) · C级证据 · 大模型、基础模型、MaaS平台
- [桌面Widget增长案例](<./knowledge/cases/china/widget-growth.md>) · C级证据 · Widget、桌面美化、社交货币
- [淘宝直播-内容电商转型](<./knowledge/cases/china/taobao-live.md>) · C级证据 · 电商、直播、内容电商
- [滴滴-出行平台增长](<./knowledge/cases/china/didi.md>) · B级证据 · 出行、平台、双边市场
- [白拿送礼-社交裂变增长](<./knowledge/cases/china/white-get-gift.md>) · C级证据 · 社交裂变、免费获客、送礼
- [知乎-知识分享增长](<./knowledge/cases/china/zhihu.md>) · B级证据 · 社交、知识、问答
- [秘塔AI搜索 - AI搜索赛道的差异化突围](<./knowledge/cases/china/mita-ai-search.md>) · C级证据 · AI搜索、无广告、深度研究
- [美团-本地生活平台增长](<./knowledge/cases/china/meituan.md>) · C级证据 · 本地生活、平台、外卖
- [腾讯元宝（Tencent Yuanbao）- AI to C 的生态攻坚战](<./knowledge/cases/china/tencent-yuanbao.md>) · C级证据 · AI助手、腾讯生态、微信嵌入
- [芭芭农场-游戏化增长](<./knowledge/cases/china/baba-farm.md>) · C级证据 · 游戏化、养成、社交裂变
- [蚂蚁森林-用户粘性增长](<./knowledge/cases/china/ant-forest.md>) · B级证据 · 金融、游戏化、公益
- [豆包（字节跳动）- 互联网巨头的AI助手增长](<./knowledge/cases/china/doubao-bytedance.md>) · B级证据 · AI助手、免费获客、字节生态
- [贝壳-居住平台增长](<./knowledge/cases/china/beike.md>) · B级证据 · 居住、平台、经纪人
- [趣头条-看新闻赚金币](<./knowledge/cases/china/qutoutiao.md>) · C级证据 · 资讯、游戏化、金币激励
- [银发人群增长-视频奖励与任务体系](<./knowledge/cases/china/silver-hair-growth.md>) · C级证据 · 银发经济、看视频赚钱、任务体系
- [陌陌-陌生社交增长](<./knowledge/cases/china/momo.md>) · B级证据 · 社交、直播、陌生人社交
- [饿了么-外卖平台增长](<./knowledge/cases/china/ele.md>) · B级证据 · 本地生活、外卖、平台

</details>

<details>
<summary>海外案例（28）</summary>

- [Airbnb-信任机制增长](<./knowledge/cases/overseas/airbnb.md>) · B级证据 · 住宿、平台、双边市场
- [Airbnb-房源增长策略](<./knowledge/cases/overseas/airbnb-host.md>) · C级证据 · 住宿、房东、平台
- [Allbirds-口碑增长](<./knowledge/cases/overseas/allbirds.md>) · B级证据 · 鞋、DTC、可持续
- [Anthropic/Claude — AI助手产品增长案例](<./knowledge/cases/overseas/claude-anthropic.md>) · B级证据 · AI、大语言模型、企业级AI
- [Calendly-工具产品增长](<./knowledge/cases/overseas/calendly.md>) · B级证据 · 工具、日程、预约
- [Character.AI-社区裂变增长](<./knowledge/cases/overseas/character-ai.md>) · B级证据 · AI、对话机器人、社区
- [Cursor - AI编程工具爆发式增长](<./knowledge/cases/overseas/cursor-ai-editor.md>) · B级证据 · AI编程、SaaS、工具
- [Dollar Shave Club-订阅电商](<./knowledge/cases/overseas/dollar-shave-club.md>) · C级证据 · 订阅、DTC、剃须刀
- [DoorDash-外卖平台增长](<./knowledge/cases/overseas/doordash.md>) · B级证据 · 外卖、平台、本地生活
- [Dropbox-推荐裂变增长](<./knowledge/cases/overseas/dropbox.md>) · B级证据 · SaaS、存储、邀请裂变
- [ElevenLabs — AI语音合成产品增长案例](<./knowledge/cases/overseas/elevenlabs-ai.md>) · B级证据 · AI语音、生成式AI、企业级AI
- [GitHub Copilot — AI编程工具市场开创者与增长](<./knowledge/cases/overseas/github-copilot.md>) · B级证据 · AI编程、SaaS、B2D
- [Glossier-社交电商](<./knowledge/cases/overseas/glossier.md>) · B级证据 · 美妆、DTC、社区
- [HubSpot-入站营销增长](<./knowledge/cases/overseas/hubspot.md>) · C级证据 · SaaS、营销自动化、入站营销
- [Midjourney-社区驱动增长](<./knowledge/cases/overseas/midjourney.md>) · C级证据 · AI、图像生成、Discord社区
- [Notion-社区驱动增长](<./knowledge/cases/overseas/notion.md>) · B级证据 · SaaS、协作、社区
- [OpenAI/ChatGPT-生成式AI产品增长](<./knowledge/cases/overseas/openai-chatgpt.md>) · B级证据 · AI、大语言模型、消费应用
- [Perplexity-答案引擎增长](<./knowledge/cases/overseas/perplexity.md>) · B级证据 · AI、搜索引擎、答案引擎
- [Pika AI-社区+产品驱动增长](<./knowledge/cases/overseas/pika-ai.md>) · C级证据 · AI、视频生成、Discord社区
- [Runway AI-内容生态驱动增长](<./knowledge/cases/overseas/runway-ai.md>) · C级证据 · AI、视频生成、影视合作
- [Slack-产品驱动增长](<./knowledge/cases/overseas/slack.md>) · C级证据 · SaaS、协作、工具
- [Stripe-开发者生态增长](<./knowledge/cases/overseas/stripe.md>) · B级证据 · 支付、开发者、API
- [Suno — AI音乐生成产品增长案例](<./knowledge/cases/overseas/suno-music-ai.md>) · B级证据 · AI音乐、生成式AI、消费级AI
- [Uber-双边市场增长](<./knowledge/cases/overseas/uber.md>) · B级证据 · 出行、平台、双边市场
- [Warby Parker-眼镜直销](<./knowledge/cases/overseas/warby-parker.md>) · B级证据 · 眼镜、DTC、Home Try-On
- [Windsurf - AI编程工具差异化增长](<./knowledge/cases/overseas/windsurf-ai-editor.md>) · C级证据 · AI编程、SaaS、工具
- [Zoom-病毒式增长](<./knowledge/cases/overseas/zoom.md>) · B级证据 · SaaS、视频会议、病毒传播
- [海外银发奖励平台-Swagbucks/InboxDollars](<./knowledge/cases/overseas/silver-hair-reward-platforms.md>) · C级证据 · 任务墙、积分奖励、银发用户

</details>

<details>
<summary>垂直行业案例（10）</summary>

- [Coursera-在线教育增长](<./knowledge/cases/vertical/coursera.md>) · C级证据 · 教育、在线、MOOC
- [Duolingo-游戏化学习增长](<./knowledge/cases/vertical/duolingo.md>) · B级证据 · 教育、游戏化、学习
- [SHAREit（茄子快传）-工具出海](<./knowledge/cases/vertical/shareit.md>) · C级证据 · 工具、出海、预装
- [SHEIN-快时尚出海](<./knowledge/cases/vertical/shein.md>) · B级证据 · 快时尚、出海、供应链
- [TikTok-海外增长](<./knowledge/cases/vertical/tiktok.md>) · C级证据 · 短视频、出海、算法推荐
- [VIPKID-少儿英语增长](<./knowledge/cases/vertical/vipkid.md>) · B级证据 · 教育、英语、在线
- [字节跳动-海外产品矩阵](<./knowledge/cases/vertical/bytedance-overseas.md>) · B级证据 · 互联网、出海、产品矩阵
- [猿辅导-题库产品增长](<./knowledge/cases/vertical/yuanfudao.md>) · B级证据 · 教育、在线、英语
- [腾讯游戏-出海增长](<./knowledge/cases/vertical/tencent-games.md>) · C级证据 · 游戏、出海、投资
- [跨境电商独立站-品牌出海](<./knowledge/cases/vertical/dtc-brand.md>) · C级证据 · 跨境、DTC、独立站

</details>

<!-- AUTO-CASE-INDEX:END -->

### Play Index

<!-- AUTO-WEAPON-INDEX:START -->
<details>
<summary>冷启动增长（10）</summary>

- [手动拉种子用户](<./knowledge/weapons/01-cold-start/weapons/001-手动拉种子用户.md>) · Low effort · Medium impact · C级证据
- [冷邮件/私信](<./knowledge/weapons/01-cold-start/weapons/002-冷邮件-私信.md>) · Low effort · Medium impact · C级证据
- [社区深度参与](<./knowledge/weapons/01-cold-start/weapons/003-社区深度参与.md>) · Low effort · Medium impact · C级证据
- [手动服务前100用户](<./knowledge/weapons/01-cold-start/weapons/004-手动服务前100用户.md>) · Low effort · Medium impact · C级证据
- [创始人个人IP](<./knowledge/weapons/01-cold-start/weapons/005-创始人个人IP.md>) · Medium effort · High impact · C级证据
- [Waitlist候补名单](<./knowledge/weapons/01-cold-start/weapons/006-Waitlist候补名单.md>) · Low effort · Medium impact · B级证据
- [Beta邀请制](<./knowledge/weapons/01-cold-start/weapons/007-Beta邀请制.md>) · Low effort · High impact · B级证据
- [Landing Page注册](<./knowledge/weapons/01-cold-start/weapons/008-Landing Page注册.md>) · Medium effort · High impact · C级证据
- [Product Hunt发布](<./knowledge/weapons/01-cold-start/weapons/009-Product Hunt发布.md>) · Medium effort · High impact · C级证据
- [种子用户群](<./knowledge/weapons/01-cold-start/weapons/010-种子用户群.md>) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>病毒裂变（15）</summary>

- [邀请奖励机制](<./knowledge/weapons/02-viral-referral/weapons/011-邀请奖励机制.md>) · Medium effort · High impact · B级证据
- [双边奖励](<./knowledge/weapons/02-viral-referral/weapons/012-双边奖励.md>) · Medium effort · High impact · A级证据
- [分享解锁功能](<./knowledge/weapons/02-viral-referral/weapons/013-分享解锁功能.md>) · Low effort · Medium impact · C级证据
- [分享解锁内容](<./knowledge/weapons/02-viral-referral/weapons/014-分享解锁内容.md>) · High effort · High impact · A级证据
- [裂变海报生成](<./knowledge/weapons/02-viral-referral/weapons/015-裂变海报生成.md>) · High effort · High impact · B级证据
- [排行榜分享](<./knowledge/weapons/02-viral-referral/weapons/016-排行榜分享.md>) · Medium effort · Medium impact · C级证据
- [拼团机制](<./knowledge/weapons/02-viral-referral/weapons/017-拼团机制.md>) · Medium effort · High impact · A级证据
- [砍价玩法](<./knowledge/weapons/02-viral-referral/weapons/018-砍价玩法.md>) · High effort · High impact · B级证据
- [社交挑战赛](<./knowledge/weapons/02-viral-referral/weapons/019-社交挑战赛.md>) · Low effort · Medium impact · C级证据
- [模板分享裂变](<./knowledge/weapons/02-viral-referral/weapons/020-模板分享裂变.md>) · High effort · High impact · B级证据
- [AI生成内容分享](<./knowledge/weapons/02-viral-referral/weapons/021-AI生成内容分享.md>) · Low effort · Medium impact · B级证据
- [分享后去水印](<./knowledge/weapons/02-viral-referral/weapons/022-分享后去水印.md>) · Medium effort · High impact · B级证据
- [推荐码体系](<./knowledge/weapons/02-viral-referral/weapons/023-推荐码体系.md>) · Low effort · Medium impact · C级证据
- [邀请排行榜](<./knowledge/weapons/02-viral-referral/weapons/024-邀请排行榜.md>) · Medium effort · Medium impact · C级证据
- [好友助力解锁](<./knowledge/weapons/02-viral-referral/weapons/025-好友助力解锁.md>) · Medium effort · High impact · B级证据

</details>

<details>
<summary>内容增长（15）</summary>

- [SEO关键词矩阵](<./knowledge/weapons/03-content-growth/weapons/026-SEO关键词矩阵.md>) · Medium effort · High impact · B级证据
- [程序化SEO页面](<./knowledge/weapons/03-content-growth/weapons/027-程序化SEO页面.md>) · Medium effort · High impact · B级证据
- [长尾关键词文章](<./knowledge/weapons/03-content-growth/weapons/028-长尾关键词文章.md>) · Medium effort · Medium impact · C级证据
- [教程型内容](<./knowledge/weapons/03-content-growth/weapons/029-教程型内容.md>) · High effort · High impact · C级证据
- [行业报告](<./knowledge/weapons/03-content-growth/weapons/030-行业报告.md>) · Medium effort · Medium impact · C级证据
- [免费工具](<./knowledge/weapons/03-content-growth/weapons/031-免费工具.md>) · Low effort · Medium impact · C级证据
- [YouTube教程](<./knowledge/weapons/03-content-growth/weapons/032-YouTube教程.md>) · High effort · High impact · B级证据
- [TikTok矩阵](<./knowledge/weapons/03-content-growth/weapons/033-TikTok矩阵.md>) · Medium effort · High impact · C级证据
- [Newsletter](<./knowledge/weapons/03-content-growth/weapons/034-Newsletter.md>) · Low effort · Medium impact · C级证据
- [播客](<./knowledge/weapons/03-content-growth/weapons/035-播客.md>) · High effort · High impact · B级证据
- [客座博客](<./knowledge/weapons/03-content-growth/weapons/036-客座博客.md>) · Low effort · Medium impact · C级证据
- [免费电子书](<./knowledge/weapons/03-content-growth/weapons/037-免费电子书.md>) · Medium effort · Medium impact · C级证据
- [案例研究](<./knowledge/weapons/03-content-growth/weapons/038-案例研究.md>) · Medium effort · High impact · B级证据
- [模板资源库](<./knowledge/weapons/03-content-growth/weapons/039-模板资源库.md>) · Low effort · Medium impact · C级证据
- [内容再分发](<./knowledge/weapons/03-content-growth/weapons/040-内容再分发.md>) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>社区增长（10）</summary>

- [Discord社区](<./knowledge/weapons/04-community/weapons/041-Discord社区.md>) · High effort · High impact · C级证据
- [Slack社区](<./knowledge/weapons/04-community/weapons/042-Slack社区.md>) · Medium effort · High impact · B级证据
- [用户大使计划](<./knowledge/weapons/04-community/weapons/043-用户大使计划.md>) · Medium effort · Medium impact · C级证据
- [用户共创](<./knowledge/weapons/04-community/weapons/044-用户共创.md>) · Medium effort · High impact · B级证据
- [线下Meetup](<./knowledge/weapons/04-community/weapons/045-线下Meetup.md>) · Medium effort · Medium impact · C级证据
- [用户访谈公开化](<./knowledge/weapons/04-community/weapons/046-用户访谈公开化.md>) · Low effort · Medium impact · C级证据
- [用户故事栏目](<./knowledge/weapons/04-community/weapons/047-用户故事栏目.md>) · Medium effort · Medium impact · C级证据
- [社区挑战赛](<./knowledge/weapons/04-community/weapons/048-社区挑战赛.md>) · Medium effort · High impact · B级证据
- [超级用户计划](<./knowledge/weapons/04-community/weapons/049-超级用户计划.md>) · Low effort · Medium impact · C级证据
- [用户UGC活动](<./knowledge/weapons/04-community/weapons/050-用户UGC活动.md>) · High effort · Medium impact · C级证据

</details>

<details>
<summary>产品驱动增长（15）</summary>

- [Freemium模式](<./knowledge/weapons/05-plg/weapons/051-Freemium模式.md>) · Medium effort · High impact · A级证据
- [免费试用](<./knowledge/weapons/05-plg/weapons/052-免费试用.md>) · Low effort · Medium impact · B级证据
- [无需登录体验](<./knowledge/weapons/05-plg/weapons/053-无需登录体验.md>) · Medium effort · High impact · B级证据
- [快速Onboarding](<./knowledge/weapons/05-plg/weapons/054-快速Onboarding.md>) · Medium effort · High impact · B级证据
- [产品内引导](<./knowledge/weapons/05-plg/weapons/055-产品内引导.md>) · Low effort · Medium impact · B级证据
- [模板库](<./knowledge/weapons/05-plg/weapons/056-模板库.md>) · High effort · High impact · B级证据
- [空状态设计](<./knowledge/weapons/05-plg/weapons/057-空状态设计.md>) · Low effort · Medium impact · C级证据
- [产品内分享](<./knowledge/weapons/05-plg/weapons/058-产品内分享.md>) · Medium effort · Medium impact · C级证据
- [产品水印](<./knowledge/weapons/05-plg/weapons/059-产品水印.md>) · High effort · High impact · B级证据
- [团队协作](<./knowledge/weapons/05-plg/weapons/060-团队协作.md>) · High effort · High impact · B级证据
- [使用量限制触发](<./knowledge/weapons/05-plg/weapons/061-使用量限制触发.md>) · Medium effort · Medium impact · C级证据
- [成果导出传播](<./knowledge/weapons/05-plg/weapons/062-成果导出传播.md>) · Low effort · High impact · A级证据
- [使用报告](<./knowledge/weapons/05-plg/weapons/063-使用报告.md>) · Medium effort · High impact · B级证据
- [内置社区入口](<./knowledge/weapons/05-plg/weapons/064-内置社区入口.md>) · Low effort · Medium impact · C级证据
- [产品内推荐](<./knowledge/weapons/05-plg/weapons/065-产品内推荐.md>) · Medium effort · Medium impact · C级证据

</details>

<details>
<summary>留存增长（10）</summary>

- [邮件生命周期](<./knowledge/weapons/06-retention/weapons/066-邮件生命周期.md>) · Low effort · Medium impact · C级证据
- [推送通知](<./knowledge/weapons/06-retention/weapons/067-推送通知.md>) · Low effort · Medium impact · C级证据
- [连续使用奖励](<./knowledge/weapons/06-retention/weapons/068-连续使用奖励.md>) · Medium effort · High impact · B级证据
- [里程碑提示](<./knowledge/weapons/06-retention/weapons/069-里程碑提示.md>) · Low effort · Medium impact · B级证据
- [数据报告邮件](<./knowledge/weapons/06-retention/weapons/070-数据报告邮件.md>) · Medium effort · Medium impact · B级证据
- [周报/月报](<./knowledge/weapons/06-retention/weapons/071-周报-月报.md>) · Medium effort · Medium impact · B级证据
- [新功能提醒](<./knowledge/weapons/06-retention/weapons/072-新功能提醒.md>) · Low effort · Medium impact · C级证据
- [用户成就系统](<./knowledge/weapons/06-retention/weapons/073-用户成就系统.md>) · Low effort · Medium impact · C级证据
- [习惯培养](<./knowledge/weapons/06-retention/weapons/074-习惯培养.md>) · Low effort · Low impact · C级证据
- [流失召回](<./knowledge/weapons/06-retention/weapons/075-流失召回.md>) · High effort · High impact · A级证据

</details>

<details>
<summary>变现增长（10）</summary>

- [分层定价](<./knowledge/weapons/07-monetization/weapons/076-分层定价.md>) · Medium effort · Medium impact · B级证据
- [使用量计费](<./knowledge/weapons/07-monetization/weapons/077-使用量计费.md>) · Medium effort · High impact · B级证据
- [年付折扣](<./knowledge/weapons/07-monetization/weapons/078-年付折扣.md>) · Medium effort · High impact · B级证据
- [限时优惠](<./knowledge/weapons/07-monetization/weapons/079-限时优惠.md>) · Medium effort · High impact · B级证据
- [功能升级提示](<./knowledge/weapons/07-monetization/weapons/080-功能升级提示.md>) · High effort · High impact · B级证据
- [捆绑套餐](<./knowledge/weapons/07-monetization/weapons/081-捆绑套餐.md>) · Medium effort · High impact · B级证据
- [企业版升级](<./knowledge/weapons/07-monetization/weapons/082-企业版升级.md>) · Low effort · Medium impact · C级证据
- [增值插件市场](<./knowledge/weapons/07-monetization/weapons/083-增值插件市场.md>) · Low effort · Medium impact · C级证据
- [付费模板市场](<./knowledge/weapons/07-monetization/weapons/084-付费模板市场.md>) · Medium effort · High impact · B级证据
- [Upsell邮件](<./knowledge/weapons/07-monetization/weapons/085-Upsell邮件.md>) · Medium effort · High impact · A级证据

</details>

<details>
<summary>付费广告（10）</summary>

- [Google Ads](<./knowledge/weapons/08-paid-ads/weapons/086-Google Ads.md>) · Medium effort · Medium impact · B级证据
- [Facebook Ads](<./knowledge/weapons/08-paid-ads/weapons/087-Facebook Ads.md>) · Medium effort · Medium impact · B级证据
- [TikTok Ads](<./knowledge/weapons/08-paid-ads/weapons/088-TikTok Ads.md>) · High effort · High impact · B级证据
- [YouTube Ads](<./knowledge/weapons/08-paid-ads/weapons/089-YouTube Ads.md>) · High effort · High impact · B级证据
- [再营销广告](<./knowledge/weapons/08-paid-ads/weapons/090-再营销广告.md>) · Low effort · Medium impact · B级证据
- [Lookalike人群](<./knowledge/weapons/08-paid-ads/weapons/091-Lookalike人群.md>) · Low effort · Medium impact · C级证据
- [App Store Ads](<./knowledge/weapons/08-paid-ads/weapons/092-App Store Ads.md>) · Low effort · Medium impact · C级证据
- [KOL投放](<./knowledge/weapons/08-paid-ads/weapons/093-KOL投放.md>) · Medium effort · Medium impact · B级证据
- [联盟营销](<./knowledge/weapons/08-paid-ads/weapons/094-联盟营销.md>) · Medium effort · Medium impact · B级证据
- [Influencer合作](<./knowledge/weapons/08-paid-ads/weapons/095-Influencer合作.md>) · Medium effort · Medium impact · B级证据

</details>

<details>
<summary>品牌增长（8）</summary>

- [品牌故事](<./knowledge/weapons/09-brand/weapons/096-品牌故事.md>) · Medium effort · High impact · C级证据
- [创始人IP](<./knowledge/weapons/09-brand/weapons/097-创始人IP.md>) · Low effort · High impact · B级证据
- [PR媒体](<./knowledge/weapons/09-brand/weapons/098-PR媒体.md>) · Medium effort · Medium impact · C级证据
- [行业大会](<./knowledge/weapons/09-brand/weapons/099-行业大会.md>) · High effort · Medium impact · C级证据
- [品牌视觉统一](<./knowledge/weapons/09-brand/weapons/100-品牌视觉统一.md>) · Medium effort · Medium impact · B级证据
- [标志性活动](<./knowledge/weapons/09-brand/weapons/101-标志性活动.md>) · High effort · Medium impact · C级证据
- [价值观营销](<./knowledge/weapons/09-brand/weapons/102-价值观营销.md>) · High effort · Medium impact · C级证据
- [社会议题](<./knowledge/weapons/09-brand/weapons/103-社会议题.md>) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>B2B销售（8）</summary>

- [冷启动外呼](<./knowledge/weapons/10-b2b-sales/weapons/104-冷启动外呼.md>) · Medium effort · High impact · C级证据
- [LinkedIn外联](<./knowledge/weapons/10-b2b-sales/weapons/105-LinkedIn外联.md>) · Low effort · Medium impact · C级证据
- [Webinar](<./knowledge/weapons/10-b2b-sales/weapons/106-Webinar.md>) · Medium effort · Medium impact · C级证据
- [Demo演示](<./knowledge/weapons/10-b2b-sales/weapons/107-Demo演示.md>) · Medium effort · High impact · C级证据
- [白皮书下载](<./knowledge/weapons/10-b2b-sales/weapons/108-白皮书下载.md>) · Medium effort · Medium impact · C级证据
- [销售自动化](<./knowledge/weapons/10-b2b-sales/weapons/109-销售自动化.md>) · Low effort · High impact · B级证据
- [客户成功](<./knowledge/weapons/10-b2b-sales/weapons/110-客户成功.md>) · High effort · High impact · B级证据
- [转介绍计划](<./knowledge/weapons/10-b2b-sales/weapons/111-转介绍计划.md>) · Low effort · High impact · B级证据

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
