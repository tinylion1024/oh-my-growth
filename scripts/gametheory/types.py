"""Game Theory types and data structures.

This module contains all enum types and dataclass definitions for game theory analysis.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal, Tuple, Any
from enum import Enum
from datetime import datetime


class GameType(Enum):
    """Types of game scenarios"""
    PRISONER_DILEMMA = "prisoner_dilemma"
    COURNOT_COMPETITION = "cournot_competition"
    SIGNALING_GAME = "signaling_game"
    COMMITMENT_GAME = "commitment_game"
    BARGAINING_GAME = "bargaining_game"
    TWO_SIDED_MARKET = "two_sided_market"
    CUSTOM = "custom"


class TimingType(Enum):
    """Game timing structure"""
    SIMULTANEOUS = "simultaneous"  # Players move at the same time
    SEQUENTIAL = "sequential"      # Players move in order


class InformationType(Enum):
    """Information structure"""
    COMPLETE = "complete"      # All players know all payoffs
    INCOMPLETE = "incomplete"  # Some information is private


class EquilibriumType(Enum):
    """Types of equilibrium"""
    NASH = "nash"
    SUBGAME_PERFECT = "subgame_perfect"
    BAYESIAN = "bayesian"
    MIXED_STRATEGY = "mixed_strategy"


class ConfidenceLevel(Enum):
    """Confidence levels for predictions"""
    HIGH = "high"        # >= 0.75
    MEDIUM = "medium"    # 0.50 - 0.74
    LOW = "low"          # < 0.50


class CommitmentCredibility(Enum):
    """Commitment credibility levels"""
    HIGH = "high"        # >= 75
    MEDIUM = "medium"    # 50 - 74
    LOW = "low"          # < 50


@dataclass
class Player:
    """Game participant"""
    name: str
    player_type: str = "competitor"  # competitor, customer, supplier, regulator
    objectives: List[str] = field(default_factory=list)
    historical_behavior: Dict[str, Any] = field(default_factory=dict)
    rationality_score: float = 0.8  # 0-1, how rational the player typically behaves


@dataclass
class Strategy:
    """A strategy option for a player"""
    name: str
    description: str = ""
    cost: float = 0.0
    is_commitment: bool = False
    commitment_type: str = ""  # burning_bridge, reputation, contract, investment


@dataclass
class PayoffCell:
    """A cell in the payoff matrix"""
    strategy_combo: Tuple[str, ...]  # Strategy selected by each player
    payoffs: Dict[str, float]        # Payoff for each player
    payoff_type: Dict[str, str] = field(default_factory=dict)  # observed, estimated, assumed
    notes: str = ""


@dataclass
class EquilibriumResult:
    """Result of equilibrium analysis"""
    equilibrium_type: str
    strategy_profile: Tuple[str, ...]
    payoffs: Dict[str, float]
    is_pareto_optimal: bool = False
    is_unique: bool = True
    reasoning: str = ""
    stability_score: float = 0.8  # How stable this equilibrium is


@dataclass
class HistoricalCalibration:
    """Historical behavior calibration data"""
    player_name: str
    behavior_type: str
    historical_frequency: float
    last_observed: str
    consistency_score: float
    reference_class: str
    prediction_confidence: float


@dataclass
class CommitmentCheck:
    """Commitment credibility check result"""
    player_name: str
    commitment_type: str
    irreversibility_score: float    # 0-25
    observability_score: float      # 0-20
    cost_score: float               # 0-25
    consistency_score: float        # 0-15
    incentive_score: float          # 0-15
    total_score: float              # 0-100
    credibility_level: str
    analysis: str = ""


@dataclass
class SignalCheck:
    """Signal quality check result"""
    player_name: str
    signal_type: str  # separating, pooling, semi_separating
    cost_to_mimic: float
    observability: float
    consistency: float
    verifiability: float
    signal_quality: str  # high, medium, low
    analysis: str = ""


@dataclass
class GameReport:
    """Complete game theory analysis report"""
    game_type: str
    players: List[str]
    strategies: Dict[str, List[str]]
    payoff_matrix: Dict[Tuple[str, ...], Dict[str, float]]
    equilibrium: Optional[EquilibriumResult]
    historical_calibration: List[HistoricalCalibration]
    commitment_checks: List[CommitmentCheck]
    signal_checks: List[SignalCheck]
    strategic_recommendation: str
    confidence_level: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
