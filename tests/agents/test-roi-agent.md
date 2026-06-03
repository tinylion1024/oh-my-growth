# ROI Agent 测试用例

## 测试概览

测试 ROI Agent 的投资回报计算能力。

---

## 测试用例 1：邀请裂变 ROI

### 输入

```json
{
  "mechanism": {
    "type": "邀请裂变",
    "reward_per_invite": 50,
    "expected_k_factor": 1.3,
    "reward_for_both": true
  },
  "business_metrics": {
    "ltv": 500,
    "current_users": 10000,
    "monthly_active": 3000,
    "cac_other_channels": 100
  }
}
```

### 预期输出

```json
{
  "roi_analysis": {
    "base_case": {
      "investment": 50000,
      "expected_new_users": 3000,
      "cost_per_new_user": 33.3,
      "expected_return": 150000,
      "payback_period": "3-4个月",
      "roi_percentage": 200
    },
    "upside_case": {
      "k_factor": 1.5,
      "expected_new_users": 5000,
      "roi_percentage": 350
    },
    "downside_case": {
      "k_factor": 1.0,
      "expected_new_users": 1000,
      "roi_percentage": 50,
      "risk": "K因子<1时无法自传播"
    }
  },
  "cost_breakdown": {
    "one_time": ["奖励发放预算50000", "技术开发"],
    "ongoing": ["运营监控", "防滥用系统"]
  },
  "key_assumptions": [
    "K因子能达到1.3",
    "新用户留存率40%",
    "奖励会被合理使用"
  ],
  "sensitivity_analysis": [
    "K因子每下降0.1，ROI下降约30%",
    "留存率对LTV影响最大"
  ],
  "confidence": "Medium"
}
```

### 验证点

- [ ] 三种情景分析完整
- [ ] 成本分解合理
- [ ] 敏感性分析有意义
- [ ] 与其他渠道CAC对比

---

## 测试用例 2：内容营销 ROI

### 输入

```json
{
  "mechanism": {
    "type": "内容营销",
    "content_type": "技术博客",
    "frequency": "每周2篇"
  },
  "business_metrics": {
    "organic_traffic": 5000,
    "conversion_rate": 0.02,
    "ltv": 1000
  },
  "costs": {
    "content_writer": 15000,
    "tools": 2000,
    "time_to_results": "6个月"
  }
}
```

### 预期输出

```json
{
  "roi_analysis": {
    "base_case": {
      "monthly_investment": 17000,
      "expected_new_traffic": 3000,
      "expected_new_users": 60,
      "expected_return": 60000,
      "payback_period": "12-18个月",
      "roi_percentage": 350,
      "note": "内容资产持续产生价值"
    },
    "compound_effect": {
      "month_6": "用户数增加180",
      "month_12": "用户数增加720（累计）",
      "month_24": "用户数增加2880（累计）"
    }
  },
  "key_assumptions": [
    "SEO效果6个月后显现",
    "内容质量足够高",
    "持续投入至少12个月"
  ],
  "confidence": "Medium"
}
```

### 验证点

- [ ] 考虑长周期特性
- [ ] 展示复利效应
- [ ] 回本周期合理

---

## 测试用例 3：边界情况 - 高不确定性

### 输入

```json
{
  "mechanism": {
    "type": "未知",
    "description": "投放新渠道广告"
  },
  "business_metrics": {
    "unknown_metrics": true
  }
}
```

### 预期输出

```json
{
  "roi_analysis": {
    "feasibility": "Low",
    "reason": "关键指标未知，无法准确计算ROI"
  },
  "recommended_action": "先进行小规模测试收集数据",
  "minimum_test": {
    "budget": "预算的10%",
    "duration": "2周",
    "metrics_to_track": ["点击率", "转化率", "CAC"]
  },
  "confidence": "Low"
}
```

### 验证点

- [ ] 正确识别不确定性
- [ ] 推荐小规模测试

---

## 测试结果记录

| 用例 | 状态 | 通过/失败 | 备注 |
|------|------|-----------|------|
| TC1 | 待测试 | - | - |
| TC2 | 待测试 | - | - |
| TC3 | 待测试 | - | - |
