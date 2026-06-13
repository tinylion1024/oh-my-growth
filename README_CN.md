<div align="center">

<img src="./assets/cover.png" alt="oh-my-growth" width="100%">

# 🚀 oh-my-growth - 增长策略外脑

**Claude Code & OpenClaw 专用增长决策插件**

整合 **81个案例** · **111种玩法** · **12大流派** · **完整决策框架**

输入一个增长问题，直接输出：
`阶段判断` · `核心矛盾` · `优先级排序` · `建议做/别做` · `两周实验`

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./VERSION)
[![Tests](https://img.shields.io/badge/tests-84%2F84%20passed-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[安装](#-安装) · [快速开始](#-快速开始) · [核心框架](#-核心框架) · [文档](#-文档)

**[English](./README.md)**

</div>

---

## 💡 这是什么？

**oh-my-growth** 是一个**增长决策插件**，支持 Claude Code 和 OpenClaw。

在 Claude Code 会话中，你可以直接调用专业的增长策略分析能力：

```
/oh-my-growth diagnose 我的产品日活下降20%，该怎么办？
/oh-my-growth assess 我们准备做裂变，先评估可行性
/oh-my-growth design SaaS产品如何设计变现策略？
```

**缩写支持**：也可使用 `/omg` 代替 `/oh-my-growth`

```
/omg diagnose 我的产品日活下降20%，该怎么办？
/omg assess 我们准备做裂变，先评估可行性
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
/oh-my-growth diagnose 测试安装
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

---

## ✨ 快速开始

### 在 Claude Code 中使用

**核心命令：**

```bash
# 策略诊断 - 诊断增长问题并给出优先级排序
/omg diagnose SaaS产品如何获取首批用户
/omg diagnose 我的产品日活下降20%，该怎么办？

# 机会评估 - 评估是否值得深入分析
/omg assess 我们要不要做邀请裂变
/omg assess 我们准备做病毒增长，先评估可行性

# 策略设计 - 可落地的策略方案
/omg design 如何提升月活跃用户留存率
/omg design SaaS产品变现策略

# 案例匹配 - 找成功案例参考
/omg match 游戏化提升用户活跃
/omg match 教育行业裂变增长案例

# 学习路径 - 系统学习路线图
/omg learn 如何系统学习裂变增长
/omg learn B2B SaaS留存策略
```

**快速判断：**

```bash
# 快速扫描 - 快速可行性判断
/omg fast-scan TikTok广告适合我们SaaS吗？

# 决策文档 - 完整决策文档（用于申请预算）
/omg brd 我们要不要投入5万做裂变
```

**工具命令：**

```bash
# 直接搜索知识库
/omg search 病毒增长
/omg search PLG onboarding

# 校验输出文档
/omg validate report.md
```

**场景快捷入口：**

```bash
# 冷启动场景
/omg cold-start AI写作SaaS如何拿到前100个种子用户

# 留存场景
/omg retention 如何提升30日留存率

# 变现场景
/omg monetization SaaS产品如何设计定价

# 裂变场景
/omg referral 我们要不要做邀请裂变
```

### 命令参考

| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `diagnose` | 诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| `assess` | 评估是否值得深入分析 | 现状还不够清楚，先做清晰度评估 |
| `design` | 可落地的策略方案 | 知道要做什么，但不知道怎么设计执行路径 |
| `fast-scan` | 快速判断 | 这个想法靠谱吗？ |
| `brd` | 完整决策文档 | 需要申请预算/资源 |
| `match` | 找成功案例 | 想看看别人怎么做的 |
| `learn` | 系统学习路径 | 想深入了解某个增长领域 |
| `search` | 搜索知识库 | 直接查找案例/玩法/理论 |
| `validate` | 校验输出文档 | 检查报告完整性 |
| `cold-start` | 冷启动场景 | 首批用户获取 |
| `retention` | 留存场景 | 提升用户留存 |
| `monetization` | 变现场景 | 设计变现策略 |
| `referral` | 裂变场景 | 规划裂变方案 |

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
| 脚本化主测试 | 84/84 | ✅ |
| CLI 集成测试 | diagnose / assess / match / validate / learn | ✅ |
| Golden 场景回归 | 错阶段 / 错约束 / 错方向 | ✅ |
| Agent / 索引验证 | 结构和知识完整性 | ✅ |

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
