---
id: lifecycle-email-retention-system
name: 生命周期邮件与留存系统
summary: 把冷邮件、drip、onboarding、召回、失败付款和邮件送达整合成生命周期触达系统。
domains: [email, lifecycle, cold-outreach, retention, deliverability]
problem_types: [acquisition, activation, retention, monetization]
categories: [b2b-sales, retention, monetization]
growth_process: 用户深耕
journey_stage: 留存
stage_fit: [0-1, 1-10, 10-100]
resource_profile: 低预算可启动；需要 CRM、内容和运营节奏
evidence_tier: C
source_skills:
  - coreyhaines31/cold-email
  - coreyhaines31/email-sequence
  - coreyhaines31/churn-prevention
  - resend/resend
  - resend/react-email
  - resend/email-best-practices
  - trycourier/courier-skills
  - CosmoBlk/email-marketing-bible
canonical_questions:
  - 这封邮件服务于获客、激活、留存、升级还是挽回？
  - 触发条件是用户行为、生命周期阶段，还是销售动作？
  - 邮件成功后用户下一步关键动作是什么？
decision_rules:
  - 先定义触发事件和下一步动作，再写邮件。
  - 冷邮件看高意向回复和会议质量，不只看打开率。
  - 生命周期邮件必须和产品内行为联动。
experiment_shapes:
  - 测试两个 cold email 角度，比较正向回复和合格会议。
  - 为未激活用户设置 3 封 onboarding drip，观察首次价值达成率。
  - 为取消和失败付款用户设计挽回流程，观察恢复率和投诉率。
guardrails:
  - 不要用高频触达替代产品价值。
  - 不要只优化打开率而忽略下一步行为。
  - 不要牺牲送达率和品牌信任。
related_weapons: [b2b-sales, retention, monetization]
related_failures:
  - knowledge/failures/acquisition-anti-patterns.md
  - knowledge/failures/retention-failure-modes.md
---

# 生命周期邮件与留存系统

## 适用场景

需要用邮件、通知或多渠道触达支持冷启动外联、激活、召回、升级、失败付款恢复或取消挽回。

## 触达设计顺序

1. 明确生命周期阶段：获客、激活、留存、升级、挽回。
2. 明确触发事件：行为、时间、销售动作或风险信号。
3. 明确下一步动作：回复、预约、完成首次价值、升级或续费。
4. 明确约束线：投诉、退订、送达率、品牌信任。

## 决策规则

- 先定义触发事件和下一步动作，再写邮件。
- 冷邮件看高意向回复和合格会议，不只看打开率。
- 生命周期邮件必须和产品内行为联动。

## 实验样式

- 测试两个 cold email 角度，比较正向回复和合格会议。
- 为未激活用户设置 3 封 onboarding drip，观察首次价值达成率。
- 为取消和失败付款用户设计挽回流程，观察恢复率和投诉率。

## 停止信号

- 高频触达替代了产品价值。
- 打开率提升但下一步行为没有变化。
- 投诉、退订或送达率恶化。
