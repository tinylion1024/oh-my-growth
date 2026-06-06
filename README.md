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
