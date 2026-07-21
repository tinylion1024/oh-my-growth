---
name: oh-my-growth
description: 增长策略外脑 - 整合81个案例、111种玩法、12大流派，面向SEO、AEO、GEO和LLM检索输出诊断、优先级判断、实验计划
triggers:
  - /omg-diagnose
  - /omg-assess
  - /omg-design
  - /omg-match
  - /omg-learn
  - /omg-fast-scan
  - /omg-brd
  - /omg-cold-start
  - /omg-retention
  - /omg-monetization
  - /omg-referral
  - /omg-search
  - /omg-validate
metadata:
  author: Growth Master Team
  maturity: production
  version: 1.0.2
  license: MIT
  category: business-strategy
---

# oh-my-growth - 增长策略外脑

**多平台增长决策插件** — 支持 Claude Code、OpenClaw 和 Hermes Agent；主 Skill 可在 Claude Code 会话中直接调用。

将增长知识库、多Agent决策引擎与营销增长方法论包融合，帮助增长负责人完成前 70% 的策略思考。

**核心价值**：从”查阅知识”升级为”先诊断、再判断、后给实验”的增长外脑

## 快速开始

```
/omg-diagnose 我的产品日活下降20%，该怎么办？
/omg-assess 我们准备做裂变，先评估可行性
/omg-design SaaS产品如何设计变现策略？
/omg-match 游戏化留存案例
```

## 所有命令

| 命令 | 描述 | 使用场景 |
|------|------|----------|
| `/omg-diagnose` | 策略诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| `/omg-assess` | 机会可行性评估 | 现状还不够清楚，先做清晰度评估 |
| `/omg-design` | 可落地的策略设计 | 知道要做什么，需要执行路径 |
| `/omg-fast-scan` | 快速判断 | 这个想法靠谱吗？ |
| `/omg-brd` | 完整决策文档 | 需要申请预算/资源 |
| `/omg-match` | 匹配成功案例 | 想看看别人怎么做的 |
| `/omg-learn` | 系统学习路径 | 想深入了解某个增长领域 |
| `/omg-search` | 搜索知识库 | 直接检索案例/玩法/理论 |
| `/omg-validate` | 验证输出文档 | 检查报告完整性 |

### 场景快捷入口

| 命令 | 描述 |
|------|------|
| `/omg-cold-start` | 冷启动场景 - 获取前 100 个用户 |
| `/omg-retention` | 留存场景 - 提升用户留存率 |
| `/omg-monetization` | 变现场景 - 设计变现策略 |
| `/omg-referral` | 裂变场景 - 评估裂变可行性 |

## 核心工作流

详见 [workflow.md](references/workflow.md)

```
用户输入 → 阶段/业务过程定位 → 问题诊断 → 知识检索 → 方法论包匹配 → 优先级判断 → 实验建议 → 输出生成
```

1. **阶段与业务过程定位** → 先判断当前属于产品验证期、增长放大期还是规模经营期，以及问题更偏用户获取还是用户深耕
2. **项目记忆注入** → 结合公司画像、目标用户、历史实验和重复失败模式
3. **问题诊断** → 再判断主目标、北极星指标、最大约束与最可能的主矛盾
4. **知识检索** → Case/Weapon/Theory Agent 检索最相关的案例、打法和理论
5. **方法论包匹配** → 匹配吸收后的 SEO/AEO、GEO/LLM、CRO、Paid Ads、GTM、Lifecycle Email、Referral/RevOps 框架
6. **优先级判断** → 用 ROI、执行复杂度、阶段匹配度、证据加分和失败模式惩罚排序
7. **建议做 / 不做** → 明确指出当前该押注什么，不该分散到什么方向
8. **实验计划** → 输出最小实验、成功信号、停止信号和复盘节奏

## Agent 体系

详见 [agents/](agents/) 目录和 [agent-contract.md](references/agent-contract.md)

### 核心决策Agent

| Agent | 职责 |
|-------|------|
| Lead Agent | 编排协调、问题分类、冲突解决 |
| Growth Agent | 增长机制可行性评估 |
| Monetization Agent | 变现影响评估 |
| ROI Agent | 投资回报计算 |
| Execution Agent | 执行可行性评估 |
| Skeptic Agent | 假设挑战、风险识别 |
| Narrative Agent | 最终文档撰写 |

### 知识驱动Agent

| Agent | 职责 |
|-------|------|
| Case Agent | 从案例库匹配相似案例 |
| Weapon Agent | 从武器库推荐增长玩法 |
| Theory Agent | 引用相关理论流派 |

## 决策规则

详见 [bayesian-decision.md](references/bayesian-decision.md)

**核心原则**：

1. 弱机制 + 弱ROI → 不推荐投入
2. 可行机制 + 低证据 → 推荐小实验
3. 高收益 + 高执行复杂度 → 推荐分阶段推进
4. 短期变现损害长期留存/品牌 → 降低优先级
5. Agent间重大分歧 → 显式呈现分歧，转化为验证问题
6. 有成功案例支撑的机制 → 提升置信度

## 框架配置

```yaml
decision_frameworks:
  bayesian:
    reference: references/bayesian-decision.md
    script: scripts/bayesian_decision.py
    thresholds: { invest: 0.75, experiment: 0.50, collect: 0.30, stop: 0.20 }
  
  gametheory:
    reference: references/gametheory-framework.md
    script: scripts/gametheory_analysis.py
    scenarios: [competitive_response, pricing_strategy, platform_strategy, negotiation]
  
  kelly:
    reference: references/kelly-allocation.md
    script: scripts/kelly_sizing.py
  
  business_model:
    reference: references/business-model.md

quality_assurance:
  clarity_gate:
    reference: references/current-state-clarity.md
    thresholds: { insufficient: 54, workable: 74, clear: 75 }
  
  safety_protocol:
    reference: references/safety-boundaries.md
    domains: [financial, legal, regulatory, operational]

output:
  contract: references/report-contract.md
  schema: references/output-schema.md
```

## 知识库结构

详见 [knowledge-router.md](references/knowledge-router.md)

```
knowledge/
├── cases/           # 81个增长案例（china/overseas/vertical）
├── weapons/         # 111种增长玩法
├── method-packs/    # 营销增长方法论包（吸收外部skill后重写）
├── guides/          # 核心方法论
├── schools/         # 12大流派理论
└── modules/         # 系统学习模块
```

## 置信度声明

明确声明每个建议的置信度：

- **High**：强证据、可测试机制、执行可控
- **Medium**：可行机制但有重要假设
- **Low**：证据稀少、重大未知、无法验证

低置信度建议转化为实验计划，而非全量投入建议。

## 设计原则

1. **决策导向**：目标是决定是否值得投入，不是让想法听起来不错
2. **知识驱动**：每个决策都有案例/理论支撑
3. **因果逻辑**：强制清晰的因果链
4. **早期暴露问题**：在投入前识别风险
5. **证据先行**：证据弱时推荐实验而非全量投入

---

## 引用文件索引

### 核心框架
- [贝叶斯决策框架](references/bayesian-decision.md)
- [博弈论战略框架](references/gametheory-framework.md)
- [Kelly资源分配框架](references/kelly-allocation.md)
- [商业模式分析框架](references/business-model.md)
- [营销增长方法论包](knowledge/method-packs/README.md)

### 质量保障
- [现状清晰度门控](references/current-state-clarity.md)
- [安全边界](references/safety-boundaries.md)
- [问题库](references/question-bank.md)
- [输出契约](references/report-contract.md)

### 工作流与模板
- [工作流定义](references/workflow.md)
- [增长操作框架](references/growth-operating-framework.md)
- [输出模板](references/output-schema.md)
- [Agent契约](references/agent-contract.md)
- [知识检索路由](references/knowledge-router.md)

### 计算脚本
- `scripts/bayesian_decision.py` - 贝叶斯计算
- `scripts/kelly_sizing.py` - Kelly资源计算
- `scripts/gametheory_analysis.py` - 博弈论分析
- `scripts/assess_clarity.py` - 清晰度评估
- `scripts/knowledge_retriever.py` - 知识检索

---

## Claude Code 兼容性

- 在主会话中保持编排逻辑
- 不要假设subagent可以spawn其他subagent
- 使用 `.claude/agents/` 中的项目subagent
- 将此 `SKILL.md` 作为可移植的工作流规则源
