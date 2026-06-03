# Case Agent 测试用例

## 测试概览

测试 Case Agent 的案例匹配能力。

---

## 测试用例 1：SaaS 邀请裂变匹配

### 输入

```json
{
  "user_input": {
    "problem_type": "acquisition",
    "industry": "saas",
    "stage": "1-10",
    "keywords": ["邀请", "裂变", "协作工具"]
  }
}
```

### 预期输出

```json
{
  "matched_cases": [
    {
      "name": "Dropbox",
      "similarity_score": 0.92,
      "match_reasons": ["SaaS工具", "邀请裂变", "协作属性"],
      "key_tactics": ["双边奖励", "存储空间激励", "产品内分享"],
      "results": "用户增长3900%",
      "replicable_points": [
        "双边奖励激励双方参与",
        "奖励与产品核心价值相关（存储空间）",
        "分享流程无缝集成"
      ],
      "warnings": ["需要设计防刷机制"]
    },
    {
      "name": "Slack",
      "similarity_score": 0.85,
      "match_reasons": ["SaaS协作工具", "团队传播"],
      "key_tactics": ["团队协作天然传播", "Freemium模式"],
      "replicable_points": ["让产品成为传播载体"]
    },
    {
      "name": "Notion",
      "similarity_score": 0.80,
      "match_reasons": ["SaaS工具", "内容分享传播"]
    }
  ],
  "cross_case_insights": [
    "成功SaaS裂变都让产品本身成为传播载体",
    "奖励与核心价值相关比现金更有效",
    "团队协作场景天然有传播属性"
  ],
  "confidence": "High"
}
```

### 验证点

- [ ] 返回3-5个相关案例
- [ ] Dropbox 应排第一（最相关）
- [ ] 提取可复制要点
- [ ] 提供跨案例洞察

---

## 测试用例 2：电商留存匹配

### 输入

```json
{
  "user_input": {
    "problem_type": "retention",
    "industry": "ecommerce",
    "stage": "10-100",
    "keywords": ["复购", "会员", "留存"]
  }
}
```

### 预期输出

```json
{
  "matched_cases": [
    {
      "name": "京东会员",
      "similarity_score": 0.88,
      "match_reasons": ["电商", "会员体系", "留存"],
      "key_tactics": ["付费会员", "专属优惠", "Plus会员"],
      "replicable_points": [
        "会员权益要有真实价值感知",
        "高频场景的优惠最有效"
      ]
    },
    {
      "name": "小红书",
      "similarity_score": 0.75,
      "match_reasons": ["电商", "内容驱动留存"]
    }
  ],
  "confidence": "High"
}
```

### 验证点

- [ ] 返回电商相关案例
- [ ] 包含会员体系案例

---

## 测试用例 3：边界情况 - 无匹配案例

### 输入

```json
{
  "user_input": {
    "problem_type": "unknown",
    "industry": "新兴行业",
    "keywords": ["非常小众的关键词"]
  }
}
```

### 预期输出

```json
{
  "matched_cases": [],
  "reason": "案例库中无直接匹配案例",
  "alternative_suggestions": [
    "可参考相近行业的案例",
    "可参考相似问题类型的案例"
  ],
  "confidence": "Low"
}
```

### 验证点

- [ ] 正确处理无匹配情况
- [ ] 提供替代建议

---

## 测试结果记录

| 用例 | 状态 | 通过/失败 | 备注 |
|------|------|-----------|------|
| TC1 | 待测试 | - | - |
| TC2 | 待测试 | - | - |
| TC3 | 待测试 | - | - |
