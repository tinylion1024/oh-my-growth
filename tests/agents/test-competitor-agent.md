# Competitor Agent 测试用例

## 测试概览

测试 Competitor Agent 分析竞品增长策略的能力。

---

## 测试用例 1：竞品增长策略分析

### 输入

```json
{
  "competitor": {
    "name": "竞品A",
    "industry": "saas",
    "stage": "1-10"
  },
  "analysis_scope": ["获客策略", "留存策略", "变现策略"]
}
```

### 预期输出

```json
{
  "acquisition_strategy": {
    "main_channels": ["内容营销", "SEO", "产品驱动"],
    "estimated_cac": "低-中",
    "key_tactics": ["免费试用", "模板分享", "社区运营"]
  },
  "retention_strategy": {
    "mechanisms": ["邮件召回", "功能更新通知", "社区互动"],
    "estimated_retention": "中等偏上"
  },
  "monetization_strategy": {
    "model": "Freemium",
    "conversion_rate_estimate": "3-5%",
    "pricing_tiers": "3档"
  },
  "weaknesses": [
    "高级功能定价偏高",
    "移动端体验一般"
  ],
  "opportunities": [
    "差异化定价策略",
    "优化移动端体验"
  ]
}
```

### 验证点

- [ ] 分析获客渠道
- [ ] 分析留存机制
- [ ] 分析变现模式
- [ ] 识别弱点机会

---

## 测试用例 2：竞品对比分析

### 输入

```json
{
  "competitors": ["竞品A", "竞品B", "竞品C"],
  "our_product": {
    "name": "我方产品",
    "stage": "0-1"
  }
}
```

### 预期输出

```json
{
  "comparison_matrix": {
    "features": {
      "竞品A": "功能全，定价高",
      "竞品B": "轻量级，免费版强",
      "竞品C": "垂直领域深耕"
    },
    "market_position": {
      "竞品A": "高端市场领导者",
      "竞品B": "中小企业首选",
      "竞品C": "细分领域专家"
    }
  },
  "differentiation_opportunities": [
    "价格带空白点",
    "功能差异化",
    "服务差异化"
  ],
  "recommended_positioning": "避开A的正面竞争，对标B做差异化"
}
```

### 验证点

- [ ] 多竞品对比
- [ ] 识别定位差异
- [ ] 提供差异化建议
