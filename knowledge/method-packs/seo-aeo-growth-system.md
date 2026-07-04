---
id: seo-aeo-growth-system
name: SEO/AEO 获客系统
summary: 把搜索、内容结构、Schema、AEO 与内容实验合成一个可验证的自然获客系统。
domains: [seo, aeo, content, programmatic-seo]
problem_types: [acquisition]
categories: [content-growth]
growth_process: 用户获取
journey_stage: 认知/到达
stage_fit: [0-1, 1-10, 10-100]
resource_profile: 内容、工程、数据协同；适合低预算但需要持续产能
evidence_tier: C
source_skills:
  - coreyhaines31/ai-seo
  - coreyhaines31/programmatic-seo
  - coreyhaines31/schema-markup
  - coreyhaines31/seo-audit
  - sanity-io/seo-aeo-best-practices
  - addyosmani/seo
  - AgriciDaniel/claude-seo
canonical_questions:
  - 目标用户会用哪些问题、替代品、场景和结果词来搜索？
  - 现有页面是否能同时回答人类搜索和 AI 摘要引用？
  - 哪些页面模板可以规模化生成但仍保持可验证价值？
decision_rules:
  - 先修搜索意图和页面结构，再扩大内容产能。
  - 程序化 SEO 只有在模板能承载独立价值时才放大。
  - AEO 输出必须有实体、步骤、比较和可引用结论。
experiment_shapes:
  - 选 10 个高意图长尾词，重写页面结构，观察 4 周索引、点击和转化。
  - 为 3 类页面加入结构化数据，比较搜索展示和转化质量。
  - 生成一个小规模模板集，先验证收录和高意向线索再扩库。
guardrails:
  - 不要用低质量批量内容替代真实问题回答。
  - 不要只看流量，必须看高意向行为和线索质量。
  - 不要在技术 SEO 未达标时盲目扩内容。
related_weapons: [content-growth]
related_failures:
  - knowledge/failures/acquisition-anti-patterns.md
---

# SEO/AEO 获客系统

## 适用场景

搜索流量弱、内容增长没有结构、AI 搜索引用缺失、程序化页面想放大但还没有验证页面价值。

## 决策顺序

1. 先判断用户搜索意图：问题、替代品、场景、结果词。
2. 再判断页面是否能回答完整任务，而不是只堆关键词。
3. 再修技术可发现性：索引、内部链接、结构化数据、页面性能。
4. 最后才扩内容模板和产能。

## 核心输出

- 搜索意图地图
- 页面结构审计
- Schema 和实体清单
- 程序化 SEO 模板假设
- 4 周自然获客实验

## 实验样式

- 选 10 个高意图长尾词，重写页面结构，观察索引、点击、高意向行为。
- 为 3 类页面加入结构化数据，比较搜索展示和转化质量。
- 生成一个小规模模板集，先验证收录和线索质量再扩库。

## 停止信号

- 页面被收录但没有高意向行为。
- 内容生成速度提升，但搜索意图和页面价值没有提升。
- 技术 SEO 问题导致内容无法稳定被发现。
