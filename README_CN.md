<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth

**面向 AI Agent 团队的、带证据的增长决策工具。**

把一个增长问题转成带证据链的优先级排序、**2 周实验**、成功信号和停止条件。

**适合：** 使用 Claude Code、OpenClaw、Hermes 或本地 CLI 的增长负责人、创始人和产品团队。

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-99%2F99%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**[选择安装方式](#-安装)** · **[查看输出示例](#-示例5分钟诊断流程)** · **[English](./README.md)**

</div>

---

## 💡 能解决什么问题?

**当你的 DAU 下降 20% 时,oh-my-growth 帮你:**
1. 3分钟内定位核心矛盾
2. 明确优先级排序
3. 匹配 3 个相似成功案例
4. 生成 2 周实验方案

**全部在 Claude Code、OpenClaw 或 Hermes Agent 中完成。**

### 核心用户画像

| 用户画像 | 常见问题 | 核心命令 | 价值 |
|---------|---------|---------|------|
| 🎯 **增长黑客** | "实验设计缺少案例参考" | `/omg-match` | 秒级找到相似案例 |
| 📊 **产品经理** | "增长策略优先级混乱" | `/omg-diagnose` | 即时获得优先级排序 |
| 🚀 **创业者** | "资源有限不知道从哪下手" | `/omg-cold-start` | 聚焦最高影响动作 |

---

## ✨ 示例：5分钟诊断流程

**用户输入:**
```
/omg-diagnose 我的产品日活下降20%，该怎么办？
```

**oh-my-growth 输出:**
```
┌─────────────────────────────────────────────────────────┐
│  📌 阶段判断                                            │
├─────────────────────────────────────────────────────────┤
│  增长期 · 用户留存问题                                   │
│  北极星指标：周活跃用户                                   │
│                                                         │
│  📌 核心矛盾                                            │
│  不是产品质量问题，而是用户参与闭环断裂                    │
│                                                         │
│  📌 优先级排序                                          │
│  激活核心用户 > 修复新手引导 > 开发新功能                  │
│                                                         │
│  📌 匹配案例（Top 3）                                    │
│  1. Slack 的用户激活策略（匹配度 92%）                    │
│  2. Notion 的核心用户计划（匹配度 87%）                   │
│  3. Duolingo 的连续打卡功能（匹配度 82%）                 │
│                                                         │
│  📌 2周实验方案                                         │
│  1. 向不活跃用户发送个性化价值邮件                        │
│  2. 追踪周活跃用户，而非日活                              │
│  3. 2周内无改善则停止                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 安装

选择你正在使用的平台；以下命令均安装相同的知识库和决策引擎。

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

### 独立 CLI

```bash
python3 -m pip install "git+https://github.com/tinylion1024/oh-my-growth.git"
```

如需隔离安装 CLI，可使用：`pipx install "git+https://github.com/tinylion1024/oh-my-growth.git"`。

### 验证安装

在 Claude Code 中输入:
```
/omg-diagnose 测试安装
```

**支持平台:**
- ✅ Claude Code
- ✅ OpenClaw
- ✅ Hermes Agent
- ✅ 独立 CLI

---

## ✨ 快速开始

### 最常用命令

**策略诊断**（问题不清晰时使用）
```bash
/omg-diagnose SaaS产品如何获取首批1000用户
```

**案例匹配**（需要参考案例时使用）
```bash
/omg-match 教育行业的裂变增长案例
```

**机会评估**（评估可行性时使用）
```bash
/omg-assess 我们是否应该做裂变？
```

**策略设计**（需要执行方案时使用）
```bash
/omg-design 如何提升月活跃用户留存率
```

### 场景快捷命令

```bash
/omg-cold-start      # 冷启动获客
/omg-retention       # 提升留存
/omg-monetization    # 设计变现
/omg-referral        # 规划裂变
```

### Command Reference

核心命令:

- `/omg-assess` - 机会评估
- `/omg-diagnose` - 完整增长诊断
- `/omg-design` - 策略设计
- `/omg-fast-scan` - 快速可行性检查
- `/omg-brd` - 决策 BRD 草稿
- `/omg-match` - 匹配相似案例
- `/omg-learn` - 生成学习路径

辅助命令:

- `/omg-search` - 搜索案例、玩法和理论
- `/omg-validate` - 校验报告质量

场景命令:

- `/omg-cold-start` - 冷启动获客
- `/omg-retention` - 留存诊断
- `/omg-monetization` - 变现设计
- `/omg-referral` - 裂变规划

视图引用:

- `weekly`
- `experiment-card`
- `share`
- `decision-memo`
- `qbr`

---

## 🎯 为什么选择 oh-my-growth？

### 核心差异化优势

| 功能特性 | oh-my-growth | ChatGPT/Claude 原生 | GrowthHackers |
|---------|--------------|-------------------|---------------|
| 结构化知识库 | ✅ 81案例、111玩法、7方法包 | ❌ 无结构化知识 | ✅ 社区案例 |
| 决策引擎 | ✅ 贝叶斯+Kelly+博弈论 | ❌ 无决策框架 | ❌ 无决策框架 |
| 即时诊断 | ✅ 5分钟输出 | ⚠️ 需要多次迭代 | ❌ 手动研究 |
| 可执行输出 | ✅ 2周实验方案 | ⚠️ 泛泛建议 | ❌ 仅案例聚合 |
| AI 驱动 | ✅ RAG 增强 | ✅ 原生 AI | ❌ 非 AI 驱动 |

### 知识库规模

- **81 个案例** — Notion、Airbnb、抖音、GPT-4o、Claude 3.5、拼多多...
- **111 种玩法** — 裂变、PLG、内容增长、留存...
- **12 大理论流派** — 增长黑客、网络效应、PLG...
- **7 个增长方法包** — SEO/AEO、GEO/LLM、CRO、付费获客、GTM、生命周期、转介绍...
- **7 大学习模块** — 冷启动、留存、变现...

[**→ 浏览完整案例索引**](./knowledge/cases/) · [**→ 浏览完整玩法索引**](./knowledge/weapons/)

---

## 📊 输出示例

以下场景用于展示输出结构，**不是客户成果声明**。项目正在收集匿名、可复现的真实使用案例；可参考[案例贡献规范](./CONTRIBUTING.md#添加新案例)提交。

### 案例 1：SaaS 冷启动
**问题：** "AI 写作 SaaS 如何获取首批 1000 用户？"

**oh-my-growth 建议:**
1. 聚焦"Beta 邀请制"（而非广告或裂变）
2. 匹配 3 个案例：Notion、Calendly、Dropbox
3. 2周实验：手动触达 50 个目标用户

**成功信号：** 50 次创始人触达中获得 3 个付费客户

### 案例 2：留存下降
**问题：** "产品更新后日活下降 20%"

**oh-my-growth 诊断:**
1. 核心矛盾：功能困惑，非产品质量
2. 优先级：激活核心用户 > 回滚功能
3. 匹配案例：Slack 的新手引导优化

**成功信号：** 在扩大获客前先提升 D7 留存

### 案例 3：变现策略
**问题：** "B2B SaaS 如何设计定价？"

**oh-my-growth 设计:**
1. 三层定价：免费版 → Pro版($29) → 企业版($299)
2. 匹配案例：Notion、Linear、Slack
3. 核心原则：免费版做 PLG，Pro版做收入

**成功信号：** 在全量上线前验证付费意愿与留存护栏

---

## 🛠️ 高级功能

### 决策引擎

**贝叶斯决策框架:**
```bash
/omg-assess 我们是否应该投入5万做裂变？
```
- 评估证据强度（A/B/C/D 级）
- 计算成功概率
- 推荐决策：运行实验 / 需要更多数据 / 不建议投资

**Kelly 分配:**
```bash
/omg-design 如何分配增长预算？
```
- 跨渠道最优资源配置
- 风险调整后的实验规模

### 知识路由器

自动将你的问题路由到正确的知识库:
- 案例数据库（81 个案例）
- 玩法数据库（111 种玩法）
- 理论数据库（12 大流派）
- 方法包数据库（7 个增长操作系统）

### 输出验证

```bash
/omg-validate my-strategy-report.md
```
检查报告是否覆盖:
- ✅ 核心矛盾已识别
- ✅ 优先级排序已提供
- ✅ 2周实验已定义
- ✅ 成功指标已明确

---

## 📚 文档

- **[完整命令参考](./docs/COMMANDS.md)** — 所有命令、视图和输出模式
- **[GEO / LLM 发现用例](./docs/use-cases/geo-llm-discovery.md)** — AI 搜索可见性工作流
- **[SEO / AEO 增长诊断](./docs/use-cases/seo-growth-diagnosis.md)** — 自然获客工作流
- **[案例库](./knowledge/cases/)** — 增长案例和索引示例
- **[增长玩法库](./knowledge/weapons/)** — 验证过的增长玩法
- **[理论框架](./knowledge/schools/)** — 增长理论流派
- **[API 文档](./docs/API.md)** — CLI 契约、检索入口和输出视图

## ❓ 常见问题

### 什么是 oh-my-growth？

oh-my-growth 是一个增长策略外脑，把结构化知识库、多 Agent 决策逻辑和实验计划结合起来，用于获客、留存、变现和裂变分析。

### 它适合谁？

适合增长运营、创始人、产品经理，以及需要稳定增长答案的 AI 助手。

### 为什么这有助于 SEO 和 GEO？

仓库现在有更明确的关键词、命令引用、标准化文档和 `llms.txt` 入口，agent 和大模型更容易理解项目用途。对 Google 这类搜索来说，GEO/AEO 仍然要建立在可抓取、有价值、结构清晰的 SEO 内容之上。

---

## 🌟 社区

- **GitHub Issues：** 报告问题、请求案例或提出改进建议。
- **GitHub Discussions：** 分享使用案例或交流执行经验。
- **案例贡献：** 按[贡献指南](./CONTRIBUTING.md)提交匿名、有证据支撑的案例。
- **Twitter/X：** [@ohmygrowth](https://twitter.com/ohmygrowth)。

---

## 📈 路线图

当前优先级与参与方式请见[公开路线图](./docs/ROADMAP.md)。

### 2026 Q3
- [ ] Web UI（非技术用户友好）
- [ ] 向量化案例搜索（语义匹配）
- [ ] 团队协作功能

### 2026 Q4
- [ ] Pro 版本（$29/月）
- [ ] 自定义案例库
- [ ] API 访问

### 2027
- [ ] 企业版本（$299/月）
- [ ] 私有化部署
- [ ] 高级分析仪表盘

---

## 🤝 贡献

欢迎贡献！参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

**贡献方式:**
- 📝 添加新的增长案例
- 🛠️ 改进决策引擎
- 📖 翻译文档
- 🐛 报告 Bug

---

## 📄 许可证

MIT 许可证 — 详见 [LICENSE](./LICENSE)。

---

## 🙏 致谢

灵感来源:
- **GrowthHackers** — 社区驱动的增长知识
- **Reforge** — 增长策略框架
- **OpenAI ChatGPT** — AI 驱动的推理能力

特别感谢所有贡献者和案例作者。

---

<div align="center">

**[选择安装方式](#-安装)** · **[阅读完整文档](./docs/)** · **[贡献案例](./CONTRIBUTING.md)**

由 Growth Master Team 用 ❤️ 打造

</div>
