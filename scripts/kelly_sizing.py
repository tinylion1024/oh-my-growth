#!/usr/bin/env python3
"""
Kelly Sizing Module for Growth Master Skill

Implements Kelly criterion for optimal resource allocation in growth decisions.
Provides binary Kelly, scenario-based Kelly, fractional Kelly, and decision
readiness assessment.

Reference: references/kelly-allocation.md

Usage:
    from kelly_sizing import KellySizing

    ks = KellySizing()

    # Binary Kelly
    result = ks.binary_kelly(win_prob=0.60, win_amount=100, loss_amount=30)
    print(result.full_kelly)  # 0.48
    print(result.half_kelly)  # 0.24

    # Scenario Kelly
    scenarios = [
        {"outcome": "success", "return": 2.0, "probability": 0.20},
        {"outcome": "partial", "return": 0.5, "probability": 0.30},
        {"outcome": "neutral", "return": 0.0, "probability": 0.30},
        {"outcome": "loss", "return": -0.5, "probability": 0.20},
    ]
    result = ks.scenario_kelly(scenarios)

    # Decision readiness
    readiness = ks.decision_readiness(context)
    print(readiness.score)  # 75
    print(readiness.status)  # "ready"
"""

import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal
from enum import Enum
from datetime import datetime
from scipy.optimize import minimize_scalar
import numpy as np


class DecisionReadinessStatus(Enum):
    """Decision readiness status based on score"""
    READY = "ready"                     # >= 70
    NEED_MORE_INFO = "need_more_info"   # 50-69
    NOT_SUITABLE = "not_suitable"       # < 50


class KellySuitability(Enum):
    """Kelly applicability assessment"""
    SUITABLE = "suitable"
    CAUTION = "caution"
    NOT_SUITABLE = "not_suitable"


@dataclass
class BinaryKellyResult:
    """Result of binary Kelly calculation"""
    full_kelly: float
    half_kelly: float
    quarter_kelly: float
    eighth_kelly: float
    net_odds: float
    win_probability: float
    loss_probability: float
    edge: float  # Expected advantage (bp - q)
    expected_value: float

    def get_recommended(self, uncertainty_level: str = "normal") -> tuple[float, str]:
        """
        Get recommended Kelly fraction based on uncertainty level.

        Args:
            uncertainty_level: "low", "normal", "high", "very_high"

        Returns:
            Tuple of (fraction, description)
        """
        recommendations = {
            "low": (self.half_kelly, "1/2 Kelly - 正常推荐"),
            "normal": (self.half_kelly, "1/2 Kelly - 推荐默认"),
            "high": (self.quarter_kelly, "1/4 Kelly - 高不确定性"),
            "very_high": (self.eighth_kelly, "1/8 Kelly - 极高不确定性"),
        }
        return recommendations.get(uncertainty_level, recommendations["normal"])


@dataclass
class Scenario:
    """Single scenario for multi-scenario Kelly"""
    outcome: str
    return_rate: float  # Return rate (e.g., 2.0 = 200% gain, -0.5 = 50% loss)
    probability: float
    description: str = ""


@dataclass
class ScenarioKellyResult:
    """Result of scenario-based Kelly calculation"""
    optimal_fraction: float
    half_kelly: float
    quarter_kelly: float
    expected_log_growth: float
    scenarios: List[Scenario]
    optimization_method: str = "numerical"

    def get_recommended(self, uncertainty_level: str = "normal") -> tuple[float, str]:
        """Get recommended Kelly fraction based on uncertainty level"""
        recommendations = {
            "low": (self.half_kelly, "1/2 Kelly - 正常推荐"),
            "normal": (self.half_kelly, "1/2 Kelly - 推荐默认"),
            "high": (self.quarter_kelly, "1/4 Kelly - 高不确定性"),
            "very_high": (self.eighth_kelly, "1/8 Kelly - 极高不确定性"),
        }
        return recommendations.get(uncertainty_level, recommendations["normal"])

    @property
    def eighth_kelly(self) -> float:
        return self.optimal_fraction * 0.125


@dataclass
class FractionalKellyResult:
    """Result of fractional Kelly calculation"""
    original_kelly: float
    fraction: float
    adjusted_kelly: float
    growth_efficiency: float  # % of theoretical growth rate
    risk_reduction: float     # % risk reduction vs full Kelly


@dataclass
class DecisionReadinessResult:
    """Decision readiness assessment result"""
    score: int  # 0-100
    status: DecisionReadinessStatus
    dimensions: Dict[str, int]  # Individual dimension scores
    gaps: List[str]  # Missing information
    recommendations: List[str]

    @property
    def is_ready(self) -> bool:
        return self.status == DecisionReadinessStatus.READY


@dataclass
class ActionPackage:
    """Minimum actionable package derived from Kelly calculation"""
    action: str
    owner: str
    allocation: float  # Amount to allocate
    allocation_ratio: float  # Percentage of risk budget
    metrics: List[str]
    review_window: str
    add_conditions: List[str]
    stop_conditions: List[str]
    review_triggers: List[str]


@dataclass
class KellyAllocationReport:
    """Complete Kelly allocation report"""
    executive_summary: Dict
    suitability_assessment: Dict
    resource_snapshot: Dict
    kelly_calculation: Dict
    action_packages: List[ActionPackage]
    conditions: Dict
    assumptions: List[Dict]
    readiness: DecisionReadinessResult
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class KellySizing:
    """
    Kelly Criterion Resource Allocation Engine.

    Implements Kelly criterion for optimal resource allocation with
    support for binary outcomes, multi-scenario analysis, and
    fractional Kelly adjustments.
    """

    # Decision readiness dimension weights
    READINESS_WEIGHTS = {
        "resource_clarity": 0.20,       # 资源池是否明确
        "probability_estimate": 0.25,   # 概率估计是否合理
        "payoff_clarity": 0.20,         # 收益结构是否清晰
        "downside_bound": 0.15,         # 下限风险是否可控
        "repeatability": 0.10,          # 是否可重复
        "feedback_mechanism": 0.10,     # 是否有反馈机制
    }

    # Default total exposure cap
    DEFAULT_EXPOSURE_CAP = 0.50

    # Conservative exposure caps
    EXPOSURE_CAPS = {
        "conservative": 0.30,
        "moderate": 0.50,
        "aggressive": 0.70,
    }

    def __init__(self, risk_profile: str = "moderate"):
        """
        Initialize Kelly Sizing engine.

        Args:
            risk_profile: "conservative", "moderate", or "aggressive"
        """
        self.risk_profile = risk_profile
        self.exposure_cap = self.EXPOSURE_CAPS.get(risk_profile, self.DEFAULT_EXPOSURE_CAP)

    def binary_kelly(
        self,
        win_prob: float,
        win_amount: float,
        loss_amount: float
    ) -> BinaryKellyResult:
        """
        Calculate Kelly fraction for binary outcome scenarios.

        Uses the classic Kelly formula: f* = (bp - q) / b
        where b = net odds, p = win probability, q = loss probability.

        Args:
            win_prob: Probability of winning (0.0 - 1.0)
            win_amount: Amount gained on win
            loss_amount: Amount lost on loss

        Returns:
            BinaryKellyResult with full and fractional Kelly values

        Example:
            >>> ks = KellySizing()
            >>> result = ks.binary_kelly(0.60, 100, 30)
            >>> result.full_kelly  # ~0.48
        """
        # Validate inputs
        win_prob = max(0.0, min(1.0, win_prob))
        loss_amount = abs(loss_amount)  # Ensure positive

        # Calculate net odds (b)
        net_odds = win_amount / loss_amount if loss_amount > 0 else float('inf')

        # Loss probability (q)
        loss_prob = 1.0 - win_prob

        # Kelly formula: f* = (bp - q) / b
        if net_odds == float('inf'):
            # Infinite odds (no loss possible)
            full_kelly = 1.0
        else:
            # Standard Kelly calculation
            edge = (net_odds * win_prob) - loss_prob
            full_kelly = edge / net_odds if net_odds > 0 else 0.0

        # Ensure non-negative (no bet if edge is negative)
        full_kelly = max(0.0, full_kelly)

        # Calculate fractional Kelly values
        half_kelly = full_kelly * 0.5
        quarter_kelly = full_kelly * 0.25
        eighth_kelly = full_kelly * 0.125

        # Calculate edge and expected value
        edge = (net_odds * win_prob) - loss_prob
        expected_value = (win_prob * win_amount) - (loss_prob * loss_amount)

        return BinaryKellyResult(
            full_kelly=full_kelly,
            half_kelly=half_kelly,
            quarter_kelly=quarter_kelly,
            eighth_kelly=eighth_kelly,
            net_odds=net_odds,
            win_probability=win_prob,
            loss_probability=loss_prob,
            edge=edge,
            expected_value=expected_value
        )

    def scenario_kelly(
        self,
        scenarios: List[Dict]
    ) -> ScenarioKellyResult:
        """
        Calculate Kelly fraction for multiple outcome scenarios.

        Uses numerical optimization to maximize E[log(1 + f * r)]
        where r is the return rate for each scenario.

        Args:
            scenarios: List of scenario dicts with keys:
                - outcome: str (scenario name)
                - return_rate: float (e.g., 2.0 = 200% gain, -0.5 = 50% loss)
                - probability: float (0.0 - 1.0)
                - description: str (optional)

        Returns:
            ScenarioKellyResult with optimal fraction

        Example:
            >>> scenarios = [
            ...     {"outcome": "success", "return_rate": 2.0, "probability": 0.20},
            ...     {"outcome": "partial", "return_rate": 0.5, "probability": 0.30},
            ...     {"outcome": "neutral", "return_rate": 0.0, "probability": 0.30},
            ...     {"outcome": "loss", "return_rate": -0.5, "probability": 0.20},
            ... ]
            >>> result = ks.scenario_kelly(scenarios)
        """
        # Convert to Scenario objects
        scenario_objs = []
        for s in scenarios:
            scenario_objs.append(Scenario(
                outcome=s.get("outcome", "unknown"),
                return_rate=s.get("return_rate", s.get("return", 0.0)),
                probability=s.get("probability", 0.0),
                description=s.get("description", "")
            ))

        # Normalize probabilities
        total_prob = sum(s.probability for s in scenario_objs)
        if total_prob > 0:
            for s in scenario_objs:
                s.probability /= total_prob

        def expected_log_growth(f: float) -> float:
            """Calculate expected log growth for given fraction f."""
            result = 0.0
            for scenario in scenario_objs:
                # Growth factor: 1 + f * return_rate
                growth_factor = 1.0 + f * scenario.return_rate
                # Avoid log of negative or zero
                if growth_factor <= 0:
                    return float('inf')  # Penalize bankruptcy
                result -= scenario.probability * np.log(growth_factor)
            return result

        # Optimize using scipy
        # Search in [0, 1] range (can extend if needed)
        result = minimize_scalar(
            expected_log_growth,
            bounds=(0.0, 2.0),
            method='bounded'
        )

        optimal_fraction = result.x

        # Check if optimization converged and result is valid
        if not result.success or optimal_fraction < 0:
            optimal_fraction = 0.0

        # Calculate expected log growth at optimal
        expected_log = -result.fun if result.success else 0.0

        return ScenarioKellyResult(
            optimal_fraction=optimal_fraction,
            half_kelly=optimal_fraction * 0.5,
            quarter_kelly=optimal_fraction * 0.25,
            expected_log_growth=expected_log,
            scenarios=scenario_objs,
            optimization_method="numerical"
        )

    def fractional_kelly(
        self,
        kelly_fraction: float,
        fraction: float = 0.5
    ) -> FractionalKellyResult:
        """
        Apply fractional Kelly adjustment.

        Fractional Kelly reduces position size to lower volatility
        while maintaining most of the growth rate.

        Args:
            kelly_fraction: Original Kelly fraction (full Kelly)
            fraction: Fraction to apply (0.5 = half Kelly)

        Returns:
            FractionalKellyResult with adjusted values

        Example:
            >>> result = ks.fractional_kelly(0.40, 0.5)
            >>> result.adjusted_kelly  # 0.20
            >>> result.growth_efficiency  # ~0.75 (75% of growth)
        """
        adjusted_kelly = kelly_fraction * fraction

        # Growth efficiency: approximate as fraction for small adjustments
        # More precisely: (1 - (1-f)^2) / (1 + (1-f)^2) for log-normal
        # Simplified approximation
        growth_efficiency = fraction * (2 - fraction)  # ~75% for half Kelly

        # Risk reduction: variance scales as fraction^2
        risk_reduction = 1.0 - (fraction ** 2)

        return FractionalKellyResult(
            original_kelly=kelly_fraction,
            fraction=fraction,
            adjusted_kelly=adjusted_kelly,
            growth_efficiency=growth_efficiency,
            risk_reduction=risk_reduction
        )

    def decision_readiness(
        self,
        context: Dict
    ) -> DecisionReadinessResult:
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

        Example:
            >>> context = {
            ...     "resource_pool": 1000000,
            ...     "resource_clarity": "clear",
            ...     "probability_source": "data",
            ...     "payoff_clarity": "clear",
            ...     "downside_bound": "bounded",
            ...     "repeatability": "repeatable",
            ...     "feedback_mechanism": "yes"
            ... }
            >>> result = ks.decision_readiness(context)
            >>> result.score  # 95
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
            weight = self.READINESS_WEIGHTS.get(dim, 0)
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

    def assess_kelly_suitability(
        self,
        context: Dict
    ) -> Dict[str, any]:
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

    def apply_exposure_cap(
        self,
        kelly_fraction: float,
        total_current_exposure: float = 0.0
    ) -> float:
        """
        Apply total exposure cap to Kelly fraction.

        Ensures total exposure doesn't exceed the risk profile's cap.

        Args:
            kelly_fraction: Calculated Kelly fraction
            total_current_exposure: Current total exposure across all opportunities

        Returns:
            Adjusted Kelly fraction respecting exposure cap
        """
        remaining_capacity = self.exposure_cap - total_current_exposure
        return min(kelly_fraction, max(0, remaining_capacity))

    def correlation_adjustment(
        self,
        kelly_fractions: List[float],
        correlations: List[List[float]]
    ) -> List[float]:
        """
        Adjust Kelly fractions for correlations between opportunities.

        For highly correlated opportunities, reduce combined exposure.
        For independent opportunities, can sum fractions (with cap).

        Args:
            kelly_fractions: List of Kelly fractions for each opportunity
            correlations: Correlation matrix (n x n)

        Returns:
            Adjusted Kelly fractions
        """
        n = len(kelly_fractions)
        if n == 0:
            return []

        if n == 1:
            return kelly_fractions

        # Simple adjustment: reduce based on average correlation
        adjusted = []
        for i, f in enumerate(kelly_fractions):
            # Average correlation with other opportunities
            avg_corr = np.mean([correlations[i][j] for j in range(n) if j != i])

            # Apply haircut: reduce by correlation
            adjustment = 1.0 - abs(avg_corr) * 0.5
            adjusted.append(f * adjustment)

        return adjusted

    def create_action_package(
        self,
        kelly_fraction: float,
        resource_pool: float,
        opportunity_name: str,
        metrics: List[str],
        add_conditions: List[str],
        stop_conditions: List[str]
    ) -> ActionPackage:
        """
        Create a minimum actionable package from Kelly calculation.

        Converts Kelly fraction into concrete action with allocation,
        conditions, and review triggers.

        Args:
            kelly_fraction: Kelly allocation fraction
            resource_pool: Total available resource pool
            opportunity_name: Name of the opportunity
            metrics: Key metrics to track
            add_conditions: Conditions for increasing allocation
            stop_conditions: Conditions for stopping/exit

        Returns:
            ActionPackage with concrete allocation and conditions
        """
        allocation = kelly_fraction * resource_pool

        return ActionPackage(
            action=f"启动 {opportunity_name}",
            owner="待指定",
            allocation=allocation,
            allocation_ratio=kelly_fraction,
            metrics=metrics,
            review_window="30天",
            add_conditions=add_conditions,
            stop_conditions=stop_conditions,
            review_triggers=[
                "达到复盘周期",
                "触发止损条件",
                "触发加仓条件"
            ]
        )

    def generate_full_report(
        self,
        opportunity_name: str,
        kelly_result: BinaryKellyResult | ScenarioKellyResult,
        context: Dict,
        action_package: ActionPackage
    ) -> KellyAllocationReport:
        """
        Generate complete Kelly allocation report.

        Args:
            opportunity_name: Name of the opportunity
            kelly_result: Kelly calculation result
            context: Decision context
            action_package: Action package derived from Kelly

        Returns:
            KellyAllocationReport with all required sections
        """
        # Suitability assessment
        suitability = self.assess_kelly_suitability(context)

        # Readiness assessment
        readiness = self.decision_readiness(context)

        # Get recommended Kelly
        uncertainty = context.get("uncertainty_level", "normal")
        if isinstance(kelly_result, BinaryKellyResult):
            recommended, recommendation_desc = kelly_result.get_recommended(uncertainty)
        else:
            recommended, recommendation_desc = kelly_result.get_recommended(uncertainty)

        return KellyAllocationReport(
            executive_summary={
                "opportunity": opportunity_name,
                "recommended_action": action_package.action,
                "allocation": action_package.allocation,
                "allocation_ratio": f"{action_package.allocation_ratio:.1%}",
                "recommendation": recommendation_desc,
            },
            suitability_assessment=suitability,
            resource_snapshot={
                "total_pool": context.get("resource_pool", 0),
                "protected_reserve": context.get("protected_reserve", 0),
                "risk_budget": context.get("risk_budget", 0),
                "allocated": action_package.allocation,
            },
            kelly_calculation={
                "method": "binary" if isinstance(kelly_result, BinaryKellyResult) else "scenario",
                "full_kelly": kelly_result.full_kelly if isinstance(kelly_result, BinaryKellyResult) else kelly_result.optimal_fraction,
                "half_kelly": kelly_result.half_kelly,
                "quarter_kelly": kelly_result.quarter_kelly,
                "recommended": recommended,
            },
            action_packages=[action_package],
            conditions={
                "add_conditions": action_package.add_conditions,
                "stop_conditions": action_package.stop_conditions,
                "review_triggers": action_package.review_triggers,
            },
            assumptions=[
                {"assumption": a, "source": context.get("assumption_sources", {}).get(a, "unknown")}
                for a in context.get("assumptions", [])
            ],
            readiness=readiness,
        )

    def to_dict(self, obj: any) -> Dict:
        """Convert result object to dictionary for JSON serialization."""
        if obj is None:
            return None
        if hasattr(obj, 'value') and isinstance(obj, Enum):  # Enum
            return obj.value
        if hasattr(obj, '__dataclass_fields__'):  # Dataclass
            result = {}
            for k, v in obj.__dict__.items():
                result[k] = self.to_dict(v)
            return result
        if isinstance(obj, list):
            return [self.to_dict(item) for item in obj]
        if isinstance(obj, dict):
            return {k: self.to_dict(v) for k, v in obj.items()}
        if isinstance(obj, (int, float, str, bool)):
            return obj
        return str(obj)

    def to_json(self, obj: any) -> str:
        """Convert result object to JSON string."""
        return json.dumps(self.to_dict(obj), ensure_ascii=False, indent=2, default=str)


def main():
    """Demo: Kelly Sizing for growth experiment"""

    print("=" * 60)
    print("Kelly 资源分配示例：邀请裂变实验")
    print("=" * 60)

    # Initialize
    ks = KellySizing(risk_profile="moderate")

    # Example 1: Binary Kelly
    print("\n📊 场景 1: 二元机会")
    print("-" * 40)

    result = ks.binary_kelly(
        win_prob=0.60,
        win_amount=100,
        loss_amount=30
    )

    print(f"成功概率: {result.win_probability:.0%}")
    print(f"净赔率: {result.net_odds:.2f}")
    print(f"边缘: {result.edge:.2f}")
    print(f"Full Kelly: {result.full_kelly:.1%}")
    print(f"Half Kelly: {result.half_kelly:.1%}")
    print(f"Quarter Kelly: {result.quarter_kelly:.1%}")

    recommended, desc = result.get_recommended("normal")
    print(f"\n推荐: {recommended:.1%} ({desc})")

    # Example 2: Scenario Kelly
    print("\n📊 场景 2: 多场景机会")
    print("-" * 40)

    scenarios = [
        {"outcome": "大成功", "return_rate": 2.0, "probability": 0.20},
        {"outcome": "小成功", "return_rate": 0.5, "probability": 0.30},
        {"outcome": "持平", "return_rate": 0.0, "probability": 0.30},
        {"outcome": "失败", "return_rate": -0.5, "probability": 0.20},
    ]

    scenario_result = ks.scenario_kelly(scenarios)

    print(f"最优比例: {scenario_result.optimal_fraction:.1%}")
    print(f"Half Kelly: {scenario_result.half_kelly:.1%}")
    print(f"Quarter Kelly: {scenario_result.quarter_kelly:.1%}")
    print(f"期望对数增长: {scenario_result.expected_log_growth:.4f}")

    # Example 3: Fractional Kelly
    print("\n📊 场景 3: 分数 Kelly")
    print("-" * 40)

    frac_result = ks.fractional_kelly(0.40, fraction=0.5)

    print(f"原始 Kelly: {frac_result.original_kelly:.1%}")
    print(f"分数: {frac_result.fraction:.1%}")
    print(f"调整后: {frac_result.adjusted_kelly:.1%}")
    print(f"增长效率: {frac_result.growth_efficiency:.1%}")
    print(f"风险降低: {frac_result.risk_reduction:.1%}")

    # Example 4: Decision Readiness
    print("\n📊 场景 4: 决策准备度")
    print("-" * 40)

    context = {
        "resource_pool": 1000000,
        "resource_clarity": "clear",
        "probability_source": "expert",
        "payoff_clarity": "partial",
        "downside_bound": "bounded",
        "repeatability": "repeatable",
        "feedback_mechanism": "yes",
    }

    readiness = ks.decision_readiness(context)

    print(f"总分: {readiness.score}")
    print(f"状态: {readiness.status.value}")
    print(f"\n维度得分:")
    for dim, score in readiness.dimensions.items():
        print(f"  - {dim}: {score}")

    if readiness.gaps:
        print(f"\n信息缺口:")
        for gap in readiness.gaps:
            print(f"  - {gap}")

    if readiness.recommendations:
        print(f"\n建议:")
        for rec in readiness.recommendations:
            print(f"  - {rec}")

    # Example 5: Full Report
    print("\n" + "=" * 60)
    print("完整 Kelly 分配报告")
    print("=" * 60)

    full_context = {
        "resource_pool": 800000,  # 80万风险预算
        "protected_reserve": 200000,
        "risk_budget": 800000,
        "resource_clarity": "clear",
        "probability_source": "expert",
        "payoff_clarity": "partial",
        "downside_bound": "bounded",
        "repeatability": "repeatable",
        "feedback_mechanism": "yes",
        "uncertainty_level": "normal",
        "assumptions": ["用户有足够动机邀请", "激励成本可控"],
        "assumption_sources": {
            "用户有足够动机邀请": "assumed",
            "激励成本可控": "estimated"
        }
    }

    action_pkg = ks.create_action_package(
        kelly_fraction=result.half_kelly,
        resource_pool=800000,
        opportunity_name="邀请裂变 MVP",
        metrics=["病毒系数", "CAC", "新用户留存率"],
        add_conditions=["病毒系数 > 0.5 且 CAC < 50元"],
        stop_conditions=["病毒系数 < 0.3 或 CAC > 80元"]
    )

    report = ks.generate_full_report(
        opportunity_name="邀请裂变实验",
        kelly_result=result,
        context=full_context,
        action_package=action_pkg
    )

    print(ks.to_json(report))


if __name__ == "__main__":
    main()
