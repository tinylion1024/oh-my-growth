# Monetization Agent 测试用例

## 测试概览

测试 Monetization Agent 对变现影响评估的能力。

---

## 测试用例 1：订阅付费转化评估

### 输入

```json
{
  "user_input": {
    "problem_type": "monetization",
    "industry": "saas",
    "stage": "1-10"
  },
  "mechanism": {
    "description": "从免费版升级到付费版",
    "pricing_model": "Freemium",
    "conversion_target": "免费用户 → 付费用户",
    "current_rate": "2%"
  }
}
```

### 预期输出

```json
{
  "monetization_assessment": {
    "revenue_impact": "正向，付费转化提升直接增加收入",
    "user_impact": "需评估对免费用户留存的影响",
    "pricing_appropriateness": "需确认定价与价值匹配",
    "conversion_path": "免费试用 → 价值感知 → 付费转化"
  },
  "trade_offs": [
    "付费墙可能降低新用户激活率",
    "过度变现可能损害口碑"
  ],
  "recommendations": [
    "设计渐进式功能限制",
    "提供试用期体验完整功能",
    "追踪付费用户LTV"
  ],
  "confidence": "Medium"
}
```

### 验证点

- [ ] 正确评估变现影响
- [ ] 识别潜在权衡
- [ ] 提供优化建议
- [ ] 考虑长期影响

---

## 测试用例 2：广告变现评估

### 输入

```json
{
  "user_input": {
    "problem_type": "monetization",
    "industry": "content",
    "stage": "1-10"
  },
  "mechanism": {
    "description": "在内容流中插入广告",
    "ad_type": "信息流广告",
    "expected_revenue": "每千次展示50元"
  }
}
```

### 预期输出

```json
{
  "monetization_assessment": {
    "revenue_impact": "正向，但需平衡用户体验",
    "user_impact": "过多广告会降低留存",
    "optimal_density": "建议广告密度 < 15%"
  },
  "risks": [
    "用户反感导致流失",
    "广告质量影响品牌形象"
  ],
  "recommendations": [
    "原生广告优于硬广",
    "根据用户价值分层展示",
    "监控广告对留存的影响"
  ],
  "confidence": "High"
}
```

### 验证点

- [ ] 平衡变现与体验
- [ ] 识别广告风险
- [ ] 提供密度建议
- [ ] 建议监控指标

---

## 测试用例 3：增值服务评估

### 输入

```json
{
  "user_input": {
    "problem_type": "monetization",
    "industry": "education",
    "stage": "1-10"
  },
  "mechanism": {
    "description": "基础课程免费，高级课程付费",
    "value_proposition": "深度内容 + 1对1辅导",
    "target_segment": "高意向学习者"
  }
}
```

### 预期输出

```json
{
  "monetization_assessment": {
    "revenue_impact": "正向，增值服务LTV高",
    "segment_fit": "精准定位高价值用户",
    "value_delivery": "需确保付费内容价值显著高于免费"
  },
  "pricing_suggestions": [
    "分级定价满足不同需求",
    "提供打包优惠",
    "设计续费激励"
  ],
  "confidence": "High"
}
```

### 验证点

- [ ] 评估增值服务价值
- [ ] 建议定价策略
- [ ] 考虑续费设计
