# Theory Agent 测试用例

## 测试概览

测试 Theory Agent 匹配相关理论流派的能力。

---

## 测试用例 1：增长理论匹配

### 输入

```json
{
  "problem_context": {
    "type": "acquisition",
    "industry": "saas",
    "mechanism": "产品驱动增长"
  }
}
```

### 预期输出

```json
{
  "matched_theories": [
    {
      "name": "PLG理论",
      "relevance": "High",
      "key_principles": [
        "产品即营销",
        "Freemium降低门槛",
        "用户自发传播"
      ],
      "evidence_tier": "B"
    },
    {
      "name": "AARRR模型",
      "relevance": "Medium",
      "key_principles": [
        "关注漏斗转化",
        "数据驱动优化"
      ],
      "evidence_tier": "B"
    }
  ],
  "application_guidance": "结合PLG设计自传播机制，用AARRR追踪漏斗"
}
```

### 验证点

- [ ] 匹配相关理论
- [ ] 提供证据等级
- [ ] 给出应用指导

---

## 测试用例 2：留存理论匹配

### 输入

```json
{
  "problem_context": {
    "type": "retention",
    "industry": "education",
    "mechanism": "游戏化"
  }
}
```

### 预期输出

```json
{
  "matched_theories": [
    {
      "name": "游戏化理论",
      "relevance": "High",
      "key_principles": [
        "即时反馈",
        "成就系统",
        "社交竞争"
      ],
      "evidence_tier": "B"
    },
    {
      "name": "上瘾模型",
      "relevance": "High",
      "key_principles": [
        "触发 → 行动 → 酬赏 → 投入",
        "习惯养成"
      ],
      "evidence_tier": "B"
    }
  ],
  "application_guidance": "设计连胜机制+排行榜，结合上瘾模型优化触发"
}
```

### 验证点

- [ ] 匹配游戏化相关理论
- [ ] 提供上瘾模型
- [ ] 给出具体应用建议
