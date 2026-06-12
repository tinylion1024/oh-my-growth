"""Strategy constants and configuration.

This module contains all constant definitions for the strategy brain:
- Problem labels and mappings
- Stage framework definitions
- Category actions and avoids
- Metric mappings
"""

# Problem type labels (Chinese)
PROBLEM_LABELS = {
    "acquisition": "获客",
    "activation": "激活",
    "retention": "留存",
    "monetization": "变现",
    "referral": "裂变",
}

# Stage labels (Chinese)
STAGE_LABELS = {
    "0-1": "冷启动",
    "1-10": "增长期",
    "10-100": "规模化",
}

# Stage framework with focus and reasoning
STAGE_FRAMEWORK = {
    "0-1": {
        "name": "产品验证期",
        "focus": "先验证可复制主路径与核心价值成立，再决定是否放大投入。",
        "reason": "这个阶段最怕表面增长，真正关键的是高意向用户是否持续留下。",
    },
    "1-10": {
        "name": "增长放大期",
        "focus": "把已验证动作变成稳定系统，同时补齐漏斗、归因和资源协同。",
        "reason": "这个阶段最重要的是放大已成立抓手，而不是重新分散尝试。",
    },
    "10-100": {
        "name": "规模经营期",
        "focus": "平衡效率、收入质量和长期价值，并为新增量做准备。",
        "reason": "这个阶段的主要问题通常不是有没有动作，而是资源配置和结构优化。",
    },
}

# Problem to growth process mapping
PROBLEM_TO_PROCESS = {
    "acquisition": ("用户获取", "先稳定新增路径、控制 CAC，并验证用户质量。"),
    "activation": ("用户深耕", "先缩短首次价值到达时间，提升关键动作转化。"),
    "retention": ("用户深耕", "先修复持续回访与复购理由，避免假活跃。"),
    "monetization": ("用户深耕", "先验证价值付费链条，再放大商业化动作。"),
    "referral": ("用户获取", "先验证分享动机和邀请转化，再考虑放大裂变机制。"),
}

# Problem to journey stage mapping
PROBLEM_TO_JOURNEY = {
    "acquisition": ("认知/到达", "流量来源与到达后的高意向转化是否成立。"),
    "activation": ("注册/激活", "用户能否在首次使用中尽快获得核心价值。"),
    "retention": ("留存", "用户是否持续获得回来使用的理由。"),
    "monetization": ("付费", "核心价值和付费触发点是否真正对齐。"),
    "referral": ("分享", "产品价值是否强到足以支撑用户主动传播。"),
}

# Recommended actions by category
CATEGORY_ACTIONS = {
    "cold-start": ["先集中拿到 20-50 个高意向种子用户", "优先验证转介绍或高触达渠道是否能稳定出单"],
    "viral-referral": ["只设计一个低摩擦分享触点", "先跑奖励成本可控的双边激励实验"],
    "content-growth": ["先围绕单一高意图关键词做内容闭环", "把内容产出绑定到注册或留资动作"],
    "community": ["先识别核心用户群并建立固定反馈场景", "让社区承担分发和留存，而不是只做运营热闹"],
    "plg": ["先缩短首次价值到达时间", "优先做能自传播的产品节点，而不是大而全功能"],
    "retention": ["只盯一个关键留存节点", "先用提醒、习惯、回流机制验证复访提升"],
    "monetization": ["先明确付费触发点", "优先做不伤害核心留存的轻量商业化实验"],
    "paid-ads": ["先小预算验证创意和人群", "没有自然转化基础前不要放大预算"],
    "brand": ["只围绕一个品牌心智重复投入", "品牌动作必须绑定长期获客或转化假设"],
    "b2b-sales": ["先提高高意向线索密度", "把销售动作拆成可复盘的话术和漏斗"],
}

# Things to avoid by category
CATEGORY_AVOIDS = {
    "cold-start": ["不要一开始就铺太多渠道", "不要先做重工程的大系统"],
    "viral-referral": ["不要先上复杂裂变玩法", "不要用高补贴换来低质量用户"],
    "content-growth": ["不要同时做太多内容形态", "不要只做曝光不设计转化路径"],
    "community": ["不要把社区活跃误当成增长结果", "不要一开始就追求大规模社区运营"],
    "plg": ["不要先做复杂功能矩阵", "不要用销售动作掩盖产品体验问题"],
    "retention": ["不要同时改太多留存机制", "不要在主价值未成立前堆激励"],
    "monetization": ["不要先用强打扰付费墙", "不要为了短期收入破坏长期留存"],
    "paid-ads": ["不要在素材和转化路径未验证前扩量", "不要让 CAC 脱离 LTV 讨论"],
    "brand": ["不要把品牌动作当短期拉新速效药", "不要做没有复用价值的一次性 campaign"],
    "b2b-sales": ["不要只盯线索数不看成交路径", "不要过早扩销售团队而不修转化漏斗"],
}

# Metrics by problem type
PROBLEM_TO_METRICS = {
    "acquisition": ["新增高意向用户数", "获客成本/CAC", "首周激活率"],
    "activation": ["首个关键动作转化率", "首次价值达成率", "激活到留存转化率"],
    "retention": ["7日/30日留存", "复访频次", "流失召回率"],
    "monetization": ["付费转化率", "ARPU/ARPPU", "升级率"],
    "referral": ["分享率", "邀请转化率", "K 因子"],
}
