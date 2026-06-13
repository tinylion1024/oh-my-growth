"""Kelly Sizing core module.

This module contains the main KellySizing class that coordinates
Kelly criterion resource allocation operations.
"""

import json
from typing import List, Optional, Dict, Any
from enum import Enum
import numpy as np

from kelly.types import (
    DecisionReadinessStatus,
    KellySuitability,
    BinaryKellyResult,
    ScenarioKellyResult,
    FractionalKellyResult,
    DecisionReadinessResult,
    ActionPackage,
    KellyAllocationReport,
)
from kelly.calculation import (
    binary_kelly as _binary_kelly,
    scenario_kelly as _scenario_kelly,
    fractional_kelly as _fractional_kelly,
)
from kelly.readiness import (
    decision_readiness as _decision_readiness,
    assess_kelly_suitability as _assess_kelly_suitability,
)


# Default total exposure cap
DEFAULT_EXPOSURE_CAP = 0.50

# Conservative exposure caps
EXPOSURE_CAPS = {
    "conservative": 0.30,
    "moderate": 0.50,
    "aggressive": 0.70,
}


class KellySizing:
    """
    Kelly Criterion Resource Allocation Engine.

    Implements Kelly criterion for optimal resource allocation with
    support for binary outcomes, multi-scenario analysis, and
    fractional Kelly adjustments.
    """

    def __init__(self, risk_profile: str = "moderate"):
        """
        Initialize Kelly Sizing engine.

        Args:
            risk_profile: "conservative", "moderate", or "aggressive"
        """
        self.risk_profile = risk_profile
        self.exposure_cap = EXPOSURE_CAPS.get(risk_profile, DEFAULT_EXPOSURE_CAP)

    def binary_kelly(
        self,
        win_prob: float,
        win_amount: float,
        loss_amount: float
    ) -> BinaryKellyResult:
        """Calculate Kelly fraction for binary outcome scenarios."""
        return _binary_kelly(win_prob, win_amount, loss_amount)

    def scenario_kelly(self, scenarios: List[Dict]) -> ScenarioKellyResult:
        """Calculate Kelly fraction for multiple outcome scenarios."""
        return _scenario_kelly(scenarios)

    def fractional_kelly(
        self,
        kelly_fraction: float,
        fraction: float = 0.5
    ) -> FractionalKellyResult:
        """Apply fractional Kelly adjustment."""
        return _fractional_kelly(kelly_fraction, fraction)

    def decision_readiness(self, context: Dict) -> DecisionReadinessResult:
        """Assess decision readiness based on context."""
        return _decision_readiness(context)

    def assess_kelly_suitability(self, context: Dict) -> Dict[str, any]:
        """Assess whether Kelly criterion is suitable for the decision context."""
        return _assess_kelly_suitability(context)

    def apply_exposure_cap(
        self,
        kelly_fraction: float,
        total_current_exposure: float = 0.0
    ) -> float:
        """
        Apply total exposure cap to Kelly fraction.

        Ensures total exposure doesn't exceed the risk profile's cap.
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
        """Generate complete Kelly allocation report."""
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
