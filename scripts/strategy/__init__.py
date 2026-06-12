"""Strategy Brain Module.

This package provides strategy analysis capabilities for growth decisions.

Main components:
- constants: Strategy configuration and labels
- brain: StrategyBrain main class
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

__all__ = [
    "PROBLEM_LABELS",
    "STAGE_LABELS",
    "STAGE_FRAMEWORK",
    "PROBLEM_TO_PROCESS",
    "PROBLEM_TO_JOURNEY",
    "CATEGORY_ACTIONS",
    "CATEGORY_AVOIDS",
    "PROBLEM_TO_METRICS",
]
