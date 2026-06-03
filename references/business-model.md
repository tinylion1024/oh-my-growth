# Business Model Framework

商业模式分析框架：设计、诊断、研究商业模式。

---

## 一、核心概念

### 1.1 商业模式画布

```yaml
business_model_canvas:
  customer_segments:    # 客户细分
    - "目标客户是谁？"
    - "如何细分？"
  
  value_propositions:   # 价值主张
    - "提供什么价值？"
    - "解决什么问题？"
  
  channels:             # 渠道
    - "如何触达客户？"
    - "如何交付价值？"
  
  customer_relationships: # 客户关系
    - "如何获取、保持、增长客户？"
  
  revenue_streams:      # 收入来源
    - "如何赚钱？"
    - "定价模式？"
  
  key_resources:        # 核心资源
    - "需要什么资源？"
  
  key_activities:       # 核心活动
    - "必须做什么？"
  
  key_partnerships:     # 关键合作
    - "谁是关键伙伴？"
  
  cost_structure:       # 成本结构
    - "主要成本是什么？"
    - "固定成本 vs 变动成本？"
```

### 1.2 商业模式类型

| 类型 | 特征 | 案例 |
|------|------|------|
| **订阅模式** | 周期性收费 | Netflix, SaaS |
| **平台模式** | 双边市场 | 淘宝, Uber |
| **免费增值** | 基础免费，高级付费 | Notion, Dropbox |
| **长尾模式** | 小众产品规模化 | Amazon, Netflix |
| **多边平台** | 多方连接 | App Store, 支付宝 |
| **刀架刀片** | 低价主体，高价耗材 | 打印机, 游戏机 |

### 1.3 AI 时代升级路径

```yaml
ai_upgrade_paths:
  automation:
    from: "人工服务"
    to: "AI 自动化"
    example: "客服 → AI 客服"
  
  personalization:
    from: "标准化产品"
    to: "AI 个性化"
    example: "推荐算法"
  
  prediction:
    from: "事后分析"
    to: "AI 预测"
    example: "需求预测"
  
  generation:
    from: "人工创作"
    to: "AI 生成"
    example: "内容生成"
```

---

## 二、竞争分析

### 2.1 五力分析

```yaml
porter_five_forces:
  competitive_rivalry:   # 行业竞争
    - "竞争者数量"
    - "行业增长率"
    - "产品差异化程度"
  
  supplier_power:        # 供应商议价能力
    - "供应商数量"
    - "替代品可用性"
  
  buyer_power:           # 买方议价能力
    - "买家数量"
    - "价格敏感度"
  
  threat_of_substitution: # 替代品威胁
    - "替代品数量"
    - "转换成本"
  
  threat_of_new_entry:   # 新进入者威胁
    - "进入壁垒"
    - "资本要求"
```

### 2.2 竞品分析框架

```yaml
competitor_analysis:
  dimensions:
    - pricing: "定价策略"
    - features: "功能对比"
    - positioning: "定位差异"
    - target_audience: "目标客户"
    - marketing: "营销策略"
    - distribution: "渠道策略"
```

---

## 三、输出契约

```yaml
business_model_report:
  sections:
    - "商业模式画布"
    - "收入模型分析"
    - "成本结构分析"
    - "竞争分析"
    - "AI 升级机会"
    - "风险与建议"
```

---

## 四、Reference Map

- `references/gametheory-framework.md`: 博弈论框架（竞争博弈）
- `references/kelly-allocation.md`: Kelly 资源分配
