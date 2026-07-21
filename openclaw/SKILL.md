---
name: oh-my-growth
description: "增长策略外脑 - 整合 81 案例、111 玩法、12 流派的增长决策插件"
version: 1.0.2
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3"]
    install:
      - id: "pip"
        kind: "pip"
        requirements: ["requirements.txt"]
        label: "Install Python dependencies"
    triggers:
      - /omg-diagnose
      - /omg-assess
      - /omg-design
      - /omg-match
      - /omg-learn
      - /omg-fast-scan
      - /omg-brd
      - /omg-cold-start
      - /omg-retention
      - /omg-monetization
      - /omg-referral
      - /omg-search
      - /omg-validate
---

# oh-my-growth - 增长策略外脑

**OpenClaw 专用增长决策插件** — 在 OpenClaw 会话中直接调用专业的增长策略分析能力。

整合 **81 个案例** · **111 种玩法** · **12 大流派** · **完整决策框架**

---

## 快速开始

```
/omg-diagnose 我的产品日活下降20%，该怎么办？
/omg-assess 我们准备做裂变，先评估可行性
/omg-design SaaS产品如何设计变现策略？
/omg-match 游戏化留存案例
```

---

## 所有命令

| 命令 | 描述 | 使用场景 |
|------|------|----------|
| `/omg-diagnose` | 策略诊断 + 优先级 + 实验建议 | 增长负责人需要快速形成判断 |
| `/omg-assess` | 机会可行性评估 | 现状还不够清楚，先做清晰度评估 |
| `/omg-design` | 可落地的策略设计 | 知道要做什么，需要执行路径 |
| `/omg-fast-scan` | 快速判断 | 这个想法靠谱吗？ |
| `/omg-brd` | 完整决策文档 | 需要申请预算/资源 |
| `/omg-match` | 匹配成功案例 | 想看看别人怎么做的 |
| `/omg-learn` | 系统学习路径 | 想深入了解某个增长领域 |
| `/omg-search` | 搜索知识库 | 直接检索案例/玩法/理论 |
| `/omg-validate` | 验证输出文档 | 检查报告完整性 |

### 场景快捷入口

| 命令 | 描述 |
|------|------|
| `/omg-cold-start` | 冷启动场景 - 获取前 100 个用户 |
| `/omg-retention` | 留存场景 - 提升用户留存率 |
| `/omg-monetization` | 变现场景 - 设计变现策略 |
| `/omg-referral` | 裂变场景 - 评估裂变可行性 |

---

## 核心工作流

```
用户输入 → 阶段定位 → 问题诊断 → 知识检索 → 优先级判断 → 实验建议 → 输出生成
```

### 1. 阶段与业务过程定位

先判断当前属于：
- **产品验证期** (0-1) - PMF 验证阶段
- **增长放大期** (1-10) - 规模化增长阶段
- **规模经营期** (10-100) - 效率优化阶段

以及问题更偏：
- **用户获取** (acquisition)
- **用户深耕** (retention/monetization)

### 2. 问题诊断

判断：
- 主目标是什么？
- 北极星指标应该是什么？
- 最大约束是什么？
- 最可能的主矛盾是什么？

### 3. 知识检索

从知识库检索：
- **Case Agent** - 匹配相似案例
- **Weapon Agent** - 推荐增长玩法
- **Theory Agent** - 引用相关理论

### 4. 优先级判断

使用以下维度排序：
- ROI 预期
- 执行复杂度
- 阶段匹配度
- 证据加分
- 失败模式惩罚

### 5. 建议做 / 不做

明确指出：
- 当前该押注什么
- 不该分散到什么方向
- 为什么

### 6. 实验计划

输出：
- 最小实验设计
- 成功信号
- 停止信号
- 复盘节奏

---

## 决策框架

### 贝叶斯决策引擎

将不确定的增长决策转化为可审计的概率推理过程：

```
初始假设 → 设置先验 → 收集证据 → 更新后验 → 比较阈值 → 推荐行动
```

**行动阈值**：

| 后验概率 | 决策 | 说明 |
|----------|------|------|
| ≥ 75% | **立即投入** | 高置信度，可执行 |
| 50-75% | **运行实验** | 中等置信度，需验证 |
| 30-50% | **收集证据** | 低置信度，信息不足 |
| < 30% | **停止** | 很低置信度，不推荐 |

### Kelly 资源分配

计算最优投资比例：

```
f* = (bp - q) / b

f* = 最优投资比例
b  = 净赔率（盈利/亏损）
p  = 胜率
q  = 败率
```

输出：
- 建议投入比例
- 加仓条件
- 停止条件
- 复盘周期

### 证据分级系统

| 等级 | 定义 | 更新幅度 |
|------|------|----------|
| A | Meta 分析、系统综述 | ±25% |
| B | 同行评审、行业报告 | ±15% |
| C | 专家意见、内部数据 | ±10% |
| D | LLM 建议、类比 | ±5% |
| E | 博客、营销文案 | 0% |

---

## 知识库结构

```
knowledge/
├── cases/           # 81 个增长案例
│   ├── china/      # 中国案例（拼多多、抖音、小红书...）
│   ├── overseas/   # 海外案例（Notion、Figma、Airbnb...）
│   └── vertical/   # 垂直行业案例
├── weapons/         # 111 种增长玩法
│   ├── acquisition/  # 获客玩法
│   ├── retention/    # 留存玩法
│   ├── monetization/ # 变现玩法
│   └── referral/     # 裂变玩法
├── schools/         # 12 大流派理论
│   ├── growth-hacking.md
│   ├── network-effects.md
│   ├── plg.md
│   └── ...
└── indexes/         # JSON 索引
```

---

## 使用示例

### 场景 1：DAU 下降

```
/omg-diagnose 我们的产品 DAU 最近下降了 20%，该怎么办？
```

输出：
- 阶段诊断
- 核心矛盾分析
- 优先级排序
- 2 周最小实验

### 场景 2：评估裂变可行性

```
/omg-assess 我们准备做裂变活动，先评估一下可行性
```

输出：
- 清晰度评估
- 可行性判断
- 风险因素
- 建议下一步

### 场景 3：设计留存策略

```
/omg-design 如何提升 B2B SaaS 产品的 30 天留存率？
```

输出：
- 核心策略
- 分阶段执行路径
- 关键指标
- 相关案例

---

## 场景快捷入口

```
/omg-cold-start 如何获得 AI 写作 SaaS 的前 100 个付费用户？
/omg-retention 如何提升电商 APP 的 30 天留存率？
/omg-monetization 如何为内容社区设计变现策略？
/omg-referral 我们的教育 APP 适合做裂变吗？
```

---

## 置信度声明

每个建议都会明确声明置信度：

- **High** - 强证据、可测试机制、执行可控
- **Medium** - 可行机制但有重要假设
- **Low** - 证据稀少、重大未知、无法验证

低置信度建议会转化为实验计划，而非全量投入建议。

---

## 设计原则

1. **决策导向** - 目标是决定是否值得投入，不是让想法听起来不错
2. **知识驱动** - 每个决策都有案例/理论支撑
3. **因果逻辑** - 强制清晰的因果链
4. **早期暴露问题** - 在投入前识别风险
5. **证据先行** - 证据弱时推荐实验而非全量投入

---

## 相关文件

### 核心框架
- [贝叶斯决策框架](../references/bayesian-decision.md)
- [博弈论战略框架](../references/gametheory-framework.md)
- [Kelly 资源分配框架](../references/kelly-allocation.md)
- [商业模式分析框架](../references/business-model.md)

### 质量保障
- [现状清晰度门控](../references/current-state-clarity.md)
- [安全边界](../references/safety-boundaries.md)
- [输出契约](../references/report-contract.md)

### 计算脚本
- `../scripts/bayesian_decision.py` - 贝叶斯计算
- `../scripts/kelly_sizing.py` - Kelly 资源计算
- `../scripts/gametheory_analysis.py` - 博弈论分析
- `../scripts/assess_clarity.py` - 清晰度评估
