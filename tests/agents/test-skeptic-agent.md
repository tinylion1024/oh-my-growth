# Skeptic Agent 测试用例

## 测试概览

测试 Skeptic Agent 对假设挑战和风险识别的能力。

---

## 测试用例 1：因果链挑战

### 输入

```json
{
  "proposal": {
    "mechanism": "邀请裂变",
    "claimed_effect": "用户增长100%",
    "assumptions": [
      "用户愿意分享",
      "新用户会转化",
      "成本可控"
    ]
  },
  "evidence": {
    "case_references": ["Dropbox增长3900%"],
    "data_quality": "中等"
  }
}
```

### 预期输出

```json
{
  "skepticism_assessment": {
    "causal_chain_strength": "Medium",
    "weakest_link": "用户分享意愿未经验证",
    "assumption_challenges": [
      {
        "assumption": "用户愿意分享",
        "challenge": "是否有足够的分享动机？需要量化激励效果"
      },
      {
        "assumption": "新用户会转化",
        "challenge": "邀请用户质量可能低于自然用户"
      }
    ]
  },
  "alternative_explanations": [
    "增长可能来自其他渠道",
    "短期增长可能不可持续"
  ],
  "required_evidence": [
    "A/B测试数据",
    "邀请用户留存率",
    "单用户获取成本"
  ],
  "confidence_adjustment": "建议从High下调至Medium"
}
```

### 验证点

- [ ] 识别弱因果链
- [ ] 挑战关键假设
- [ ] 提供替代解释
- [ ] 要求必要证据

---

## 测试用例 2：风险评估

### 输入

```json
{
  "proposal": {
    "mechanism": "补贴获客",
    "budget": "100万元",
    "target_users": "10万新用户"
  },
  "context": {
    "stage": "0-1",
    "runway": "12个月"
  }
}
```

### 预期输出

```json
{
  "risk_assessment": {
    "severity": "High",
    "risks": [
      {
        "risk": "补贴用户质量低",
        "probability": "High",
        "impact": "高成本获取低价值用户"
      },
      {
        "risk": "补贴停止后流失",
        "probability": "Medium",
        "impact": "无法形成自然增长"
      },
      {
        "risk": "资金消耗过快",
        "probability": "High",
        "impact": "缩短runway"
      }
    ]
  },
  "mitigation_suggestions": [
    "设置补贴上限",
    "追踪补贴用户留存",
    "设计补贴退出策略"
  ],
  "recommendation": "建议小规模实验验证后再大规模投入"
}
```

### 验证点

- [ ] 识别重大风险
- [ ] 评估风险概率和影响
- [ ] 提供缓解措施
- [ ] 给出保守建议

---

## 测试用例 3：证据质量审查

### 输入

```json
{
  "proposal": {
    "mechanism": "游戏化提升留存",
    "evidence": [
      {
        "source": "Duolingo案例",
        "tier": "B"
      },
      {
        "source": "博客文章",
        "tier": "E"
      }
    ]
  }
}
```

### 预期输出

```json
{
  "evidence_review": {
    "overall_quality": "Medium",
    "strongest_evidence": {
      "source": "Duolingo案例",
      "quality": "良好，有公开数据支撑"
    },
    "weakest_evidence": {
      "source": "博客文章",
      "quality": "低，缺乏数据支撑"
    }
  },
  "confidence_adjustment": "建议降低置信度至Medium",
  "additional_evidence_needed": [
    "同类产品A/B测试结果",
    "用户行为数据分析"
  ]
}
```

### 验证点

- [ ] 评估证据质量
- [ ] 区分强/弱证据
- [ ] 调整置信度
- [ ] 要求补充证据
