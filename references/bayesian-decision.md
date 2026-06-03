# Bayesian Decision Framework

贝叶斯决策框架：将不确定的增长决策转化为可审计的概率推理过程。

---

## 一、核心概念

### 1.1 贝叶斯决策流程

```
初始假设 → 设置先验概率 → 收集证据 → 更新后验概率 → 比较行动阈值 → 推荐行动
     ↑                                          ↓
     └──────────── 多轮迭代 ←───────────────────┘
```

### 1.2 关键术语

| 术语 | 说明 | 示例 |
|------|------|------|
| **Hypothesis (假设)** | 待验证的增长命题 | "邀请裂变能带来有效增长" |
| **Prior (先验)** | 初始置信度 (0-1) | 0.3 (低置信度开始) |
| **Evidence (证据)** | 支持或反对假设的信息 | 案例数据、行业报告、实验结果 |
| **Likelihood (似然)** | 证据在假设成立时出现的概率 | P(证据\|假设成立) |
| **Posterior (后验)** | 更新后的置信度 | 0.65 (证据支持后) |
| **Action Threshold (行动阈值)** | 触发决策的置信度边界 | ≥0.75 → 投入资源 |

---

## 二、先验概率设置

### 2.1 默认先验规则

| 场景类型 | 默认先验 | 理由 |
|----------|---------|------|
| 全新机制，无案例 | 0.20 | 高不确定性 |
| 有相似案例，但不同行业 | 0.35 | 可参考性有限 |
| 有同行业案例 | 0.50 | 中等可信度 |
| 有多个成功案例 | 0.65 | 强参考支撑 |
| 有内部实验数据 | 0.75 | 高可信度 |

### 2.2 先验卫生检查

在设置先验前，必须检查：

```yaml
prior_hygiene_checklist:
  - anchor_to_evidence: "先验是否锚定到具体证据？"
  - avoid_overconfidence: "先验是否避免了过度自信？（默认不超过0.75）"
  - state_assumptions: "是否明确声明了假设？"
  - consider_base_rate: "是否考虑了基础概率？"
  - acknowledge_uncertainty: "是否承认不确定性？"
```

### 2.3 弱先验原则

**默认从弱先验开始**（0.2-0.4），避免过早锁定判断：

```yaml
weak_prior_policy:
  principle: "从不完整输入开始，先给弱先验"
  default_prior: 0.30
  max_initial_prior: 0.50
  rationale: "让证据说话，而非预设立场"
```

---

## 三、证据分级与更新幅度

### 3.1 证据等级定义

| 等级 | 定义 | 更新幅度 | 示例 |
|------|------|---------|------|
| **A** | 元分析、系统综述、官方统计 | ±0.25 | 学术研究、平台经济学分析 |
| **B** | 同行评审、行业报告、标杆数据 | ±0.15 | Notion 增长案例、SaaS 基准 |
| **C** | 结构化专家意见、内部数据 | ±0.10 | 内部实验结果、专家访谈 |
| **D** | LLM 建议、类比、常识 | ±0.05 | 非正式启发式 |
| **E** | 博客、营销文案、未注明来源 | ±0.00 | 不作为更新依据 |

### 3.2 更新方向

| 证据方向 | 说明 | 更新操作 |
|----------|------|----------|
| **支持假设** | 证据与假设一致 | posterior = prior + update |
| **反对假设** | 证据与假设矛盾 | posterior = prior - update |
| **中性** | 证据无关或矛盾 | posterior = prior (不更新) |

### 3.3 更新幅度计算

```python
def calculate_update(evidence_tier: str, evidence_direction: str, prior: float) -> float:
    """计算证据更新幅度"""
    tier_updates = {
        "A": 0.25,
        "B": 0.15,
        "C": 0.10,
        "D": 0.05,
        "E": 0.00
    }
    
    base_update = tier_updates.get(evidence_tier, 0.05)
    
    # 边界保护：后验不超过 [0.05, 0.95]
    if evidence_direction == "support":
        return min(base_update, 0.95 - prior)
    elif evidence_direction == "oppose":
        return min(base_update, prior - 0.05)
    else:
        return 0.0
```

### 3.4 多证据组合

当有多条证据时，采用**保守累积策略**：

```yaml
evidence_combination:
  strategy: "conservative"  # 保守策略
  
  rules:
    - "同向证据：幅度递减（第一条100%，第二条70%，第三条50%）"
    - "反向证据：完整抵消"
    - "冲突证据：取最弱证据方向"
  
  formula: |
    累积更新 = Σ(单条更新 × 递减系数)
    
    其中递减系数：
    - 第1条同向证据：1.0
    - 第2条同向证据：0.7
    - 第3条同向证据：0.5
    - 第4条及以后：0.3
```

---

## 四、行动阈值

### 4.1 默认阈值设置

| 阈值 | 后验范围 | 行动 | 说明 |
|------|---------|------|------|
| **invest_now** | ≥ 0.75 | 直接投入资源 | 高置信度，可执行 |
| **run_experiment** | 0.50 - 0.74 | 小规模实验 | 中等置信度，需要验证 |
| **collect_evidence** | 0.30 - 0.49 | 继续收集证据 | 低置信度，信息不足 |
| **stop** | < 0.30 | 停止考虑 | 极低置信度，不推荐 |

### 4.2 阈值调整规则

```yaml
threshold_adjustment:
  # 高风险场景：提高阈值
  high_risk:
    triggers: ["财务风险", "法律风险", "品牌风险"]
    invest_now: 0.85      # 提高到 0.85
    run_experiment: 0.60
  
  # 低成本场景：降低阈值
  low_cost:
    triggers: ["预算<1万", "可逆操作", "无品牌风险"]
    invest_now: 0.65      # 降低到 0.65
    run_experiment: 0.40
```

### 4.3 决策输出

```yaml
decision_output:
  when_posterior_>=_invest_now:
    recommendation: "推荐投入资源"
    action: "制定执行计划，分配预算和人力"
    confidence: "高"
  
  when_posterior_in_run_experiment:
    recommendation: "推荐小规模实验"
    action: "设计 MVP，验证关键假设"
    confidence: "中"
  
  when_posterior_in_collect_evidence:
    recommendation: "继续收集证据"
    action: "列出待收集证据清单，设计调研方案"
    confidence: "低"
  
  when_posterior_<_stop:
    recommendation: "不推荐继续"
    action: "记录决策理由，转向其他机会"
    confidence: "低"
```

---

## 五、多轮迭代机制

### 5.1 迭代日志结构

```yaml
iteration_log:
  round_1:
    hypothesis: "邀请裂变能带来有效增长"
    prior: 0.30
    evidence_collected:
      - source: "Notion 案例"
        tier: "B"
        direction: "support"
        update: +0.15
      - source: "内部用户画像"
        tier: "C"
        direction: "support"
        update: +0.07
    posterior: 0.52
    readiness_score: 52  # 等于 posterior × 100
    decision: "run_experiment"
    remaining_gaps: ["病毒系数未知", "奖励成本未测算"]
    next_questions:
      - "目标用户的邀请意愿有多强？"
      - "每个邀请的成本预计是多少？"
  
  round_2:
    prior: 0.52  # 继承上一轮后验
    evidence_collected:
      - source: "小范围测试"
        tier: "C"
        direction: "support"
        update: +0.05
    posterior: 0.57
    readiness_score: 57
    decision: "run_experiment"
    remaining_gaps: ["样本量不足"]
    next_questions:
      - "能否扩大测试范围到 500 用户？"
```

### 5.2 终止条件

```yaml
termination_conditions:
  # 满足任一条件即终止迭代
  conditions:
    - "后验 ≥ invest_now 阈值"
    - "后验 < stop 阈值"
    - "达到最大轮数 (5轮)"
    - "用户明确要求停止"
    - "无新证据可收集"
```

---

## 六、敏感性分析

### 6.1 敏感性检查问题

每个决策报告必须回答：

```yaml
sensitivity_questions:
  - question: "什么证据会让结论反转？"
    purpose: "识别关键假设"
    example: "如果测试发现病毒系数<0.5，结论将反转为不推荐"
  
  - question: "先验变化多少会影响决策？"
    purpose: "评估先验依赖度"
    example: "先验从0.3变到0.2，仍会得出'实验'建议"
  
  - question: "最脆弱的假设是什么？"
    purpose: "识别风险点"
    example: "假设用户愿意邀请，但未验证"
  
  - question: "如果最佳证据被推翻，结论会怎样？"
    purpose: "压力测试"
    example: "去掉 Notion 案例后，后验降至0.45，仍推荐实验"
```

### 6.2 敏感性报告

```yaml
sensitivity_report:
  required_sections:
    - "关键假设列表"
    - "假设失效的影响"
    - "反转结论的条件"
    - "建议收集的保护性证据"
```

---

## 七、输出契约

### 7.1 贝叶斯决策报告必需章节

```yaml
bayesian_report_sections:
  - id: hypothesis
    title: "待验证假设"
    required: true
    content: "清晰陈述增长命题"
  
  - id: prior_assessment
    title: "先验评估"
    required: true
    content:
      - "初始置信度"
      - "先验设置理由"
      - "先验卫生检查"
  
  - id: evidence_analysis
    title: "证据分析"
    required: true
    content:
      - "证据列表（含等级、方向）"
      - "更新幅度计算"
      - "累积更新过程"
  
  - id: posterior_assessment
    title: "后验评估"
    required: true
    content:
      - "最终置信度"
      - "置信度变化过程"
      - "迭代日志"
  
  - id: decision
    title: "决策建议"
    required: true
    content:
      - "行动阈值比较"
      - "推荐行动"
      - "执行建议"
  
  - id: sensitivity
    title: "敏感性分析"
    required: true
    content:
      - "关键假设"
      - "反转条件"
      - "风险提示"
  
  - id: next_evidence
    title: "待收集证据"
    required: false
    content: "如果继续迭代，需要收集哪些证据"
```

### 7.2 用户友好标题映射

| 概念术语 | 用户友好标题 |
|---------|-------------|
| 先验概率 | 初始信心 |
| 后验概率 | 更新后的信心 |
| 证据更新 | 证据影响 |
| 行动阈值 | 决策标准 |
| 敏感性分析 | 结论有多稳固 |

---

## 八、安全边界

### 8.1 高风险场景处理

```yaml
high_risk_bayesian:
  # 检测到高风险领域时的特殊处理
  on_detection:
    - "提高 invest_now 阈值到 0.85"
    - "要求更高质量证据（仅 A/B 级有效）"
    - "强制敏感性分析"
    - "添加专业审查警告"
  
  domains:
    financial: ["投资决策", "融资", "估值"]
    legal: ["合规", "合同", "知识产权"]
    regulatory: ["牌照", "数据合规", "反垄断"]
```

### 8.2 置信度上限

```yaml
confidence_cap:
  # 即使后验很高，也要承认不确定性
  max_reportable_confidence: 0.95
  rationale: "增长决策永远存在不确定性，不接受绝对确信"
```

---

## 九、示例

### 9.1 完整示例：SaaS 邀请裂变决策

```yaml
bayesian_decision:
  hypothesis:
    statement: "邀请裂变机制能为 SaaS 产品带来有效增长"
    success_metric: "每月新增 1000 付费用户"
    time_horizon: "3个月"
  
  prior:
    value: 0.35
    rationale: "有 Notion、Dropbox 等成功案例，但产品形态不同"
    hygiene_check:
      - ✅ 锚定到案例证据
      - ✅ 避免过度自信
      - ✅ 考虑基础概率
  
  evidence_round_1:
    - source: "Notion 模板社区案例"
      tier: "B"
      direction: "support"
      summary: "Notion 通过模板分享实现病毒增长"
      update: +0.15
    
    - source: "SaaS 行业基准报告"
      tier: "B"
      direction: "support"
      summary: "SaaS 产品平均病毒系数 0.3-0.8"
      update: +0.10
    
    - source: "内部用户调研"
      tier: "C"
      direction: "neutral"
      summary: "用户愿意邀请，但需要激励"
      update: 0.00
  
  posterior_round_1:
    value: 0.52
    calculation: "0.35 + 0.15 + 0.10 = 0.60 → 保守调整为 0.52"
    decision: "run_experiment"
  
  sensitivity:
    reversal_condition: "如果病毒系数 < 0.3，结论反转为不推荐"
    key_assumption: "用户有足够的邀请动机"
    vulnerable_point: "奖励机制成本未验证"
  
  recommendation:
    action: "设计小规模邀请裂变实验"
    scope: "500 种子用户，30 天周期"
    budget: "2万元激励预算"
    success_criteria: "病毒系数 > 0.5，CAC < 50元"
```

---

## 十、Reference Map

- `references/current-state-clarity.md`: 现状清晰度门控
- `references/safety-boundaries.md`: 安全边界
- `scripts/bayesian_decision.py`: 贝叶斯计算脚本
- `scripts/assess_clarity.py`: 清晰度评估（集成到贝叶斯）
