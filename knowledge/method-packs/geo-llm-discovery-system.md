---
id: geo-llm-discovery-system
name: GEO/LLM 发现系统
summary: 把生成式搜索、答案引擎可见性、品牌实体一致性和可引用事实组织成一个可验证的发现系统。
domains: [geo, llm-search, answer-engine, generative-search]
problem_types: [acquisition, brand]
categories: [content-growth, brand]
growth_process: 用户获取
journey_stage: 认知/到达
stage_fit: [1-10, 10-100]
resource_profile: 内容、品牌、工程、数据协同；适合已有基础内容资产和可验证事实的团队
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
  - 目标用户在生成式搜索里会问什么，答案引擎会引用哪些实体和事实？
  - 哪些品牌事实、产品事实和比较结论能够被机器稳定提取？
  - 当前内容是否对人类可读，也对模型可引用？
decision_rules:
  - 先统一品牌实体、事实口径和页面结构，再扩内容规模。
  - 生成式搜索优化优先做可引用结论、实体定义和对比表，而不是先扩词。
  - 只有能被验证的内容资产才值得被 LLM 与答案引擎引用。
experiment_shapes:
  - 为 5 个核心页面补实体、FAQ、对比和结论块，观察生成式搜索引用与自然访问变化。
  - 对 10 个高意图问题页加入结构化数据和可引用摘要，观察 AI 搜索可见性。
  - 统一品牌术语与产品命名，比较引用一致性和落地页转化质量。
guardrails:
  - 不要伪造引用、来源或数据。
  - 不要用生成式搜索当作低质量内容分发渠道。
  - 不要在品牌事实不一致时扩内容规模。
related_weapons: [content-growth, brand]
related_failures:
  - knowledge/failures/acquisition-anti-patterns.md
---

# GEO/LLM 发现系统

## 适用场景

品牌在 AI 搜索、答案引擎和生成式检索中的可见性不足，或者现有内容对人类可读但对模型不可稳定引用。

## 决策顺序

1. 先统一品牌事实和实体口径。
2. 再重写核心页面结构，让答案引擎能直接提取结论。
3. 再补结构化数据、FAQ、对比和引用锚点。
4. 最后才扩大内容规模。

## 核心输出

- 生成式搜索引用地图
- 品牌实体与术语表
- 可引用结论块
- FAQ / 对比 / 摘要模板
- 4 周 GEO 实验

## 实验样式

- 为 5 个核心页面补实体、FAQ、对比和结论块，观察引用与访问变化。
- 对 10 个高意图问题页加入结构化数据和可引用摘要，观察 AI 搜索可见性。
- 统一品牌术语与产品命名，比较引用一致性和落地页转化质量。

## 停止信号

- 引用增加但品牌事实不一致。
- 页面更像内容工厂而不是可验证信息源。
- AI 搜索可见性提升，但没有带来高意向访问和转化。
