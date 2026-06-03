---
name: growth-master-skill
description: 智能增长顾问 - 知识驱动的增长决策系统。整合77个案例、111种玩法、12大流派，通过多Agent协作生成决策BRD、策略方案、案例推荐。适用于增长评估、策略设计、知识学习、方案审计、案例匹配等场景。
metadata:
  author: Growth Master Team
  maturity: production-scaffold
  public_release: sanitized
  version: 1.1.0
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
- 使用多Agent协作生成决策BRD
- 进行现状清晰度门控评估
- 输出标准化报告（10个必需章节）

## Do Not Route Here

- 纯理论讨论，没有具体业务场景
- 最终投资建议（提供框架，不提供决策）
- 法律合规结论（提供风险清单，不提供合规判断）
- 医疗、心理危机等专业领域建议
- 无需诊断或行动报告的头脑风暴
- 矛盾论文本解读，无实际案例
- 历史或意识形态评论

## 核心架构

```
用户输入 → 问题理解 → 知识检索 → 多Agent评估 → 冲突解决 → 输出生成
              │            │            │            │           │
           Lead Agent   知识Agent群   决策Agent群   Lead Agent  Narrative
         (Case/Weapon/  (Growth/ROI/
          Theory)       Skeptic/...)
```

## 五大模式

### 1. Fast Scan (快速扫描)

**适用**：初步想法、快速判断、证据不足时

**Agent组合**：Lead + ROI + Skeptic + (可选)Case

**输出**：
- 一句话建议
- 核心理由（2-3点）
- 主要风险
- 下一步行动

### 2. Decision BRD (决策文档)

**适用**：需要预算/资源/人力的正式决策

**Agent组合**：Lead + Growth + Monetization + ROI + Execution + Skeptic + Narrative + Case + Weapon

**输出**：
- 执行摘要
- 业务问题与机会
- 提议机制与因果链
- ROI逻辑（基础/乐观/悲观）
- 资源需求
- 关键假设
- 风险与反对意见
- 决策与下一步

### 3. Strategy Design (策略设计)

**适用**：需要具体增长策略和玩法组合

**Agent组合**：Lead + Growth + Weapon + Theory + Narrative

**输出**：
- 策略方向
- 推荐玩法组合（来自武器库）
- 成功案例参考
- 实施路径
- 关键指标

### 4. Case Match (案例匹配)

**适用**：寻找可借鉴的成功案例

**Agent组合**：Lead + Case + Theory

**输出**：
- 匹配案例列表
- 各案例核心策略
- 可复制要点
- 注意事项

### 5. Learning Path (学习路径)

**适用**：系统学习增长知识

**Agent组合**：Lead + Theory + Narrative

**输出**：
- 推荐学习模块
- 相关理论流派
- 案例+玩法组合
- 进阶路径

## 核心工作流

### Step 1: 问题理解与分类

Lead Agent 分析用户输入：

- **问题类型**：acquisition / activation / retention / resurrection / referral / pricing / monetization / hybrid
- **业务阶段**：0→1 / 1→10 / 10→100
- **行业特征**：电商 / SaaS / 社交 / 内容 / 金融 / ...
- **模式选择**：根据问题复杂度和用户意图选择模式

### Step 2: 知识检索

知识Agent群协作检索：

```
Case Agent    → 匹配相似成功案例
Weapon Agent  → 推荐适用增长玩法
Theory Agent  → 引用相关理论流派
```

输出：`Knowledge Context = {cases, weapons, theories}`

### Step 3: 多Agent评估

决策Agent群并行评估：

```
Growth Agent       → 增长机制可行性
Monetization Agent → 变现影响评估
ROI Agent          → 投资回报计算
Skeptic Agent      → 假设挑战与风险识别
Execution Agent    → 执行可行性评估
```

每个Agent接收Knowledge Context作为输入，输出遵循统一Schema。

### Step 4: 冲突解决

Lead Agent 汇总各Agent输出：

- 归类：共识 / 分歧 / 不确定
- 冲突解决原则：
  - 怀疑优先：因果链弱时，Skeptic胜出
  - ROI优先：收益不确定时，ROI胜出
  - 执行优先：资源不现实时，Execution胜出
  - 知识佐证：有案例支撑的论点权重更高

### Step 5: 输出生成

Narrative Agent 生成最终文档，格式见 [output-schema.md](references/output-schema.md)

## Agent 体系

### 核心决策Agent (来自growth-decision-brd)

| Agent | 职责 |
|-------|------|
| Lead Agent | 编排协调、问题分类、冲突解决 |
| Growth Agent | 增长机制可行性评估 |
| Monetization Agent | 变现影响评估 |
| ROI Agent | 投资回报计算 |
| Execution Agent | 执行可行性评估 |
| Skeptic Agent | 假设挑战、风险识别 |
| Narrative Agent | 最终文档撰写 |

### 知识驱动Agent (新增)

| Agent | 职责 |
|-------|------|
| Case Agent | 从案例库匹配相似案例 |
| Weapon Agent | 从武器库推荐增长玩法 |
| Theory Agent | 引用相关理论流派 |

详细定义见 [agents/](agents/) 目录。

## 知识库结构

整合自 growth-skill 知识库：

```
knowledge/
├── cases/           # 77个增长案例
│   ├── china/       # 中国案例
│   ├── overseas/    # 海外案例
│   └── vertical/    # 垂直行业案例
├── weapons/         # 111种增长玩法
├── guides/          # 核心方法论
├── schools/         # 12大流派理论
└── modules/         # 系统学习模块
```

知识检索路由见 [knowledge-router.md](references/knowledge-router.md)

## 决策规则

使用以下默认规则（除非用户指定其他政策）：

1. **弱机制 + 弱ROI** → 不推荐投入
2. **可行机制 + 低证据** → 推荐小实验
3. **高收益 + 高执行复杂度** → 推荐分阶段推进
4. **短期变现损害长期留存/品牌** → 降低优先级（除非收益异常高）
5. **变现收益依赖损害激活/留存的产品变更** → 推荐分阶段实验
6. **Agent间重大分歧** → 显式呈现分歧，转化为验证问题
7. **有成功案例支撑的机制** → 提升置信度
8. **激励机制缺少防滥用设计** → 降级为实验或要求补充

## 输出标准

每个输出帮助决策者回答：

1. 解决什么业务问题？
2. 为什么是现在？
3. 为什么这个机制会有效？
4. 预期ROI是多少？
5. 需要什么资源？
6. 主要风险和反对意见是什么？
7. 应该投资、小试、还是停止？

## 置信度政策

明确声明置信度：

- **High**：强证据、可测试机制、执行可控
- **Medium**：可行机制但有重要假设
- **Low**：证据稀少、重大未知、无法验证

低置信度建议转化为实验计划，而非全量投入建议。

## Claude Code 兼容性

- 在主会话中保持编排逻辑
- 不要假设subagent可以spawn其他subagent
- 使用 `.claude/agents/` 中的项目subagent
- 将此 `SKILL.md` 作为可移植的工作流规则源

## 安装

```bash
# 复制到Claude技能目录
cp -R growth-master ~/.claude/skills/

# 安装Claude Agent模板到项目
./scripts/install.sh /path/to/project
```

## 文件结构

```
growth-master/
├── SKILL.md                    # 本文件 - 主技能定义
├── agents/
│   ├── core/                   # 核心决策Agent
│   │   ├── lead-agent.md
│   │   ├── growth-agent.md
│   │   ├── monetization-agent.md
│   │   ├── roi-agent.md
│   │   ├── execution-agent.md
│   │   ├── skeptic-agent.md
│   │   └── narrative-agent.md
│   ├── knowledge/              # 知识驱动Agent
│   │   ├── case-agent.md
│   │   ├── weapon-agent.md
│   │   └── theory-agent.md
│   └── openai.yaml             # UI元数据
├── knowledge/                  # 知识库
├── references/
│   ├── workflow.md             # 路由与工作流
│   ├── output-schema.md        # 输出模板
│   ├── agent-contract.md       # Agent契约
│   ├── knowledge-router.md     # 知识检索路由
│   └── prompt-templates.md     # 提示模板
├── scripts/
│   └── install.sh
└── README.md
```

## 设计原则

1. **决策导向**：目标是决定是否值得投入，不是让想法听起来不错
2. **知识驱动**：每个决策都有案例/理论支撑
3. **因果逻辑**：强制清晰的因果链
4. **早期暴露问题**：在投入前识别风险
5. **证据先行**：证据弱时推荐实验而非全量投入

---

## Decision Gates

现状清晰度门控，避免信息不足时盲目诊断。

```yaml
decision_gates:
  current_state_clarity:
    enabled: true
    reference: "references/current-state-clarity.md"
    dimensions:
      - goal_success: 20      # 目标与成功标准
      - facts_evidence: 20    # 事实与证据
      - stage: 12             # 阶段判断
      - scarce_resources: 12  # 稀缺资源
      - hard_constraints: 12  # 硬约束
      - stakeholders: 8       # 相关方
      - repeated_patterns: 8  # 重复模式
    thresholds:
      insufficient: 54        # 停止诊断，追问最多 3 个问题
      workable: 74            # 临时判断，问剩余问题
      clear: 75               # 深入诊断，输出完整报告
    hard_requirements:
      - goal_with_deadline_or_metric
      - at_least_2_facts_observed_or_estimated
      - scarce_resources_identified
      - hard_constraints_identified
```

**门控行为**：

| 清晰度等级 | 分数范围 | 行动 |
|-----------|---------|------|
| insufficient | 0-54 | 不输出主要结论，问最多 3 个关键问题 |
| workable | 55-74 | 输出临时判断（标记为临时），问剩余问题 |
| clear | 75-100 | 重述现状快照，请用户确认后深入诊断 |

---

## Safety Protocol

安全边界机制，避免高风险建议。

```yaml
safety_protocol:
  enabled: true
  reference: "references/safety-boundaries.md"
  check_triggers: true
  block_high_risk_recommendations: true
  require_professional_disclaimer: true
  domains:
    financial:
      triggers: ["投资", "融资", "估值", "定价", "重大支出", "股权", "并购"]
      response: "提供决策框架，不提供最终投资建议"
      warning: "重大财务决策建议咨询专业顾问"
    legal:
      triggers: ["合规", "合同", "知识产权", "竞争法", "监管", "诉讼"]
      response: "提供风险清单和准备问题，不提供法律建议"
      warning: "法律风险建议咨询律师"
    regulatory:
      triggers: ["牌照", "数据合规", "隐私保护", "反垄断", "税务"]
      response: "提供合规检查清单，不提供合规结论"
      warning: "监管合规建议咨询专业机构"
    operational:
      triggers: ["裁员", "重大组织变更", "品牌危机", "核心业务调整"]
      response: "提供分析框架和选项，不提供执行建议"
      warning: "重大运营决策建议咨询专业顾问"
```

**响应规则**：

1. 检测到高风险领域时，添加警告声明
2. 不让高评分覆盖硬安全边界
3. 高风险案例的行动建议必须可逆、保守、审查导向

---

## Output Contract

输出契约，确保报告一致性。

```yaml
output_contract:
  reference: "references/report-contract.md"
  principle:
    - 结论在前，推理在后
    - 概念术语后紧跟实用翻译
    - 标记事实为 observed/estimated/assumed
    - 每个行动必须说明改变什么
  required_sections:
    - id: conclusion
      user_title: "先看结论"
      required: true
    - id: current_state
      user_title: "先把现状说清楚"
      required: true
    - id: clarity_assessment
      user_title: "现状够不够清楚"
      required: true
    - id: decision_process
      user_title: "判断过程"
      required: true
    - id: recommendation
      user_title: "推荐方案"
      required: true
    - id: resource_allocation
      user_title: "时间、精力、资源应该怎么重新分配"
      required: true
    - id: actions
      user_title: "接下来怎么做"
      required: true
    - id: projection
      user_title: "做完以后可能怎样"
      required: true
    - id: review_trigger
      user_title: "什么时候回头看"
      required: true
    - id: caveats
      user_title: "注意事项"
      required: true
```

**用户友好标题映射**：

| 概念术语 | 用户友好标题 |
|---------|------------|
| 主要矛盾 | 最关键的卡点 |
| 次要矛盾 | 先不主攻，但要盯住 |
| 矛盾主要方面 | 现在最影响局面的一侧 |
| 概率推演 | 做完以后可能怎样 |
| 监控阈值 | 什么时候回头看 |

---

## Bayesian Decision

贝叶斯决策系统：将不确定的增长决策转化为可审计的概率推理过程。

```yaml
bayesian_decision:
  enabled: true
  reference: "references/bayesian-decision.md"
  script: "scripts/bayesian_decision.py"

  # 核心流程
  workflow:
    - set_hypothesis      # 设置待验证假设
    - set_prior           # 设置先验概率
    - collect_evidence    # 收集证据
    - update_posterior    # 更新后验概率
    - compare_thresholds  # 比较行动阈值
    - recommend_action    # 推荐行动

  # 默认先验规则
  default_priors:
    new_mechanism: 0.20      # 全新机制，无案例
    similar_case: 0.35       # 有相似案例，不同行业
    same_industry: 0.50      # 有同行业案例
    multiple_cases: 0.65     # 有多个成功案例
    internal_data: 0.75      # 有内部实验数据

  # 证据更新幅度（与知识库证据分级一致）
  evidence_tiers:
    A: 0.25  # 元分析、系统综述、官方统计
    B: 0.15  # 同行评审、行业报告、标杆数据
    C: 0.10  # 专家意见、内部数据
    D: 0.05  # LLM建议、类比、常识
    E: 0.00  # 博客、营销文案（不更新）

  # 行动阈值
  action_thresholds:
    invest_now: 0.75        # 后验 ≥ 75% → 直接投入资源
    run_experiment: 0.50    # 后验 50-75% → 小规模实验
    collect_evidence: 0.30  # 后验 30-50% → 继续收集证据
    stop: 0.20              # 后验 < 20% → 停止考虑

  # 多轮迭代
  iteration:
    max_rounds: 5
    diminishing_returns: [1.0, 0.7, 0.5, 0.3]  # 同向证据递减系数
    termination_conditions:
      - "后验 ≥ invest_now 阈值"
      - "后验 < stop 阈值"
      - "达到最大轮数"
      - "无新证据可收集"

  # 敏感性分析
  sensitivity:
    required_questions:
      - "什么证据会让结论反转？"
      - "先验变化多少会影响决策？"
      - "最脆弱的假设是什么？"
      - "如果最佳证据被推翻，结论会怎样？"

  # 安全边界
  safety:
    max_reportable_confidence: 0.95  # 最高报告置信度
    high_risk_threshold_boost: 0.10  # 高风险场景阈值提升
```

**贝叶斯决策输出示例**：

```json
{
  "hypothesis": "邀请裂变能带来有效增长",
  "prior": 0.35,
  "evidence": [
    {"source": "Notion案例", "tier": "B", "direction": "support", "update": 0.15},
    {"source": "SaaS基准", "tier": "B", "direction": "support", "update": 0.10}
  ],
  "posterior": 0.52,
  "decision": "run_experiment",
  "readiness_score": 52,
  "recommendation": "推荐小规模实验，验证关键假设"
}
```

---

## Game Theory Framework

博弈论战略框架：分析竞争、定价、谈判等战略互动。

```yaml
gametheory_framework:
  enabled: true
  reference: "references/gametheory-framework.md"

  # 适用场景
  scenarios:
    - competitive_response:  # 竞争反应
        question: "对手会怎么反应？"
        frameworks: ["prisoner_dilemma", "cournot_competition"]
    
    - pricing_strategy:      # 定价博弈
        question: "如何定价不会被跟进？"
        frameworks: ["signaling_game", "commitment_game"]
    
    - platform_strategy:     # 平台博弈
        question: "双边市场如何启动？"
        frameworks: ["two_sided_market", "network_effects"]
    
    - negotiation:           # 谈判博弈
        question: "如何分配利益？"
        frameworks: ["bargaining_game"]
    
    - alliance:              # 联盟博弈
        question: "合作还是背叛？"
        frameworks: ["cooperative_game", "shapley_value"]

  # 核心分析工具
  analysis_tools:
    - payoff_matrix: "收益矩阵构建"
    - nash_equilibrium: "纳什均衡分析"
    - commitment_check: "承诺可信性检验"
    - signal_quality: "信号质量评估"
    - historical_calibration: "历史行为校准"
```

---

## Kelly Allocation Framework

Kelly 资源分配框架：计算最优投入比例。

```yaml
kelly_allocation:
  enabled: true
  reference: "references/kelly-allocation.md"

  # Kelly 公式
  formula: "f* = (bp - q) / b"

  # 核心原则
  principles:
    - "默认使用分数 Kelly（1/2 或 1/4）"
    - "公式不是主要产品，行动计划才是"
    - "包含加仓、止损、复盘条件"

  # 适用判断
  suitability_check:
    suitable:
      - "可重复实验"
      - "有反馈机制"
      - "下限风险可控"
    not_suitable:
      - "不可逆决策"
      - "无下限风险"
      - "概率完全未知"

  # 输出
  output:
    - kelly_fraction: "Kelly 比例"
    - action_package: "最小行动包"
    - add_conditions: "加仓条件"
    - stop_conditions: "止损条件"
```

---

## Extended Frameworks

扩展框架：集成更多专业能力。

```yaml
extended_frameworks:
  # 商业模式分析
  business_model:
    reference: "references/business-model.md"
    features:
      - business_model_canvas
      - revenue_model_analysis
      - competitor_analysis
      - ai_upgrade_paths

  # 以下框架待实现，暂不可用
  # # 教程生产
  # tutorial_production:
  #   reference: "references/tutorial-production.md"
  #   features:
  #     - module_design
  #     - visual_enhancement
  #     - multi_format_export

  # # 个性化学习
  # learning_builder:
  #   reference: "references/learning-builder.md"
  #   features:
  #     - learner_profile
  #     - authority_first_resources
  #     - personalized_curriculum

  # # Web 安全审计
  # websecurity_audit:
  #   reference: "references/websecurity-audit.md"
  #   features:
  #     - vulnerability_scanning
  #     - security_reporting
  #     - owasp_top10

  # # 微信读书报告
  # weread_report:
  #   reference: "references/weread-report.md"
  #   features:
  #     - reading_analytics
  #     - visualization
  #     - report_generation

  # # 版权管理
  # copyright_management:
  #   reference: "references/copyright-management.md"
  #   features:
  #     - copyright_header_management
  #     - license_compliance

  # # 技能同步
  # skills_sync:
  #   reference: "references/skills-sync.md"
  #   features:
  #     - open_source_evaluation
  #     - catalog_management

  # # 安全测试
  # security_test:
  #   reference: "references/security-test-skills.md"
  #   features:
  #     - code_review
  #     - dependency_check
  #     - tech_selection_security
```

---

## Reference Map

### 核心决策框架
- `references/bayesian-decision.md`: 贝叶斯决策框架 ⭐
- `references/gametheory-framework.md`: 博弈论战略框架 ⭐
- `references/kelly-allocation.md`: Kelly 资源分配框架 ⭐
- `references/business-model.md`: 商业模式分析框架 ⭐

### 质量保障机制
- `references/current-state-clarity.md`: 现状清晰度门控
- `references/safety-boundaries.md`: 安全边界
- `references/question-bank.md`: 问题库
- `references/report-contract.md`: 输出契约
- `references/workflow.md`: 工作流定义
- `references/output-schema.md`: 输出模板
- `references/agent-contract.md`: Agent 契约
- `references/knowledge-router.md`: 知识检索路由
- `references/visualization.md`: 可视化组件

### 扩展框架（待实现）
# 以下框架文件尚未创建，待后续实现：
# - `references/tutorial-production.md`: 教程生产框架
# - `references/learning-builder.md`: 学习教程构建框架
# - `references/websecurity-audit.md`: Web 安全审计框架
# - `references/weread-report.md`: 微信读书报告框架
# - `references/copyright-management.md`: 版权管理框架
# - `references/skills-sync.md`: 技能同步框架
# - `references/security-test-skills.md`: 安全测试技能框架

### 计算脚本
- `scripts/bayesian_decision.py`: 贝叶斯计算脚本 ⭐
- `scripts/kelly_sizing.py`: Kelly 资源计算脚本 (待实现)
- `scripts/gametheory_analysis.py`: 博弈论分析脚本 (待实现)
- `references/output-schema.md`: 输出模板
- `references/agent-contract.md`: Agent 契约
- `references/knowledge-router.md`: 知识检索路由
- `references/visualization.md`: 可视化组件
