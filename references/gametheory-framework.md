# Game Theory Framework

博弈论战略框架：将竞争、定价、谈判、平台等战略互动转化为可分析的博弈模型。

---

## 一、核心概念

### 1.1 适用场景

| 场景类型 | 典型问题 | 博弈论框架 |
|----------|----------|-----------|
| **竞争博弈** | 对手会怎么反应？价格战会怎样？ | 囚徒困境、古诺竞争 |
| **定价博弈** | 如何定价不会被跟进？ | 信号博弈、承诺博弈 |
| **谈判博弈** | 如何分配利益？谁先出价？ | 讨价还价博弈 |
| **平台博弈** | 双边市场如何启动？ | 网络效应博弈 |
| **联盟博弈** | 合作还是背叛？如何分配收益？ | 合作博弈、夏普利值 |
| **进入博弈** | 是否进入新市场？在位者如何防御？ | 进入威慑、限制性定价 |

### 1.2 博弈论核心要素

```yaml
game_model:
  players:           # 博弈参与者
    - name: "参与者名称"
      type: "competitor|customer|supplier|regulator"
      objectives: ["目标1", "目标2"]
  
  strategies:        # 可选策略
    player_1: ["策略A", "策略B"]
    player_2: ["策略C", "策略D"]
  
  payoffs:          # 收益矩阵
    # (策略组合) → (收益1, 收益2)
  
  timing:           # 时序
    type: "simultaneous|sequential"
    order: ["player_1", "player_2"]
  
  information:      # 信息结构
    type: "complete|incomplete"
    beliefs: {}
  
  equilibrium:      # 均衡分析
    type: "Nash|Subgame Perfect|Bayesian"
```

---

## 二、博弈框架库

### 2.1 竞争博弈框架

#### 囚徒困境（Prisoner's Dilemma）

**适用**：价格战、广告竞赛、恶性竞争

```yaml
prisoner_dilemma:
  scenario: "双方都有动机背叛，但合作对双方更好"
  
  payoff_matrix:
    cooperate:     # 对手合作
      cooperate: [3, 3]   # 双赢
      defect: [0, 5]      # 被利用
    defect:        # 对手背叛
      cooperate: [5, 0]   # 利用对方
      defect: [1, 1]      # 双输
  
  nash_equilibrium: "(背叛, 背叛)"
  pareto_optimal: "(合作, 合作)"
  
  strategic_insight:
    - "单次博弈：背叛是占优策略"
    - "重复博弈：可以通过声誉/报复维持合作"
    - "解决方案：改变收益结构、引入第三方、建立声誉机制"
  
  growth_application:
    - "价格竞争：如何避免恶性价格战"
    - "广告竞争：如何避免广告军备竞赛"
    - "补贴竞争：如何退出补贴战"
```

#### 古诺竞争（Cournot Competition）

**适用**：产能决策、市场份额竞争

```yaml
cournot_competition:
  scenario: "两家企业同时决定产量，价格由市场决定"
  
  model:
    demand_function: "P = a - b(Q1 + Q2)"
    cost_function: "Ci = c * qi"
    profit: "πi = (P - c) * qi"
  
  equilibrium:
    reaction_function: "q1* = (a - c - q2) / 2b"
    nash_equilibrium: "q1* = q2* = (a-c) / 3b"
  
  strategic_insight:
    - "均衡产量低于垄断，高于社会最优"
    - "企业数量增加 → 价格下降 → 接近竞争均衡"
    - "产能承诺可以改变均衡"
```

### 2.2 定价博弈框架

#### 信号博弈（Signaling Game）

**适用**：定价信号、质量信号、意图信号

```yaml
signaling_game:
  scenario: "发送者有私有信息，通过行动向接收者传递信号"
  
  players:
    sender: "有私有信息的一方"
    receiver: "根据信号做出反应的一方"
  
  signal_types:
    separating: "不同类型发送不同信号（可区分）"
    pooling: "所有类型发送相同信号（不可区分）"
    semi_separating: "部分区分"
  
  application:
    - "高价 = 高质量信号"
    - "不降价 = 承诺不跟进"
    - "提前公告 = 威慑信号"
  
  credibility_check:
    - "信号成本：高成本低类型无法模仿"
    - "一致性历史：过往行为是否一致"
    - "可验证性：信号是否可以被验证"
```

#### 承诺博弈（Commitment Game）

**适用**：战略承诺、威慑、先发优势

```yaml
commitment_game:
  scenario: "通过承诺改变对手的信念和行为"
  
  commitment_types:
    - burning_bridge: "断后路承诺（不可逆）"
    - reputation: "声誉承诺（可逆但有成本）"
    - contract: "合同承诺（法律约束）"
    - investment: "投资承诺（沉没成本）"
  
  credibility_test:
    questions:
      - "承诺是否可逆？"
      - "违约成本有多高？"
      - "对手是否能观察到承诺？"
      - "承诺是否与激励一致？"
  
  application:
    - "价格承诺：承诺不降价"
    - "产能承诺：承诺扩产"
    - "退出承诺：承诺退出某个市场"
```

### 2.3 平台博弈框架

#### 双边市场博弈（Two-Sided Market）

**适用**：平台冷启动、补贴策略

```yaml
two_sided_market:
  scenario: "平台连接两边用户，存在网络效应"
  
  model:
    side_a: "供给端（商家、司机、房东）"
    side_b: "需求端（消费者、乘客、房客）"
    network_effect: "cross-side"
  
  chicken_and_egg:
    problem: "没有供给就没有需求，没有需求就没有供给"
    solutions:
      - "补贴一边：补贴供给端获取库存"
      - "分阶段：先获取供给，再获取需求"
      - "单边工具：供给端工具化，先有价值"
  
  pricing_strategy:
    - "价格结构 ≠ 价格水平"
    - "补贴弹性更高的一边"
    - "收"钱"方补贴"免费"方"
  
  growth_application:
    - "电商平台：如何获取首批商家和用户"
    - "打车平台：如何获取司机和乘客"
    - "内容平台：如何获取创作者和观众"
```

### 2.4 谈判博弈框架

#### 讨价还价博弈（Bargaining Game）

**适用**：合作谈判、利益分配

```yaml
bargaining_game:
  scenario: "双方就利益分配进行谈判"
  
  rubinstein_model:
    setup: "轮流出价，无限期博弈"
    discount_factors: "δ1, δ2（耐心程度）"
    equilibrium: "x* = (1-δ2) / (1-δ1*δ2)"
  
  strategic_insight:
    - "耐心者获得更多份额"
    - "先动优势 vs 后动优势"
    - "外部选项增加谈判筹码"
  
  application:
    - "供应商谈判"
    - "合作伙伴分成"
    - "并购谈判"
```

---

## 三、博弈分析工作流

### 3.1 标准工作流

```
Step 1: 识别博弈类型
    ↓
Step 2: 定义参与者与策略
    ↓
Step 3: 构建收益矩阵
    ↓
Step 4: 分析均衡
    ↓
Step 5: 历史行为校准
    ↓
Step 6: 承诺与信号检验
    ↓
Step 7: 敏感性分析
    ↓
Step 8: 战略建议
```

### 3.2 收益矩阵构建

```yaml
payoff_matrix_construction:
  dimensions:
    - "收益量化（利润、市场份额、用户量）"
    - "概率估计（对手选择某策略的概率）"
    - "时间因素（短期 vs 长期收益）"
  
  marking_rules:
    - "observed: 基于历史数据"
    - "estimated: 基于行业基准"
    - "assumed: 基于合理假设"
  
  example:
    players: ["我方", "竞争对手"]
    strategies:
      我方: ["降价", "不降价"]
      竞争对手: ["跟进降价", "不跟进"]
    payoffs:
      (降价, 跟进):
        我方: -5%利润 (estimated)
        竞争对手: -5%利润 (estimated)
      (降价, 不跟进):
        我方: +15%份额 (assumed)
        竞争对手: -10%份额 (assumed)
      (不降价, 跟进降价):
        我方: -8%份额 (estimated)
        竞争对手: +12%份额 (assumed)
      (不降价, 不跟进):
        我方: 0 (observed)
        竞争对手: 0 (observed)
```

### 3.3 均衡分析

```yaml
equilibrium_analysis:
  nash_equilibrium:
    definition: "任何一方单独改变策略都不会更好"
    finding_method:
      - "检查每个策略组合是否稳定"
      - "剔除被占优策略"
      - "寻找最优反应交点"
  
  subgame_perfect:
    definition: "在每个子博弈上都是纳什均衡"
    finding_method: "逆向归纳法"
    application: "序贯博弈、可信威胁"
  
  mixed_strategy:
    definition: "以概率混合多个策略"
    application: "无法预测对手选择时"
```

---

## 四、承诺与信号检验

### 4.1 承诺可信性检验

```yaml
commitment_credibility_check:
  checklist:
    - id: irreversibility
      question: "承诺是否不可逆？"
      score_weight: 0.25
    
    - id: observability
      question: "对手是否能观察到承诺？"
      score_weight: 0.20
    
    - id: cost
      question: "违约成本有多高？"
      score_weight: 0.25
    
    - id: consistency
      question: "承诺是否与历史行为一致？"
      score_weight: 0.15
    
    - id: incentive
      question: "承诺是否与激励一致？"
      score_weight: 0.15
  
  scoring:
    high_credibility: "≥ 75分"
    medium_credibility: "50-74分"
    low_credibility: "< 50分"
  
  examples:
    high:
      - "公开签订长期合同"
      - "巨额沉没成本投资"
      - "法律约束的承诺"
    medium:
      - "公开声明"
      - "历史一致的行为"
    low:
      - "私下口头承诺"
      - "容易撤销的决策"
```

### 4.2 信号质量检验

```yaml
signal_quality_check:
  dimensions:
    - cost_to_mimic: "低成本类型能否模仿？（分离信号）"
    - observability: "信号是否可观察？"
    - consistency: "信号是否与历史一致？"
    - verifiability: "信号是否可验证？"
  
  signal_types:
    separating:
      description: "不同类型发送不同信号"
      condition: "低成本类型无法模仿高成本信号"
      example: "高价信号高质量"
    
    pooling:
      description: "所有类型发送相同信号"
      condition: "信号成本相同"
      example: "所有品牌都说自己好"
  
  strategic_use:
    - "发送高成本信号区分自己"
    - "识别对手信号的真伪"
    - "避免被低成本类型模仿"
```

---

## 五、历史行为校准

### 5.1 理性校准

```yaml
rationality_calibration:
  purpose: "调整对对手行为的预测"
  
  factors:
    - historical_behavior: "过去类似情况下的行为"
    - reference_class: "同类企业/行业的典型行为"
    - capability: "执行能力（资源、技术、组织）"
    - incentive: "激励结构（KPI、考核、利益）"
  
  adjustment_rules:
    - "历史一致 → 提高预测置信度"
    - "历史不一致 → 降低预测置信度"
    - "参考类相似 → 借鉴典型行为"
  
  example:
    competitor: "竞争对手A"
    historical:
      price_war: "从不主动发起价格战"
      follow_discount: "总是跟进降价"
      new_product: "通常在6个月后跟进"
    calibration:
      predict_follow_discount: "高置信度（历史一致）"
      predict_price_war: "低置信度（历史不一致）"
```

### 5.2 参考类分析

```yaml
reference_class_analysis:
  definition: "用类似企业的行为预测目标企业"
  
  reference_classes:
    - industry: "同行业企业"
    - stage: "同阶段企业"
    - strategy: "同战略定位企业"
    - ownership: "同所有权类型"
  
  application:
    - "上市公司 → 分析财报、公告"
    - "创业公司 → 分析融资、用户数据"
    - "国企 → 考虑政策约束"
    - "外企 → 考虑总部决策"
```

---

## 六、输出契约

### 6.1 博弈论报告必需章节

```yaml
game_theory_report:
  required_sections:
    - id: executive_summary
      title: "执行摘要"
      content:
        - "核心建议"
        - "对手反应预测"
        - "承诺可信性判断"
    
    - id: game_description
      title: "博弈描述"
      content:
        - "参与者"
        - "策略选项"
        - "收益矩阵"
        - "时序"
    
    - id: equilibrium_analysis
      title: "均衡分析"
      content:
        - "纳什均衡"
        - "其他均衡（如适用）"
        - "均衡稳定性"
    
    - id: historical_calibration
      title: "历史行为校准"
      content:
        - "对手历史行为"
        - "参考类分析"
        - "预测置信度调整"
    
    - id: commitment_signal
      title: "承诺与信号"
      content:
        - "承诺可信性评分"
        - "信号质量分析"
    
    - id: sensitivity
      title: "敏感性分析"
      content:
        - "关键假设"
        - "假设变化影响"
        - "反转条件"
    
    - id: strategic_recommendation
      title: "战略建议"
      content:
        - "推荐策略"
        - "预期对手反应"
        - "执行路径"
```

---

## 七、使用示例

### 7.1 定价博弈示例

```yaml
scenario:
  problem: "是否降价应对竞争对手？"
  context:
    industry: "SaaS"
    my_share: "25%"
    competitor_share: "20%"
    other_share: "55%"

game_model:
  players:
    - name: "我方"
      type: "market_leader"
    - name: "竞争对手"
      type: "challenger"
  
  strategies:
    我方: ["降价10%", "不降价"]
    竞争对手: ["跟进降价", "不跟进"]
  
  payoffs:
    (降价, 跟进):
      我方: "-5%利润, 份额不变"
      竞争对手: "-5%利润, 份额不变"
    (降价, 不跟进):
      我方: "-3%利润, +5%份额"
      竞争对手: "-8%份额"
    (不降价, 跟进降价):
      我方: "-5%份额"
      竞争对手: "-2%利润, +5%份额"
    (不降价, 不跟进):
      我方: "不变"
      竞争对手: "不变"

equilibrium_analysis:
  nash_equilibrium: "(降价, 跟进降价)"
  reasoning: "双方都有降价动机，但都会损失利润"

historical_calibration:
  competitor_behavior: "过去2年从不主动降价，但总是跟进"
  prediction: "我方降价 → 竞争对手高概率跟进"
  confidence: "高"

commitment_check:
  my_commitment: "无承诺"
  competitor_commitment: "无承诺"
  signal: "我方降价会被视为进攻信号"

recommendation:
  primary: "不降价"
  reasoning:
    - "降价会引发价格战，双方都受损"
    - "竞争对手历史行为表明会跟进"
    - "作为市场领导者，应避免价格战"
  alternative: "如果必须降价，考虑公开承诺'最终价格'，减少被跟进风险"
```

---

## 八、Reference Map

- `references/bayesian-decision.md`: 贝叶斯决策（概率更新）
- `references/current-state-clarity.md`: 现状清晰度门控
- `references/safety-boundaries.md`: 安全边界
- `scripts/gametheory_analysis.py`: 博弈论计算脚本（待实现）
