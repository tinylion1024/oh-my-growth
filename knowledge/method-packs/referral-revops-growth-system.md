---
id: referral-revops-growth-system
name: 推荐裂变与 RevOps 系统
summary: 把推荐、affiliate、口碑、线索生命周期和营销销售交接整合成可控的增长运营系统。
domains: [referral, affiliate, revops, sales-handoff]
problem_types: [referral, acquisition, monetization]
categories: [viral-referral, b2b-sales, monetization]
growth_process: 用户获取
journey_stage: 分享
stage_fit: [1-10, 10-100]
resource_profile: 跨团队协同；需要销售、市场、数据和客户成功共同维护
evidence_tier: C
source_skills:
  - coreyhaines31/referral-program
  - coreyhaines31/revops
  - coreyhaines31/sales-enablement
  - phuryn/growth-loops
  - phuryn/north-star-metric
  - realkimbarrett/objection-crusher
canonical_questions:
  - 用户为什么愿意推荐：身份、利益、便利、关系还是成果证明？
  - 推荐进入后，谁负责跟进，什么时候算合格线索？
  - 增长飞轮的输入、循环动作、复利资产和约束线分别是什么？
decision_rules:
  - 先验证非补贴型分享动机，再设计奖励。
  - 推荐计划必须接入线索状态和销售跟进定义。
  - RevOps 的目标是减少漏损，不是增加报表。
experiment_shapes:
  - 对高 NPS 用户测试低摩擦推荐入口，观察邀请、激活和留存。
  - 建立 MQL/SQL 交接定义，观察线索响应时间和成交率。
  - 为一个增长飞轮设置输入指标、循环指标和约束线，跑 4 周复盘。
guardrails:
  - 不要让补贴吸引低质量用户和套利行为。
  - 不要把所有新增都塞给销售而不分层。
  - 不要只看线索量，必须看转化、回收和留存。
related_weapons: [viral-referral, b2b-sales, monetization]
related_failures:
  - knowledge/failures/acquisition-anti-patterns.md
  - knowledge/failures/referral-failure-modes.md
---

# 推荐裂变与 RevOps 系统

## 适用场景

要设计推荐、affiliate、口碑传播、销售线索生命周期，或修复市场到销售交接漏损。

## 推荐机制判断

用户愿意推荐通常来自五类动机：

1. 身份表达：推荐能表达自己是谁。
2. 关系帮助：推荐对朋友确实有用。
3. 结果证明：用户已经获得可展示成果。
4. 利益激励：奖励明确且成本可控。
5. 便利触发：推荐入口足够低摩擦。

## RevOps 判断

- MQL、SQL、机会和成交定义必须一致。
- 每个阶段要有 owner、SLA、退出条件和失败原因。
- 线索量增长必须和成交率、回收周期、留存一起看。

## 实验样式

- 对高 NPS 用户测试低摩擦推荐入口，观察邀请、激活和留存。
- 建立 MQL/SQL 交接定义，观察线索响应时间和成交率。
- 为一个增长飞轮设置输入指标、循环指标和约束线，跑 4 周复盘。

## 停止信号

- 分享率高但被邀请用户激活和留存差。
- 销售跟进没有分层，导致高意向线索被淹没。
- 只汇报线索量，不解释转化、回收和留存。
