# Growth Master 优化计划

基于 Yao Open Skills 精华分析，制定系统性优化方案。

---

## 一、优化目标

### 核心目标

将 Yao Open Skills 的 12 项精华整合进 Growth Master，提升：

1. **输入质量** - 现状清晰度门控，避免信息不足时盲目诊断
2. **决策安全** - 安全边界机制，避免高风险建议
3. **追问质量** - 结构化问题库，提升信息收集效率
4. **证据可信** - 证据分级系统，明确标记可信度
5. **输出一致** - 输出契约规范，统一报告结构

### 选择方案

**采用方案 A：最小侵入式**

- 在现有架构上打补丁，不改变核心结构
- 预估工作量：3 天
- 风险：低
- 优先级：P0 + P1 核心项

---

## 二、分阶段实施计划

### Phase 1：基础设施（Day 1 上午）

**目标**：建立 references 目录和核心配置文件

| 序号 | 任务 | 文件 | 说明 |
|:---:|------|------|------|
| 1.1 | 创建安全边界配置 | `references/safety-boundaries.md` | 定义高风险领域和响应规则 |
| 1.2 | 创建问题库 | `references/question-bank.md` | 结构化追问问题，按模式分类 |
| 1.3 | 创建输出契约 | `references/report-contract.md` | 统一报告结构和必选章节 |
| 1.4 | 创建现状清晰度配置 | `references/current-state-clarity.md` | 定义维度权重和门控阈值 |
| 1.5 | 更新主 SKILL | `SKILL.md` | 添加 decision_gates 和 safety_protocol |

**验证点**：
- [ ] 所有 references 文件已创建
- [ ] SKILL.md 包含新的配置段落
- [ ] 文件格式正确（Markdown）

---

### Phase 2：Agent 增强（Day 1 下午）

**目标**：为核心 Agent 添加新能力

| 序号 | 任务 | 文件 | 说明 |
|:---:|------|------|------|
| 2.1 | 增强 Lead Agent | `agents/core/lead-agent.md` | 添加多轮对话、现状门控、Reference Map |
| 2.2 | 增强 Guide Agent | `agents/core/guide-agent.md` | 引入问题库、追问策略 |
| 2.3 | 增强 Growth Agent | `agents/core/growth-agent.md` | 添加三问门控、第一性原理分层 |
| 2.4 | 增强 Skeptic Agent | `agents/core/skeptic-agent.md` | 添加安全边界检查 |
| 2.5 | 增强 Narrative Agent | `agents/core/narrative-agent.md` | 添加输出契约遵循 |

**验证点**：
- [ ] 所有核心 Agent 已更新
- [ ] 每个 Agent 包含 Reference Map
- [ ] 新能力配置已添加

---

### Phase 3：知识库增强（Day 2 上午）

**目标**：为知识索引添加证据分级

| 序号 | 任务 | 文件 | 说明 |
|:---:|------|------|------|
| 3.1 | 更新案例索引 | `knowledge/indexes/cases-index.json` | 添加 evidence_tier 字段 |
| 3.2 | 更新玩法索引 | `knowledge/indexes/weapons-index.json` | 添加 evidence_tier 字段 |
| 3.3 | 更新理论索引 | `knowledge/indexes/theories-index.json` | 添加 evidence_tier 字段 |
| 3.4 | 创建证据分级说明 | `references/evidence-tiers.md` | 定义 A/B/C/D/E 五级标准 |

**验证点**：
- [ ] 所有索引文件包含 evidence_tier 字段
- [ ] 证据分级说明已创建
- [ ] JSON 格式正确

---

### Phase 4：脚本与验证（Day 2 下午）

**目标**：添加现状清晰度评估脚本

| 序号 | 任务 | 文件 | 说明 |
|:---:|------|------|------|
| 4.1 | 创建清晰度评估脚本 | `scripts/assess_clarity.py` | 评估现状清晰度，输出追问问题 |
| 4.2 | 创建报告验证脚本 | `scripts/verify_report.py` | 验证输出契约遵循 |
| 4.3 | 更新测试套件 | `tests/run-tests.sh` | 添加新脚本测试 |

**验证点**：
- [ ] 脚本可执行
- [ ] 测试通过
- [ ] 输出格式正确

---

### Phase 5：文档更新（Day 3）

**目标**：更新所有文档，确保一致性

| 序号 | 任务 | 文件 | 说明 |
|:---:|------|------|------|
| 5.1 | 更新 README | `README.md` | 添加新功能说明 |
| 5.2 | 更新用户指南 | `docs/user-guide.md` | 添加新使用方式 |
| 5.3 | 更新开发者指南 | `docs/developer-guide.md` | 添加新架构说明 |
| 5.4 | 更新最佳实践 | `docs/best-practices.md` | 添加新最佳实践 |
| 5.5 | 创建变更日志 | `CHANGELOG.md` | 记录本次优化 |

**验证点**：
- [ ] 所有文档已更新
- [ ] 内容一致
- [ ] 无死链接

---

## 三、详细任务清单

### Task 1.1：创建安全边界配置

**文件**：`references/safety-boundaries.md`

**内容框架**：
```markdown
# Safety Boundaries

## 硬边界领域

### 财务风险
- 触发词：投资、融资、估值、定价、重大支出
- 响应：提供决策框架，不提供最终投资建议
- 警告：重大财务决策建议咨询专业顾问

### 法律风险
- 触发词：合规、合同、知识产权、竞争法、监管
- 响应：提供风险清单和准备问题，不提供法律建议
- 警告：法律风险建议咨询律师

### 运营风险
- 触发词：裁员、重大组织变更、品牌危机
- 响应：提供分析框架，不提供执行建议
- 警告：重大运营决策建议咨询专业顾问

## 响应规则

1. 检测到高风险领域时，添加警告声明
2. 不让高评分覆盖硬安全边界
3. 高风险案例的行动建议必须可逆、保守、审查导向

## 报告要求

高风险案例必须包含：
- 风险边界章节
- 专业审查触发条件
- 低风险下一步建议
```

---

### Task 1.2：创建问题库

**文件**：`references/question-bank.md`

**内容框架**：
```markdown
# Question Bank

## 快速扫描模式（3 问）

1. **目标锁定**：你希望这个问题在什么期限内变成什么状态？怎样算解决？
2. **稀缺资源**：现在最稀缺的是时间、人、钱、权限、注意力、信任，还是数据？
3. **单问题测试**：如果 30 天只能解决一个问题，解决哪个会带来最大变化？

## 战略设计模式（5 问）

1. **阶段识别**：这是启动期、验证期、增长期、修复期、转型期，还是恢复期？
2. **事实与解释分离**：哪些是已经发生的事实？哪些是你的解释、担心或推测？
3. **内外因分离**：哪些因素你能直接改变？哪些只能影响、规避或等待？
4. **重复模式**：类似问题出现过几次？通常在什么节点爆发？
5. **相关方冲突**：涉及哪些人？每个人最在意的结果分别是什么？

## 决策 BRD 模式（7 问）

1. **目标与成功标准**：...
2. **当前阶段**：...
3. **稀缺资源**：...
4. **硬约束**：...
5. **已尝试动作**：...
6. **相关方利益**：...
7. **复盘条件**：...

## 上游诊断问题

用于从症状上升到根因：

- 这些看得见的问题背后，有没有一个共同原因？
- 如果当前阶段只能改变一个变量，哪一个会让多个可见问题更容易？
- 哪个约束解释了为什么有能力的人仍然被困在细节中？
- 领导者当前最高杠杆的工作是什么：做、决定、招聘、销售、学习、修复信任，还是建立系统？
```

---

### Task 1.3：创建输出契约

**文件**：`references/report-contract.md`

**内容框架**：
```markdown
# Report Contract

## 必选章节

### 1. 先看结论
- 最该先解决什么
- 为什么是它
- 置信度（高/中/低）
- 第一个行动

### 2. 先把现状说清楚
- 目标
- 阶段
- 约束
- 资源
- 关键事实（标记 observed/estimated/assumed）

### 3. 现状够不够清楚
- 清晰度评分（0-100）
- 是否可以开始诊断
- 缺失的关键信息

### 4. 判断过程
- 至少 3 个候选方案对比
- 评分依据
- 为什么不是其他选项

### 5. 推荐方案
- 明确命名
- 核心理由
- 实施路径

### 6. 资源分配建议
- 主攻线：50%-70%
- 次要线：10%-25%
- 监控线：10%-20%

### 7. 接下来怎么做
- 1-3 个突破行动
- 每个行动的负责人、期限、资源、验收标准

### 8. 做完以后可能怎样
- 概率区间
- 假设敏感性
- 什么证据会改变判断

### 9. 什么时候回头看
- 复盘时间
- 转移信号
- 新证据收集

### 10. 注意事项
- 专业边界警告
- 不确定性声明

## 语言规范

- 结论在前，推理在后
- 概念术语后紧跟实用翻译
- 标记事实为 observed/estimated/assumed
- 每个行动必须说明改变什么
```

---

### Task 1.4：创建现状清晰度配置

**文件**：`references/current-state-clarity.md`

**内容框架**：
```markdown
# Current State Clarity

## 评估维度

| 维度 | 权重 | 什么算清楚 |
| --- | ---: | --- |
| 目标和成功标准 | 20 | 用户说明了应该变成什么状态、期限、怎样算成功 |
| 事实和证据 | 20 | 至少 2 个具体的观察或估计事实，不只是解释 |
| 阶段 | 12 | 当前阶段已命名：启动、验证、增长、修复、转型、恢复等 |
| 稀缺资源 | 12 | 时间、人、现金、权限、注意力、信任、数据、精力约束已明确 |
| 硬约束 | 12 | 法律、健康、安全、伦理、现金、关系、承诺边界已明确 |
| 相关方 | 8 | 相关人员或组织及其利益已可见 |
| 重复模式 | 8 | 用户说明了重复出现、触发点、之前尝试、缺失证据 |

## 门控阈值

- **0-54（insufficient）**：不输出主要结论，问最多 3 个关键问题
- **55-74（workable）**：输出临时判断，问剩余问题
- **75-100（clear）**：深入诊断，输出完整报告

## 硬性要求

诊断前必须满足：
- 目标带期限或成功指标
- 至少 2 个具体事实（observed 或 estimated）
- 稀缺资源已明确
- 硬约束已明确

## 追问策略

信息不足时，按优先级问：
1. 目标与成功标准
2. 事实与证据
3. 稀缺资源
4. 硬约束
5. 阶段
6. 相关方
7. 重复模式
```

---

### Task 1.5：更新主 SKILL

**文件**：`SKILL.md`

**添加内容**：
```yaml
## Decision Gates

现状清晰度门控，避免信息不足时盲目诊断：

decision_gates:
  current_state_clarity:
    enabled: true
    dimensions:
      - goal_success: 20      # 目标与成功标准
      - facts_evidence: 20    # 事实与证据
      - stage: 12             # 阶段判断
      - scarce_resources: 12  # 稀缺资源
      - hard_constraints: 12  # 硬约束
      - stakeholders: 8       # 相关方
      - repeated_patterns: 8  # 重复模式
    thresholds:
      insufficient: 54        # 停止诊断，追问
      workable: 74            # 临时判断
      clear: 75               # 深入诊断

## Safety Protocol

安全边界机制，避免高风险建议：

safety_protocol:
  enabled: true
  check_triggers: true
  block_high_risk_recommendations: true
  require_professional_disclaimer: true
  domains:
    - financial               # 财务风险
    - legal                   # 法律风险
    - regulatory              # 监管风险
    - operational             # 运营风险

## Output Contract

输出契约，确保报告一致性：

output_contract:
  required_sections:
    - conclusion              # 先看结论
    - current_state           # 现状说清楚
    - clarity_assessment      # 现状清晰度
    - decision_process        # 判断过程
    - recommendation          # 推荐方案
    - resource_allocation     # 资源分配
    - actions                 # 接下来怎么做
    - projection              # 做完以后可能怎样
    - review_trigger          # 什么时候回头看
    - caveats                 # 注意事项
```

---

### Task 2.1：增强 Lead Agent

**文件**：`agents/core/lead-agent.md`

**添加内容**：
```yaml
## 多轮对话模式

dialogue_mode:
  enabled: true
  max_rounds: 5
  min_questions_per_round: 1
  max_questions_per_round: 3

## 现状清晰度门控

clarity_gate:
  reference: "../../references/current-state-clarity.md"
  action_on_insufficient:
    - 停止诊断
    - 输出现状快照
    - 提出最多 3 个关键问题
  action_on_workable:
    - 输出临时判断
    - 标记为"临时判断，等待更多证据"
    - 提出剩余问题
  action_on_clear:
    - 深入诊断
    - 输出完整报告

## Reference Map

- `../../references/current-state-clarity.md`: 现状清晰度门控
- `../../references/safety-boundaries.md`: 安全边界
- `../../references/question-bank.md`: 问题库
- `../../references/report-contract.md`: 输出契约
- `../core/orchestrator-agent.md`: 编排和冲突解决
- `../../knowledge/indexes/cases-index.json`: 案例知识库
- `../../knowledge/indexes/weapons-index.json`: 玩法知识库
- `../../knowledge/indexes/theories-index.json`: 理论知识库
```

---

### Task 2.2：增强 Guide Agent

**文件**：`agents/core/guide-agent.md`

**添加内容**：
```yaml
## 问题库引用

question_bank:
  reference: "../../references/question-bank.md"
  
  mode_selection:
    fast_scan: 3 问
    strategy_design: 5 问
    decision_brd: 7 问

## 追问策略

follow_up_strategy:
  principle: "先追问后判断"
  max_questions_initial: 3
  max_questions_total: 7
  
  priority_order:
    1. 目标与成功标准
    2. 事实与证据
    3. 稀缺资源
    4. 硬约束
    5. 阶段
    6. 相关方
    7. 重复模式

## Reference Map

- `../../references/question-bank.md`: 问题库
- `../../references/current-state-clarity.md`: 现状清晰度门控
- `../core/lead-agent.md`: 主控 Agent
```

---

### Task 2.3：增强 Growth Agent

**文件**：`agents/core/growth-agent.md`

**添加内容**：
```yaml
## 三问门控

three_question_gate:
  decisiveness:
    question: "不解决它，当前目标是不是很难真正推进？"
    fail_signal: "解决它会有用，但不会移动目标指标"
  
  leverage:
    question: "解决它后，多个表面问题会不会一起变轻？"
    fail_signal: "它只修复一个局部痛点"
  
  stage_fit:
    question: "在当前期限、资源和阶段里，它是不是最该先抓？"
    fail_signal: "它重要，但属于后续阶段"

## 第一性原理分层

first_principles_gate:
  layer_1:
    name: "看得见的问题"
    description: "用户已经能叫出名字的症状"
  
  layer_2:
    name: "上升一层"
    description: "哪个隐藏变量可以同时解释多个可见问题"
  
  layer_3:
    name: "看不见的根部变量"
    description: "用运营术语命名上游约束"
  
  layer_4:
    name: "反证"
    description: "什么证据能证明可见问题其实不是主要矛盾"

## Reference Map

- `../../references/current-state-clarity.md`: 现状清晰度门控
- `../core/lead-agent.md`: 主控 Agent
- `../../knowledge/indexes/weapons-index.json`: 玩法知识库
- `../../knowledge/indexes/theories-index.json`: 理论知识库
```

---

### Task 2.4：增强 Skeptic Agent

**文件**：`agents/core/skeptic-agent.md`

**添加内容**：
```yaml
## 安全边界检查

safety_check:
  reference: "../../references/safety-boundaries.md"
  
  check_triggers:
    - 财务风险关键词
    - 法律风险关键词
    - 监管风险关键词
    - 运营风险关键词
  
  on_detection:
    - 添加警告声明
    - 降低建议置信度
    - 要求专业审查

## Reference Map

- `../../references/safety-boundaries.md`: 安全边界
- `../core/lead-agent.md`: 主控 Agent
```

---

### Task 2.5：增强 Narrative Agent

**文件**：`agents/core/narrative-agent.md`

**添加内容**：
```yaml
## 输出契约遵循

output_contract:
  reference: "../../references/report-contract.md"
  
  required_sections:
    - conclusion
    - current_state
    - clarity_assessment
    - decision_process
    - recommendation
    - resource_allocation
    - actions
    - projection
    - review_trigger
    - caveats
  
  language_rules:
    - 结论在前，推理在后
    - 概念术语后紧跟实用翻译
    - 标记事实为 observed/estimated/assumed

## Reference Map

- `../../references/report-contract.md`: 输出契约
- `../core/lead-agent.md`: 主控 Agent
```

---

### Task 3.1-3.3：更新知识索引

**文件**：`knowledge/indexes/cases-index.json` 等

**添加字段**：
```json
{
  "cases": [
    {
      "id": "case-001",
      "name": "案例名称",
      "evidence_tier": "B",
      "evidence_sources": ["公开数据集", "行业报告"],
      "confidence": 0.75,
      "tier_description": "同行评审论文、公开数据集、行业标准"
    }
  ]
}
```

**证据分级标准**：
- A：元分析、系统综述、官方统计
- B：同行评审论文、公开数据集、行业标准
- C：专家意见、内部数据、现场证据
- D：LLM 建议、类比、常识
- E：博客、营销文案、未注明来源

---

### Task 4.1：创建清晰度评估脚本

**文件**：`scripts/assess_clarity.py`

**功能**：
- 读取用户输入 JSON
- 评估 7 个维度得分
- 计算总分和清晰度等级
- 输出缺失维度和追问问题

---

### Task 4.2：创建报告验证脚本

**文件**：`scripts/verify_report.py`

**功能**：
- 检查必选章节存在
- 检查事实标记正确
- 检查安全警告存在
- 检查资源分配合理

---

## 四、验证检查清单

### Phase 1 完成验证

- [ ] `references/safety-boundaries.md` 已创建
- [ ] `references/question-bank.md` 已创建
- [ ] `references/report-contract.md` 已创建
- [ ] `references/current-state-clarity.md` 已创建
- [ ] `SKILL.md` 包含 decision_gates 配置
- [ ] `SKILL.md` 包含 safety_protocol 配置

### Phase 2 完成验证

- [ ] `agents/core/lead-agent.md` 包含多轮对话配置
- [ ] `agents/core/lead-agent.md` 包含 Reference Map
- [ ] `agents/core/guide-agent.md` 包含问题库引用
- [ ] `agents/core/growth-agent.md` 包含三问门控
- [ ] `agents/core/skeptic-agent.md` 包含安全边界检查
- [ ] `agents/core/narrative-agent.md` 包含输出契约

### Phase 3 完成验证

- [ ] `knowledge/indexes/cases-index.json` 包含 evidence_tier
- [ ] `knowledge/indexes/weapons-index.json` 包含 evidence_tier
- [ ] `knowledge/indexes/theories-index.json` 包含 evidence_tier
- [ ] `references/evidence-tiers.md` 已创建

### Phase 4 完成验证

- [ ] `scripts/assess_clarity.py` 可执行
- [ ] `scripts/verify_report.py` 可执行
- [ ] 测试通过

### Phase 5 完成验证

- [ ] `README.md` 已更新
- [ ] `docs/user-guide.md` 已更新
- [ ] `docs/developer-guide.md` 已更新
- [ ] `CHANGELOG.md` 已创建

---

## 五、风险与注意事项

### 风险

1. **兼容性风险**：新配置可能与现有 Agent 冲突
   - 缓解：渐进式添加，保持向后兼容

2. **性能风险**：门控机制可能增加延迟
   - 缓解：门控检查轻量化，仅评估必要维度

3. **用户接受风险**：追问可能让用户不耐烦
   - 缓解：限制最多 3 个初始问题，提供跳过选项

### 注意事项

1. **保持简洁**：新配置不应过度复杂化现有架构
2. **文档同步**：所有变更必须同步更新文档
3. **测试覆盖**：新脚本必须有对应测试
4. **版本记录**：CHANGELOG 必须记录所有变更

---

## 六、成功标准

### 定量标准

- [ ] 所有 5 个 Phase 完成
- [ ] 所有验证检查通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] 文档一致性检查通过

### 定性标准

- [ ] 现状清晰度门控正常工作
- [ ] 安全边界警告正确触发
- [ ] 问题库问题有效引导用户
- [ ] 输出契约确保报告一致
- [ ] 证据分级提升可信度透明度

---

## 七、执行顺序

```
Day 1 上午: Phase 1 (基础设施)
    ↓
Day 1 下午: Phase 2 (Agent 增强)
    ↓
Day 2 上午: Phase 3 (知识库增强)
    ↓
Day 2 下午: Phase 4 (脚本与验证)
    ↓
Day 3: Phase 5 (文档更新)
    ↓
验证 & 发布
```

---

## 八、下一步行动

1. **确认计划**：用户审阅并确认优化计划
2. **开始执行**：从 Phase 1 开始实施
3. **迭代验证**：每个 Phase 完成后验证
4. **最终发布**：所有 Phase 完成后发布

准备好后，可以开始执行 Phase 1。
