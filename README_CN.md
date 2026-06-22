<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth - 增长策略外脑

**Claude Code, OpenClaw & Hermes Agent 专用增长决策插件**

整合 **194个案例** · **111种玩法** · **12大流派** · **完整决策框架**

输入一个增长问题，直接输出：
`阶段判断` · `核心矛盾` · `优先级排序` · `建议做/别做` · `两周实验`

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-96%2F96%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[安装](#-安装) · [快速开始](#-快速开始) · [核心框架](#-核心框架) · [文档](#-文档)

**[English](./README.md)**

</div>

---

## 💡 这是什么？

**oh-my-growth** 是一个**增长决策插件**，支持 Claude Code、OpenClaw 和 Hermes Agent。

在 Claude Code 会话中，你可以直接调用专业的增长策略分析能力：

```
/omg-diagnose 我的产品日活下降20%，该怎么办？
/omg-assess 我们准备做裂变，先评估可行性
/omg-design SaaS产品如何设计变现策略？
```

**缩写支持**：也可使用 `/omg` 代替 `/oh-my-growth`

```
/omg-diagnose 我的产品日活下降20%，该怎么办？
/omg-assess 我们准备做裂变，先评估可行性
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
cd oh-my-growth
./scripts/install.sh
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 安装到 Claude Code skills 目录
cp -R oh-my-growth ~/.claude/skills/oh-my-growth
```

### 验证安装

在 Claude Code 中输入：
```
/omg-diagnose 测试安装
```

### 安装到 OpenClaw

oh-my-growth 也支持 **OpenClaw**：

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 安装到 OpenClaw skills 目录
cp -R oh-my-growth/openclaw ~/.openclaw/skills/oh-my-growth
cp -R oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.openclaw/skills/oh-my-growth/

# 安装 Python 依赖
pip install -r oh-my-growth/requirements.txt
```

详细安装说明请参考 [openclaw/INSTALL.md](./openclaw/INSTALL.md)。

### 安装到 Hermes Agent

oh-my-growth 也支持 **Hermes Agent**：

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 安装到 Hermes skills 目录
mkdir -p ~/.hermes/skills/oh-my-growth
cp -R oh-my-growth/hermes/SKILL.md ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/knowledge ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.hermes/skills/oh-my-growth/

# 安装 Python 依赖
pip install -r oh-my-growth/requirements.txt
```

详细安装说明请参考 [hermes/INSTALL.md](./hermes/INSTALL.md)。

---

## ✨ 快速开始

### 在 Claude Code 中使用

**核心命令：**

```bash
# 策略诊断 - 诊断增长问题并给出优先级排序
/omg-diagnose SaaS产品如何获取首批用户
/omg-diagnose 我的产品日活下降20%，该怎么办？

# 机会评估 - 评估是否值得深入分析
/omg-assess 我们要不要做邀请裂变
/omg-assess 我们准备做病毒增长，先评估可行性

# 策略设计 - 可落地的策略方案
/omg-design 如何提升月活跃用户留存率
/omg-design SaaS产品变现策略

# 案例匹配 - 找成功案例参考
/omg-match 游戏化提升用户活跃
/omg-match 教育行业裂变增长案例

# 学习路径 - 系统学习路线图
/omg-learn 如何系统学习裂变增长
/omg-learn B2B SaaS留存策略
```

**快速判断：**

```bash
# 快速扫描 - 快速可行性判断
/omg-fast-scan TikTok广告适合我们SaaS吗？

# 决策文档 - 完整决策文档（用于申请预算）
/omg-brd 我们要不要投入5万做裂变
```

**工具命令：**

```bash
# 直接搜索知识库
/omg-search 病毒增长
/omg-search PLG onboarding

# 校验输出文档
/omg-validate report.md
```

**场景快捷入口：**

```bash
# 冷启动场景
/omg-cold-start AI写作SaaS如何拿到前100个种子用户

# 留存场景
/omg-retention 如何提升30日留存率

# 变现场景
/omg-monetization SaaS产品如何设计定价

# 裂变场景
/omg-referral 我们要不要做邀请裂变
```

### 命令参考

| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `/omg-diagnose` | 诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| `/omg-assess` | 评估是否值得深入分析 | 现状还不够清楚，先做清晰度评估 |
| `/omg-design` | 可落地的策略方案 | 知道要做什么，但不知道怎么设计执行路径 |
| `/omg-fast-scan` | 快速判断 | 这个想法靠谱吗？ |
| `/omg-brd` | 完整决策文档 | 需要申请预算/资源 |
| `/omg-match` | 找成功案例 | 想看看别人怎么做的 |
| `/omg-learn` | 系统学习路径 | 想深入了解某个增长领域 |
| `/omg-search` | 搜索知识库 | 直接查找案例/玩法/理论 |
| `/omg-validate` | 校验输出文档 | 检查报告完整性 |
| `/omg-cold-start` | 冷启动场景 | 首批用户获取 |
| `/omg-retention` | 留存场景 | 提升用户留存 |
| `/omg-monetization` | 变现场景 | 设计变现策略 |
| `/omg-referral` | 裂变场景 | 规划裂变方案 |

### 输出视图

独立 CLI 可通过 `--view` 使用 `operator`、`executive`、`report`、`json`、
`weekly`、`experiment-card`、`decision-memo` 和 `qbr` 视图。

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

## 🎯 知识库规模

| 类型 | 数量 | 说明 |
|---

### 案例索引

<!-- AUTO-CASE-INDEX:START -->
<details>
<summary>中国案例（118个）</summary>

**AI产品2025（25个）**
- [Manus AI - AI智能体平台](<./knowledge/cases/china/ai-products-2025/manus-ai.md>) · AI智能体 · 生产力工具
- [Monica AI - 全能AI助手](<./knowledge/cases/china/ai-products-2025/monica-ai.md>) · AI助手 · 浏览器插件
- [通义千问（阿里）- 企业AI](<./knowledge/cases/china/ai-products-2025/tongyi-qianwen.md>) · 大模型 · 企业AI
- [文心一言（百度）- 中文AI助手](<./knowledge/cases/china/ai-products-2025/wenxin-yiyan.md>) · AI助手 · 搜索
- [Kimi（月之暗面）- 长上下文AI](<./knowledge/cases/china/ai-products-2025/moonshot-kimi.md>) · AI助手 · 长上下文
- [DeepSeek - 开源AI模型](<./knowledge/cases/china/deepseek.md>) · B级证据 · 开源 · 低成本训练
- [百川AI - 中文大模型](<./knowledge/cases/china/ai-products-2025/baichuan-ai.md>) · 大模型 · 中文AI
- [智谱AI（GLM）- 中文大模型独角兽](<./knowledge/cases/china/zhipu-ai.md>) · 大模型 · 企业AI
- [MiniMax - AI产品增长](<./knowledge/cases/china/minimax-ai.md>) · AI · 视频生成
- [豆包（字节跳动）- AI助手](<./knowledge/cases/china/doubao-bytedance.md>) · B级证据 · AI助手 · 字节生态

**新商业模式2025（25个）**
- [TEMU出海 - 跨境电商](<./knowledge/cases/china/new-models-2025/temu-overseas.md>) · 电商 · 跨境
- [TikTok Shop - 社交电商](<./knowledge/cases/china/new-models-2025/tiktok-shop.md>) · 电商 · 短视频
- [蔚来换电 - 新能源创新](<./knowledge/cases/china/new-models-2025/nio-battery-swap.md>) · 新能源汽车 · 换电模式
- [理想汽车 - 增程式电动车](<./knowledge/cases/china/new-models-2025/lixiang-auto.md>) · 新能源汽车 · 增程
- [小鹏汽车 - 智能电动车](<./knowledge/cases/china/new-models-2025/xiaopeng-auto.md>) · 新能源汽车 · 自动驾驶

**金融科技（16个）**
- [微众银行 - 互联网银行](<./knowledge/cases/china/fintech/webank.md>) · 互联网银行 · 微信生态
- [网商银行 - 小微银行](<./knowledge/cases/china/fintech/mybank.md>) · 互联网银行 · 小微企业
- [陆金所 - 财富管理](<./knowledge/cases/china/fintech/lufax.md>) · 财富管理 · P2P转型
- [京东数科 - 金融科技平台](<./knowledge/cases/china/fintech/jd-digits.md>) · 金融科技 · 数字金融
- [支付宝 - 支付平台](<./knowledge/cases/china/alipay.md>) · B级证据 · 支付 · 金融

**游戏娱乐（10个）**
- [原神 - 开放世界游戏](<./knowledge/cases/china/gaming/genshin-impact.md>) · 开放世界 · 跨平台
- [王者荣耀 - MOBA游戏](<./knowledge/cases/china/gaming/honor-of-kings.md>) · MOBA · 手游
- [和平精英 - 吃鸡游戏](<./knowledge/cases/china/gaming/peace-elite.md>) · 吃鸡 · 手游
- [黑神话：悟空 - 3A大作](<./knowledge/cases/china/gaming/black-myth-wukong.md>) · 3A · 动作RPG

**医疗健康（10个）**
- [平安好医生 - 互联网医疗](<./knowledge/cases/china/healthcare/pingan-doctor.md>) · 互联网医疗 · 远程诊疗
- [京东健康 - 医药电商](<./knowledge/cases/china/healthcare/jd-health.md>) · 医药电商
- [阿里健康 - 医药平台](<./knowledge/cases/china/healthcare/ali-health.md>) · 医药平台

**电商零售（9个）**
- [拼多多 - 拼团增长](<./knowledge/cases/china/pinduoduo-group-buy.md>) · 电商 · 社交裂变
- [抖音电商 - 直播带货](<./knowledge/cases/china/douyin-ecommerce.md>) · 电商 · 直播
- [小红书 - 社区种草](<./knowledge/cases/china/xiaohongshu.md>) · 电商 · 社区

**社交社区（6个）**
- [B站 - 社区增长](<./knowledge/cases/china/bilibili.md>) · C级证据 · 社交 · 社区 · Z世代
- [知乎 - 知识分享](<./knowledge/cases/china/zhihu.md>) · B级证据 · 社交 · 知识 · 问答

**本地生活（5个）**
- [美团 - 本地生活平台](<./knowledge/cases/china/meituan.md>) · C级证据 · 本地生活 · 平台
- [滴滴 - 出行平台](<./knowledge/cases/china/didi.md>) · B级证据 · 出行 · 平台

</details>

<details>
<summary>海外案例（66个）</summary>

**AI产品2025（29个）**
- [Claude 3.5（Anthropic）- AI助手](<./knowledge/cases/overseas/ai-products-2025/claude-3-5.md>) · AI助手 · 企业AI
- [GPT-4o（OpenAI）- 多模态AI](<./knowledge/cases/overseas/ai-products-2025/gpt-4o.md>) · 多模态AI · 语音
- [Gemini 2（Google）- 多模态AI](<./knowledge/cases/overseas/ai-products-2025/gemini-2.md>) · 多模态AI · 搜索
- [Llama 3（Meta）- 开源大模型](<./knowledge/cases/overseas/ai-products-2025/llama-3.md>) · 开源 · 大模型
- [ChatGPT（OpenAI）- 生成式AI产品](<./knowledge/cases/overseas/openai-chatgpt.md>) · B级证据 · AI · 大模型 · 消费应用
- [Midjourney - 社区驱动增长](<./knowledge/cases/overseas/midjourney.md>) · C级证据 · AI · 图像生成 · Discord
- [Perplexity - 答案引擎增长](<./knowledge/cases/overseas/perplexity.md>) · B级证据 · AI · 搜索引擎
- [Character.AI - 社区裂变增长](<./knowledge/cases/overseas/character-ai.md>) · B级证据 · AI · 对话机器人 · 社区
- [Cursor - AI编程工具爆发式增长](<./knowledge/cases/overseas/cursor-ai-editor.md>) · B级证据 · AI编程 · SaaS · 工具

**新商业模式2025（15个）**
- [Figma设计 - 设计协作](<./knowledge/cases/overseas/new-models-2025/figma-design.md>) · 设计工具 · 协作
- [Canva设计 - 设计民主化](<./knowledge/cases/overseas/new-models-2025/canva-design.md>) · 设计工具 · 免费增值
- [Webflow无代码 - 网站构建](<./knowledge/cases/overseas/new-models-2025/webflow-nocode.md>) · 无代码 · 网站构建
- [Notion - 社区驱动增长](<./knowledge/cases/overseas/notion.md>) · B级证据 · SaaS · 协作 · 社区

**SaaS工具（7个）**
- [Zoom - 病毒式增长](<./knowledge/cases/overseas/zoom.md>) · B级证据 · SaaS · 视频会议 · 病毒传播
- [Slack - 产品驱动增长](<./knowledge/cases/overseas/slack.md>) · C级证据 · SaaS · 协作 · 工具
- [Dropbox - 推荐裂变增长](<./knowledge/cases/overseas/dropbox.md>) · B级证据 · SaaS · 存储 · 邀请裂变

**消费品牌（4个）**
- [Glossier - 社交电商](<./knowledge/cases/overseas/glossier.md>) · B级证据 · 美妆 · DTC · 社区
- [Allbirds - 口碑增长](<./knowledge/cases/overseas/allbirds.md>) · B级证据 · 鞋 · DTC · 可持续

**出行交通（3个）**
- [Airbnb - 信任机制增长](<./knowledge/cases/overseas/airbnb.md>) · B级证据 · 住宿 · 平台 · 双边市场
- [Uber - 双边市场增长](<./knowledge/cases/overseas/uber.md>) · B级证据 · 出行 · 平台 · 双边市场

</details>

<details>
<summary>垂直行业案例（10个）</summary>

- [Coursera - 在线教育增长](<./knowledge/cases/vertical/coursera.md>) · C级证据 · 教育 · 在线 · MOOC
- [Duolingo - 游戏化学习增长](<./knowledge/cases/vertical/duolingo.md>) · B级证据 · 教育 · 游戏化 · 学习
- [茄子快传 - 工具出海](<./knowledge/cases/vertical/shareit.md>) · C级证据 · 工具 · 出海 · 预装
- [SHEIN - 快时尚出海](<./knowledge/cases/vertical/shein.md>) · B级证据 · 快时尚 · 出海 · 供应链
- [TikTok - 海外增长](<./knowledge/cases/vertical/tiktok.md>) · C级证据 · 短视频 · 出海 · 算法

</details>
<!-- AUTO-CASE-INDEX:END -->


---

### 玩法索引

<!-- AUTO-WEAPON-INDEX:START -->
<details>
<summary>冷启动增长（10个）</summary>

- [手动拉种子用户](<./knowledge/weapons/01-cold-start/weapons/001-手动拉种子用户.md>) · 低成本 · 中影响 · C级证据
- [冷邮件/私信](<./knowledge/weapons/01-cold-start/weapons/002-冷邮件-私信.md>) · 低成本 · 中影响 · C级证据
- [社区深度参与](<./knowledge/weapons/01-cold-start/weapons/003-社区深度参与.md>) · 低成本 · 中影响 · C级证据
- [手动服务前100用户](<./knowledge/weapons/01-cold-start/weapons/004-手动服务前100用户.md>) · 低成本 · 中影响 · C级证据
- [创始人个人IP](<./knowledge/weapons/01-cold-start/weapons/005-创始人个人IP.md>) · 中成本 · 高影响 · C级证据
- [Waitlist候补名单](<./knowledge/weapons/01-cold-start/weapons/006-Waitlist候补名单.md>) · 低成本 · 中影响 · B级证据
- [Beta邀请制](<./knowledge/weapons/01-cold-start/weapons/007-Beta邀请制.md>) · 低成本 · 高影响 · B级证据
- [Landing Page注册](<./knowledge/weapons/01-cold-start/weapons/008-Landing Page注册.md>) · 中成本 · 高影响 · C级证据
- [Product Hunt发布](<./knowledge/weapons/01-cold-start/weapons/009-Product Hunt发布.md>) · 中成本 · 高影响 · C级证据
- [种子用户群](<./knowledge/weapons/01-cold-start/weapons/010-种子用户群.md>) · 低成本 · 中影响 · C级证据

</details>

<details>
<summary>病毒裂变（15个）</summary>

- [邀请奖励机制](<./knowledge/weapons/02-viral-referral/weapons/011-邀请奖励机制.md>) · 中成本 · 高影响 · B级证据
- [双边奖励](<./knowledge/weapons/02-viral-referral/weapons/012-双边奖励.md>) · 中成本 · 高影响 · A级证据
- [分享解锁功能](<./knowledge/weapons/02-viral-referral/weapons/013-分享解锁功能.md>) · 低成本 · 中影响 · C级证据
- [分享解锁内容](<./knowledge/weapons/02-viral-referral/weapons/014-分享解锁内容.md>) · 高成本 · 高影响 · A级证据
- [裂变海报生成](<./knowledge/weapons/02-viral-referral/weapons/015-裂变海报生成.md>) · 高成本 · 高影响 · B级证据
- [排行榜分享](<./knowledge/weapons/02-viral-referral/weapons/016-排行榜分享.md>) · 中成本 · 中影响 · C级证据
- [拼团机制](<./knowledge/weapons/02-viral-referral/weapons/017-拼团机制.md>) · 中成本 · 高影响 · A级证据
- [砍价玩法](<./knowledge/weapons/02-viral-referral/weapons/018-砍价玩法.md>) · 高成本 · 高影响 · B级证据
- [社交挑战赛](<./knowledge/weapons/02-viral-referral/weapons/019-社交挑战赛.md>) · 低成本 · 中影响 · C级证据
- [模板分享裂变](<./knowledge/weapons/02-viral-referral/weapons/020-模板分享裂变.md>) · 高成本 · 高影响 · B级证据
- [AI生成内容分享](<./knowledge/weapons/02-viral-referral/weapons/021-AI生成内容分享.md>) · 低成本 · 中影响 · B级证据
- [分享后去水印](<./knowledge/weapons/02-viral-referral/weapons/022-分享后去水印.md>) · 中成本 · 高影响 · B级证据
- [推荐码体系](<./knowledge/weapons/02-viral-referral/weapons/023-推荐码体系.md>) · 低成本 · 中影响 · C级证据
- [邀请排行榜](<./knowledge/weapons/02-viral-referral/weapons/024-邀请排行榜.md>) · 中成本 · 中影响 · C级证据
- [好友助力解锁](<./knowledge/weapons/02-viral-referral/weapons/025-好友助力解锁.md>) · 中成本 · 高影响 · B级证据

</details>

<details>
<summary>内容增长（15个）</summary>

- [SEO关键词矩阵](<./knowledge/weapons/03-content-growth/weapons/026-SEO关键词矩阵.md>) · 中成本 · 高影响 · B级证据
- [程序化SEO页面](<./knowledge/weapons/03-content-growth/weapons/027-程序化SEO页面.md>) · 中成本 · 高影响 · B级证据
- [长尾关键词文章](<./knowledge/weapons/03-content-growth/weapons/028-长尾关键词文章.md>) · 中成本 · 中影响 · C级证据
- [教程型内容](<./knowledge/weapons/03-content-growth/weapons/029-教程型内容.md>) · 高成本 · 高影响 · C级证据
- [行业报告](<./knowledge/weapons/03-content-growth/weapons/030-行业报告.md>) · 中成本 · 中影响 · C级证据
- [免费工具](<./knowledge/weapons/03-content-growth/weapons/031-免费工具.md>) · 低成本 · 中影响 · C级证据
- [YouTube教程](<./knowledge/weapons/03-content-growth/weapons/032-YouTube教程.md>) · 高成本 · 高影响 · B级证据
- [TikTok矩阵](<./knowledge/weapons/03-content-growth/weapons/033-TikTok矩阵.md>) · 中成本 · 高影响 · C级证据
- [Newsletter](<./knowledge/weapons/03-content-growth/weapons/034-Newsletter.md>) · 低成本 · 中影响 · C级证据
- [播客](<./knowledge/weapons/03-content-growth/weapons/035-播客.md>) · 高成本 · 高影响 · B级证据
- [客座博客](<./knowledge/weapons/03-content-growth/weapons/036-客座博客.md>) · 低成本 · 中影响 · C级证据
- [免费电子书](<./knowledge/weapons/03-content-growth/weapons/037-免费电子书.md>) · 中成本 · 中影响 · C级证据
- [案例研究](<./knowledge/weapons/03-content-growth/weapons/038-案例研究.md>) · 中成本 · 高影响 · B级证据
- [模板资源库](<./knowledge/weapons/03-content-growth/weapons/039-模板资源库.md>) · 低成本 · 中影响 · C级证据
- [内容再分发](<./knowledge/weapons/03-content-growth/weapons/040-内容再分发.md>) · 低成本 · 中影响 · C级证据

</details>

<details>
<summary>社区增长（10个）</summary>

- [Discord社区](<./knowledge/weapons/04-community/weapons/041-Discord社区.md>) · 高成本 · 高影响 · C级证据
- [Slack社区](<./knowledge/weapons/04-community/weapons/042-Slack社区.md>) · 中成本 · 高影响 · B级证据
- [用户大使计划](<./knowledge/weapons/04-community/weapons/043-用户大使计划.md>) · 中成本 · 中影响 · C级证据
- [用户共创](<./knowledge/weapons/04-community/weapons/044-用户共创.md>) · 中成本 · 高影响 · B级证据
- [线下Meetup](<./knowledge/weapons/04-community/weapons/045-线下Meetup.md>) · 中成本 · 中影响 · C级证据
- [用户访谈公开化](<./knowledge/weapons/04-community/weapons/046-用户访谈公开化.md>) · 低成本 · 中影响 · C级证据
- [用户故事栏目](<./knowledge/weapons/04-community/weapons/047-用户故事栏目.md>) · 中成本 · 中影响 · C级证据
- [社区挑战赛](<./knowledge/weapons/04-community/weapons/048-社区挑战赛.md>) · 中成本 · 高影响 · B级证据
- [超级用户计划](<./knowledge/weapons/04-community/weapons/049-超级用户计划.md>) · 低成本 · 中影响 · C级证据
- [用户UGC活动](<./knowledge/weapons/04-community/weapons/050-用户UGC活动.md>) · 高成本 · 中影响 · C级证据

</details>

<details>
<summary>产品驱动增长（15个）</summary>

- [Freemium模式](<./knowledge/weapons/05-plg/weapons/051-Freemium模式.md>) · 中成本 · 高影响 · A级证据
- [免费试用](<./knowledge/weapons/05-plg/weapons/052-免费试用.md>) · 低成本 · 中影响 · B级证据
- [无需登录体验](<./knowledge/weapons/05-plg/weapons/053-无需登录体验.md>) · 中成本 · 高影响 · B级证据
- [快速Onboarding](<./knowledge/weapons/05-plg/weapons/054-快速Onboarding.md>) · 中成本 · 高影响 · B级证据
- [产品内引导](<./knowledge/weapons/05-plg/weapons/055-产品内引导.md>) · 低成本 · 中影响 · B级证据
- [模板库](<./knowledge/weapons/05-plg/weapons/056-模板库.md>) · 高成本 · 高影响 · B级证据
- [空状态设计](<./knowledge/weapons/05-plg/weapons/057-空状态设计.md>) · 低成本 · 中影响 · C级证据
- [产品内分享](<./knowledge/weapons/05-plg/weapons/058-产品内分享.md>) · 中成本 · 中影响 · C级证据
- [产品水印](<./knowledge/weapons/05-plg/weapons/059-产品水印.md>) · 高成本 · 高影响 · B级证据
- [团队协作](<./knowledge/weapons/05-plg/weapons/060-团队协作.md>) · 高成本 · 高影响 · B级证据
- [使用量限制触发](<./knowledge/weapons/05-plg/weapons/061-使用量限制触发.md>) · 中成本 · 中影响 · C级证据
- [成果导出传播](<./knowledge/weapons/05-plg/weapons/062-成果导出传播.md>) · 低成本 · 高影响 · A级证据
- [使用报告](<./knowledge/weapons/05-plg/weapons/063-使用报告.md>) · 中成本 · 高影响 · B级证据
- [内置社区入口](<./knowledge/weapons/05-plg/weapons/064-内置社区入口.md>) · 低成本 · 中影响 · C级证据
- [产品内推荐](<./knowledge/weapons/05-plg/weapons/065-产品内推荐.md>) · 中成本 · 中影响 · C级证据

</details>

<details>
<summary>留存增长（10个）</summary>

- [邮件生命周期](<./knowledge/weapons/06-retention/weapons/066-邮件生命周期.md>) · 低成本 · 中影响 · C级证据
- [推送通知](<./knowledge/weapons/06-retention/weapons/067-推送通知.md>) · 低成本 · 中影响 · C级证据
- [连续使用奖励](<./knowledge/weapons/06-retention/weapons/068-连续使用奖励.md>) · 中成本 · 高影响 · B级证据
- [里程碑提示](<./knowledge/weapons/06-retention/weapons/069-里程碑提示.md>) · 低成本 · 中影响 · B级证据
- [数据报告邮件](<./knowledge/weapons/06-retention/weapons/070-数据报告邮件.md>) · 中成本 · 中影响 · B级证据
- [周报/月报](<./knowledge/weapons/06-retention/weapons/071-周报-月报.md>) · 中成本 · 中影响 · B级证据
- [新功能提醒](<./knowledge/weapons/06-retention/weapons/072-新功能提醒.md>) · 低成本 · 中影响 · C级证据
- [用户成就系统](<./knowledge/weapons/06-retention/weapons/073-用户成就系统.md>) · 低成本 · 中影响 · C级证据
- [习惯培养](<./knowledge/weapons/06-retention/weapons/074-习惯培养.md>) · 低成本 · 低影响 · C级证据
- [流失召回](<./knowledge/weapons/06-retention/weapons/075-流失召回.md>) · 高成本 · 高影响 · A级证据

</details>

<details>
<summary>变现增长（10个）</summary>

- [分层定价](<./knowledge/weapons/07-monetization/weapons/076-分层定价.md>) · 中成本 · 中影响 · B级证据
- [使用量计费](<./knowledge/weapons/07-monetization/weapons/077-使用量计费.md>) · 中成本 · 高影响 · B级证据
- [年付折扣](<./knowledge/weapons/07-monetization/weapons/078-年付折扣.md>) · 中成本 · 高影响 · B级证据
- [限时优惠](<./knowledge/weapons/07-monetization/weapons/079-限时优惠.md>) · 中成本 · 高影响 · B级证据
- [功能升级提示](<./knowledge/weapons/07-monetization/weapons/080-功能升级提示.md>) · 高成本 · 高影响 · B级证据
- [捆绑套餐](<./knowledge/weapons/07-monetization/weapons/081-捆绑套餐.md>) · 中成本 · 高影响 · B级证据
- [企业版升级](<./knowledge/weapons/07-monetization/weapons/082-企业版升级.md>) · 低成本 · 中影响 · C级证据
- [增值插件市场](<./knowledge/weapons/07-monetization/weapons/083-增值插件市场.md>) · 低成本 · 中影响 · C级证据
- [付费模板市场](<./knowledge/weapons/07-monetization/weapons/084-付费模板市场.md>) · 中成本 · 高影响 · B级证据
- [Upsell邮件](<./knowledge/weapons/07-monetization/weapons/085-Upsell邮件.md>) · 中成本 · 高影响 · A级证据

</details>

<details>
<summary>付费广告（10个）</summary>

- [Google Ads](<./knowledge/weapons/08-paid-ads/weapons/086-Google Ads.md>) · 中成本 · 中影响 · B级证据
- [Facebook Ads](<./knowledge/weapons/08-paid-ads/weapons/087-Facebook Ads.md>) · 中成本 · 中影响 · B级证据
- [TikTok Ads](<./knowledge/weapons/08-paid-ads/weapons/088-TikTok Ads.md>) · 高成本 · 高影响 · B级证据
- [YouTube Ads](<./knowledge/weapons/08-paid-ads/weapons/089-YouTube Ads.md>) · 高成本 · 高影响 · B级证据
- [再营销广告](<./knowledge/weapons/08-paid-ads/weapons/090-再营销广告.md>) · 低成本 · 中影响 · B级证据
- [Lookalike人群](<./knowledge/weapons/08-paid-ads/weapons/091-Lookalike人群.md>) · 低成本 · 中影响 · C级证据
- [App Store Ads](<./knowledge/weapons/08-paid-ads/weapons/092-App Store Ads.md>) · 低成本 · 中影响 · C级证据
- [KOL投放](<./knowledge/weapons/08-paid-ads/weapons/093-KOL投放.md>) · 中成本 · 中影响 · B级证据
- [联盟营销](<./knowledge/weapons/08-paid-ads/weapons/094-联盟营销.md>) · 中成本 · 中影响 · B级证据
- [Influencer合作](<./knowledge/weapons/08-paid-ads/weapons/095-Influencer合作.md>) · 中成本 · 中影响 · B级证据

</details>

<details>
<summary>品牌增长（8个）</summary>

- [品牌故事](<./knowledge/weapons/09-brand/weapons/096-品牌故事.md>) · 中成本 · 高影响 · C级证据
- [创始人IP](<./knowledge/weapons/09-brand/weapons/097-创始人IP.md>) · 低成本 · 高影响 · B级证据
- [PR媒体](<./knowledge/weapons/09-brand/weapons/098-PR媒体.md>) · 中成本 · 中影响 · C级证据
- [行业大会](<./knowledge/weapons/09-brand/weapons/099-行业大会.md>) · 高成本 · 中影响 · C级证据
- [品牌视觉统一](<./knowledge/weapons/09-brand/weapons/100-品牌视觉统一.md>) · 中成本 · 中影响 · B级证据
- [标志性活动](<./knowledge/weapons/09-brand/weapons/101-标志性活动.md>) · 高成本 · 中影响 · C级证据
- [价值观营销](<./knowledge/weapons/09-brand/weapons/102-价值观营销.md>) · 高成本 · 中影响 · C级证据
- [社会议题](<./knowledge/weapons/09-brand/weapons/103-社会议题.md>) · 低成本 · 中影响 · C级证据

</details>

<details>
<summary>B2B销售（8个）</summary>

- [冷启动外呼](<./knowledge/weapons/10-b2b-sales/weapons/104-冷启动外呼.md>) · 中成本 · 高影响 · C级证据
- [LinkedIn外联](<./knowledge/weapons/10-b2b-sales/weapons/105-LinkedIn外联.md>) · 低成本 · 中影响 · C级证据
- [Webinar](<./knowledge/weapons/10-b2b-sales/weapons/106-Webinar.md>) · 中成本 · 中影响 · C级证据
- [Demo演示](<./knowledge/weapons/10-b2b-sales/weapons/107-Demo演示.md>) · 中成本 · 高影响 · C级证据
- [白皮书下载](<./knowledge/weapons/10-b2b-sales/weapons/108-白皮书下载.md>) · 中成本 · 中影响 · C级证据
- [销售自动化](<./knowledge/weapons/10-b2b-sales/weapons/109-销售自动化.md>) · 低成本 · 高影响 · B级证据
- [客户成功](<./knowledge/weapons/10-b2b-sales/weapons/110-客户成功.md>) · 高成本 · 高影响 · B级证据
- [转介绍计划](<./knowledge/weapons/10-b2b-sales/weapons/111-转介绍计划.md>) · 低成本 · 高影响 · B级证据

</details>

<!-- AUTO-WEAPON-INDEX:END -->


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

# 验证 agents 和索引
python3 scripts/validate-agents.py
python3 scripts/validate-indexes.py
```

| 测试类型 | 覆盖 | 状态 |
|----------|------|------|
| 脚本化主测试 | 96/96 | ✅ |
| CLI 集成测试 | diagnose / assess / match / validate / learn | ✅ |
| Golden 场景回归 | 错阶段 / 错约束 / 错方向 | ✅ |
| Agent / 索引验证 | 结构和知识完整性 | ✅ |

---

## 🚀 产品化优化状态

当前高 ROI 优化状态和活跃 backlog 见 [`docs/optimization-status.md`](./docs/optimization-status.md)。

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

[⬆ 回到顶部](#-oh-my-growth---增长策略外脑)

</div>
