# Yao Open Skills 精华分析报告

## 分析目的

深度分析 yao-open-skills 项目，识别可吸收进 Growth Master 的精华内容。

## 分析范围

- yao-crux-skill（主次矛盾诊断）
- yao-bayesian-skill（证据到行动决策）
- yao-business-skill（商业模式分析）
- yao-gametheory-skill（博弈论战略报告）
- yao-tutorial-skill（教程生产）
- 相关 reference 文件和脚本

---

## 一、核心精华提炼

### 1. 现状清晰度门控机制（Current-State Clarity Gate）

**来源**: yao-crux-skill/references/intake-and-questioning.md

**精华内容**:
```text
| 维度 | 权重 | 什么算清楚 |
| --- | ---: | --- |
| 目标和成功标准 | 20 | 用户说明了应该变成什么状态、期限、怎样算成功 |
| 事实和证据 | 20 | 至少2个具体的观察或估计事实，不只是解释 |
| 阶段 | 12 | 当前阶段已命名：启动、验证、增长、修复、转型、恢复等 |
| 稀缺资源 | 12 | 时间、人、现金、权限、注意力、信任、数据、精力约束已明确 |
| 硬约束 | 12 | 法律、健康、安全、伦理、现金、关系、承诺边界已明确 |
| 相关方 | 8 | 相关人员或组织及其利益已可见 |
| 重复模式和已尝试动作 | 8 | 用户说明了重复出现、触发点、之前尝试、缺失证据 |

门控规则:
- 0-54: insufficient - 不输出主要矛盾，问最多3个关键问题
- 55-74: workable - 输出现状快照和临时判断，问剩余问题
- 75-100: clear - 重述现状快照，请用户确认或修正后再深入诊断
```

**可吸收价值**:
- Growth Master 当前缺乏"输入质量门控"，经常在信息不足时就开始分析
- 可以引入类似的清晰度评分和门控机制
- 代码实现参考: `scripts/current_state_clarity.py`

**建议整合方式**:
```yaml
# 在 growth-master/SKILL.md 中添加
decision_gates:
  current_state_clarity:
    dimensions:
      - goal_success: 20  # 目标与成功标准
      - facts_evidence: 20  # 事实与证据
      - stage: 12  # 阶段判断
      - scarce_resources: 12  # 稀缺资源
      - hard_constraints: 12  # 硬约束
      - stakeholders: 8  # 相关方
      - repeated_patterns: 8  # 重复模式
    thresholds:
      insufficient: 54  # 停止诊断，追问
      workable: 74  # 临时判断
      clear: 75  # 深入诊断
```

---

### 2. 证据分级系统（Evidence Quality Tiers）

**来源**: yao-bayesian-skill/references/evidence-prior-playbook.md

**精华内容**:
```text
| 等级 | 典型来源 | 如何使用 |
| --- | --- | --- |
| A | 元分析、系统综述、监管指南、官方统计、权威教材 | 强先验或强更新输入 |
| B | 同行评审论文、公开数据集、行业标准、良好文档的基准 | 中等强度先验或更新输入 |
| C | 结构化专家意见、内部历史数据、仔细收集的现场证据 | 可用但需明确说明 |
| D | LLM建议、类比、常识、非正式启发式 | 仅作为弱先验 |
| E | 博客文章、营销文案、社交媒体、未注明来源的声称 | 不作为核心证据 |
```

**可吸收价值**:
- Growth Master 的案例、玩法、理论可以按此标准分级
- 决策建议的可信度可以基于证据等级加权
- 当前 knowledge/indexes 缺乏证据等级标记

**建议整合方式**:
```json
// 在 knowledge/indexes/cases-index.json 中添加
{
  "cases": [
    {
      "id": "case-001",
      "name": "案例名称",
      "evidence_tier": "B",  // 新增字段
      "evidence_sources": ["公开数据集", "行业报告"],
      "confidence": 0.75
    }
  ]
}
```

---

### 3. 多轮对话与弱先验机制（Multi-Turn Dialogue with Weak Priors）

**来源**: yao-bayesian-skill/references/multi-turn-dialogue-loop.md

**精华内容**:
```text
核心原则：从不完整输入开始，先给弱先验和初步判断

迭代循环:
1. 用户提供输入
2. 识别缺失信息
3. 建立弱先验（明确标记为弱）
4. 提出最小必要问题
5. 收集新证据
6. 更新先验和后验
7. 记录概率变化和决策准备度
8. 判断是否足够成熟行动

每轮记录:
- prior: 当前先验
- posterior: 更新后后验
- readiness: 决策准备度
- gaps: 剩余信息缺口
- update_path: 使用的更新路径
```

**可吸收价值**:
- Growth Master 的 5 种决策模式可以都支持"多轮迭代"
- 当前设计假设"一次性输入"，不够灵活
- 引入"决策准备度"概念，避免过早下结论

**建议整合方式**:
```yaml
# 在 agents/core/lead-agent.md 中添加
dialogue_mode:
  enabled: true
  max_rounds: 5
  min_questions_per_round: 1
  max_questions_per_round: 3
  
round_log:
  fields:
    - round_number
    - user_input_summary
    - prior_state
    - new_evidence
    - posterior_state
    - readiness_score  # 0-100
    - remaining_gaps
    - next_questions
```

---

### 4. 输出契约与报告结构（Output Contract & Report Structure）

**来源**: yao-crux-skill/references/report-contract.md

**精华内容**:
```text
报告必选章节（用户友好标题）:
1. 先看结论 - 最该先解决什么，为什么是它
2. 先把现状说清楚 - 目标、阶段、约束、资源、关键事实
3. 现状够不够清楚 - 清晰度评分，是否可以开始诊断
4. 一张图看懂：从表象到主要矛盾 - 分析流程图、冰山模型
5. 主要矛盾判断过程 - 从可见症状到上游约束
6. 主要矛盾（最关键的卡点）- 明确命名，解释主要方面
7. 次要矛盾（先不主攻，但要盯住）- 推迟原因，监控触发条件
8. 时间、精力、资源应该怎么重新分配 - 50%-70% 主攻，10%-25% 次要，10%-20% 证据监控
9. 接下来怎么做 - 1-3 个突破行动，每个行动说明改变哪一侧
10. 做完以后可能怎样 - 概率区间，假设敏感性
11. 主要矛盾什么时候会转移 - 下一个可能的主要矛盾，转移信号
12. 什么时候回头看 - 复盘时间，什么信号说明焦点变化
13. 注意事项 - 专业边界，不确定性警告

核心原则:
- 结论在前，推理在后
- 概念术语后紧跟实用翻译（如"主要矛盾（最关键的卡点）"）
- 标记事实为 observed/estimated/assumed
- 每个行动必须说明改变主要矛盾的哪一侧
```

**可吸收价值**:
- Growth Master 缺乏统一的报告结构规范
- 可以建立类似的"输出契约"，确保所有 Agent 输出一致
- 用户友好标题设计非常值得学习

**建议整合方式**:
```yaml
# 创建 references/report-contract.md
report_contract:
  required_sections:
    - id: conclusion
      user_title: "先看结论"
      content_requirements:
        - "最该先解决什么"
        - "为什么是它"
        - "置信度（高/中/低）"
        - "第一个行动"
    
    - id: current_state
      user_title: "先把现状说清楚"
      content_requirements:
        - "目标"
        - "阶段"
        - "约束"
        - "资源"
        - "关键事实（标记 observed/estimated/assumed）"
    
    - id: decision_process
      user_title: "判断过程"
      content_requirements:
        - "至少 3 个候选方案对比"
        - "评分依据"
        - "为什么不是其他选项"
```

---

### 5. 主次矛盾判断三问门控（Principal Contradiction Three-Question Gate）

**来源**: yao-crux-skill/references/contradiction-model.md

**精华内容**:
```text
在详细评分之前，先用三个问题检验:

| 检查 | 直白问题 | 失败信号 |
| --- | --- | --- |
| 决定性 | 不解决它，当前目标是不是很难真正推进？ | 解决它会有用，但不会移动目标指标 |
| 牵引性 | 解决它后，多个表面问题会不会一起变轻？ | 它只修复一个局部痛点 |
| 阶段性 | 在当前期限、资源和阶段里，它是不是最该先抓？ | 它重要，但属于后续阶段 |

这三个检查是面向用户的解释，加权评分是审计痕迹。
```

**可吸收价值**:
- Growth Master 的"最关键问题识别"可以借鉴这个三问门控
- 当前 growth-agent.md 有类似思路但不系统
- 可以作为"快速扫描"模式的核心检查清单

**建议整合方式**:
```yaml
# 在 agents/core/growth-agent.md 中添加
principal_check:
  three_question_gate:
    - decisiveness: "不解决它，目标是否难以推进？"
    - leverage: "解决它后，多个问题是否一起变轻？"
    - stage_fit: "当前阶段是否最该先抓？"
  
  scoring_model:
    dimensions:
      - goal_impact: 0.25  # 是否直接决定目标达成
      - causal_leverage: 0.20  # 是否上游于多个症状
      - stage_urgency: 0.15  # 时间窗口是否关键
      - resource_constraint: 0.15  # 是否阻塞稀缺资源
      - changeability: 0.10  # 用户能否直接影响
      - spillover_risk: 0.10  # 忽略是否放大其他风险
      - evidence_strength: 0.05  # 是否有事实支撑
```

---

### 6. 第一性原理分层门控（First-Principles Layer Gate）

**来源**: yao-crux-skill/references/contradiction-model.md

**精华内容**:
```text
主要诊断风险是离用户的可见抱怨太近。主要矛盾往往是上游且部分不可见的。

分层检查:
1. 看得见的问题: 列出用户已经能叫出名字的症状
2. 上升一层: 问哪个隐藏变量可以同时解释多个可见问题
3. 看不见的根部变量: 用运营术语命名上游约束
4. 反证: 什么证据能证明可见问题其实不是主要矛盾

关键问题:
- 如果当前阶段只能改变一个变量，哪一个会让多个可见问题更容易？
- 哪个约束解释了为什么有能力的人仍然被困在细节中？
- 领导者当前最高杠杆的工作是什么：做、决定、招聘、销售、学习、修复信任，还是建立系统？
- 这主要是流程问题，还是让流程失败的能力/人才/系统生成问题？
```

**可吸收价值**:
- Growth Master 的 Strategy Design 模式可以引入这个分层
- 帮助用户从"症状"层面上升到"根因"层面
- 与当前的"问题分析"结合，增加深度

**建议整合方式**:
```yaml
# 在 modes/strategy-design 中添加
first_principles_gate:
  layers:
    - name: "看得见的问题"
      description: "用户已经能叫出名字的症状"
      output: "symptoms_list"
    
    - name: "上升一层"
      description: "哪个隐藏变量可以同时解释多个可见问题"
      output: "hidden_variable_hypothesis"
    
    - name: "看不见的根部变量"
      description: "用运营术语命名上游约束"
      output: "root_constraint"
    
    - name: "反证"
      description: "什么证据能证明可见问题不是主要矛盾"
      output: "falsification_test"
```

---

### 7. 安全边界与专业约束（Safety and Boundaries）

**来源**: yao-crux-skill/references/safety-and-boundaries.md

**精华内容**:
```text
硬边界领域:
- 医疗诊断、用药、自伤、严重心理健康风险
- 法律责任、诉讼、移民、刑事风险、合同解释
- 投资建议、债务困境、破产、税务、保险、重大财务风险
- 人身安全、家庭暴力、职场骚扰、胁迫、紧急危险
- 监管合规、安全漏洞、数据泄露、安全关键操作

响应规则:
- 如果出现即时危险或自伤风险，优先支持紧急/专业援助
- 如果用户要求最终法律、医疗、投资或危机建议，拒绝并提供结构化准备问题、风险清单和专业咨询框架
- 不让高评分覆盖硬安全边界
- 高风险案例的行动建议必须是可逆、保守、审查导向的

高风险案例报告要求:
- 风险边界章节
- 明确声明报告仅为决策支持
- 专业审查触发条件
- 低风险下一步
- 不可逆行动前必须收集的证据
```

**可吸收价值**:
- Growth Master 当前完全没有安全边界机制
- 增长决策可能涉及财务、法律、监管风险
- 必须引入类似的边界警告机制

**建议整合方式**:
```yaml
# 创建 references/safety-boundaries.md
safety_domains:
  - id: financial
    triggers: ["投资决策", "融资", "重大支出", "定价"]
    response: "提供决策框架，不提供最终投资建议"
    warning: "重大财务决策建议咨询专业顾问"
  
  - id: legal
    triggers: ["合规", "合同", "知识产权", "竞争"]
    response: "提供风险清单和准备问题，不提供法律建议"
    warning: "法律风险建议咨询律师"
  
  - id: regulatory
    triggers: ["监管", "牌照", "数据合规"]
    response: "提供合规检查清单，不提供合规结论"
    warning: "监管合规建议咨询专业机构"

# 在 SKILL.md 中添加
safety_protocol:
  enabled: true
  check_triggers: true
  block_high_risk_recommendations: true
  require_professional_disclaimer: true
```

---

### 8. 激进资源分配原则（Aggressive Resource Allocation）

**来源**: yao-crux-skill/references/contradiction-model.md

**精华内容**:
```text
当清晰度足够且主要矛盾评分稳定时，不要平均分配资源。建议明显的倾斜。

默认分配:
| 桶 | 典型份额 | 含义 |
| --- | ---: | --- |
| 主攻主要矛盾 | 50%-70% | 高杠杆时间、注意力、决策权和稀缺预算投入主线 |
| 压缩次要矛盾 | 10%-25% | 仅保持止损行动 |
| 证据与监控 | 10%-20% | 收集证据、监控触发器、准备阶段转移 |

更激进的条件:
- 主要矛盾解释多个可见问题
- 当前资源模式被困在低杠杆响应工作中
- 期限短，机会成本高
- 次要矛盾真实但尚未决定性

更温和的条件:
- 存在硬性安全、法律、健康、现金或声誉约束
```

**可吸收价值**:
- Growth Master 的"资源分配"建议往往过于保守
- 应该基于置信度提供更激进的建议
- 引入"资源倾斜度"概念

**建议整合方式**:
```yaml
# 在 decision-output 中添加
resource_allocation:
  principle: "aggressive_when_clear"
  
  default_split:
    main_focus: 0.60  # 50%-70%
    secondary_cap: 0.15  # 10%-25%
    monitoring: 0.15  # 10%-20%
  
  aggressiveness_factors:
    - "主要矛盾解释多个可见问题"
    - "当前被困在低杠杆响应"
    - "期限短，机会成本高"
  
  conservative_factors:
    - "存在硬性安全/法律/健康/现金约束"
  
  output_fields:
    - what_to_reduce: "列出应该减少的活动"
    - what_to_protect: "列出应该保护的底线"
    - what_to_overinvest: "列出应该超额投入的主线"
```

---

### 9. 动态时间视图（Dynamic Time View）

**来源**: yao-crux-skill/references/contradiction-model.md

**精华内容**:
```text
主要矛盾是阶段绑定的。每个报告应该包含转移视图:

- 当前阶段主要矛盾
- 显示它已被缓解的条件
- 下一个可能的主要矛盾
- 切换焦点前需要收集的证据

不要把当前主要矛盾当作永久标签。
```

**可吸收价值**:
- Growth Master 缺乏"阶段迁移"视角
- 增长阶段会变化，策略应该随之调整
- 引入"转移信号"监控

**建议整合方式**:
```yaml
# 在 decision-output 中添加
stage_transition:
  current_stage:
    name: "当前阶段"
    principal_contradiction: "当前主要矛盾"
  
  relief_signals:
    - "信号1：XX指标连续N周期改善"
    - "信号2：XX问题不再占用关键资源"
  
  next_likely_stage:
    name: "下一阶段"
    likely_principal_contradiction: "下一个可能的主要矛盾"
  
  evidence_to_collect:
    - "监控指标1"
    - "监控指标2"
  
  review_trigger: "什么信号出现时重新诊断"
```

---

### 10. 引用地图结构（Reference Map）

**来源**: 所有 yao-*-skill/SKILL.md

**精华内容**:
```text
每个 Skill 都有清晰的 Reference Map:

## Reference Map

- `references/intake-contract.md`: 请求到简介的转换
- `references/theory-anchors.md`: 理论到规则的锚点
- `references/contradiction-model.md`: 评分模型、主要方面、次要矛盾
- `references/report-contract.md`: 报告章节和语言标准
- `references/report-export-pipeline.md`: 四格式生成工作流
- `references/safety-and-boundaries.md`: 高风险和专业边界门控
- `scripts/current_state_clarity.py`: 现状清晰度门控
- `scripts/generate_report_bundle.py`: JSON 到 Markdown、HTML、DOCX、PDF
- `scripts/verify_report_bundle.py`: 生成的工件检查
```

**可吸收价值**:
- Growth Master 当前缺乏清晰的"引用地图"
- Agent 文件之间的引用关系不明确
- 应该为每个 Agent 添加 Reference Map

**建议整合方式**:
```markdown
# 在每个 Agent 文件末尾添加

## Reference Map

- `../core/orchestrator-agent.md`: 编排和冲突解决
- `../../knowledge/indexes/cases-index.json`: 案例知识库
- `../../knowledge/indexes/weapons-index.json`: 玩法知识库
- `../../knowledge/indexes/theories-index.json`: 理论知识库
- `../../references/decision-rules.md`: 决策规则
- `../../references/safety-boundaries.md`: 安全边界
```

---

### 11. 四格式同步报告生成（Four-Format Synchronized Reports）

**来源**: yao-crux-skill/references/report-export-pipeline.md

**精华内容**:
```text
同一份规范报告 JSON 驱动四种格式:
- .md: 最易编辑和审查
- .html: 样式化阅读和打印界面
- .docx: 便携 Word 移交
- .pdf: 最终展示工件

验证脚本检查:
- 所有格式存在
- 中文内容
- 关键章节存在
- 图表数量
- 本地路径泄露
- 打印/PDF 控件
```

**可吸收价值**:
- Growth Master 当前只支持 Markdown
- 可以扩展支持 HTML/PDF 导出
- 验证机制确保报告质量

**建议整合方式**:
```yaml
# 添加 scripts/generate_report_bundle.py
report_formats:
  - markdown:  # 基础格式
      extension: .md
      purpose: "易编辑审查"
  
  - html:  # 视觉格式
      extension: .html
      purpose: "样式化阅读和打印"
      features:
        - sticky_navigation: true
        - print_ready: true
        - responsive: true
  
  - pdf:  # 最终格式
      extension: .pdf
      purpose: "最终展示工件"
      from_html: true  # 从 HTML 打印生成

# 添加 scripts/verify_report_bundle.py
validation_checks:
  - all_formats_exist
  - chinese_content
  - required_sections
  - no_local_paths
  - chart_count
```

---

### 12. 追问策略与高价值问题库（Follow-Up Strategy & High-Value Question Bank）

**来源**: yao-crux-skill/references/intake-and-questioning.md

**精华内容**:
```text
如果用户给的信息很少，问恰好3个问题:
1. 你希望这个问题在什么期限内变成什么状态？怎样算解决？
2. 当前最卡住你的是什么？请尽量说事实，而不是解释。
3. 你现在最稀缺的资源是什么：时间、人、钱、权限、注意力、信任、数据，还是其他？

高价值问题库:
| 目的 | 问题 |
| --- | --- |
| 锁定目标 | 你希望这个问题在什么期限内变成什么状态？怎样算解决？ |
| 识别阶段 | 这是启动期、验证期、增长期、修复期、转型期，还是恢复期的问题？ |
| 找稀缺资源 | 现在最稀缺的是时间、人、钱、权限、注意力、信任，还是数据？ |
| 分离事实与解释 | 哪些是已经发生的事实？哪些是你的解释、担心或推测？ |
| 找重复模式 | 类似问题出现过几次？通常在什么节点爆发？ |
| 分离内外因 | 哪些因素你能直接改变？哪些只能影响、规避或等待？ |
| 相关方冲突 | 涉及哪些人？每个人最在意的结果分别是什么？ |
| 单问题测试 | 如果接下来30天只能解决一个问题，解决哪个会带来最大变化？ |
| 次要矛盾测试 | 哪些问题很烦，但即使解决也不能明显改变目标结果？ |
| 复盘条件 | 什么信号出现时，说明主要矛盾已经转移？ |
```

**可吸收价值**:
- Growth Master 的 Guide Agent 可以直接使用这些问题
- 当前缺乏结构化的问题库
- 可以基于场景选择最优问题组合

**建议整合方式**:
```yaml
# 创建 references/question-bank.md
question_bank:
  quick_scan:  # 快速扫描模式
    - target_lock: "你希望这个问题在什么期限内变成什么状态？"
    - scarcest_resource: "现在最稀缺的是时间、人、钱、权限、注意力、信任，还是数据？"
    - single_problem_test: "如果30天只能解决一个问题，解决哪个会带来最大变化？"
  
  strategy_design:  # 战略设计模式
    - stage_identification: "这是启动期、验证期、增长期、修复期、转型期，还是恢复期？"
    - fact_interpretation_split: "哪些是事实？哪些是解释、担心或推测？"
    - internal_external_split: "哪些因素你能直接改变？哪些只能影响、规避或等待？"
    - recurring_pattern: "类似问题出现过几次？通常在什么节点爆发？"
  
  decision_brd:  # 决策 BRD 模式
    - stakeholder_conflict: "涉及哪些人？每个人最在意的结果分别是什么？"
    - secondary_contradiction_test: "哪些问题很烦，但即使解决也不能明显改变目标结果？"
    - review_condition: "什么信号出现时，说明主要矛盾已经转移？"
```

---

## 二、整合优先级建议

### P0 - 立即整合（核心体验提升）

| 精华 | 整合到 | 预估工作量 | 价值 |
| --- | --- | --- | --- |
| 现状清晰度门控 | Lead Agent + Guide Agent | 1天 | 避免信息不足时盲目诊断 |
| 安全边界机制 | 全局 SKILL.md | 0.5天 | 避免高风险建议 |
| 追问策略与问题库 | Guide Agent | 0.5天 | 提升追问质量 |
| 引用地图结构 | 所有 Agent | 0.5天 | 提升可维护性 |

### P1 - 短期整合（能力增强）

| 精华 | 整合到 | 预估工作量 | 价值 |
| --- | --- | --- | --- |
| 证据分级系统 | Knowledge Indexes | 1天 | 提升决策可信度 |
| 多轮对话机制 | Lead Agent | 1天 | 支持迭代决策 |
| 输出契约与报告结构 | 全局 | 1天 | 统一输出规范 |
| 主次矛盾三问门控 | Growth Agent | 0.5天 | 提升判断效率 |

### P2 - 中期整合（深度增强）

| 精华 | 整合到 | 预估工作量 | 价值 |
| --- | --- | --- | --- |
| 第一性原理分层 | Strategy Design 模式 | 1天 | 提升分析深度 |
| 激进资源分配 | Decision Output | 0.5天 | 提升建议力度 |
| 动态时间视图 | Decision Output | 0.5天 | 增加阶段视角 |
| 四格式报告生成 | Scripts | 2天 | 提升交付能力 |

---

## 三、具体整合方案

### 方案 A：最小侵入式（推荐）

在现有架构上打补丁，不改变核心结构：

```yaml
整合步骤:
1. 添加 references/safety-boundaries.md
2. 添加 references/question-bank.md
3. 添加 references/report-contract.md
4. 在 SKILL.md 中添加 decision_gates 配置
5. 在 Guide Agent 中引入问题库
6. 在所有 Agent 末尾添加 Reference Map
7. 在 Knowledge Indexes 中添加 evidence_tier 字段

预估工作量: 3天
风险: 低
```

### 方案 B：深度重构式

重构核心架构，吸收全部精华：

```yaml
整合步骤:
1. 重构 Lead Agent 支持多轮对话
2. 引入 current_state_clarity.py 脚本
3. 重构 Growth Agent 引入三问门控和分层检查
4. 重构 Decision Output 引入资源分配和阶段迁移
5. 添加四格式报告生成脚本
6. 建立统一的输出契约验证

预估工作量: 7天
风险: 中
```

---

## 四、关键脚本参考

### current_state_clarity.py 核心逻辑

```python
def assess_current_state_clarity(request: dict) -> dict:
    """评估现状清晰度，返回评分、等级、缺失维度、追问问题"""
    scores, present = _dimension_scores(request)
    total = sum(scores.values())
    level = _clarity_level(total)  # insufficient/workable/clear
    
    return {
        "score": round(total, 1),
        "clarity_level": level,
        "diagnosis_allowed": total >= 60 and required_ready,
        "missing_dimensions": [...],
        "questions": [...],  # 最多 3-5 个
        "snapshot": "现状快照文本"
    }
```

### verify_report_bundle.py 核心检查

```python
REQUIRED_HTML_IDS = [
    "summary", "situation", "current-state", "visuals",
    "contradictions", "principal", "secondary", "allocation",
    "actions", "projection", "transition", "review", "risks"
]

def check_report_json(path: Path) -> list[str]:
    """检查报告 JSON 完整性"""
    # 检查必选字段
    # 检查图表数量
    # 检查清晰度门控
    # 检查分析逻辑
    # 检查资源分配
    # 检查概率范围
    # 检查风险警告
```

---

## 五、总结

### yao-open-skills 的核心设计哲学

1. **先追问后判断** - 不在信息不足时下结论
2. **先目标后矛盾** - 先明确目标再识别障碍
3. **先事实后解释** - 区分观察到的事实和主观解释
4. **证据分级** - 明确标记证据来源可信度
5. **输出契约** - 统一报告结构和用户友好标题
6. **安全边界** - 高风险领域保持专业边界
7. **激进分配** - 清晰时果断倾斜资源
8. **动态视角** - 承认阶段变化和矛盾转移
9. **可验证** - 脚本验证报告质量和完整性

### Growth Master 最需要吸收的精华

1. **现状清晰度门控** - 最优先，立竿见影
2. **安全边界机制** - 必须有，避免风险
3. **证据分级系统** - 提升可信度
4. **多轮对话机制** - 提升灵活性
5. **输出契约** - 提升一致性

### 下一步行动

1. 选择整合方案（推荐方案 A）
2. 创建 references/safety-boundaries.md
3. 创建 references/question-bank.md
4. 更新 SKILL.md 添加 decision_gates
5. 更新 Guide Agent 引入问题库
6. 更新 Knowledge Indexes 添加 evidence_tier
7. 为所有 Agent 添加 Reference Map
