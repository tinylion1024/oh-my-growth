# Orchestrator Agent 测试用例

## 测试概览

测试 Orchestrator Agent 自动编排工作流的能力。

---

## 测试用例 1：自动模式选择

### 输入

```json
{
  "user_input": {
    "problem": "如何提升用户留存？",
    "context": {
      "industry": "education",
      "stage": "1-10",
      "clarity_score": 75
    }
  }
}
```

### 预期输出

```json
{
  "orchestration": {
    "selected_mode": "design",
    "reason": "问题明确，清晰度足够，适合设计模式",
    "workflow": [
      {"step": 1, "agent": "Lead", "action": "问题分类"},
      {"step": 2, "agent": "Theory", "action": "匹配留存理论"},
      {"step": 3, "agent": "Weapon", "action": "推荐留存玩法"},
      {"step": 4, "agent": "Growth", "action": "评估机制可行性"},
      {"step": 5, "agent": "Skeptic", "action": "风险识别"},
      {"step": 6, "agent": "Narrative", "action": "生成报告"}
    ]
  }
}
```

### 验证点

- [ ] 正确选择模式
- [ ] 编排合理工作流
- [ ] 包含必要Agent

---

## 测试用例 2：信息不足时编排

### 输入

```json
{
  "user_input": {
    "problem": "我想做增长",
    "context": {
      "clarity_score": 30
    }
  }
}
```

### 预期输出

```json
{
  "orchestration": {
    "selected_mode": "assess",
    "reason": "信息不足，先评估澄清",
    "workflow": [
      {"step": 1, "agent": "Lead", "action": "识别缺失信息"},
      {"step": 2, "agent": "Guide", "action": "交互式引导"},
      {"step": 3, "agent": "Lead", "action": "重新分类"}
    ]
  }
}
```

### 验证点

- [ ] 识别信息不足
- [ ] 启动引导流程
- [ ] 不急于给出结论

---

## 测试用例 3：多模式组合编排

### 输入

```json
{
  "user_input": {
    "problem": "评估并设计裂变方案",
    "context": {
      "clarity_score": 80
    }
  }
}
```

### 预期输出

```json
{
  "orchestration": {
    "selected_mode": "assess + design",
    "workflow": [
      {"step": 1, "agent": "Lead", "action": "问题分类"},
      {"step": 2, "agent": "Case", "action": "匹配裂变案例"},
      {"step": 3, "agent": "ROI", "action": "评估ROI"},
      {"step": 4, "agent": "Skeptic", "action": "风险识别"},
      {"step": 5, "agent": "Weapon", "action": "推荐裂变玩法"},
      {"step": 6, "agent": "Growth", "action": "评估可行性"},
      {"step": 7, "agent": "Execution", "action": "评估执行可行性"},
      {"step": 8, "agent": "Narrative", "action": "生成报告"}
    ]
  }
}
```

### 验证点

- [ ] 支持多模式组合
- [ ] 编排完整工作流
- [ ] 包含所有必要Agent
