"""Game Theory Analysis Module.

This package provides game theory analysis capabilities for strategic decision making.

Main components:
- types: Enum and dataclass definitions
- equilibrium: Nash equilibrium calculation
- calibration: Historical calibration, commitment, and signal analysis
- core: GameTheoryAnalysis main class
"""

from gametheory.types import (
    GameType,
    TimingType,
    InformationType,
    EquilibriumType,
    ConfidenceLevel,
    CommitmentCredibility,
    Player,
    Strategy,
    PayoffCell,
    EquilibriumResult,
    HistoricalCalibration,
    CommitmentCheck,
    SignalCheck,
    GameReport,
)
from gametheory.equilibrium import (
    find_nash_equilibrium,
    find_dominated_strategies,
)
from gametheory.calibration import (
    calibrate_with_history,
    check_commitment_credibility,
    check_signal_quality,
)
from gametheory.core import GameTheoryAnalysis

__all__ = [
    # Enums
    "GameType",
    "TimingType",
    "InformationType",
    "EquilibriumType",
    "ConfidenceLevel",
    "CommitmentCredibility",
    # Dataclasses
    "Player",
    "Strategy",
    "PayoffCell",
    "EquilibriumResult",
    "HistoricalCalibration",
    "CommitmentCheck",
    "SignalCheck",
    "GameReport",
    # Functions
    "find_nash_equilibrium",
    "find_dominated_strategies",
    "calibrate_with_history",
    "check_commitment_credibility",
    "check_signal_quality",
    # Main class
    "GameTheoryAnalysis",
]
