"""Kelly Sizing Module.

This package provides Kelly criterion resource allocation capabilities
for growth decisions.

Main components:
- types: Enum and dataclass definitions
- calculation: Kelly calculation functions
- readiness: Decision readiness assessment
- core: KellySizing main class
"""

from kelly.types import (
    DecisionReadinessStatus,
    KellySuitability,
    BinaryKellyResult,
    Scenario,
    ScenarioKellyResult,
    FractionalKellyResult,
    DecisionReadinessResult,
    ActionPackage,
    KellyAllocationReport,
)
from kelly.calculation import (
    binary_kelly,
    scenario_kelly,
    fractional_kelly,
)
from kelly.readiness import (
    decision_readiness,
    assess_kelly_suitability,
)
from kelly.core import KellySizing

__all__ = [
    # Enums
    "DecisionReadinessStatus",
    "KellySuitability",
    # Dataclasses
    "BinaryKellyResult",
    "Scenario",
    "ScenarioKellyResult",
    "FractionalKellyResult",
    "DecisionReadinessResult",
    "ActionPackage",
    "KellyAllocationReport",
    # Functions
    "binary_kelly",
    "scenario_kelly",
    "fractional_kelly",
    "decision_readiness",
    "assess_kelly_suitability",
    # Main class
    "KellySizing",
]
