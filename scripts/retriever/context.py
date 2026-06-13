"""Context helper methods for knowledge retrieval.

This module contains methods for context analysis, query expansion,
and context-based preference calculation.
"""

import re
from typing import Dict, List, Set, Tuple, Any


def normalize_text(text: Any) -> str:
    """Normalize text for comparison."""
    return re.sub(r"\s+", " ", str(text).lower().replace("_", " ").replace("-", " ")).strip()


def tokenize(text: str) -> List[str]:
    """Tokenize English terms and Chinese phrases/bigrams for retrieval."""
    normalized = normalize_text(text)
    normalized = re.sub(r"[^0-9a-z一-鿿\s]", " ", normalized)

    tokens: List[str] = []
    tokens.extend(re.findall(r"[a-z0-9]+", normalized))

    for chunk in re.findall(r"[一-鿿]+", normalized):
        tokens.append(chunk)
        if len(chunk) == 1:
            continue
        for size in (2, 3):
            if len(chunk) < size:
                continue
            for index in range(len(chunk) - size + 1):
                tokens.append(chunk[index:index + size])

    return list(dict.fromkeys(token for token in tokens if token))


def compute_similarity(query_tokens: List[str], doc_tokens: List[str]) -> float:
    """Combine token overlap and substring matching for mixed CN/EN text."""
    if not query_tokens or not doc_tokens:
        return 0.0

    query_set = set(query_tokens)
    doc_set = set(doc_tokens)

    intersection = len(query_set & doc_set)
    union = len(query_set | doc_set)
    token_score = intersection / union if union else 0.0

    doc_text = " ".join(doc_tokens)
    substring_hits = 0
    for token in query_tokens:
        if len(token) < 2:
            continue
        if token in doc_text:
            substring_hits += 1

    substring_score = min(0.45, substring_hits * 0.08)
    return token_score + substring_score


def expand_query(query: str, context: Dict) -> List[str]:
    """Expand queries using lightweight domain synonyms."""
    expansions: List[str] = []

    industry_synonyms = {
        "saas": ["软件", "订阅", "b2b", "企业服务"],
        "ecommerce": ["电商", "购物", "零售", "交易", "平台"],
        "education": ["教育", "学习", "培训", "课程", "知识"],
        "fintech": ["金融", "支付", "理财", "信贷"],
        "social": ["社交", "社区", "好友", "互动", "关系"],
        "content": ["内容", "媒体", "视频", "文章", "信息"],
        "marketplace": ["平台", "双边市场", "供给", "商家"],
    }

    problem_synonyms = {
        "acquisition": ["获客", "增长", "拉新", "用户", "注册", "冷启动"],
        "retention": ["留存", "粘性", "活跃", "回访", "留存率", "复购"],
        "monetization": ["变现", "收入", "付费", "盈利", "商业化", "定价"],
        "referral": ["裂变", "传播", "分享", "邀请", "病毒", "推荐"],
        "activation": ["激活", "首购", "转化", "体验价值"],
    }

    category_keywords = {
        "cold-start": ["冷启动", "种子用户", "早期用户", "首批用户"],
        "viral-referral": ["裂变", "邀请", "推荐", "病毒", "分享"],
        "content-growth": ["内容", "seo", "教程", "newsletter", "案例研究"],
        "community": ["社区", "用户社群", "超级用户", "共创"],
        "plg": ["产品驱动增长", "plg", "freemium", "onboarding", "模板"],
        "retention": ["留存", "活跃", "召回", "复购", "习惯"],
        "monetization": ["变现", "付费", "定价", "upsell", "订阅"],
        "paid-ads": ["广告", "投放", "获客成本", "cac", "推广"],
        "brand": ["品牌", "pr", "创始人ip", "视觉"],
        "b2b-sales": ["销售", "线索", "demo", "客户成功", "外联"],
    }

    theory_keywords = {
        "growth-hacking": ["增长黑客", "实验", "aarrr", "ice"],
        "plg": ["产品驱动增长", "plg", "自传播", "自助体验"],
        "network-effects": ["网络效应", "双边市场", "临界质量"],
        "content-growth": ["内容增长", "内容营销", "seo", "入站"],
        "community-growth": ["社区增长", "超级用户", "共创"],
        "brand-growth": ["品牌增长", "品牌资产", "价值观"],
        "viral-growth": ["病毒增长", "裂变", "推荐", "分享"],
        "performance-marketing": ["效果营销", "投放", "广告"],
        "gamification": ["游戏化", "积分", "成就", "排行榜"],
        "flywheel": ["飞轮", "复利增长", "长期增长"],
        "business-models": ["商业模式", "变现", "付费", "定价"],
    }

    industry = context.get("industry", "").lower()
    problem = context.get("problem_type", "").lower()
    business_model_kind = context_business_model_kind(context)
    if business_model_kind in {"marketplace", "local-services"}:
        expansions.extend(["供给", "需求", "撮合", "流动性"])
        side_focus = context_marketplace_side_focus(query, context)
        if side_focus == "supply":
            expansions.extend(["商家", "司机", "房东", "入驻"])
        elif side_focus == "demand":
            expansions.extend(["买家", "乘客", "房客", "拉新"])
    if business_model_kind == "local-services":
        expansions.extend(["单城", "区域密度", "履约", "到店", "上门", "同城"])

    expansions.extend(industry_synonyms.get(industry, []))
    expansions.extend(problem_synonyms.get(problem, []))

    query_text = normalize_text(query)
    for category_id, keywords in category_keywords.items():
        if any(keyword in query_text for keyword in keywords):
            expansions.extend(keywords)
            expansions.append(category_id)

    for theory_id, keywords in theory_keywords.items():
        if any(keyword in query_text for keyword in keywords):
            expansions.extend(keywords)
            expansions.append(theory_id)

    return list(dict.fromkeys(expansions))


def build_query_tokens(query: str, context: Dict) -> List[str]:
    """Build query tokens from query and expanded terms."""
    query_tokens = tokenize(query)
    expansions = expand_query(query, context)
    query_tokens.extend(tokenize(" ".join(expansions)))
    return list(dict.fromkeys(query_tokens))


def context_business_model(context: Dict) -> str:
    """Get normalized business model from context."""
    profile = context.get("company_profile", {})
    if isinstance(profile, dict):
        return normalize_text(str(profile.get("business_model", "")))
    return ""


def context_business_model_kind(context: Dict) -> str:
    """Determine business model kind from context."""
    industry = normalize_text(context.get("industry", ""))
    business_model = context_business_model(context)
    if industry == "local-services" or any(
        token in business_model
        for token in ["local services", "本地生活", "到店", "上门", "同城", "配送", "外卖", "出行"]
    ):
        return "local-services"
    if any(token in business_model for token in ["b2b", "sales led", "sales-led", "销售驱动"]):
        return "b2b-sales-led"
    if industry == "marketplace" or any(token in business_model for token in ["marketplace", "双边", "平台"]):
        return "marketplace"
    if industry == "ai" or any(token in business_model for token in ["ai", "agent", "copilot"]):
        return "ai"
    return "general"


def context_marketplace_side_focus(query: str, context: Dict) -> str:
    """Determine marketplace side focus from context."""
    text = normalize_text(
        " ".join(
            [
                query,
                str(context.get("goal", "")),
                str(context.get("metric", "")),
                str(context.get("constraints", "")),
            ]
        )
    )
    explicit_demand_markers = ["先补需求侧", "先做需求侧", "需求侧优先", "先拉需求", "先做需求"]
    explicit_supply_markers = ["先补供给侧", "先做供给侧", "供给侧优先", "先拉供给", "先做供给"]
    if any(marker in text for marker in explicit_demand_markers):
        return "demand"
    if any(marker in text for marker in explicit_supply_markers):
        return "supply"

    supply_hits = sum(
        1 for token in ["供给", "商家", "司机", "房东", "创作者", "seller", "supply", "inventory", "入驻"]
        if token in text
    )
    demand_hits = sum(
        1 for token in ["需求", "买家", "乘客", "房客", "游客", "buyer", "demand", "rider", "guest"]
        if token in text
    )
    if demand_hits > supply_hits:
        return "demand"
    if supply_hits > demand_hits:
        return "supply"
    return "liquidity"


def context_preferred_categories(context: Dict, problem: str) -> Set[str]:
    """Get preferred categories based on context and problem."""
    categories = set(problem_to_categories(problem))
    business_model_kind = context_business_model_kind(context)

    if business_model_kind == "b2b-sales-led":
        categories.add("b2b-sales")
    if business_model_kind == "marketplace":
        categories.update({"community", "viral-referral"})
    if business_model_kind == "local-services":
        categories.update({"cold-start", "community"})
    if business_model_kind == "ai":
        categories.update({"content-growth", "plg"})

    return categories


def context_preferred_theories(context: Dict, problem: str) -> Set[str]:
    """Get preferred theories based on context and problem."""
    theories = set(problem_to_theories(problem))
    business_model_kind = context_business_model_kind(context)

    if business_model_kind == "b2b-sales-led":
        theories.update({"business-models", "plg"})
    if business_model_kind in {"marketplace", "local-services"}:
        theories.update({"network-effects", "flywheel"})
    if business_model_kind == "ai":
        theories.update({"content-growth", "plg"})

    return theories


def problem_to_categories(problem: str) -> Set[str]:
    """Map problem type to relevant categories."""
    mapping = {
        "acquisition": {"cold-start", "content-growth", "paid-ads", "plg", "b2b-sales"},
        "activation": {"plg", "community", "retention"},
        "retention": {"retention", "community", "gamification"},
        "monetization": {"monetization", "plg", "b2b-sales"},
        "referral": {"viral-referral", "community", "plg"},
    }
    return mapping.get(problem, set())


def problem_to_theories(problem: str) -> Set[str]:
    """Map problem type to relevant theories."""
    mapping = {
        "acquisition": {"growth-hacking", "content-growth", "plg", "network-effects"},
        "activation": {"growth-hacking", "plg", "gamification"},
        "retention": {"gamification", "flywheel", "community-growth"},
        "monetization": {"business-models", "plg"},
        "referral": {"viral-growth", "network-effects", "plg"},
    }
    return mapping.get(problem, set())


def problem_to_process(problem: str) -> str:
    """Map problem type to growth process."""
    mapping = {
        "acquisition": "用户获取",
        "activation": "用户深耕",
        "retention": "用户深耕",
        "monetization": "用户深耕",
        "referral": "用户获取",
    }
    return mapping.get(problem, "增长经营")


def problem_to_journey(problem: str) -> str:
    """Map problem type to journey stage."""
    mapping = {
        "acquisition": "认知/到达",
        "activation": "注册/激活",
        "retention": "留存",
        "monetization": "付费",
        "referral": "分享",
    }
    return mapping.get(problem, "用户旅程待明确")


def category_stage_fit(category: str, stage: str) -> float:
    """Calculate fit between category and stage."""
    stage_fit = {
        "0-1": {"cold-start": 1.0, "content-growth": 0.7, "plg": 0.6, "viral-referral": 0.6, "paid-ads": 0.1, "b2b-sales": 0.5},
        "1-10": {"plg": 1.0, "retention": 0.9, "community": 0.8, "viral-referral": 0.8, "content-growth": 0.7, "b2b-sales": 1.0},
        "10-100": {"paid-ads": 1.0, "brand": 0.9, "b2b-sales": 0.9, "monetization": 0.8, "retention": 0.7},
    }
    return stage_fit.get(stage, {}).get(category, 0.4)


def category_journey_fit(category: str, journey_stage: str) -> float:
    """Calculate fit between category and journey stage."""
    journey_fit = {
        "认知/到达": {"cold-start": 1.0, "content-growth": 0.9, "paid-ads": 0.8, "brand": 0.7, "b2b-sales": 0.95},
        "注册/激活": {"plg": 1.0, "community": 0.6, "retention": 0.6},
        "留存": {"retention": 1.0, "community": 0.8, "plg": 0.7},
        "付费": {"monetization": 1.0, "plg": 0.7, "b2b-sales": 0.8},
        "分享": {"viral-referral": 1.0, "community": 0.7, "plg": 0.6},
    }
    return journey_fit.get(journey_stage, {}).get(category, 0.3)


def resource_fit(effort: str, context: Dict) -> float:
    """Calculate resource fit based on effort and context."""
    budget_text = normalize_text(context.get("budget", ""))
    team_text = normalize_text(context.get("team", ""))
    effort_fit = {"Low": 1.0, "Medium": 0.7, "High": 0.3}.get(effort, 0.6)

    constrained_budget = any(token in budget_text for token in ["小", "有限", "10万", "5万", "无预算", "低预算"])
    constrained_team = any(token in team_text for token in ["1", "2", "单人", "兼职", "最小"])

    if constrained_budget and effort == "High":
        effort_fit -= 0.3
    if constrained_team and effort == "High":
        effort_fit -= 0.3
    if constrained_team and effort == "Medium":
        effort_fit -= 0.1

    return max(0.1, effort_fit)


def resource_profile_fit(resource_profile: str, context: Dict) -> float:
    """Calculate resource profile fit."""
    profile_text = normalize_text(resource_profile)
    if not profile_text:
        return 0.5

    budget_text = normalize_text(context.get("budget", ""))
    team_text = normalize_text(context.get("team", ""))
    business_model_kind = context_business_model_kind(context)
    constrained_budget = any(token in budget_text for token in ["小", "有限", "10万", "5万", "5000", "无预算", "低预算"])
    constrained_team = any(token in team_text for token in ["1", "2", "单人", "兼职", "最小", "小团队"])
    multi_role_team = sum(1 for token in ["产品", "工程", "运营", "销售", "数据", "市场"] if token in team_text) >= 3
    product_engineering_fit = "产品" in team_text and "工程" in team_text and any(
        token in profile_text for token in ["产品", "工程", "实验节奏", "价值快速达成"]
    )
    content_growth_fit = any(token in team_text for token in ["内容", "增长", "市场"]) and any(
        token in profile_text for token in ["内容", "分发", "产能", "传播"]
    )
    sales_fit = "销售" in team_text and "销售" in profile_text
    ops_fit = "运营" in team_text and any(token in profile_text for token in ["运营", "长期维护", "核心用户"])

    fit = 0.5
    if constrained_budget and any(token in profile_text for token in ["低预算", "创始人驱动", "小团队"]):
        fit += 0.35
    if constrained_budget and any(token in profile_text for token in ["预算密集", "中长期投入"]):
        fit -= 0.3
    if constrained_team and any(token in profile_text for token in ["创始人驱动", "小团队"]):
        fit += 0.3
    if constrained_team and any(token in profile_text for token in ["跨团队协同", "长期维护"]):
        fit -= 0.18
    if constrained_team and "工程驱动" in profile_text and not product_engineering_fit:
        fit -= 0.18
    if multi_role_team and "跨团队协同" in profile_text:
        fit += 0.2
    if product_engineering_fit:
        fit += 0.25
    if content_growth_fit:
        fit += 0.25
    if sales_fit:
        fit += 0.25
    if ops_fit:
        fit += 0.2
    if business_model_kind == "b2b-sales-led" and "销售" in profile_text:
        fit += 0.22
    if business_model_kind in {"marketplace", "local-services"} and any(
        token in profile_text for token in ["供给", "需求", "撮合", "单城", "履约", "线下"]
    ):
        fit += 0.22
    if business_model_kind == "ai" and any(token in profile_text for token in ["产品", "工程", "价值快速达成"]):
        fit += 0.12

    return max(0.1, min(1.0, fit))


def metric_category_focus(context: Dict) -> Set[str]:
    """Determine category focus from metric context."""
    text = normalize_text(" ".join([str(context.get("metric", "")), str(context.get("goal", ""))]))
    focus: Set[str] = set()
    if any(token in text for token in ["高意向线索", "线索", "demo", "成单", "成交"]):
        focus.add("b2b-sales")
    if any(token in text for token in ["首次价值", "激活", "试用", "onboarding"]):
        focus.add("plg")
    if any(token in text for token in ["曝光", "内容", "seo", "自然流量", "品牌搜索"]):
        focus.add("content-growth")
    if any(token in text for token in ["分享", "邀请", "传播", "k 因子"]):
        focus.add("viral-referral")
    if any(token in text for token in ["留存", "复购", "回访", "活跃"]):
        focus.add("retention")
    if any(token in text for token in ["付费", "收入", "升级", "订阅", "arpu", "arppu"]):
        focus.add("monetization")
    if any(token in text for token in ["履约", "到店", "订单", "撮合"]):
        focus.update({"cold-start", "community"})
    return focus


def metric_theory_focus(context: Dict) -> Set[str]:
    """Determine theory focus from metric context."""
    category_focus = metric_category_focus(context)
    mapping = {
        "b2b-sales": {"business-models", "plg"},
        "plg": {"plg", "growth-hacking"},
        "content-growth": {"content-growth"},
        "viral-referral": {"viral-growth", "network-effects"},
        "retention": {"flywheel", "community-growth", "gamification"},
        "monetization": {"business-models", "plg"},
        "cold-start": {"network-effects", "growth-hacking"},
        "community": {"community-growth", "flywheel"},
    }
    theories: Set[str] = set()
    for category in category_focus:
        theories.update(mapping.get(category, set()))
    return theories


def guardrail_penalty(guardrail_risk: str, context: Dict) -> float:
    """Calculate guardrail penalty."""
    risk_text = normalize_text(guardrail_risk)
    constraint_text = normalize_text(" ".join([str(context.get("constraints", "")), str(context.get("history", ""))]))
    if not risk_text or not constraint_text:
        return 0.0

    penalty = 0.0
    if any(token in constraint_text for token in ["不能依赖付费投放", "低预算", "预算有限", "cac"]):
        if any(token in risk_text for token in ["cac", "投放", "预算"]):
            penalty += 0.12
    if any(token in constraint_text for token in ["不能伤害核心留存", "假活跃", "留存"]):
        if any(token in risk_text for token in ["留存", "假活跃"]):
            penalty += 0.12
    if any(token in constraint_text for token in ["不能用高补贴", "补贴", "低质量用户"]):
        if any(token in risk_text for token in ["低质量用户", "激励滥用"]):
            penalty += 0.1

    return min(0.24, penalty)


def guardrail_risk(category: str, problem: str) -> str:
    """Get default guardrail risk for category."""
    risk_map = {
        "viral-referral": "可能带来低质量用户和激励滥用",
        "paid-ads": "可能放大未验证转化链路并拉高 CAC",
        "plg": "可能在核心价值未成立时形成空转 onboarding",
        "retention": "可能用假活跃掩盖主价值问题",
        "monetization": "可能短期收入提升但伤害长期留存",
    }
    if category in risk_map:
        return risk_map[category]
    if problem == "acquisition":
        return "需要警惕低质量流量替代真实增长"
    return "需要结合约束线验证副作用"


def case_stage_fit(case: Dict, stage: str) -> float:
    """Calculate case fit with stage."""
    case_stages = set(case.get("stage_fit", []) or case.get("tags", {}).get("stage", []))
    if not stage:
        return 0.4
    if stage in case_stages:
        return 1.0
    return 0.3


def case_journey_fit(case: Dict, journey_stage: str, problem: str) -> float:
    """Calculate case fit with journey stage."""
    if not journey_stage:
        return 0.4
    indexed_journey = case.get("journey_stage", "")
    if indexed_journey == journey_stage:
        return 1.0
    tactics = " ".join(case.get("tags", {}).get("tactics", []))
    summary = f"{case.get('summary', '')} {tactics}"
    summary_text = normalize_text(summary)
    journey_keywords = {
        "认知/到达": ["获客", "拉新", "内容", "投放", "入口", "曝光"],
        "注册/激活": ["激活", "引导", "onboarding", "首次价值", "转化"],
        "留存": ["留存", "复访", "召回", "习惯", "活跃"],
        "付费": ["付费", "定价", "变现", "订阅", "升级"],
        "分享": ["分享", "邀请", "裂变", "推荐", "传播"],
    }
    hits = sum(1 for keyword in journey_keywords.get(journey_stage, []) if keyword in summary_text)
    if hits:
        return min(1.0, 0.5 + hits * 0.15)
    return 0.8 if problem_to_journey(problem) == journey_stage else 0.3
