---
name: growth-master-skill
description: 智能增长顾问 - 知识驱动的增长决策系统。整合87个案例、111种玩法、12大流派，通过多Agent协作生成决策BRD、策略方案、案例推荐。
metadata:
  author: Growth Master Team
  maturity: production
  version: 1.3.0
  license: MIT
---

# Growth Master - 智能增长顾问

将增长知识库与多Agent决策引擎融合，提供端到端的增长解决方案。

**核心价值**：从"查阅知识"升级为"智能增长顾问"

## Use This Skill For

- 评估增长/变现机会，判断是否值得投入资源
- 设计增长策略，获得具体的玩法组合和实施路径
- 学习增长知识，获取案例、理论、方法论的系统性指引
- 审计现有方案，识别风险和改进空间
- 匹配成功案例，找到可借鉴的参考

## Do Not Route Here

- 纯理论讨论，没有具体业务场景
- 最终投资建议（提供框架，不提供决策）
- 法律合规结论（提供风险清单，不提供合规判断）
- 医疗、心理危机等专业领域建议
- 无需诊断或行动报告的头脑风暴

## 五大模式

| 模式 | 适用场景 | Agent组合 | 输出模板 |
|------|----------|-----------|----------|
| Fast Scan | 快速判断、证据不足 | Lead + ROI + Skeptic | [快速扫描模板](references/output-schema.md#fast-scan) |
| Decision BRD | 正式决策、需预算审批 | 全Agent协作 | [决策文档模板](references/output-schema.md#decision-brd) |
| Strategy Design | 具体策略设计 | Lead + Growth + Weapon + Theory | [策略设计模板](references/output-schema.md#strategy-design) |
| Case Match | 寻找参考案例 | Lead + Case + Theory | [案例匹配模板](references/output-schema.md#case-match) |
| Learning Path | 系统学习增长知识 | Lead + Theory + Narrative | [学习路径模板](references/output-schema.md#learning-path) |

## 核心工作流

详见 [workflow.md](references/workflow.md)

```
用户输入 → 问题理解 → 知识检索 → 多Agent评估 → 冲突解决 → 输出生成
```

1. **问题理解** → Lead Agent 分析问题类型、业务阶段、行业特征，选择模式
2. **知识检索** → Case/Weapon/Theory Agent 从知识库检索相关案例、玩法、理论
3. **多Agent评估** → Growth/Monetization/ROI/Execution/Skeptic 并行评估
4. **冲突解决** → Lead Agent 汇总归类（共识/分歧/不确定），按优先级规则解决
5. **输出生成** → Narrative Agent 生成标准化报告

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
├── cases/           # 87个增长案例（china/overseas/vertical）
├── weapons/         # 111种增长玩法
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

### 质量保障
- [现状清晰度门控](references/current-state-clarity.md)
- [安全边界](references/safety-boundaries.md)
- [问题库](references/question-bank.md)
- [输出契约](references/report-contract.md)

### 工作流与模板
- [工作流定义](references/workflow.md)
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
