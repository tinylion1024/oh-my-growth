"""Decision readiness assessment methods.

This module contains methods for assessing decision readiness and
Kelly criterion suitability.
"""

from typing import Dict, List

from .types import (
    DecisionReadinessStatus,
    DecisionReadinessResult,
    KellySuitability,
)


# Decision readiness dimension weights
READINESS_WEIGHTS = {
    "resource_clarity": 0.20,       # 资源池是否明确
    "probability_estimate": 0.25,   # 概率估计是否合理
    "payoff_clarity": 0.20,         # 收益结构是否清晰
    "downside_bound": 0.15,         # 下限风险是否可控
    "repeatability": 0.10,          # 是否可重复
    "feedback_mechanism": 0.10,     # 是否有反馈机制
}


def decision_readiness(context: Dict) -> DecisionReadinessResult:
    """
    Assess decision readiness based on context.

    Evaluates six dimensions of readiness:
    1. Resource clarity (20%)
    2. Probability estimate quality (25%)
    3. Payoff clarity (20%)
    4. Downside bound control (15%)
    5. Repeatability (10%)
    6. Feedback mechanism (10%)

    Args:
        context: Dict with keys:
            - resource_pool: float (total available resources)
            - resource_clarity: str ("clear", "partial", "unclear")
            - probability_source: str ("data", "expert", "guess", "unknown")
            - payoff_clarity: str ("clear", "partial", "unclear")
            - downside_bound: str ("bounded", "partial", "unbounded")
            - repeatability: str ("repeatable", "partial", "one_time")
            - feedback_mechanism: str ("yes", "partial", "no")

    Returns:
        DecisionReadinessResult with score and recommendations
    """
    dimension_scores = {}
    gaps = []
    recommendations = []

    # 1. Resource clarity (20%)
    resource_clarity = context.get("resource_clarity", "unclear")
    resource_scores = {"clear": 100, "partial": 60, "unclear": 20}
    dimension_scores["resource_clarity"] = resource_scores.get(resource_clarity, 20)
    if resource_clarity != "clear":
        gaps.append("资源池总量或分配规则不明确")
        recommendations.append("明确可用资源总量和保护储备")

    # 2. Probability estimate quality (25%)
    prob_source = context.get("probability_source", "unknown")
    prob_scores = {"data": 100, "expert": 70, "guess": 40, "unknown": 10}
    dimension_scores["probability_estimate"] = prob_scores.get(prob_source, 10)
    if prob_source in ["guess", "unknown"]:
        gaps.append("成功概率估计依据不足")
        recommendations.append("收集更多数据或专家意见来估计概率")

    # 3. Payoff clarity (20%)
    payoff_clarity = context.get("payoff_clarity", "unclear")
    payoff_scores = {"clear": 100, "partial": 60, "unclear": 20}
    dimension_scores["payoff_clarity"] = payoff_scores.get(payoff_clarity, 20)
    if payoff_clarity != "clear":
        gaps.append("收益结构不够清晰")
        recommendations.append("量化成功和失败场景的具体收益/损失")

    # 4. Downside bound control (15%)
    downside = context.get("downside_bound", "unbounded")
    downside_scores = {"bounded": 100, "partial": 50, "unbounded": 0}
    dimension_scores["downside_bound"] = downside_scores.get(downside, 0)
    if downside == "unbounded":
        gaps.append("下限风险不可控")
        recommendations.append("设定止损机制或保护措施")

    # 5. Repeatability (10%)
    repeatability = context.get("repeatability", "one_time")
    repeat_scores = {"repeatable": 100, "partial": 50, "one_time": 20}
    dimension_scores["repeatability"] = repeat_scores.get(repeatability, 20)
    if repeatability == "one_time":
        gaps.append("一次性决策，Kelly 适用性受限")
        recommendations.append("考虑使用决策树分析替代 Kelly")

    # 6. Feedback mechanism (10%)
    feedback = context.get("feedback_mechanism", "no")
    feedback_scores = {"yes": 100, "partial": 50, "no": 0}
    dimension_scores["feedback_mechanism"] = feedback_scores.get(feedback, 0)
    if feedback != "yes":
        gaps.append("缺乏反馈机制")
        recommendations.append("设计指标追踪和复盘机制")

    # Calculate weighted total score
    total_score = 0
    for dim, score in dimension_scores.items():
        weight = READINESS_WEIGHTS.get(dim, 0)
        total_score += score * weight

    total_score = int(total_score)

    # Determine status
    if total_score >= 70:
        status = DecisionReadinessStatus.READY
    elif total_score >= 50:
        status = DecisionReadinessStatus.NEED_MORE_INFO
    else:
        status = DecisionReadinessStatus.NOT_SUITABLE

    return DecisionReadinessResult(
        score=total_score,
        status=status,
        dimensions=dimension_scores,
        gaps=gaps,
        recommendations=recommendations
    )


def assess_kelly_suitability(context: Dict) -> Dict[str, any]:
    """
    Assess whether Kelly criterion is suitable for the decision context.

    Args:
        context: Decision context dict

    Returns:
        Dict with suitability status and reasoning
    """
    reasons_suitable = []
    reasons_unsuitable = []
    warnings = []

    # Check repeatability
    if context.get("repeatability") == "one_time":
        reasons_unsuitable.append("一次性、不可逆决策，Kelly 不适用")

    # Check downside
    if context.get("downside_bound") == "unbounded":
        reasons_unsuitable.append("无下限风险，必须先设定止损")

    # Check probability knowledge
    if context.get("probability_source") == "unknown":
        warnings.append("概率完全未知，建议先小规模实验")

    # Check for guaranteed return claims
    if context.get("guaranteed_return"):
        reasons_unsuitable.append("声称保证收益，可能存在风险")

    # Determine overall suitability
    if reasons_unsuitable:
        suitability = KellySuitability.NOT_SUITABLE
    elif warnings:
        suitability = KellySuitability.CAUTION
    else:
        suitability = KellySuitability.SUITABLE

    return {
        "suitability": suitability.value,
        "reasons_suitable": reasons_suitable,
        "reasons_unsuitable": reasons_unsuitable,
        "warnings": warnings,
        "alternative": "决策树分析" if suitability != KellySuitability.SUITABLE else None
    }
