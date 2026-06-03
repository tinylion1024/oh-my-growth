# Kelly Allocation Framework

Kelly 资源分配框架：使用 Kelly 准则计算最优投入比例，转化为可执行的资源分配计划。

---

## 一、核心概念

### 1.1 Kelly 准则

**核心公式**：
```
f* = (bp - q) / b

其中：
- f* = 最优投入比例
- b = 净赔率（盈利/亏损）
- p = 胜率（成功概率）
- q = 1 - p（失败概率）
```

**直观理解**：
- 当优势越大（p 越高），投入比例越大
- 当赔率越好（b 越大），投入比例越大
- Kelly 给出的是"长期增长最优"的比例，不是"单次最优"

### 1.2 适用场景判断

| 场景 | 是否适用 Kelly | 替代方案 |
|------|---------------|----------|
| 可重复实验、有反馈 | ✅ 适用 | - |
| 下限风险可控 | ✅ 适用 | - |
| 概率可估计 | ✅ 适用 | - |
| 一次性、不可逆决策 | ❌ 不适用 | 风险审查、决策树 |
| 无下限风险 | ❌ 不适用 | 止损机制 |
| 概率完全未知 | ⚠️ 谨慎 | 先小实验 |

### 1.3 核心原则

```yaml
kelly_principles:
  - "默认使用分数 Kelly（如 1/2 Kelly、1/4 Kelly）"
  - "Kelly 是长期最优，短期波动大"
  - "公式不是主要产品，行动计划才是"
  - "每个关键数字标记 observed/estimated/assumed"
  - "如果相关性未知，缩小投入而非假设独立"
  - "如果优势为负或脆弱，推荐不投入或先测试"
  - "总是转化为最小可执行行动"
  - "包含加仓、止损、复盘条件"
```

---

## 二、Kelly 计算方法

### 2.1 二元机会（Binary Opportunity）

**适用**：成功/失败两种结果

```yaml
binary_kelly:
  formula: "f* = (bp - q) / b"
  
  parameters:
    b: "净赔率 = 盈利金额 / 亏损金额"
    p: "成功概率"
    q: "失败概率 = 1 - p"
  
  example:
    scenario: "一个增长实验，成功概率 60%"
    win_amount: 100万  # 成功收益
    loss_amount: 30万  # 失败损失
    win_probability: 0.60
    
    calculation:
      b: 100/30 = 3.33  # 净赔率
      p: 0.60
      q: 0.40
      f_star: (3.33 * 0.60 - 0.40) / 3.33 = 0.48
    
    result:
      full_kelly: "48% 的可用资源"
      half_kelly: "24%（推荐）"
      quarter_kelly: "12%（保守）"
```

### 2.2 多场景机会（Scenario-Based）

**适用**：多种可能结果

```yaml
scenario_kelly:
  formula: "最大化 E[log(1 + f * r)]"
  
  method:
    - "列出所有可能场景"
    - "每个场景有收益率和概率"
    - "数值求解最优 f"
  
  example:
    scenarios:
      - outcome: "大成功"
        return: 2.0    # 200% 收益
        probability: 0.20
      - outcome: "小成功"
        return: 0.5    # 50% 收益
        probability: 0.30
      - outcome: "持平"
        return: 0.0
        probability: 0.30
      - outcome: "失败"
        return: -0.5   # 50% 损失
        probability: 0.20
    
    optimization:
      method: "数值求解"
      result: "f* ≈ 0.35"
```

### 2.3 多机会并行分配

**适用**：同时有多个机会

```yaml
multiple_opportunities:
  workflow:
    - "计算每个机会的独立 Kelly"
    - "应用分数 Kelly"
    - "考虑相关性调整"
    - "总暴露限制"
  
  correlation_adjustment:
    independent: "直接相加"
    partially_correlated: "缩小总暴露"
    highly_correlated: "视为一个大机会"
  
  example:
    opportunities:
      - name: "机会A"
        kelly: 0.20
        correlation: "与B相关"
      - name: "机会B"
        kelly: 0.15
        correlation: "与A相关"
      - name: "机会C"
        kelly: 0.10
        correlation: "独立"
    
    adjustment:
      - "A和B相关性高 → 合并计算"
      - "C独立 → 单独计算"
      - "总暴露上限：50%"
    
    result:
      opportunity_A_B: "15%（合并后）"
      opportunity_C: "5%（分数后）"
      total: "20%"
```

---

## 三、保守调整

### 3.1 分数 Kelly

```yaml
fractional_kelly:
  purpose: "降低波动，提高实际执行可行性"
  
  options:
    full_kelly:
      fraction: 1.0
      description: "理论最优，波动极大"
      risk: "高"
    
    half_kelly:
      fraction: 0.5
      description: "推荐默认"
      risk: "中"
      growth_tradeoff: "75%的理论增长率"
    
    quarter_kelly:
      fraction: 0.25
      description: "保守选择"
      risk: "低"
      growth_tradeoff: "50%的理论增长率"
  
  recommendation:
    default: "1/2 Kelly"
    high_uncertainty: "1/4 Kelly"
    very_conservative: "1/8 Kelly"
```

### 3.2 相关性调整

```yaml
correlation_haircut:
  rule: "如果相关性未知，缩小暴露"
  
  adjustment:
    unknown_correlation:
      action: "假设高度相关"
      haircut: "50%"
    
    partial_correlation:
      action: "按相关性调整"
      formula: "exposure * (1 - correlation)"
    
    known_independent:
      action: "无需调整"
      haircut: "0%"
```

### 3.3 总暴露限制

```yaml
total_exposure_cap:
  rule: "所有机会的总投入不超过上限"
  
  caps:
    conservative: "30%"
    moderate: "50%"
    aggressive: "70%"
  
  default: "50%"
```

---

## 四、最小行动包

### 4.1 行动包定义

```yaml
minimum_action_package:
  definition: "将 Kelly 比例转化为最小可执行行动"
  
  components:
    - action: "具体行动"
    - owner: "负责人"
    - metric: "衡量指标"
    - review_window: "复盘周期"
    - add_condition: "加仓条件"
    - stop_condition: "止损条件"
  
  example:
    opportunity: "邀请裂变实验"
    kelly_fraction: "15%"
    resource_pool: "100万预算"
    allocation: "15万"
    
    action_package:
      action: "启动邀请裂变 MVP"
      owner: "增长负责人"
      metric: "病毒系数、CAC、留存率"
      review_window: "30天"
      add_condition: "病毒系数 > 0.5 且 CAC < 50元"
      stop_condition: "病毒系数 < 0.3 或 CAC > 80元"
```

### 4.2 加仓条件

```yaml
add_conditions:
  types:
    - metric_threshold: "指标达到阈值"
    - confidence_increase: "置信度提升"
    - positive_feedback: "正向反馈"
  
  examples:
    - "病毒系数从 0.4 提升到 0.6 → 加仓 50%"
    - "CAC 从 60元 降到 40元 → 加仓"
    - "留存率 > 40% → 扩大规模"
```

### 4.3 止损条件

```yaml
stop_conditions:
  types:
    - metric_threshold: "指标跌破阈值"
    - time_limit: "时间到期"
    - budget_exhausted: "预算耗尽"
    - confidence_drop: "置信度下降"
  
  examples:
    - "病毒系数 < 0.3 → 停止"
    - "CAC > 100元 → 停止"
    - "90天无改善 → 停止"
    - "发现根本性假设错误 → 立即停止"
```

---

## 五、决策准备度

### 5.1 准备度评分

```yaml
decision_readiness:
  dimensions:
    - resource_clarity: 20%    # 资源池是否明确
    - probability_estimate: 25% # 概率估计是否合理
    - payoff_clarity: 20%      # 收益结构是否清晰
    - downside_bound: 15%      # 下限风险是否可控
    - repeatability: 10%       # 是否可重复
    - feedback_mechanism: 10%  # 是否有反馈机制
  
  thresholds:
    ready: "≥ 70分"
    need_more_info: "50-69分"
    not_suitable: "< 50分"
```

### 5.2 追问策略

```yaml
follow_up_questions:
  when_insufficient:
    - "可用资源总量是多少？"
    - "成功概率基于什么估计？"
    - "最坏情况会损失多少？"
    - "这个机会可以重复吗？"
  
  stop_asking_when:
    - "准备度达到阈值"
    - "行动类别已稳定"
    - "更多问题不会改变结论"
```

---

## 六、输出契约

### 6.1 Kelly 分配报告必需章节

```yaml
kelly_report:
  required_sections:
    - id: executive_summary
      title: "执行摘要"
      content:
        - "推荐行动"
        - "投入比例"
        - "行动类别"
    
    - id: kelly_fit_assessment
      title: "Kelly 适用性评估"
      content:
        - "是否适合 Kelly"
        - "适用/不适用理由"
        - "替代方案（如不适用）"
    
    - id: resource_snapshot
      title: "资源快照"
      content:
        - "可用资源池"
        - "保护储备"
        - "风险预算"
        - "转化后的金额"
    
    - id: kelly_calculation
      title: "Kelly 计算"
      content:
        - "公式路径"
        - "输入参数"
        - "Full Kelly 结果"
        - "保守调整后结果"
    
    - id: action_packages
      title: "最小行动包"
      content:
        - "具体行动"
        - "负责人"
        - "衡量指标"
        - "复盘周期"
    
    - id: conditions
      title: "加仓与止损条件"
      content:
        - "加仓条件"
        - "止损条件"
        - "复盘触发"
    
    - id: assumptions
      title: "关键假设"
      content:
        - "假设列表"
        - "假设来源（observed/estimated/assumed）"
        - "敏感性分析"
    
    - id: round_log
      title: "对话日志"
      content:
        - "每轮问答"
        - "准备度变化"
        - "停止追问理由"
```

---

## 七、使用示例

### 7.1 增长实验资源分配

```yaml
scenario:
  problem: "应该投入多少预算做邀请裂变实验？"
  
  context:
    total_budget: "100万"
    protected_reserve: "20万"
    risk_budget: "80万"
    opportunity: "邀请裂变"

probability_assessment:
  success_probability: 0.50  # estimated
  win_scenario:
    outcome: "病毒系数 > 0.5"
    return: "每月新增 5000 用户，LTV 200元"
    value: 100万
  loss_scenario:
    outcome: "病毒系数 < 0.3"
    return: "实验失败，预算损失"
    value: -20万

kelly_calculation:
  b: 100/20 = 5  # 净赔率
  p: 0.50
  q: 0.50
  f_star: (5 * 0.50 - 0.50) / 5 = 0.40
  
  adjustment:
    full_kelly: "40%"
    half_kelly: "20%（推荐）"
    applied_to: "80万风险预算"
    final_allocation: "16万"

action_package:
  action: "启动邀请裂变 MVP"
  owner: "增长负责人"
  budget: "16万"
  duration: "30天"
  metric:
    - "病毒系数"
    - "CAC"
    - "新用户留存率"
  add_condition: "病毒系数 > 0.5 且 CAC < 50元 → 加仓到 30万"
  stop_condition: "病毒系数 < 0.3 或 CAC > 80元 → 停止"
  review: "30天后复盘"

decision_readiness:
  score: 75
  status: "ready"
```

---

## 八、安全边界

### 8.1 不适用场景警告

```yaml
safety_warnings:
  one_way_door:
    trigger: "不可逆决策"
    response: "Kelly 不适用，建议使用决策树分析"
  
  unbounded_downside:
    trigger: "无下限风险"
    response: "必须先设定止损机制"
  
  unknown_probability:
    trigger: "概率完全未知"
    response: "建议先小规模实验收集数据"
  
  guaranteed_return_claim:
    trigger: "声称保证收益"
    response: "警告：不存在保证收益，可能存在欺诈"
```

### 8.2 专业边界

```yaml
professional_boundaries:
  - "Kelly 是决策支持工具，不是投资建议"
  - "重大财务决策建议咨询专业顾问"
  - "不适用于杠杆决策（无下限风险）"
  - "不适用于赌博策略"
```

---

## 九、Reference Map

- `references/bayesian-decision.md`: 贝叶斯决策（概率更新）
- `references/gametheory-framework.md`: 博弈论框架
- scripts/kelly_sizing.py: Kelly 计算脚本（待实现）
