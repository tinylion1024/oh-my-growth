# Lead Agent 测试用例

## 测试概览

测试 Lead Agent 的问题分类、模式选择、Agent 组配能力。

---

## 测试用例 1：SaaS 获客问题

### 输入

```json
{
  "user_input": {
    "raw": "我们是一个SaaS协作工具，目前有5000注册用户，月活只有800，想通过邀请裂变来增长",
    "parsed": {}
  }
}
```

### 预期输出

```json
{
  "classification": {
    "problem_type": "acquisition",
    "business_stage": "1-10",
    "industry": "saas"
  },
  "mode": "Fast Scan 或 Strategy Design",
  "agent_set": ["Lead", "Growth", "ROI", "Skeptic", "Case"],
  "confidence": "High|Medium|Low"
}
```

### 验证点

- [ ] 正确识别问题类型为 `acquisition`
- [ ] 正确识别业务阶段为 `1-10`
- [ ] 正确识别行业为 `saas`
- [ ] 选择了合适的模式
- [ ] Agent 集合包含必要 Agent

---

## 测试用例 2：电商留存问题

### 输入

```json
{
  "user_input": {
    "raw": "我们电商平台日活10万，用户首购后流失率60%，想设计留存策略",
    "parsed": {}
  }
}
```

### 预期输出

```json
{
  "classification": {
    "problem_type": "retention",
    "business_stage": "10-100",
    "industry": "ecommerce"
  },
  "mode": "Strategy Design",
  "agent_set": ["Lead", "Growth", "Weapon", "Theory", "Narrative"],
  "confidence": "High|Medium|Low"
}
```

### 验证点

- [ ] 正确识别问题类型为 `retention`
- [ ] 正确识别业务阶段为 `10-100`
- [ ] 正确识别行业为 `ecommerce`
- [ ] 选择 Strategy Design 模式
- [ ] 包含 Weapon Agent

---

## 测试用例 3：变现定价问题

### 输入

```json
{
  "user_input": {
    "raw": "我们的内容平台有100万用户，想设计付费会员体系，不知道如何定价",
    "parsed": {}
  }
}
```

### 预期输出

```json
{
  "classification": {
    "problem_type": "monetization",
    "business_stage": "10-100",
    "industry": "content"
  },
  "mode": "Decision BRD",
  "agent_set": ["Lead", "Monetization", "ROI", "Execution", "Skeptic", "Narrative"],
  "confidence": "High|Medium|Low"
}
```

### 验证点

- [ ] 正确识别问题类型为 `monetization`
- [ ] 包含 Monetization Agent
- [ ] 包含 ROI Agent
- [ ] 选择 Decision BRD 或 Strategy Design 模式

---

## 测试用例 4：混合问题

### 输入

```json
{
  "user_input": {
    "raw": "我们想通过裂变活动同时获取新用户和提升收入",
    "parsed": {}
  }
}
```

### 预期输出

```json
{
  "classification": {
    "problem_type": "hybrid",
    "sub_types": ["acquisition", "monetization"]
  },
  "mode": "Decision BRD",
  "agent_set": ["Lead", "Growth", "Monetization", "ROI", "Skeptic"],
  "confidence": "Medium|Low"
}
```

### 验证点

- [ ] 正确识别为混合问题
- [ ] 同时包含 Growth 和 Monetization Agent
- [ ] 置信度应该较低（信息不足）

---

## 测试用例 5：边界情况 - 信息不足

### 输入

```json
{
  "user_input": {
    "raw": "我想增长",
    "parsed": {}
  }
}
```

### 预期输出

```json
{
  "classification": {
    "problem_type": "unknown",
    "business_stage": "unknown",
    "industry": "unknown"
  },
  "mode": "需要更多信息",
  "confidence": "Low",
  "missing_info": ["问题类型", "业务阶段", "行业", "具体挑战"]
}
```

### 验证点

- [ ] 正确识别信息不足
- [ ] 列出缺失信息
- [ ] 不做武断判断

---

## 测试用例 6：边界情况 - 冲突解决

### 输入

```json
{
  "agent_outputs": {
    "growth_agent": {
      "feasibility": "High",
      "confidence": "High"
    },
    "skeptic_agent": {
      "feasibility": "Low",
      "fatal_risks": ["因果链薄弱", "证据不足"],
      "confidence": "High"
    }
  }
}
```

### 预期输出

```json
{
  "conflict_resolution": {
    "disagreement": "Growth Agent 认为可行，Skeptic Agent 认为风险高",
    "resolution": "Skeptic 优先 - 因果链弱时怀疑胜出",
    "final_verdict": "Low 或 Medium",
    "reasoning": "因果链薄弱，需要更多证据支撑"
  }
}
```

### 验证点

- [ ] 正确识别 Agent 分歧
- [ ] 应用正确的冲突解决规则
- [ ] 输出合理的最终判断

---

## 测试结果记录

| 用例 | 状态 | 通过/失败 | 备注 |
|------|------|-----------|------|
| TC1 | 待测试 | - | - |
| TC2 | 待测试 | - | - |
| TC3 | 待测试 | - | - |
| TC4 | 待测试 | - | - |
| TC5 | 待测试 | - | - |
| TC6 | 待测试 | - | - |
