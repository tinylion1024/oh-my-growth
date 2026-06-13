"""Kelly Sizing types and data structures.

This module contains all enum types and dataclass definitions for Kelly criterion
resource allocation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


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

    @property
    def full_kelly(self) -> float:
        return self.optimal_fraction


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
