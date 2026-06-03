# Weapon Agent 测试用例

## 测试概览

测试 Weapon Agent 从武器库推荐增长玩法的能力。

---

## 测试用例 1：获客玩法推荐

### 输入

```json
{
  "problem_context": {
    "type": "acquisition",
    "industry": "saas",
    "stage": "1-10",
    "budget": "limited"
  }
}
```

### 预期输出

```json
{
  "recommended_weapons": [
    {
      "id": "w01",
      "name": "双边奖励邀请",
      "category": "病毒裂变",
      "suitability": "High",
      "implementation_effort": "Low",
      "expected_effect": "K因子>1.2",
      "case_references": ["Dropbox", "Airbnb"]
    },
    {
      "id": "w02",
      "name": "Freemium模式",
      "category": "PLG",
      "suitability": "High",
      "implementation_effort": "Medium",
      "expected_effect": "降低试用门槛",
      "case_references": ["Slack", "Notion"]
    },
    {
      "id": "w03",
      "name": "内容营销",
      "category": "内容增长",
      "suitability": "Medium",
      "implementation_effort": "Medium",
      "expected_effect": "长期品牌积累",
      "case_references": ["HubSpot"]
    }
  ],
  "priority_order": ["w01", "w02", "w03"],
  "combination_suggestion": "先做邀请裂变验证，再优化Freemium转化"
}
```

### 验证点

- [ ] 推荐相关玩法
- [ ] 评估实施难度
- [ ] 提供案例参考
- [ ] 建议组合方案

---

## 测试用例 2：留存玩法推荐

### 输入

```json
{
  "problem_context": {
    "type": "retention",
    "industry": "education",
    "stage": "1-10"
  }
}
```

### 预期输出

```json
{
  "recommended_weapons": [
    {
      "id": "w20",
      "name": "连胜打卡",
      "category": "游戏化",
      "suitability": "High",
      "case_references": ["Duolingo", "蚂蚁森林"]
    },
    {
      "id": "w21",
      "name": "排行榜竞争",
      "category": "游戏化",
      "suitability": "High",
      "case_references": ["Duolingo"]
    },
    {
      "id": "w22",
      "name": "社群运营",
      "category": "社区",
      "suitability": "Medium",
      "case_references": ["小红书"]
    }
  ],
  "combination_suggestion": "连胜+排行榜组合，配合社群督促"
}
```

### 验证点

- [ ] 推荐游戏化玩法
- [ ] 提供教育行业案例
- [ ] 建议玩法组合
