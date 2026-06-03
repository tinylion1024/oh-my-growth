# 反馈系统

## 概述

反馈系统用于收集用户对增长大师输出的评价，持续改进系统质量。

## 目录结构

```
feedback/
├── logs/                # 反馈日志
│   ├── 2024-01/
│   │   ├── 2024-01-15.json
│   │   └── ...
│   └── ...
├── analysis/            # 分析报告
│   ├── weekly-report.md
│   └── patterns.md
└── actions/             # 改进行动
    ├── knowledge-update.md
    └── agent-tuning.md
```

## 反馈收集

### 输出末尾模板

每个增长大师的输出末尾应包含：

```markdown
---

## 📝 反馈

这个建议对您有帮助吗？

**评分**（1-5星）：⭐⭐⭐⭐⭐

**有用程度**：
- [ ] 非常有帮助 - 可以直接行动
- [ ] 有一定帮助 - 提供了思路
- [ ] 一般 - 有参考价值但不完整
- [ ] 不太有帮助 - 缺少关键信息
- [ ] 完全没有帮助 - 答案无关

**请告诉我们**：
1. 最有帮助的部分是？
2. 缺少什么信息？
3. 您会按建议行动吗？
4. 其他建议？

**案例相关**：
- [ ] 推荐的案例很有参考价值
- [ ] 案例不太相关
- [ ] 希望看到更多案例
```

### 反馈数据结构

```json
{
  "feedback_id": "fb-20240115-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "session-xxx",
  
  "input_summary": {
    "problem_type": "acquisition",
    "industry": "saas",
    "mode": "Fast Scan"
  },
  
  "rating": {
    "stars": 4,
    "usefulness": "有一定帮助"
  },
  
  "qualitative": {
    "most_helpful": "案例匹配很准确",
    "missing_info": "缺少具体的实施步骤",
    "will_act": true,
    "suggestions": "希望增加ROI计算模板"
  },
  
  "case_feedback": {
    "relevant": true,
    "want_more": false
  },
  
  "output_metadata": {
    "agents_used": ["Lead", "Growth", "ROI", "Case"],
    "confidence": "Medium",
    "output_length": 1500
  }
}
```

## 反馈分析

### 每周分析

`feedback/analysis/weekly-report.md`：

```markdown
# 周报：2024年第3周

## 概览

- 总反馈数：25
- 平均评分：3.8/5
- 有帮助比例：72%

## 按模式分析

| 模式 | 反馈数 | 平均分 | 有帮助% |
|------|--------|--------|---------|
| Fast Scan | 10 | 4.1 | 80% |
| Decision BRD | 8 | 3.5 | 62% |
| Strategy Design | 7 | 4.0 | 71% |

## 问题发现

1. **Decision BRD 模式评分较低**
   - 原因：输出过长，关键信息不突出
   - 改进：简化模板，突出结论

2. **案例匹配问题**
   - 原因：部分场景缺少相关案例
   - 改进：补充垂直行业案例

## 改进行动

- [ ] 简化 Decision BRD 输出模板
- [ ] 补充教育行业案例
- [ ] 优化案例匹配算法
```

### 模式分析

`feedback/analysis/patterns.md`：

```markdown
# 反馈模式分析

## 高分模式

1. **案例匹配准确** → 平均分+0.8
2. **输出简洁明确** → 平均分+0.6
3. **有具体行动建议** → 平均分+0.5

## 低分模式

1. **信息不足仍强行回答** → 平均分-1.2
2. **输出过于理论化** → 平均分-0.8
3. **案例不相关** → 平均分-0.7

## 改进优先级

1. 信息不足时主动询问而非猜测
2. 提供具体可执行的行动建议
3. 提升案例匹配准确率
```

## 持续改进

### 知识库更新

`feedback/actions/knowledge-update.md`：

```markdown
# 知识库更新建议

## 来源：2024年第3周反馈

### 需要补充的案例

| 场景 | 反馈数 | 优先级 |
|------|--------|--------|
| 在线教育游戏化 | 3 | P0 |
| B2B SaaS获客 | 2 | P1 |
| 社区团购留存 | 2 | P1 |

### 需要更新的数据

- Dropbox 裂变案例数据需要更新
- 添加更多ROI计算模板

### 已完成更新

- [x] 补充教育行业游戏化案例（Duolingo详情）
- [x] 更新SaaS获客案例数据
```

### Agent 调优

`feedback/actions/agent-tuning.md`：

```markdown
# Agent 调优建议

## Lead Agent

- 调整：信息不足时更主动询问
- 来源：5条反馈提到"答案不够针对性"

## Growth Agent

- 调整：增加更多具体行动建议
- 来源：3条反馈提到"太理论化"

## Case Agent

- 调整：优化匹配算法，提升相关性
- 来源：4条反馈提到"案例不太相关"
```

## 自动化

### 反馈聚合脚本

`scripts/aggregate-feedback.sh`：

```bash
#!/bin/bash
# 每周运行，聚合反馈并生成报告

WEEK=$(date +%Y-W%V)
FEEDBACK_DIR="feedback/logs"
OUTPUT_FILE="feedback/analysis/weekly-report-$WEEK.md"

# 统计
TOTAL=$(find $FEEDBACK_DIR -name "*.json" | wc -l)
AVG_RATING=$(jq -s 'add | .[].rating.stars' $FEEDBACK_DIR/**/*.json | awk '{sum+=$1} END {print sum/NR}')

echo "# 周报：$WEEK" > $OUTPUT_FILE
echo "" >> $OUTPUT_FILE
echo "- 总反馈数：$TOTAL" >> $OUTPUT_FILE
echo "- 平均评分：$AVG_RATING" >> $OUTPUT_FILE
```
