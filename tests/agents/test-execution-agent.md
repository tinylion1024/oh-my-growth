# Execution Agent 测试用例

## 测试概览

测试 Execution Agent 对执行可行性评估的能力。

---

## 测试用例 1：资源可行性评估

### 输入

```json
{
  "proposal": {
    "mechanism": "内容营销",
    "required_resources": {
      "team": "内容团队3人",
      "budget": "月预算5万元",
      "time": "持续6个月"
    }
  },
  "context": {
    "available_resources": {
      "team": "运营2人",
      "budget": "月预算3万元",
      "runway": "12个月"
    }
  }
}
```

### 预期输出

```json
{
  "execution_assessment": {
    "feasibility": "Partial",
    "resource_gaps": [
      {
        "resource": "人力",
        "required": 3,
        "available": 2,
        "gap": 1
      },
      {
        "resource": "预算",
        "required": 50000,
        "available": 30000,
        "gap": 20000
      }
    ],
    "alternatives": [
      "外包内容创作",
      "降低发布频率",
      "利用用户UGC"
    ]
  },
  "timeline_assessment": "可接受，runway充足",
  "recommendation": "建议先小规模启动，验证效果后再扩展"
}
```

### 验证点

- [ ] 识别资源缺口
- [ ] 提供替代方案
- [ ] 评估时间可行性
- [ ] 给出保守建议

---

## 测试用例 2：技术可行性评估

### 输入

```json
{
  "proposal": {
    "mechanism": "推荐算法优化",
    "technical_requirements": [
      "实时推荐系统",
      "用户行为追踪",
      "A/B测试平台"
    ]
  },
  "context": {
    "tech_stack": "Python + PostgreSQL",
    "team_capability": "后端2人，无算法经验"
  }
}
```

### 预期输出

```json
{
  "execution_assessment": {
    "feasibility": "Low",
    "technical_gaps": [
      "缺乏算法工程师",
      "现有架构不支持实时推荐"
    ],
    "skill_requirements": [
      "机器学习基础",
      "推荐系统经验",
      "实时系统设计"
    ]
  },
  "alternatives": [
    "使用第三方推荐服务",
    "先实现简单规则推荐",
    "招聘算法工程师"
  ],
  "timeline_estimate": "完整实现需要3-6个月",
  "recommendation": "建议先用规则推荐验证效果"
}
```

### 验证点

- [ ] 识别技术差距
- [ ] 评估团队能力
- [ ] 提供替代方案
- [ ] 给出时间估算

---

## 测试用例 3：组织可行性评估

### 输入

```json
{
  "proposal": {
    "mechanism": "跨部门协作增长",
    "involved_teams": ["产品", "运营", "技术", "市场"]
  },
  "context": {
    "organization": "职能型组织",
    "decision_process": "逐级审批"
  }
}
```

### 预期输出

```json
{
  "execution_assessment": {
    "feasibility": "Medium",
    "organizational_challenges": [
      "跨部门协调成本高",
      "决策链条长",
      "利益分配不明确"
    ]
  },
  "enablers": [
    "设立增长负责人",
    "明确各方KPI",
    "建立快速决策机制"
  ],
  "recommendation": "建议先在小团队内验证，再推动跨部门"
}
```

### 验证点

- [ ] 识别组织障碍
- [ ] 提供解决方案
- [ ] 考虑政治因素
