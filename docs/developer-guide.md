# Growth Master 开发者指南

## 架构概述

```
growth-master/
├── SKILL.md              # 主技能定义
├── agents/               # Agent定义
│   ├── core/             # 核心决策Agent
│   └── knowledge/        # 知识驱动Agent
├── knowledge/            # 知识库
│   ├── cases/            # 案例库
│   ├── weapons/          # 玩法库
│   ├── schools/          # 理论流派
│   └── indexes/          # 索引文件（带证据分级）
├── references/           # 配置与规范
│   ├── safety-boundaries.md    # 安全边界配置
│   ├── report-contract.md      # 输出契约规范
│   ├── current-state-clarity.md # 现状清晰度门控
│   └── question-bank.md        # 追问问题库
├── templates/            # 用户模板
├── tests/                # 测试套件
├── scripts/              # 工具脚本
│   ├── assess_clarity.py       # 清晰度评估
│   └── verify_report.py        # 报告验证
├── feedback/             # 反馈系统
└── decisions/            # 决策追踪
```

## Reference Map 体系

每个Agent和核心文件都有 Reference Map，明确列出依赖：

```yaml
## Reference Map

- `../../references/safety-boundaries.md`: 安全边界
- `../../references/report-contract.md`: 输出契约
- `../../references/current-state-clarity.md`: 现状清晰度门控
- `../../references/question-bank.md`: 追问问题库
- `../../knowledge/indexes/cases-index.json`: 案例知识库
```

这确保：
1. Agent 能快速找到需要的配置
2. 修改配置时能评估影响范围
3. 新增 Agent 能遵循统一结构

## 扩展Agent

### 创建新Agent

1. 创建Agent定义文件：

```markdown
# agents/core/custom-agent.md

---
name: custom-agent
description: Agent描述
model: inherit
---

# Custom Agent

你负责...

## 职责

- 职责1
- 职责2

## 输入Schema

```json
{
  "user_input": {...},
  "knowledge_context": {...},
  "agent_outputs": {...}
}
```

## 输出Schema

```json
{
  "assessment": {...},
  "risks": [...],
  "recommendations": [...],
  "confidence": "High|Medium|Low"
}
```
```

2. 在SKILL.md中注册Agent

3. 在Orchestrator Agent中添加调度逻辑

### Agent开发规范

- 遵循统一输入/输出Schema
- 明确职责边界
- 标注置信度
- 引用知识上下文

## 扩展知识库

### 添加新案例

1. 创建案例文件：

```markdown
# knowledge/cases/china/new-case.md

---
id: new-case
name: 案例名称
region: china
industry: [ecommerce]
stage: ["1-10"]
problem_types: [acquisition]
tactics: [viral_referral]
summary: 一句话摘要
replicable_points: [点1, 点2]
---

# 案例标题

## 完整背景
...

## 核心挑战
...

## 增长策略
...

## 关键数据
...

## 核心洞察
...

## 可复制点
...

## 常见误区
...
```

2. 更新索引：

```bash
# 运行索引更新脚本
python scripts/update-indexes.py
```

### 添加新玩法

1. 在 `knowledge/weapons/` 对应目录下添加玩法描述

2. 更新 `knowledge/indexes/weapons-index.json`

### 添加新理论流派

1. 创建流派文件：

```markdown
# knowledge/schools/13-new-theory.md

# 新理论名称

## 核心问题
这个理论解决什么问题？

## 核心原则
- 原则1
- 原则2

## 适用场景
- 场景1
- 场景2

## 关键战术
- 战术1
- 战术2

## 成功案例
- 案例1
- 案例2
```

2. 更新 `knowledge/indexes/theories-index.json`

## 自定义工作流

### 修改模式选择逻辑

编辑 `references/workflow.md` 中的模式选择决策树

### 修改Agent组配规则

编辑 `agents/core/orchestrator-agent.md` 中的 `compose_agents()` 函数

### 自定义输出模板

编辑 `references/output-schema.md` 中的模板

## 测试

### 运行测试

```bash
# 运行所有测试
./tests/run-tests.sh

# 运行单个Agent测试
./tests/run-tests.sh agents/test-lead-agent.md

# 运行场景测试
./tests/run-tests.sh scenarios/saas-acquisition.md

# 评估现状清晰度
python scripts/assess_clarity.py --input state.json --output assessment.json

# 验证报告契约
python scripts/verify_report.py --input report.md --output verification.json
```

### 清晰度评估脚本

`scripts/assess_clarity.py` 用于评估输入信息的充分性：

```bash
# 输入 JSON 格式
{
  "dimensions": {
    "goal_success": {
      "evidence": ["目标是提升DAU 20%", "成功标准是月底前达成"],
      "score": 70
    },
    "facts_evidence": {
      "evidence": ["当前DAU 1000 (observed)"],
      "score": 50
    }
  }
}

# 输出
{
  "total_score": 62.5,
  "level": "workable",
  "can_proceed": true,
  "follow_up_questions": [...]
}
```

### 报告验证脚本

`scripts/verify_report.py` 用于验证输出报告是否符合契约：

```bash
# 验证报告是否包含必选章节
python scripts/verify_report.py --input output.md --output result.json

# 输出
{
  "valid": true,
  "score": 85,
  "sections_found": ["先看结论", "先把现状说清楚", ...],
  "fact_markers": {"observed": 3, "estimated": 2, "assumed": 1}
}
```

### 编写测试用例

```markdown
# tests/agents/test-custom-agent.md

# Custom Agent 测试用例

## 测试用例1：[场景]

### 输入

```json
{
  "user_input": {...}
}
```

### 预期输出

```json
{
  "assessment": {...}
}
```

### 验证点

- [ ] 验证点1
- [ ] 验证点2
```

## 反馈系统

### 查看反馈

```bash
# 查看最近反馈
cat feedback/logs/$(date +%Y-%m)/$(date +%Y-%m-%d).json

# 查看周报
cat feedback/analysis/weekly-report.md
```

### 分析反馈

```bash
# 运行反馈聚合脚本
./scripts/aggregate-feedback.sh
```

## 决策追踪

### 创建决策记录

```bash
# 使用模板创建新决策
cp decisions/templates/decision-template.md decisions/$(date +%Y)/$(date +%m)/decision-$(date +%Y%m%d)-001.md
```

### 创建追踪报告

```bash
# 在决策后30/60/90天创建追踪
cp decisions/templates/tracking-template.md decisions/$(date +%Y)/$(date +%m)/decision-xxx-tracking.md
```

## CI/CD集成

### GitHub Actions

项目已包含CI配置：

```yaml
# .github/workflows/test.yml

name: Test Growth Master

on:
  pull_request:
    paths:
      - 'agents/**'
      - 'knowledge/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate
        run: ./scripts/validate.sh
```

## 调试技巧

### 查看Agent调用链

在请求中添加 `--debug` 参数：

```
/growth-master-skill assess --debug
```

### 单独测试Agent

```
/test-agent growth-agent

输入：{
  "user_input": {...}
}
```

### 查看知识检索结果

```
/test-knowledge

问题类型：acquisition
行业：saas
```

## 版本管理

### 知识库版本

```bash
# 创建新版本
cp -r knowledge knowledge/versions/v1.1

# 更新当前版本链接
ln -sfn knowledge/versions/v1.1 knowledge/current
```

### 更新CHANGELOG

```markdown
# knowledge/CHANGELOG.md

## v1.1 (2024-01-20)

### 新增
- 新增3个AI产品案例
- 新增"增长飞轮"理论详解
- 新增证据分级系统（A/B/C/D/E）
- 新增现状清晰度门控机制
- 新增安全边界配置
- 新增输出契约规范

### 修改
- 更新拼多多案例数据
- 所有Agent添加Reference Map
```

## 证据分级系统

知识库索引文件包含证据分级：

```json
{
  "metadata": {
    "evidence_tier_definition": {
      "A": "元分析、系统综述、官方统计、权威教材",
      "B": "同行评审论文、公开数据集、行业标准、良好文档的基准",
      "C": "结构化专家意见、内部历史数据、仔细收集的现场证据",
      "D": "LLM建议、类比、常识、非正式启发式",
      "E": "博客文章、营销文案、社交媒体、未注明来源的声称"
    }
  },
  "theories": [
    {
      "id": "network-effects",
      "evidence_tier": "A",
      "evidence_sources": ["学术研究", "平台经济学", "成功案例分析"],
      "confidence": 0.92
    }
  ]
}
```

## 安全边界配置

在 `references/safety-boundaries.md` 中配置风险检测规则：

```yaml
safety_check:
  domains:
    financial:
      triggers: ["投资", "融资", "估值", "定价", "重大支出"]
      response: "提供决策框架，不提供最终投资建议"
      warning: "重大财务决策建议咨询专业顾问"
      confidence_cap: "Medium"
```

Agent 通过 Reference Map 引用此配置。

## 输出契约规范

在 `references/report-contract.md` 中定义输出结构：

```yaml
required_sections:
  - id: conclusion
    user_title: "先看结论"
    required: true
    content:
      - 最该先解决什么
      - 为什么是它
      - 置信度（高/中/低）
      - 第一个行动

fact_markers:
  observed:
    usage: "有数据、记录、证据支撑"
    example: "月活用户 120 万 (observed)"
```
