# Workflow - 工作流与路由

## 模式选择决策树

```
用户输入
    │
    ▼
┌─────────────────────────────────────┐
│ Step 1: 意图识别                     │
│                                     │
│ 用户想要：                           │
│   - 先形成判断？→ diagnose           │
│   - 评估机会？→ assess               │
│   - 设计策略？→ design               │
│   - 学习知识？→ learn                │
│   - 审计方案？→ audit                │
│   - 匹配案例？→ match                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Step 2: 问题分类                     │
│                                     │
│ Lead Agent 分析：                    │
│   - 问题类型                         │
│   - 业务阶段                         │
│   - 行业特征                         │
│   - 资源约束                         │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Step 3: 模式选择                     │
│                                     │
│ if 需要先找主矛盾和优先级:           │
│     → Strategy Brain                │
│ elif 证据充分 && 需要正式决策:       │
│     → Decision BRD                  │
│ elif 需要具体策略:                   │
│     → Strategy Design               │
│ elif 寻找参考案例:                   │
│     → Case Match                    │
│ elif 系统学习:                       │
│     → Learning Path                 │
│ else:                               │
│     → Fast Scan                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Step 4: Agent组配                    │
│                                     │
│ 根据模式选择最小必要Agent集合         │
└─────────────────────────────────────┘
```

## 六大模式详解

### 0. Strategy Brain (策略外脑)

**触发条件**：
- 增长负责人需要先形成判断
- 需要明确主矛盾和优先级
- 需要“建议做/不做 + 最小实验”

**Agent组合**：
- Lead Agent
- Growth Agent
- ROI Agent
- Skeptic Agent
- Case Agent
- Weapon Agent

**流程**：
```
Lead诊断 → [Case, Weapon]检索 → [Growth, ROI, Skeptic]判断 → Lead排序 → Narrative输出
```

**输出**：
- 一句话判断
- 核心矛盾
- 优先级排序
- 建议现在做 / 先别做
- 两周实验

---

### 1. Fast Scan (快速扫描)

**触发条件**：
- 初步想法，证据不足
- 需要快速判断
- 非正式决策

**Agent组合**：
- Lead Agent（编排）
- ROI Agent（快速ROI评估）
- Skeptic Agent（风险识别）
- Case Agent（可选，案例参考）

**流程**：
```
Lead分类 → [ROI, Skeptic]并行 → Lead汇总 → Narrative输出
```

**输出**：
- 一句话建议
- 核心理由（2-3点）
- 主要风险
- 下一步行动

### 2. Decision BRD (决策文档)

**触发条件**：
- 需要预算/资源/人力
- 正式决策文档
- 多方评审

**Agent组合**：
- Lead Agent
- Growth Agent
- Monetization Agent
- ROI Agent
- Execution Agent
- Skeptic Agent
- Case Agent
- Weapon Agent
- Narrative Agent

**流程**：
```
Lead分类 → [Case, Weapon]知识检索 → [Growth, Monetization, ROI, Execution, Skeptic]并行评估 → Lead冲突解决 → Narrative输出
```

**输出**：
- 执行摘要
- 业务问题与机会
- 提议机制
- ROI分析（三种情景）
- 资源需求
- 关键假设
- 风险与反对意见
- 案例参考
- 决策与下一步

### 3. Strategy Design (策略设计)

**触发条件**：
- 需要具体增长策略
- 玩法组合建议
- 实施路径规划

**Agent组合**：
- Lead Agent
- Growth Agent
- Weapon Agent
- Theory Agent
- Narrative Agent

**流程**：
```
Lead分类 → [Weapon, Theory]知识检索 → Growth评估 → Narrative输出
```

**输出**：
- 策略方向
- 推荐玩法组合
- 成功案例参考
- 实施路径
- 关键指标

### 4. Case Match (案例匹配)

**触发条件**：
- 寻找参考案例
- 借鉴成功经验

**Agent组合**：
- Lead Agent
- Case Agent
- Theory Agent

**流程**：
```
Lead分类 → Case检索 → Theory支撑 → 输出
```

**输出**：
- 匹配案例列表
- 各案例核心策略
- 可复制要点
- 注意事项

### 5. Learning Path (学习路径)

**触发条件**：
- 系统学习增长知识
- 了解理论流派

**Agent组合**：
- Lead Agent
- Theory Agent
- Narrative Agent

**流程**：
```
Lead识别学习需求 → Theory推荐 → Narrative输出
```

**输出**：
- 推荐学习模块
- 相关理论流派
- 案例+玩法组合
- 进阶路径

## Agent执行顺序

### 并行执行组

以下Agent可以并行执行：

```
Group 1 (知识检索):
  - Case Agent
  - Weapon Agent
  - Theory Agent

Group 2 (决策评估):
  - Growth Agent
  - Monetization Agent
  - ROI Agent
  - Execution Agent
  - Skeptic Agent
```

### 顺序依赖

```
Lead分类 → 知识检索组 → 决策评估组 → Lead汇总 → Narrative输出
```

## 冲突解决

### 冲突类型

| 类型 | 说明 | 解决原则 |
|------|------|----------|
| 评估分歧 | 不同Agent对可行性判断不同 | 证据强度优先 |
| 优先级分歧 | 不同Agent对优先级判断不同 | ROI权重优先 |
| 风险评估分歧 | 对风险严重程度判断不同 | Skeptic优先 |

### 解决规则

1. **证据优先**：有案例/数据支撑的论点权重更高
2. **怀疑优先**：因果链弱时，Skeptic胜出
3. **ROI优先**：收益不确定时，ROI胜出
4. **执行优先**：资源不现实时，Execution胜出
5. **增长+变现**：混合提案需要两个Agent都认可
6. **信任优先**：机制损害用户信任时，降低优先级

## 置信度评估

### 置信度定义

| 级别 | 定义 | 建议 |
|------|------|------|
| High | 强证据、可测试机制、执行可控 | 可直接决策 |
| Medium | 可行机制但有重要假设 | 推荐小实验验证 |
| Low | 证据稀少、重大未知 | 转化为学习/研究 |

### 综合置信度

```
整体置信度 = min(Agent置信度) × 证据强度系数

其中：
- 证据强度系数：有案例支撑时为1.2，无案例时为0.8
- 任一Agent为Low时，整体不超过Medium
```

## 异常处理

### 证据不足

```
if 关键假设无证据支撑:
    → 降级为Fast Scan
    → 明确列出需要收集的证据
    → 推荐小实验而非全量投入
```

### Agent分歧严重

```
if Agent间分歧无法通过规则解决:
    → 显式呈现分歧
    → 转化为验证问题
    → 推荐分阶段决策
```

### 资源约束

```
if 资源需求超出能力:
    → Execution Agent提出分阶段方案
    → 推荐MVP范围
    → 明确最小可行投入
```
