# Agent Contract - Agent契约

## 统一输入Schema

所有Agent接收以下输入结构：

```json
{
  "user_input": {
    "raw": "用户原始输入",
    "parsed": {
      "problem_type": "acquisition|activation|retention|...",
      "business_stage": "0-1|1-10|10-100",
      "industry": "ecommerce|saas|...",
      "intent": "assess|design|learn|audit|match"
    }
  },
  "knowledge_context": {
    "matched_cases": [...],
    "recommended_weapons": [...],
    "relevant_theories": [...]
  },
  "agent_outputs": {
    "previous_agent_name": {...}
  }
}
```

## 统一输出Schema

所有Agent输出以下结构：

```json
{
  "agent_name": "string",
  "assessment": {
    "feasibility": "High|Medium|Low",
    "summary": "一句话总结"
  },
  "analysis": {
    // Agent特定分析内容
  },
  "risks": ["string"],
  "recommendations": ["string"],
  "confidence": "High|Medium|Low",
  "evidence": {
    "has_case_support": boolean,
    "has_data_support": boolean,
    "supporting_cases": ["string"]
  }
}
```

## Agent职责边界

### Lead Agent
- **职责**：编排、分类、冲突解决
- **不负责**：具体领域分析
- **输出**：分类结果、Agent组配、综合判断

### Growth Agent
- **职责**：增长机制可行性
- **不负责**：变现分析、ROI计算
- **输出**：机制评估、漏斗分析、实验建议

### Monetization Agent
- **职责**：变现影响评估
- **不负责**：增长机制设计
- **输出**：变现评估、权衡分析、定价建议

### ROI Agent
- **职责**：投资回报计算
- **不负责**：机制可行性判断
- **输出**：ROI分析、成本结构、情景分析

### Execution Agent
- **职责**：执行可行性评估
- **不负责**：机制设计
- **输出**：资源需求、时间线、分阶段建议

### Skeptic Agent
- **职责**：假设挑战、风险识别
- **不负责**：正面分析
- **输出**：风险列表、假设质疑、最坏情况

### Case Agent
- **职责**：案例匹配
- **不负责**：决策判断
- **输出**：匹配案例、可复制点、注意事项

### Weapon Agent
- **职责**：玩法推荐
- **不负责**：可行性判断
- **输出**：推荐武器、组合建议、实施难度

### Theory Agent
- **职责**：理论支撑
- **不负责**：具体策略设计
- **输出**：相关理论、应用建议、北极星建议

### Narrative Agent
- **职责**：文档撰写
- **不负责**：分析判断
- **输出**：格式化文档

## 通信规则

### 1. 知识先行

```
知识Agent（Case/Weapon/Theory）先执行
→ 输出作为决策Agent的输入
```

### 2. 并行执行

```
决策Agent（Growth/Monetization/ROI/Execution/Skeptic）可并行
→ 各自独立输出，不相互依赖
```

### 3. 汇总顺序

```
所有Agent输出完成后
→ Lead Agent汇总
→ Narrative Agent输出
```

### 4. 不允许

- Agent之间直接通信
- Agent spawn其他Agent
- Agent修改其他Agent输出

## 置信度传递

### 置信度计算

```
Agent置信度 = 内部分析置信度 × 证据强度系数

其中：
- 有案例支撑：系数 = 1.2
- 有数据支撑：系数 = 1.1
- 无支撑：系数 = 0.8
```

### 整体置信度

```
整体置信度 = min(所有Agent置信度)

特殊情况：
- 任一Agent为Low → 整体不超过Medium
- Skeptic发现致命风险 → 整体为Low
```

## 错误处理

### Agent输出异常

```
if Agent输出格式不正确:
    → Lead Agent记录错误
    → 使用默认值继续
    → 在最终输出中标注
```

### Agent分歧

```
if Agent间存在分歧:
    → Lead Agent显式记录分歧
    → 应用冲突解决规则
    → 在输出中呈现分歧和解决依据
```
