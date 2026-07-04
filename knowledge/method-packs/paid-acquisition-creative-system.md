---
id: paid-acquisition-creative-system
name: 付费获客与创意测试系统
summary: 把广告创意、受众、offer、转化路径和投放诊断合成可迭代的效果营销系统。
domains: [paid-ads, creative-testing, offer, funnel]
problem_types: [acquisition]
categories: [paid-ads]
growth_process: 用户获取
journey_stage: 认知/到达
stage_fit: [1-10, 10-100]
resource_profile: 预算密集、创意产能、投放和数据协同
evidence_tier: C
source_skills:
  - coreyhaines31/ad-creative
  - coreyhaines31/paid-ads
  - realkimbarrett/avatar-extraction
  - realkimbarrett/offer-extraction
  - realkimbarrett/ad-angle-multiplier
  - realkimbarrett/scroll-stopping-creative
  - realkimbarrett/conversion-path-builder
  - realkimbarrett/performance-diagnosis
  - nowork-studio/NotFair
canonical_questions:
  - 当前瓶颈是受众不准、创意不吸引、offer 不成立，还是落地页漏斗承接差？
  - 每个创意角度对应哪个买家痛点、触发场景和反对意见？
  - CPA 高是点击前问题、点击后问题，还是用户质量问题？
decision_rules:
  - 投放放大前必须先证明转化路径和回收期。
  - 创意测试按角度分组，不按零散素材堆量。
  - 诊断先分层：展示、点击、落地页、注册、激活、付费。
experiment_shapes:
  - 用 3 个买家痛点生成 9 个创意角度，固定落地页测试 CTR 与 CVR。
  - 同一创意分别测试两个 offer，观察 CPA、激活率和退款率。
  - 对高点击低转化广告做漏斗审计，定位断点后再加预算。
guardrails:
  - 不要用预算掩盖未验证的产品和页面问题。
  - 不要只看平台 CPA，必须看激活、付费和回收周期。
  - 不要让创意承诺超过产品实际交付。
related_weapons: [paid-ads]
related_failures:
  - knowledge/failures/acquisition-anti-patterns.md
---

# 付费获客与创意测试系统

## 适用场景

Google、Meta、TikTok、LinkedIn 等投放渠道 CPA 过高，创意测试没有结论，或预算放大后回收恶化。

## 诊断层级

1. 展示：受众和竞价是否拿到正确流量。
2. 点击：创意角度是否匹配痛点和场景。
3. 落地页：offer 和承诺是否被承接。
4. 注册/激活：转化是否带来真实用户行为。
5. 付费/回收：CAC、LTV、回收周期是否成立。

## 创意测试规则

- 按角度分组，不按零散素材堆量。
- 每个角度必须对应一个买家痛点、触发场景和反对意见。
- 固定落地页时测创意，固定创意时测 offer。

## 实验样式

- 用 3 个买家痛点生成 9 个创意角度，固定落地页测试 CTR 与 CVR。
- 同一创意分别测试两个 offer，观察 CPA、激活率和退款率。
- 对高点击低转化广告做漏斗审计，定位断点后再加预算。

## 停止信号

- CPA 依赖持续加预算才能维持。
- 创意承诺超过产品实际交付。
- 平台指标看起来变好，但激活、付费或留存恶化。
