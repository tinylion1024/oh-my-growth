<div align="center">

# 🚀 Growth Master

**增长策略外脑 — 替增长负责人完成前 70% 的策略思考**

整合 **81个案例** · **111种玩法** · **12大流派** · **13个专业Agent** · **完整决策框架**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-22%2F22%20scripted%20checks-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[快速开始](#-快速开始) · [核心框架](#-核心框架) · [文档](#-文档)

</div>

---

## 💡 这是什么？

**Growth Master** 是一个**面向增长行业人的策略外脑 skill**。

你可以把它理解为：**一个读过 81 个增长案例、掌握 111 种增长打法，并能先做诊断再给方案的增长外脑**，帮你：

- 🎯 **诊断增长问题** — 先判断主矛盾、阶段约束和优先级
- 📋 **校验决策文档** — 检查报告是否覆盖关键章节、事实标记和行动闭环
- 🛠️ **输出策略方案** — 建议做什么、先别做什么、先做哪一个实验
- 📚 **匹配成功案例** — 谁做过类似的事？怎么做到的？
- 🔢 **形成可执行判断** — 用证据、案例和轻量决策引擎支撑结论

---

## ✨ 30 秒演示

### 场景：SaaS 产品如何获取首批用户？

```bash
# 方式一：策略外脑诊断
python scripts/cli.py diagnose "SaaS产品如何获取首批1000用户" \
  --industry saas --stage 0-1 --problem acquisition

# 方式二：场景化快捷入口
python scripts/cli.py cold-start "AI写作SaaS如何拿到前100个种子用户" \
  --industry saas

# 方式三：在 Claude Code 中
/growth-master-skill assess 我们是一个AI写作SaaS，想获取首批种子用户

# 方式四：负责人摘要视图
python scripts/cli.py diagnose "SaaS产品如何获取首批1000用户" \
  --industry saas --stage 0-1 --problem acquisition --view executive
```

### 输出示例：

```
┌─────────────────────────────────────────────────────────┐
│  📌 一句话判断                                          │
├─────────────────────────────────────────────────────────┤
│  推荐小规模实验：冷启动阶段先押注「Beta邀请制」           │
│  置信度：中（先验证能否稳定拿到高意向种子用户）            │
│                                                         │
│  核心矛盾：                                              │
│  不是渠道不够多，而是还没找到可复制的低成本主路径         │
│                                                         │
│  优先级排序：Beta邀请制 > 竞品用户转化 > KOL试用          │
│                                                         │
│  两周实验：                                              │
│  1. 只验证一个动作                                      │
│  2. 追踪新增高意向用户数                                 │
│  3. 不成立就停止扩预算                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 核心功能

### 五大模式，覆盖从诊断到执行建议

| 模式 | 一句话描述 | 适用场景 |
|------|-----------|----------|
| **Strategy Brain** | 诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| **Fast Scan** | 快速判断 | 这个想法靠谱吗？ |
| **Decision BRD** | 完整决策文档 | 需要申请预算/资源 |
| **Strategy Design** | 可落地的策略 | 知道要做什么，但不知道怎么做 |
| **Case Match** | 找成功案例 | 想看看别人怎么做的 |
| **Learning Path** | 系统学习路径 | 想深入了解某个增长领域 |

### 知识库规模

| 类型 | 数量 | 说明 |
|------|------|------|
| 📚 案例 | **81个** | 拼多多、抖音、Notion、Airbnb... |
| 🛠️ 玩法 | **111种** | 裂变、PLG、内容增长、留存... |
| 📖 理论 | **12流派** | 增长黑客、网络效应、PLG... |

## 📚 知识直达索引

- [案例库总览](./knowledge/cases/README.md)
- [玩法武器库总览](./knowledge/weapons/index.md)
- [中国案例目录](./knowledge/cases/china/README.md)
- [海外案例目录](./knowledge/cases/overseas/README.md)
- [垂直行业案例目录](./knowledge/cases/vertical/README.md)

### 案例索引（直达文件）

<!-- AUTO-CASE-INDEX:START -->
<details>
<summary>中国案例（43）</summary>

- [B站-社区氛围增长](./knowledge/cases/china/bilibili.md) · C级证据 · 社交、社区、Z世代
- [DeepSeek（深度求索）- AI开源突围战](./knowledge/cases/china/deepseek.md) · B级证据 · 开源模型、低成本训练、viral增长
- [Kimi（月之暗面）- AI助手爆发式增长](./knowledge/cases/china/kimi-moonshot-ai.md) · B级证据 · AI助手、免费获客、内容营销
- [MiniMax（海螺AI/稀宇科技）- AI产品爆发式增长](./knowledge/cases/china/minimax-ai.md) · C级证据 · AI陪伴、视频生成、免费获客
- [Soul-匿名社交增长](./knowledge/cases/china/soul.md) · C级证据 · 社交、灵魂匹配、匿名
- [云集-社交电商裂变](./knowledge/cases/china/yunji.md) · C级证据 · 电商、B2B、跨境
- [京东-用户精细化运营](./knowledge/cases/china/jd-member-ops.md) · B级证据 · 电商、会员体系、用户运营
- [京东家具双11投放案例：ROI达到252](./knowledge/cases/china/jd-furniture-roi252.md) · C级证据
- [京东金融-金条白条增长](./knowledge/cases/china/jd-finance.md) · C级证据 · 金融、白条、金条
- [唯品会-特卖模式增长](./knowledge/cases/china/vipshop.md) · C级证据 · 电商、特卖、库存
- [夸克AI（阿里巴巴）- 超级入口的AI突围](./knowledge/cases/china/quark-ai.md) · C级证据 · AI助手、超级入口、阿里生态
- [小红书-社区种草转化](./knowledge/cases/china/xiaohongshu.md) · C级证据 · 电商、种草、社区
- [少儿英语产品用户洞察案例](./knowledge/cases/china/child-english-insight.md) · C级证据 · 教育、用户洞察、增长方法
- [得物-潮流社区增长](./knowledge/cases/china/dewu.md) · B级证据 · 电商、潮牌、社区
- [微众银行-互联网银行增长](./knowledge/cases/china/webank.md) · C级证据 · 金融、互联网银行、微信生态
- [微信支付-红包裂变](./knowledge/cases/china/wechat-pay.md) · B级证据 · 支付、社交、红包
- [微信红包-社交裂变增长](./knowledge/cases/china/wechat-redpacket.md) · C级证据 · 支付、社交裂变、红包
- [快手极速版-看视频赚现金](./knowledge/cases/china/kuaishou-jisu-ban.md) · C级证据 · 短视频、游戏化、现金激励
- [快手白拿-现金膨胀裂变增长](./knowledge/cases/china/kuaishou-baina.md) · C级证据 · 现金激励、邀请裂变、金币暴涨
- [抖音-算法推荐增长](./knowledge/cases/china/douyin-algorithm.md) · C级证据 · 社交、算法推荐、短视频
- [抖音支付-电商金融](./knowledge/cases/china/douyin-pay.md) · C级证据 · 支付、电商、抖音生态
- [抖音极速版-看视频赚金币](./knowledge/cases/china/douyin-jisu-ban.md) · C级证据 · 短视频、游戏化、金币激励
- [抖音电商-直播带货爆发](./knowledge/cases/china/douyin-ecommerce.md) · C级证据 · 电商、短视频、兴趣电商
- [拼多多-拼团裂变增长](./knowledge/cases/china/pinduoduo-group-buy.md) · C级证据 · 电商、社交裂变、拼团
- [携程-旅游平台增长](./knowledge/cases/china/ctrip.md) · C级证据 · 旅游、OTA、平台
- [支付宝-支付增长](./knowledge/cases/china/alipay.md) · B级证据 · 支付、金融、场景
- [智谱AI（Z.ai/GLM）——中国大模型独角兽的差异化成长之路](./knowledge/cases/china/zhipu-ai.md) · C级证据 · 大模型、基础模型、MaaS平台
- [桌面Widget增长案例](./knowledge/cases/china/widget-growth.md) · C级证据 · Widget、桌面美化、社交货币
- [淘宝直播-内容电商转型](./knowledge/cases/china/taobao-live.md) · C级证据 · 电商、直播、内容电商
- [滴滴-出行平台增长](./knowledge/cases/china/didi.md) · B级证据 · 出行、平台、双边市场
- [白拿送礼-社交裂变增长](./knowledge/cases/china/white-get-gift.md) · C级证据 · 社交裂变、免费获客、送礼
- [知乎-知识分享增长](./knowledge/cases/china/zhihu.md) · B级证据 · 社交、知识、问答
- [秘塔AI搜索 - AI搜索赛道的差异化突围](./knowledge/cases/china/mita-ai-search.md) · C级证据 · AI搜索、无广告、深度研究
- [美团-本地生活平台增长](./knowledge/cases/china/meituan.md) · C级证据 · 本地生活、平台、外卖
- [腾讯元宝（Tencent Yuanbao）- AI to C 的生态攻坚战](./knowledge/cases/china/tencent-yuanbao.md) · C级证据 · AI助手、腾讯生态、微信嵌入
- [芭芭农场-游戏化增长](./knowledge/cases/china/baba-farm.md) · C级证据 · 游戏化、养成、社交裂变
- [蚂蚁森林-用户粘性增长](./knowledge/cases/china/ant-forest.md) · B级证据 · 金融、游戏化、公益
- [豆包（字节跳动）- 互联网巨头的AI助手增长](./knowledge/cases/china/doubao-bytedance.md) · B级证据 · AI助手、免费获客、字节生态
- [贝壳-居住平台增长](./knowledge/cases/china/beike.md) · B级证据 · 居住、平台、经纪人
- [趣头条-看新闻赚金币](./knowledge/cases/china/qutoutiao.md) · C级证据 · 资讯、游戏化、金币激励
- [银发人群增长-视频奖励与任务体系](./knowledge/cases/china/silver-hair-growth.md) · C级证据 · 银发经济、看视频赚钱、任务体系
- [陌陌-陌生社交增长](./knowledge/cases/china/momo.md) · B级证据 · 社交、直播、陌生人社交
- [饿了么-外卖平台增长](./knowledge/cases/china/ele.md) · B级证据 · 本地生活、外卖、平台

</details>

<details>
<summary>海外案例（28）</summary>

- [Airbnb-信任机制增长](./knowledge/cases/overseas/airbnb.md) · B级证据 · 住宿、平台、双边市场
- [Airbnb-房源增长策略](./knowledge/cases/overseas/airbnb-host.md) · C级证据 · 住宿、房东、平台
- [Allbirds-口碑增长](./knowledge/cases/overseas/allbirds.md) · B级证据 · 鞋、DTC、可持续
- [Anthropic/Claude — AI助手产品增长案例](./knowledge/cases/overseas/claude-anthropic.md) · B级证据 · AI、大语言模型、企业级AI
- [Calendly-工具产品增长](./knowledge/cases/overseas/calendly.md) · B级证据 · 工具、日程、预约
- [Character.AI-社区裂变增长](./knowledge/cases/overseas/character-ai.md) · B级证据 · AI、对话机器人、社区
- [Cursor - AI编程工具爆发式增长](./knowledge/cases/overseas/cursor-ai-editor.md) · B级证据 · AI编程、SaaS、工具
- [Dollar Shave Club-订阅电商](./knowledge/cases/overseas/dollar-shave-club.md) · C级证据 · 订阅、DTC、剃须刀
- [DoorDash-外卖平台增长](./knowledge/cases/overseas/doordash.md) · B级证据 · 外卖、平台、本地生活
- [Dropbox-推荐裂变增长](./knowledge/cases/overseas/dropbox.md) · B级证据 · SaaS、存储、邀请裂变
- [ElevenLabs — AI语音合成产品增长案例](./knowledge/cases/overseas/elevenlabs-ai.md) · B级证据 · AI语音、生成式AI、企业级AI
- [GitHub Copilot — AI编程工具市场开创者与增长](./knowledge/cases/overseas/github-copilot.md) · B级证据 · AI编程、SaaS、B2D
- [Glossier-社交电商](./knowledge/cases/overseas/glossier.md) · B级证据 · 美妆、DTC、社区
- [HubSpot-入站营销增长](./knowledge/cases/overseas/hubspot.md) · C级证据 · SaaS、营销自动化、入站营销
- [Midjourney-社区驱动增长](./knowledge/cases/overseas/midjourney.md) · C级证据 · AI、图像生成、Discord社区
- [Notion-社区驱动增长](./knowledge/cases/overseas/notion.md) · B级证据 · SaaS、协作、社区
- [OpenAI/ChatGPT-生成式AI产品增长](./knowledge/cases/overseas/openai-chatgpt.md) · B级证据 · AI、大语言模型、消费应用
- [Perplexity-答案引擎增长](./knowledge/cases/overseas/perplexity.md) · B级证据 · AI、搜索引擎、答案引擎
- [Pika AI-社区+产品驱动增长](./knowledge/cases/overseas/pika-ai.md) · C级证据 · AI、视频生成、Discord社区
- [Runway AI-内容生态驱动增长](./knowledge/cases/overseas/runway-ai.md) · C级证据 · AI、视频生成、影视合作
- [Slack-产品驱动增长](./knowledge/cases/overseas/slack.md) · C级证据 · SaaS、协作、工具
- [Stripe-开发者生态增长](./knowledge/cases/overseas/stripe.md) · B级证据 · 支付、开发者、API
- [Suno — AI音乐生成产品增长案例](./knowledge/cases/overseas/suno-music-ai.md) · B级证据 · AI音乐、生成式AI、消费级AI
- [Uber-双边市场增长](./knowledge/cases/overseas/uber.md) · B级证据 · 出行、平台、双边市场
- [Warby Parker-眼镜直销](./knowledge/cases/overseas/warby-parker.md) · B级证据 · 眼镜、DTC、Home Try-On
- [Windsurf - AI编程工具差异化增长](./knowledge/cases/overseas/windsurf-ai-editor.md) · C级证据 · AI编程、SaaS、工具
- [Zoom-病毒式增长](./knowledge/cases/overseas/zoom.md) · B级证据 · SaaS、视频会议、病毒传播
- [海外银发奖励平台-Swagbucks/InboxDollars](./knowledge/cases/overseas/silver-hair-reward-platforms.md) · C级证据 · 任务墙、积分奖励、银发用户

</details>

<details>
<summary>垂直行业案例（10）</summary>

- [Coursera-在线教育增长](./knowledge/cases/vertical/coursera.md) · C级证据 · 教育、在线、MOOC
- [Duolingo-游戏化学习增长](./knowledge/cases/vertical/duolingo.md) · B级证据 · 教育、游戏化、学习
- [SHAREit（茄子快传）-工具出海](./knowledge/cases/vertical/shareit.md) · C级证据 · 工具、出海、预装
- [SHEIN-快时尚出海](./knowledge/cases/vertical/shein.md) · B级证据 · 快时尚、出海、供应链
- [TikTok-海外增长](./knowledge/cases/vertical/tiktok.md) · C级证据 · 短视频、出海、算法推荐
- [VIPKID-少儿英语增长](./knowledge/cases/vertical/vipkid.md) · B级证据 · 教育、英语、在线
- [字节跳动-海外产品矩阵](./knowledge/cases/vertical/bytedance-overseas.md) · B级证据 · 互联网、出海、产品矩阵
- [猿辅导-题库产品增长](./knowledge/cases/vertical/yuanfudao.md) · B级证据 · 教育、在线、英语
- [腾讯游戏-出海增长](./knowledge/cases/vertical/tencent-games.md) · C级证据 · 游戏、出海、投资
- [跨境电商独立站-品牌出海](./knowledge/cases/vertical/dtc-brand.md) · C级证据 · 跨境、DTC、独立站

</details>

<!-- AUTO-CASE-INDEX:END -->

### 玩法索引（直达文件）

<!-- AUTO-WEAPON-INDEX:START -->
<details>
<summary>冷启动增长（10）</summary>

- [手动拉种子用户](./knowledge/weapons/01-cold-start/weapons/001-手动拉种子用户.md) · Low effort · Medium impact · C级证据
- [冷邮件/私信](./knowledge/weapons/01-cold-start/weapons/002-冷邮件-私信.md) · Low effort · Medium impact · C级证据
- [社区深度参与](./knowledge/weapons/01-cold-start/weapons/003-社区深度参与.md) · Low effort · Medium impact · C级证据
- [手动服务前100用户](./knowledge/weapons/01-cold-start/weapons/004-手动服务前100用户.md) · Low effort · Medium impact · C级证据
- [创始人个人IP](./knowledge/weapons/01-cold-start/weapons/005-创始人个人IP.md) · Medium effort · High impact · C级证据
- [Waitlist候补名单](./knowledge/weapons/01-cold-start/weapons/006-Waitlist候补名单.md) · Low effort · Medium impact · B级证据
- [Beta邀请制](./knowledge/weapons/01-cold-start/weapons/007-Beta邀请制.md) · Low effort · High impact · B级证据
- [Landing Page注册](./knowledge/weapons/01-cold-start/weapons/008-Landing Page注册.md) · Medium effort · High impact · C级证据
- [Product Hunt发布](./knowledge/weapons/01-cold-start/weapons/009-Product Hunt发布.md) · Medium effort · High impact · C级证据
- [种子用户群](./knowledge/weapons/01-cold-start/weapons/010-种子用户群.md) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>病毒裂变（15）</summary>

- [邀请奖励机制](./knowledge/weapons/02-viral-referral/weapons/011-邀请奖励机制.md) · Medium effort · High impact · B级证据
- [双边奖励](./knowledge/weapons/02-viral-referral/weapons/012-双边奖励.md) · Medium effort · High impact · A级证据
- [分享解锁功能](./knowledge/weapons/02-viral-referral/weapons/013-分享解锁功能.md) · Low effort · Medium impact · C级证据
- [分享解锁内容](./knowledge/weapons/02-viral-referral/weapons/014-分享解锁内容.md) · High effort · High impact · A级证据
- [裂变海报生成](./knowledge/weapons/02-viral-referral/weapons/015-裂变海报生成.md) · High effort · High impact · B级证据
- [排行榜分享](./knowledge/weapons/02-viral-referral/weapons/016-排行榜分享.md) · Medium effort · Medium impact · C级证据
- [拼团机制](./knowledge/weapons/02-viral-referral/weapons/017-拼团机制.md) · Medium effort · High impact · A级证据
- [砍价玩法](./knowledge/weapons/02-viral-referral/weapons/018-砍价玩法.md) · High effort · High impact · B级证据
- [社交挑战赛](./knowledge/weapons/02-viral-referral/weapons/019-社交挑战赛.md) · Low effort · Medium impact · C级证据
- [模板分享裂变](./knowledge/weapons/02-viral-referral/weapons/020-模板分享裂变.md) · High effort · High impact · B级证据
- [AI生成内容分享](./knowledge/weapons/02-viral-referral/weapons/021-AI生成内容分享.md) · Low effort · Medium impact · B级证据
- [分享后去水印](./knowledge/weapons/02-viral-referral/weapons/022-分享后去水印.md) · Medium effort · High impact · B级证据
- [推荐码体系](./knowledge/weapons/02-viral-referral/weapons/023-推荐码体系.md) · Low effort · Medium impact · C级证据
- [邀请排行榜](./knowledge/weapons/02-viral-referral/weapons/024-邀请排行榜.md) · Medium effort · Medium impact · C级证据
- [好友助力解锁](./knowledge/weapons/02-viral-referral/weapons/025-好友助力解锁.md) · Medium effort · High impact · B级证据

</details>

<details>
<summary>内容增长（15）</summary>

- [SEO关键词矩阵](./knowledge/weapons/03-content-growth/weapons/026-SEO关键词矩阵.md) · Medium effort · High impact · B级证据
- [程序化SEO页面](./knowledge/weapons/03-content-growth/weapons/027-程序化SEO页面.md) · Medium effort · High impact · B级证据
- [长尾关键词文章](./knowledge/weapons/03-content-growth/weapons/028-长尾关键词文章.md) · Medium effort · Medium impact · C级证据
- [教程型内容](./knowledge/weapons/03-content-growth/weapons/029-教程型内容.md) · High effort · High impact · C级证据
- [行业报告](./knowledge/weapons/03-content-growth/weapons/030-行业报告.md) · Medium effort · Medium impact · C级证据
- [免费工具](./knowledge/weapons/03-content-growth/weapons/031-免费工具.md) · Low effort · Medium impact · C级证据
- [YouTube教程](./knowledge/weapons/03-content-growth/weapons/032-YouTube教程.md) · High effort · High impact · B级证据
- [TikTok矩阵](./knowledge/weapons/03-content-growth/weapons/033-TikTok矩阵.md) · Medium effort · High impact · C级证据
- [Newsletter](./knowledge/weapons/03-content-growth/weapons/034-Newsletter.md) · Low effort · Medium impact · C级证据
- [播客](./knowledge/weapons/03-content-growth/weapons/035-播客.md) · High effort · High impact · B级证据
- [客座博客](./knowledge/weapons/03-content-growth/weapons/036-客座博客.md) · Low effort · Medium impact · C级证据
- [免费电子书](./knowledge/weapons/03-content-growth/weapons/037-免费电子书.md) · Medium effort · Medium impact · C级证据
- [案例研究](./knowledge/weapons/03-content-growth/weapons/038-案例研究.md) · Medium effort · High impact · B级证据
- [模板资源库](./knowledge/weapons/03-content-growth/weapons/039-模板资源库.md) · Low effort · Medium impact · C级证据
- [内容再分发](./knowledge/weapons/03-content-growth/weapons/040-内容再分发.md) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>社区增长（10）</summary>

- [Discord社区](./knowledge/weapons/04-community/weapons/041-Discord社区.md) · High effort · High impact · C级证据
- [Slack社区](./knowledge/weapons/04-community/weapons/042-Slack社区.md) · Medium effort · High impact · B级证据
- [用户大使计划](./knowledge/weapons/04-community/weapons/043-用户大使计划.md) · Medium effort · Medium impact · C级证据
- [用户共创](./knowledge/weapons/04-community/weapons/044-用户共创.md) · Medium effort · High impact · B级证据
- [线下Meetup](./knowledge/weapons/04-community/weapons/045-线下Meetup.md) · Medium effort · Medium impact · C级证据
- [用户访谈公开化](./knowledge/weapons/04-community/weapons/046-用户访谈公开化.md) · Low effort · Medium impact · C级证据
- [用户故事栏目](./knowledge/weapons/04-community/weapons/047-用户故事栏目.md) · Medium effort · Medium impact · C级证据
- [社区挑战赛](./knowledge/weapons/04-community/weapons/048-社区挑战赛.md) · Medium effort · High impact · B级证据
- [超级用户计划](./knowledge/weapons/04-community/weapons/049-超级用户计划.md) · Low effort · Medium impact · C级证据
- [用户UGC活动](./knowledge/weapons/04-community/weapons/050-用户UGC活动.md) · High effort · Medium impact · C级证据

</details>

<details>
<summary>产品驱动增长（15）</summary>

- [Freemium模式](./knowledge/weapons/05-plg/weapons/051-Freemium模式.md) · Medium effort · High impact · A级证据
- [免费试用](./knowledge/weapons/05-plg/weapons/052-免费试用.md) · Low effort · Medium impact · B级证据
- [无需登录体验](./knowledge/weapons/05-plg/weapons/053-无需登录体验.md) · Medium effort · High impact · B级证据
- [快速Onboarding](./knowledge/weapons/05-plg/weapons/054-快速Onboarding.md) · Medium effort · High impact · B级证据
- [产品内引导](./knowledge/weapons/05-plg/weapons/055-产品内引导.md) · Low effort · Medium impact · B级证据
- [模板库](./knowledge/weapons/05-plg/weapons/056-模板库.md) · High effort · High impact · B级证据
- [空状态设计](./knowledge/weapons/05-plg/weapons/057-空状态设计.md) · Low effort · Medium impact · C级证据
- [产品内分享](./knowledge/weapons/05-plg/weapons/058-产品内分享.md) · Medium effort · Medium impact · C级证据
- [产品水印](./knowledge/weapons/05-plg/weapons/059-产品水印.md) · High effort · High impact · B级证据
- [团队协作](./knowledge/weapons/05-plg/weapons/060-团队协作.md) · High effort · High impact · B级证据
- [使用量限制触发](./knowledge/weapons/05-plg/weapons/061-使用量限制触发.md) · Medium effort · Medium impact · C级证据
- [成果导出传播](./knowledge/weapons/05-plg/weapons/062-成果导出传播.md) · Low effort · High impact · A级证据
- [使用报告](./knowledge/weapons/05-plg/weapons/063-使用报告.md) · Medium effort · High impact · B级证据
- [内置社区入口](./knowledge/weapons/05-plg/weapons/064-内置社区入口.md) · Low effort · Medium impact · C级证据
- [产品内推荐](./knowledge/weapons/05-plg/weapons/065-产品内推荐.md) · Medium effort · Medium impact · C级证据

</details>

<details>
<summary>留存增长（15）</summary>

- [邮件生命周期](./knowledge/weapons/06-retention/weapons/066-邮件生命周期.md) · Low effort · Medium impact · C级证据
- [推送通知](./knowledge/weapons/06-retention/weapons/067-推送通知.md) · Low effort · Medium impact · C级证据
- [连续使用奖励](./knowledge/weapons/06-retention/weapons/068-连续使用奖励.md) · Medium effort · High impact · B级证据
- [里程碑提示](./knowledge/weapons/06-retention/weapons/069-里程碑提示.md) · Low effort · Medium impact · B级证据
- [数据报告邮件](./knowledge/weapons/06-retention/weapons/070-数据报告邮件.md) · Medium effort · Medium impact · B级证据
- [周报/月报](./knowledge/weapons/06-retention/weapons/071-周报-月报.md) · Medium effort · Medium impact · B级证据
- [新功能提醒](./knowledge/weapons/06-retention/weapons/072-新功能提醒.md) · Low effort · Medium impact · C级证据
- [用户成就系统](./knowledge/weapons/06-retention/weapons/073-用户成就系统.md) · Low effort · Medium impact · C级证据
- [习惯培养](./knowledge/weapons/06-retention/weapons/074-习惯培养.md) · Low effort · Low impact · C级证据
- [流失召回](./knowledge/weapons/06-retention/weapons/075-流失召回.md) · High effort · High impact · A级证据
- [分层定价](./knowledge/weapons/07-monetization/weapons/076-分层定价.md) · Medium effort · Medium impact · B级证据
- [使用量计费](./knowledge/weapons/07-monetization/weapons/077-使用量计费.md) · Medium effort · High impact · B级证据
- [年付折扣](./knowledge/weapons/07-monetization/weapons/078-年付折扣.md) · Medium effort · High impact · B级证据
- [限时优惠](./knowledge/weapons/07-monetization/weapons/079-限时优惠.md) · Medium effort · High impact · B级证据
- [功能升级提示](./knowledge/weapons/07-monetization/weapons/080-功能升级提示.md) · High effort · High impact · B级证据

</details>

<details>
<summary>变现增长（12）</summary>

- [捆绑套餐](./knowledge/weapons/07-monetization/weapons/081-捆绑套餐.md) · Medium effort · High impact · B级证据
- [企业版升级](./knowledge/weapons/07-monetization/weapons/082-企业版升级.md) · Low effort · Medium impact · C级证据
- [增值插件市场](./knowledge/weapons/07-monetization/weapons/083-增值插件市场.md) · Low effort · Medium impact · C级证据
- [付费模板市场](./knowledge/weapons/07-monetization/weapons/084-付费模板市场.md) · Medium effort · High impact · B级证据
- [Upsell邮件](./knowledge/weapons/07-monetization/weapons/085-Upsell邮件.md) · Medium effort · High impact · A级证据
- [Google Ads](./knowledge/weapons/08-paid-ads/weapons/086-Google Ads.md) · Medium effort · Medium impact · B级证据
- [Facebook Ads](./knowledge/weapons/08-paid-ads/weapons/087-Facebook Ads.md) · Medium effort · Medium impact · B级证据
- [TikTok Ads](./knowledge/weapons/08-paid-ads/weapons/088-TikTok Ads.md) · High effort · High impact · B级证据
- [YouTube Ads](./knowledge/weapons/08-paid-ads/weapons/089-YouTube Ads.md) · High effort · High impact · B级证据
- [再营销广告](./knowledge/weapons/08-paid-ads/weapons/090-再营销广告.md) · Low effort · Medium impact · B级证据
- [Lookalike人群](./knowledge/weapons/08-paid-ads/weapons/091-Lookalike人群.md) · Low effort · Medium impact · C级证据
- [App Store Ads](./knowledge/weapons/08-paid-ads/weapons/092-App Store Ads.md) · Low effort · Medium impact · C级证据

</details>

<details>
<summary>付费广告（10）</summary>

- [KOL投放](./knowledge/weapons/08-paid-ads/weapons/093-KOL投放.md) · Medium effort · Medium impact · B级证据
- [联盟营销](./knowledge/weapons/08-paid-ads/weapons/094-联盟营销.md) · Medium effort · Medium impact · B级证据
- [Influencer合作](./knowledge/weapons/08-paid-ads/weapons/095-Influencer合作.md) · Medium effort · Medium impact · B级证据
- [品牌故事](./knowledge/weapons/09-brand/weapons/096-品牌故事.md) · Medium effort · High impact · C级证据
- [创始人IP](./knowledge/weapons/09-brand/weapons/097-创始人IP.md) · Low effort · High impact · B级证据
- [PR媒体](./knowledge/weapons/09-brand/weapons/098-PR媒体.md) · Medium effort · Medium impact · C级证据
- [行业大会](./knowledge/weapons/09-brand/weapons/099-行业大会.md) · High effort · Medium impact · C级证据
- [品牌视觉统一](./knowledge/weapons/09-brand/weapons/100-品牌视觉统一.md) · Medium effort · Medium impact · B级证据
- [标志性活动](./knowledge/weapons/09-brand/weapons/101-标志性活动.md) · High effort · Medium impact · C级证据
- [价值观营销](./knowledge/weapons/09-brand/weapons/102-价值观营销.md) · High effort · Medium impact · C级证据

</details>

<details>
<summary>品牌增长（5）</summary>

- [社会议题](./knowledge/weapons/09-brand/weapons/103-社会议题.md) · Low effort · Medium impact · C级证据
- [冷启动外呼](./knowledge/weapons/10-b2b-sales/weapons/104-冷启动外呼.md) · Medium effort · High impact · C级证据
- [LinkedIn外联](./knowledge/weapons/10-b2b-sales/weapons/105-LinkedIn外联.md) · Low effort · Medium impact · C级证据
- [Webinar](./knowledge/weapons/10-b2b-sales/weapons/106-Webinar.md) · Medium effort · Medium impact · C级证据
- [Demo演示](./knowledge/weapons/10-b2b-sales/weapons/107-Demo演示.md) · Medium effort · High impact · C级证据

</details>

<details>
<summary>B2B销售（4）</summary>

- [白皮书下载](./knowledge/weapons/10-b2b-sales/weapons/108-白皮书下载.md) · Medium effort · Medium impact · C级证据
- [销售自动化](./knowledge/weapons/10-b2b-sales/weapons/109-销售自动化.md) · Low effort · High impact · B级证据
- [客户成功](./knowledge/weapons/10-b2b-sales/weapons/110-客户成功.md) · High effort · High impact · B级证据
- [转介绍计划](./knowledge/weapons/10-b2b-sales/weapons/111-转介绍计划.md) · Low effort · High impact · B级证据

</details>

<!-- AUTO-WEAPON-INDEX:END -->

### 质量保障

| 机制 | 作用 |
|------|------|
| ✅ **现状清晰度门控** | 信息不足时主动追问，避免盲目诊断 |
| ✅ **证据分级系统** | A/B/C/D/E 五级可信度，透明标注 |
| ✅ **安全边界检测** | 自动识别财务/法律/监管风险 |
| ✅ **输出契约** | 10 个必选章节，确保报告完整 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/growth-master-skill.git

# 运行环境
# Python 3.8+，当前脚本默认仅使用标准库

# 安装到 Claude 技能目录（可选）
cp -R growth-master-skill ~/.claude/skills/
```

### 验证安装

```bash
# 验证 Agent 定义
python scripts/validate-agents.py
# ✅ 13/13 agents valid

# 验证知识索引
python scripts/validate-indexes.py
# ✅ 81 cases, 111 weapons, 12 theories indexed
```

### 第一次使用

```bash
# 快速生成策略外脑诊断
python scripts/cli.py diagnose "电商平台如何提升复购率" \
  --industry ecommerce --problem retention

# 搜索相关案例和玩法
python scripts/cli.py search "裂变" --limit 5

# 匹配相关案例
python scripts/cli.py match "教育产品如何做裂变" --problem referral

# 场景化入口
python scripts/cli.py retention "如何提升月活跃用户留存率" --industry content

# 结构化上下文输入
python scripts/cli.py diagnose "如何提升月活跃用户留存率" \
  --industry content --problem retention \
  --context-json '{"goal":"提升30日留存","metric":"30日留存率","budget":"10万元","team":"产品1+工程2+运营1"}'

# 从文件加载结构化上下文
python scripts/cli.py diagnose "我们要不要做邀请裂变" \
  --industry saas --stage 1-10 --problem referral \
  --context-file examples/referral-context.json --view report
```

---

## 💼 使用场景

### 场景一：增长外脑诊断

**问题**：老板问「我们要不要做邀请裂变？」

```bash
python scripts/cli.py diagnose "是否应该做邀请裂变" \
  --industry saas --stage 1-10 --problem referral
```

**输出**：
- 一句话判断
- 核心矛盾
- 优先级排序
- 建议现在做 / 建议先别做
- 两周实验
- 可切换为负责人摘要 / 报告版 / JSON 版
- 支持 `--context-json` / `--context-file` 注入目标、预算、团队与历史动作

---

### 场景二：校验决策文档

**问题**：已经有一份分析稿，想确认结构是否完整

```bash
python scripts/cli.py validate report.md
```

**输出**：
- 报告总分
- 是否通过校验
- 缺失章节或缺少的关键信息
- 事实标记是否完整

---

### 场景三：设计增长策略

**问题**：知道要提升留存，但不知道具体怎么做

```bash
python scripts/cli.py design "如何提升月活跃用户留存率" \
  --industry content --problem retention
```

**输出**：
- 策略方向
- 主抓手优先级
- 为什么现在做
- 两周实验与成功/停止信号
- 案例和理论支撑

---

### 场景五：给增长负责人准备汇报稿

**问题**：要去周会或季度评审，想直接拿到可以讲的摘要

```bash
python scripts/cli.py diagnose "我们要不要做邀请裂变" \
  --industry saas --stage 1-10 --problem referral --view executive
```

**输出**：
- 董事会/负责人摘要
- 本周拍板事项
- 先别做什么
- 当前置信度

---

### 场景六：导出可校验决策稿

**问题**：想生成一版可继续修改的正式决策稿

```bash
python scripts/cli.py diagnose "我们要不要做邀请裂变" \
  --industry saas --stage 1-10 --problem referral --view report > report.md

python scripts/cli.py validate report.md
```

**输出**：
- 满足报告契约的 Markdown 决策稿
- 可进一步进入校验和迭代

---

### 场景四：匹配成功案例

**问题**：想看看别人是怎么做游戏化增长的

```bash
python scripts/cli.py match "游戏化提升用户活跃" \
  --industry education
```

**输出**：
- 匹配案例列表（带相似度评分）
- 各案例核心策略
- 可复制要点
- 注意事项

---

## 🔢 贝叶斯决策引擎

### 什么是贝叶斯决策？

贝叶斯决策将不确定的增长决策转化为**可审计的概率推理过程**：

```
初始假设 → 设置先验概率 → 收集证据 → 更新后验概率 → 比较阈值 → 推荐行动
```

### 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **先验** | 初始置信度 | 35%（有案例参考） |
| **证据** | 支持或反对的信息 | Notion 成功案例（B级） |
| **更新** | 证据影响 | +15% |
| **后验** | 更新后置信度 | 50% |
| **决策** | 基于阈值的行动 | 推荐小实验 |

### 使用示例

```python
from scripts.bayesian_decision import BayesianDecision

# 初始化
bd = BayesianDecision()

# 设置假设
bd.set_hypothesis("邀请裂变能带来有效增长")
bd.set_prior(0.35, rationale="有Notion、Dropbox案例参考")

# 添加证据
bd.add_evidence("Notion案例", "B", "support")
bd.add_evidence("SaaS行业报告", "B", "support")

# 更新并获取决策
bd.update()
print(f"后验置信度: {bd.get_posterior():.0%}")  # 52%
print(f"决策建议: {bd.get_decision_text()['action']}")  # 推荐小规模实验
```

### 行动阈值

| 后验范围 | 决策 | 说明 |
|----------|------|------|
| ≥ 75% | **直接投入** | 高置信度，可执行 |
| 50-75% | **小实验** | 中等置信度，需验证 |
| 30-50% | **收集证据** | 低置信度，信息不足 |
| < 30% | **停止** | 极低置信度，不推荐 |

### 证据等级与更新幅度

| 等级 | 定义 | 更新幅度 |
|------|------|---------|
| A | 元分析、系统综述 | ±25% |
| B | 同行评审、行业报告 | ±15% |
| C | 专家意见、内部数据 | ±10% |
| D | LLM建议、类比 | ±5% |
| E | 博客、营销文案 | 0% |

### 敏感性分析

每个贝叶斯决策自动生成敏感性分析：

```markdown
🔍 结论有多稳固？
- 反转条件: 如果病毒系数 < 0.3，结论反转为不推荐
- 关键假设: 用户有足够的邀请动机
- 风险点: 奖励机制成本未验证
```

---

## 🎯 博弈论战略框架

### 什么是博弈论决策？

分析竞争、定价、谈判等战略互动：

```
识别博弈类型 → 构建收益矩阵 → 分析均衡 → 历史校准 → 承诺检验 → 战略建议
```

### 适用场景

| 场景 | 博弈框架 | 核心问题 |
|------|----------|----------|
| **竞争反应** | 囚徒困境 | 对手会怎么反应？ |
| **定价策略** | 信号博弈 | 如何定价不被跟进？ |
| **平台策略** | 双边市场 | 如何启动双边平台？ |
| **谈判分配** | 讨价还价 | 如何分配利益？ |

### 使用示例

```python
# 博弈论分析流程
from scripts.gametheory_analysis import GameTheoryAnalysis

ga = GameTheoryAnalysis()
ga.set_players(["我方", "竞争对手"])
ga.set_strategies({
    "我方": ["降价", "不降价"],
    "竞争对手": ["跟进", "不跟进"]
})
ga.build_payoff_matrix(...)  # 构建收益矩阵
ga.find_nash_equilibrium()   # 找到纳什均衡
ga.calibrate_with_history()  # 历史行为校准
```

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

## 🏗️ 完整框架体系

### 核心决策框架

| 框架 | 用途 | 文档 |
|------|------|------|
| **贝叶斯决策** | 概率推理、证据更新 | [bayesian-decision.md](./references/bayesian-decision.md) |
| **博弈论战略** | 竞争分析、均衡预测 | [gametheory-framework.md](./references/gametheory-framework.md) |
| **Kelly 分配** | 资源投入优化 | [kelly-allocation.md](./references/kelly-allocation.md) |
| **商业模式** | 商业设计与诊断 | [business-model.md](./references/business-model.md) |

### 扩展框架

| 框架 | 用途 | 文档 |
|------|------|------|
| 教程生产 | 学习内容生成 | [tutorial-production.md](./references/tutorial-production.md) |
| 学习构建 | 个性化学习路径 | [learning-builder.md](./references/learning-builder.md) |
| Web 安全 | 安全审计 | [websecurity-audit.md](./references/websecurity-audit.md) |
| 微信读书 | 阅读报告 | [weread-report.md](./references/weread-report.md) |

---

## 🏗️ 架构概览

```
用户输入
    │
    ▼
┌─────────────────┐
│ Lead Agent      │ ← 编排协调、问题分类
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ 知识  │ │ 决策  │
│ Agent │ │ Agent │
│ 群    │ │ 群    │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
┌─────────────────┐
│ Narrative Agent │ ← 输出生成
└─────────────────┘
```

**知识 Agent 群**：Case · Weapon · Theory · Competitor

**决策 Agent 群**：Growth · Monetization · ROI · Execution · Skeptic

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](./SKILL.md) | 完整技能定义 |
| [用户指南](./docs/user-guide.md) | 详细使用教程 |
| [开发者指南](./docs/developer-guide.md) | 扩展与定制 |
| [最佳实践](./docs/best-practices.md) | 使用技巧 |
| [贝叶斯决策](./references/bayesian-decision.md) | 概率推理框架 |

---

## 🧪 测试覆盖

```bash
# 运行全部测试
python scripts/validate-agents.py   # Agent 定义验证
python scripts/validate-indexes.py  # 知识索引验证
python scripts/e2e_test_runner.py   # E2E 测试
python tests/test_bayesian_decision.py  # 贝叶斯决策测试
```

| 测试类型 | 覆盖 | 状态 |
|----------|------|------|
| Agent 测试 | 13/13 | ✅ |
| E2E 测试 | 10/10 | ✅ |
| 贝叶斯决策 | 10/10 | ✅ |
| 报告评分 | 97/100 | ✅ |

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

[⬆ 回到顶部](#-growth-master)

</div>
