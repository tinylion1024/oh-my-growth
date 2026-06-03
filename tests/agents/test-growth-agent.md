# Growth Agent 测试用例

## 测试概览

测试 Growth Agent 对增长机制可行性的评估能力。

---

## 测试用例 1：邀请裂变机制评估

### 输入

```json
{
  "user_input": {
    "problem_type": "acquisition",
    "industry": "saas",
    "stage": "1-10"
  },
  "knowledge_context": {
    "matched_cases": [
      {
        "name": "Dropbox",
        "key_tactics": ["双边奖励", "存储空间激励"],
        "results": "用户增长3900%"
      }
    ],
    "recommended_weapons": [
      {
        "id": 12,
        "name": "双边奖励",
        "category": "病毒裂变"
      }
    ]
  },
  "mechanism": {
    "description": "邀请好友注册，双方各得1个月会员",
    "reward_type": "功能解锁",
    "target_users": "现有付费用户"
  }
}
```

### 预期输出

```json
{
  "mechanism_assessment": {
    "feasibility": "Medium|High",
    "target_quality": "付费用户邀请意愿较强",
    "funnel_leverage": "作用于获客漏斗顶部",
    "causal_chain": "邀请奖励 → 分享行为 → 新用户注册 → 激活 → 付费",
    "compound_potential": "SaaS协作工具有天然传播属性"
  },
  "risks": ["奖励可能吸引低质量用户", "可能被滥用"],
  "watch_outs": ["需要设计防刷机制", "需要追踪邀请质量"],
  "experiment_suggestion": {
    "hypothesis": "双边奖励机制能提升K因子到1.2以上",
    "success_metric": "K因子 > 1.2, 新用户留存率 > 40%",
    "duration": "2-4周"
  },
  "confidence": "Medium|High"
}
```

### 验证点

- [ ] 正确评估机制可行性
- [ ] 识别潜在风险
- [ ] 提供实验建议
- [ ] 引用知识上下文中的案例

---

## 测试用例 2：内容营销机制评估

### 输入

```json
{
  "user_input": {
    "problem_type": "acquisition",
    "industry": "saas",
    "stage": "0-1"
  },
  "mechanism": {
    "description": "通过SEO和技术博客获取用户",
    "content_type": "技术教程",
    "distribution": "官网博客 + 掘金 + 知乎"
  }
}
```

### 预期输出

```json
{
  "mechanism_assessment": {
    "feasibility": "High",
    "target_quality": "搜索用户意图明确，质量高",
    "funnel_leverage": "作用于漏斗顶部，持续性强",
    "causal_chain": "内容发布 → 搜索收录 → 用户搜索 → 点击访问 → 注册转化",
    "compound_potential": "内容资产持续产生流量，有复利效应"
  },
  "risks": ["见效周期长", "需要持续投入"],
  "watch_outs": ["竞品可能同样策略", "需要差异化内容"],
  "confidence": "High"
}
```

### 验证点

- [ ] 识别内容营销的长周期特性
- [ ] 评估复利潜力
- [ ] 置信度应较高（案例丰富）

---

## 测试用例 3：游戏化留存机制评估

### 输入

```json
{
  "user_input": {
    "problem_type": "retention",
    "industry": "education",
    "stage": "1-10"
  },
  "mechanism": {
    "description": "学习打卡+积分兑换+排行榜",
    "gamification_elements": ["连续打卡", "积分", "排行榜", "勋章"]
  }
}
```

### 预期输出

```json
{
  "mechanism_assessment": {
    "feasibility": "High",
    "target_quality": "学习场景适合游戏化",
    "funnel_leverage": "作用于留存环节",
    "causal_chain": "游戏化设计 → 习惯养成 → 长期留存",
    "compound_potential": "用户习惯形成后自我强化"
  },
  "risks": ["游戏化疲劳", "非核心价值用户留存"],
  "watch_outs": ["游戏化不应喧宾夺主", "需要与核心价值结合"],
  "confidence": "High"
}
```

### 验证点

- [ ] 识别教育场景适合游戏化
- [ ] 提醒游戏化疲劳风险
- [ ] 引用 Duolingo 等案例

---

## 测试用例 4：弱因果机制评估

### 输入

```json
{
  "mechanism": {
    "description": "投放大量广告期望用户自然增长",
    "channels": ["抖音", "小红书", "B站"],
    "budget": "100万",
    "expected_result": "用户量大幅增长"
  }
}
```

### 预期输出

```json
{
  "mechanism_assessment": {
    "feasibility": "Low|Medium",
    "causal_chain": "广告投放 → ??? → 用户增长",
    "causal_chain_strength": "弱 - 缺少具体转化机制"
  },
  "risks": ["投放效率低", "CAC过高", "用户质量不可控"],
  "watch_outs": ["没有明确的转化路径", "缺少承接设计"],
  "confidence": "Low",
  "recommendation": "需要设计完整的转化漏斗和承接机制"
}
```

### 验证点

- [ ] 识别因果链薄弱
- [ ] 置信度应较低
- [ ] 提出改进建议

---

## 测试用例 5：边界情况 - 虚荣指标

### 输入

```json
{
  "mechanism": {
    "description": "通过红包活动获取大量注册用户",
    "kpi": "注册用户数突破100万"
  }
}
```

### 预期输出

```json
{
  "mechanism_assessment": {
    "feasibility": "Medium",
    "risks": ["低质量用户", "羊毛党", "留存率低"]
  },
  "watch_outs": [
    "虚荣指标风险 - 注册数不等于价值用户",
    "红包用户留存通常较差"
  ],
  "recommendation": "关注激活率、留存率而非仅注册数",
  "confidence": "Medium"
}
```

### 验证点

- [ ] 识别虚荣指标风险
- [ ] 提醒关注有效指标

---

## 测试结果记录

| 用例 | 状态 | 通过/失败 | 备注 |
|------|------|-----------|------|
| TC1 | 待测试 | - | - |
| TC2 | 待测试 | - | - |
| TC3 | 待测试 | - | - |
| TC4 | 待测试 | - | - |
| TC5 | 待测试 | - | - |
