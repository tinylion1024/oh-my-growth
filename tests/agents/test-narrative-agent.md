# Narrative Agent 测试用例

## 测试概览

测试 Narrative Agent 生成最终文档的能力。

---

## 测试用例 1：决策BRD生成

### 输入

```json
{
  "decision_context": {
    "problem": "用户增长放缓",
    "proposed_mechanism": "邀请裂变",
    "agent_outputs": {
      "growth": {"feasibility": "High"},
      "roi": {"expected_return": "3x"},
      "skeptic": {"confidence": "Medium"},
      "execution": {"feasibility": "High"}
    }
  }
}
```

### 预期输出

```json
{
  "document": {
    "executive_summary": "建议启动邀请裂变实验，预期ROI为3倍",
    "problem_statement": "当前用户增长放缓，月增速从20%降至5%",
    "proposed_mechanism": "双边奖励邀请机制",
    "causal_chain": "邀请奖励 → 用户分享 → 新用户注册 → 激活 → 付费",
    "roi_analysis": {
      "optimistic": "增长50%",
      "baseline": "增长20%",
      "pessimistic": "增长5%"
    },
    "resource_requirements": "开发2周，预算5万元",
    "key_assumptions": ["用户愿意分享", "新用户转化率>10%"],
    "risks": ["可能被滥用", "邀请用户质量低"],
    "decision": "建议小规模实验"
  },
  "format": "符合Output Contract"
}
```

### 验证点

- [ ] 包含所有必需章节
- [ ] 结构清晰
- [ ] 术语翻译为用户友好版本

---

## 测试用例 2：快速扫描报告生成

### 输入

```json
{
  "mode": "fast_scan",
  "problem": "是否值得做红包裂变？",
  "analysis": {
    "recommendation": "值得尝试",
    "reasons": ["案例支撑充分", "执行成本低"],
    "risks": ["可能吸引低质量用户"]
  }
}
```

### 预期输出

```json
{
  "document": {
    "one_line_advice": "建议尝试，成本低案例多",
    "key_reasons": [
      "1. 微信红包等案例验证有效",
      "2. 技术实现简单",
      "3. 可快速验证"
    ],
    "main_risk": "需设计防刷机制",
    "next_action": "设计实验方案，预算1-2万元"
  }
}
```

### 验证点

- [ ] 简洁明了
- [ ] 包含建议和风险
- [ ] 可操作性强
