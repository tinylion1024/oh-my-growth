# Knowledge Router - 知识检索路由

## 检索策略

### 多维度检索

```
检索 = 行业匹配 × 阶段匹配 × 问题匹配 × 玩法匹配
```

### 检索流程

```
1. 解析用户输入 → 提取关键词和特征
2. 多维度匹配 → 计算相似度
3. 排序筛选 → Top N结果
4. 提取关键信息 → 输出
```

## 案例检索

### 案例标签体系

```
cases/
├── china/           # 地域：中国
├── overseas/        # 地域：海外
└── vertical/        # 地域：垂直行业

标签维度：
- 行业：电商/社交/金融/教育/SaaS/内容/...
- 阶段：0-1/1-10/10-100
- 问题：获客/激活/留存/变现/裂变/...
- 玩法：拼团/裂变/PLG/内容/社区/...
```

### 案例匹配算法

```python
def match_cases(user_input, case_library):
    # Step 1: 提取用户特征
    features = extract_features(user_input)
    # features = {
    #     "industry": "saas",
    #     "stage": "1-10",
    #     "problem": "acquisition",
    #     "keywords": ["邀请", "裂变", "协作"]
    # }
    
    # Step 2: 计算每个案例的相似度
    scores = []
    for case in case_library:
        score = 0
        # 行业匹配（权重0.3）
        if case.industry == features.industry:
            score += 0.3
        elif case.industry in related_industries(features.industry):
            score += 0.15
        
        # 阶段匹配（权重0.2）
        if case.stage == features.stage:
            score += 0.2
        
        # 问题匹配（权重0.3）
        if case.problem_type == features.problem:
            score += 0.3
        
        # 关键词匹配（权重0.2）
        keyword_score = keyword_similarity(features.keywords, case.keywords)
        score += 0.2 * keyword_score
        
        scores.append((case, score))
    
    # Step 3: 排序返回Top N
    return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
```

### 案例信息提取

```python
def extract_case_info(case):
    return {
        "name": case.name,
        "file_path": case.path,
        "similarity_score": case.score,
        "key_tactics": extract_key_tactics(case.content),
        "results": extract_results(case.content),
        "replicable_points": extract_replicable(case.content),
        "warnings": extract_warnings(case.content)
    }
```

## 玩法检索

### 玩法分类体系

```
weapons/
├── 01-cold-start/         # 冷启动
├── 02-viral-referral/     # 病毒裂变
├── 03-content-growth/     # 内容增长
├── 04-community/          # 社区增长
├── 05-plg/                # PLG
├── 06-retention/          # 留存增长
├── 07-monetization/       # 变现增长
├── 08-paid-ads/           # 付费广告
├── 09-brand/              # 品牌增长
└── 10-b2b-sales/          # B2B销售
```

### 玩法推荐逻辑

```python
def recommend_weapons(features):
    weapons = []
    
    # Step 1: 按问题类型筛选
    problem_to_category = {
        "acquisition": ["cold-start", "viral-referral", "content-growth", "paid-ads"],
        "activation": ["plg", "retention"],
        "retention": ["retention", "community"],
        "monetization": ["monetization", "plg"],
        "referral": ["viral-referral", "community"]
    }
    categories = problem_to_category.get(features.problem, [])
    
    # Step 2: 按阶段筛选
    stage_to_priority = {
        "0-1": ["cold-start", "viral-referral", "content-growth"],
        "1-10": ["plg", "retention", "community"],
        "10-100": ["paid-ads", "brand", "b2b-sales"]
    }
    stage_priority = stage_to_priority.get(features.stage, [])
    
    # Step 3: 计算推荐分数
    for weapon in all_weapons:
        if weapon.category in categories:
            score = 0.5
            if weapon.category in stage_priority:
                score += 0.3
            # 资源约束调整
            if features.budget_limited and weapon.needs_budget:
                score *= 0.5
            weapons.append((weapon, score))
    
    # Step 4: 排序返回
    return sorted(weapons, key=lambda x: x[1], reverse=True)[:5]
```

## 理论检索

### 流派匹配

```python
def match_theories(features):
    theory_mapping = {
        "acquisition": ["growth-hacking", "viral-growth", "content-growth"],
        "activation": ["plg", "gamification"],
        "retention": ["gamification", "community-growth", "flywheel"],
        "monetization": ["business-models", "plg"],
        "referral": ["viral-growth", "network-effects"]
    }
    
    relevant_theories = theory_mapping.get(features.problem, [])
    
    # 返回理论详情
    return [load_theory(t) for t in relevant_theories]
```

## 检索结果整合

### Knowledge Context 结构

```json
{
  "matched_cases": [
    {
      "name": "案例名称",
      "similarity_score": 0.85,
      "key_tactics": ["策略1", "策略2"],
      "results": "核心成果",
      "replicable_points": ["可复制点"],
      "warnings": ["注意事项"]
    }
  ],
  "recommended_weapons": [
    {
      "id": 12,
      "name": "双边奖励",
      "category": "病毒裂变",
      "suitability_score": 0.92,
      "reason": "推荐理由",
      "implementation_effort": "Medium"
    }
  ],
  "relevant_theories": [
    {
      "name": "PLG",
      "core_principle": "产品即营销",
      "application": "如何应用"
    }
  ]
}
```

## 缓存策略

### 检索缓存

```
缓存键 = hash(用户输入特征)
缓存值 = Knowledge Context
缓存时间 = 1小时
```

### 热点预加载

```
预加载高频场景：
- SaaS获客
- 电商留存
- 内容平台增长
```

## 检索质量评估

### 相关性指标

```
相关性 = 用户反馈(有用/无用) / 总反馈
```

### 覆盖率指标

```
覆盖率 = 有检索结果的查询 / 总查询
```

### 持续优化

```
1. 记录检索日志
2. 收集用户反馈
3. 调整匹配权重
4. 补充缺失案例
```
