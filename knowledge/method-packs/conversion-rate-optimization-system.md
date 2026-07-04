---
id: conversion-rate-optimization-system
name: CRO 转化率优化系统
summary: 把落地页、表单、注册、onboarding、paywall 和 popup 优化统一为旅程断点实验。
domains: [cro, landing-page, signup, onboarding, paywall]
problem_types: [activation, monetization, acquisition]
categories: [plg, retention, monetization]
growth_process: 用户深耕
journey_stage: 注册/激活
stage_fit: [1-10, 10-100]
resource_profile: 产品、设计、工程、数据协同；适合已有稳定流量的团队
evidence_tier: C
source_skills:
  - coreyhaines31/page-cro
  - coreyhaines31/form-cro
  - coreyhaines31/signup-flow-cro
  - coreyhaines31/onboarding-cro
  - coreyhaines31/paywall-upgrade-cro
  - coreyhaines31/popup-cro
  - coreyhaines31/marketing-psychology
canonical_questions:
  - 用户在哪一步停止，停止前看见了什么承诺和摩擦？
  - 转化问题来自动机不足、信任不足、理解不足还是操作摩擦？
  - 哪个微转化最能预测最终付费或留存？
decision_rules:
  - 先定位旅程断点，再改页面元素。
  - 每次实验只改一个主假设：动机、信任、理解或摩擦。
  - CRO 成功必须同时检查用户质量、留存和退款。
experiment_shapes:
  - 重写首屏承诺和 CTA，观察注册率与激活率。
  - 减少表单字段或分步展示，观察提交率与线索质量。
  - 调整 paywall 价值证明，观察升级率、退款率和留存。
guardrails:
  - 不要用诱导式文案换取低质量注册。
  - 不要只优化点击率而忽略激活和留存。
  - 不要同时改流量来源和转化路径。
related_weapons: [plg, retention, monetization]
related_failures:
  - knowledge/failures/retention-failure-modes.md
---

# CRO 转化率优化系统

## 适用场景

落地页、表单、注册、onboarding、paywall 或 popup 存在明显漏损，且已有足够稳定流量支持实验。

## 诊断模型

转化率问题通常来自四类原因：

1. 动机不足：用户不觉得值得继续。
2. 信任不足：用户不相信承诺或风险太高。
3. 理解不足：用户不知道产品能带来什么结果。
4. 摩擦过高：路径、表单、支付或引导成本太高。

## 决策规则

- 先定位旅程断点，再改页面元素。
- 每次实验只改一个主假设。
- 成功标准必须同时检查用户质量、留存和退款。

## 实验样式

- 重写首屏承诺和 CTA，观察注册率与激活率。
- 减少表单字段或分步展示，观察提交率与线索质量。
- 调整 paywall 价值证明，观察升级率、退款率和留存。

## 停止信号

- 点击率提高但激活和留存下降。
- 页面转化提高但线索质量下降。
- 团队无法判断具体是哪一个假设造成变化。
