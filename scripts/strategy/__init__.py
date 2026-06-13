"""Strategy Brain Module.

This package provides strategy analysis capabilities for growth decisions.

Main components:
- constants: Strategy configuration and labels
- brain: StrategyBrain main class
- formatter: StrategyFormatter for output formatting
- builder: StrategyBuilder coordinator for build methods
- diagnosis: DiagnosisBuilder for stage and journey diagnosis
- evidence: EvidenceBuilder for evidence chains and confidence
- experiment: ExperimentBuilder for experiment design
- planning: PlanningBuilder for resource allocation and projections
- history: StrategyHistory for experiment history analysis
- scorer: StrategyScorer for priority scoring
- utils: Shared utility functions
"""

from .constants import (
    PROBLEM_LABELS,
    STAGE_LABELS,
    STAGE_FRAMEWORK,
    PROBLEM_TO_PROCESS,
    PROBLEM_TO_JOURNEY,
    CATEGORY_ACTIONS,
    CATEGORY_AVOIDS,
    PROBLEM_TO_METRICS,
)
from .utils import normalize_text
from .formatter import StrategyFormatter
from .builder import StrategyBuilder
from .diagnosis import DiagnosisBuilder
from .evidence import EvidenceBuilder
from .experiment import ExperimentBuilder
from .planning import PlanningBuilder
from .history import StrategyHistory
from .scorer import StrategyScorer

__all__ = [
    "PROBLEM_LABELS",
    "STAGE_LABELS",
    "STAGE_FRAMEWORK",
    "PROBLEM_TO_PROCESS",
    "PROBLEM_TO_JOURNEY",
    "CATEGORY_ACTIONS",
    "CATEGORY_AVOIDS",
    "PROBLEM_TO_METRICS",
    "normalize_text",
    "StrategyFormatter",
    "StrategyBuilder",
    "DiagnosisBuilder",
    "EvidenceBuilder",
    "ExperimentBuilder",
    "PlanningBuilder",
    "StrategyHistory",
    "StrategyScorer",
]
