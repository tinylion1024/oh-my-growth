"""Game Theory Analysis core module.

This module contains the main GameTheoryAnalysis class that coordinates
game theory analysis operations.
"""

import json
from typing import List, Optional, Dict, Tuple, Any

from .types import (
    GameType,
    TimingType,
    InformationType,
    Player,
    Strategy,
    PayoffCell,
    EquilibriumResult,
    HistoricalCalibration,
    CommitmentCheck,
    SignalCheck,
    GameReport,
)
from .equilibrium import (
    find_nash_equilibrium,
    find_dominated_strategies,
)
from .calibration import (
    calibrate_with_history,
    get_predicted_behavior,
    check_commitment_credibility,
    check_signal_quality,
    generate_recommendation,
    determine_confidence_level,
)


class GameTheoryAnalysis:
    """
    Game Theory Analysis Engine for Strategic Decision Making.

    Provides comprehensive game theory analysis including:
    - Nash equilibrium calculation
    - Payoff matrix construction
    - Historical behavior calibration
    - Commitment credibility assessment
    - Signal quality analysis
    """

    def __init__(self, game_type: GameType = GameType.CUSTOM):
        """
        Initialize Game Theory Analysis Engine.

        Args:
            game_type: Type of game being analyzed
        """
        self.game_type = game_type
        self.players: List[Player] = []
        self.strategies: Dict[str, List[Strategy]] = {}
        self.payoff_matrix: Dict[Tuple[str, ...], PayoffCell] = {}
        self.timing: TimingType = TimingType.SIMULTANEOUS
        self.information: InformationType = InformationType.COMPLETE
        self.equilibrium_results: List[EquilibriumResult] = []
        self.historical_calibration: List[HistoricalCalibration] = []
        self.commitment_checks: List[CommitmentCheck] = []
        self.signal_checks: List[SignalCheck] = []

    def set_players(self, players: List[str]) -> None:
        """Set game participants."""
        self.players = [Player(name=name) for name in players]

    def set_player_details(
        self,
        name: str,
        player_type: str = "competitor",
        objectives: List[str] = None,
        historical_behavior: Dict[str, Any] = None,
        rationality_score: float = 0.8
    ) -> None:
        """Set detailed player information."""
        for player in self.players:
            if player.name == name:
                player.player_type = player_type
                player.objectives = objectives or []
                player.historical_behavior = historical_behavior or {}
                player.rationality_score = rationality_score
                break

    def set_strategies(self, strategies: Dict[str, List[str]]) -> None:
        """Set available strategies for each player."""
        for player_name, strategy_names in strategies.items():
            self.strategies[player_name] = [
                Strategy(name=s) for s in strategy_names
            ]

    def set_strategy_details(
        self,
        player_name: str,
        strategy_name: str,
        description: str = "",
        cost: float = 0.0,
        is_commitment: bool = False,
        commitment_type: str = ""
    ) -> None:
        """Set detailed strategy information."""
        if player_name in self.strategies:
            for strategy in self.strategies[player_name]:
                if strategy.name == strategy_name:
                    strategy.description = description
                    strategy.cost = cost
                    strategy.is_commitment = is_commitment
                    strategy.commitment_type = commitment_type
                    break

    def set_timing(self, timing: TimingType, order: List[str] = None) -> None:
        """Set game timing structure."""
        self.timing = timing
        self._player_order = order

    def set_information(self, info_type: InformationType) -> None:
        """Set information structure."""
        self.information = info_type

    def build_payoff_matrix(
        self,
        payoffs: Dict[Tuple[str, ...], Dict[str, float]],
        payoff_types: Dict[Tuple[str, ...], Dict[str, str]] = None,
        notes: Dict[Tuple[str, ...], str] = None
    ) -> Dict[Tuple[str, ...], PayoffCell]:
        """Build the payoff matrix."""
        payoff_types = payoff_types or {}
        notes = notes or {}

        self.payoff_matrix = {}

        for combo, payoff_dict in payoffs.items():
            self.payoff_matrix[combo] = PayoffCell(
                strategy_combo=combo,
                payoffs=payoff_dict,
                payoff_type=payoff_types.get(combo, {}),
                notes=notes.get(combo, "")
            )

        return self.payoff_matrix

    def find_nash_equilibrium(self) -> List[EquilibriumResult]:
        """Find all Nash equilibria in pure strategies."""
        self.equilibrium_results = find_nash_equilibrium(
            self.players, self.strategies, self.payoff_matrix
        )
        return self.equilibrium_results

    def find_dominated_strategies(self) -> Dict[str, List[str]]:
        """Find all strictly dominated strategies for each player."""
        return find_dominated_strategies(
            self.players, self.strategies, self.payoff_matrix
        )

    def calibrate_with_history(self, history_data: List[Dict[str, Any]]) -> List[HistoricalCalibration]:
        """Calibrate predictions using historical behavior data."""
        self.historical_calibration = calibrate_with_history(
            self.players, history_data
        )
        return self.historical_calibration

    def get_predicted_behavior(self, player_name: str, behavior_type: str) -> Tuple[float, str]:
        """Get predicted behavior probability for a player."""
        return get_predicted_behavior(
            self.historical_calibration, player_name, behavior_type
        )

    def check_commitment_credibility(
        self,
        player_name: str,
        commitment_type: str,
        irreversibility: float,
        observability: float,
        cost: float,
        consistency: float,
        incentive: float
    ) -> CommitmentCheck:
        """Check the credibility of a player's commitment."""
        check = check_commitment_credibility(
            player_name, commitment_type,
            irreversibility, observability, cost, consistency, incentive
        )
        self.commitment_checks.append(check)
        return check

    def check_signal_quality(
        self,
        player_name: str,
        signal_type: str,
        cost_to_mimic: float,
        observability: float,
        consistency: float,
        verifiability: float
    ) -> SignalCheck:
        """Check the quality of a signal."""
        check = check_signal_quality(
            player_name, signal_type,
            cost_to_mimic, observability, consistency, verifiability
        )
        self.signal_checks.append(check)
        return check

    def analyze(self) -> GameReport:
        """Perform comprehensive game theory analysis."""
        # Find Nash equilibrium if not already done
        if not self.equilibrium_results:
            self.find_nash_equilibrium()

        # Get best equilibrium
        equilibrium = self.equilibrium_results[0] if self.equilibrium_results else None

        # Generate strategic recommendation
        recommendation = generate_recommendation(
            equilibrium, self.players,
            self.historical_calibration,
            self.commitment_checks, self.signal_checks
        )

        # Determine confidence level
        confidence = determine_confidence_level(
            self.equilibrium_results, self.historical_calibration,
            self.payoff_matrix, self.commitment_checks
        )

        # Build report
        return GameReport(
            game_type=self.game_type.value,
            players=[p.name for p in self.players],
            strategies={name: [s.name for s in strats] for name, strats in self.strategies.items()},
            payoff_matrix={combo: cell.payoffs for combo, cell in self.payoff_matrix.items()},
            equilibrium=equilibrium,
            historical_calibration=self.historical_calibration,
            commitment_checks=self.commitment_checks,
            signal_checks=self.signal_checks,
            strategic_recommendation=recommendation,
            confidence_level=confidence
        )

    def to_dict(self) -> Dict:
        """Export analysis as dictionary."""
        report = self.analyze()

        return {
            "game_type": report.game_type,
            "players": report.players,
            "strategies": report.strategies,
            "payoff_matrix": {str(k): v for k, v in report.payoff_matrix.items()},
            "equilibrium": {
                "type": report.equilibrium.equilibrium_type if report.equilibrium else None,
                "strategy_profile": report.equilibrium.strategy_profile if report.equilibrium else None,
                "payoffs": report.equilibrium.payoffs if report.equilibrium else None,
                "is_pareto_optimal": report.equilibrium.is_pareto_optimal if report.equilibrium else None,
                "is_unique": report.equilibrium.is_unique if report.equilibrium else None,
                "reasoning": report.equilibrium.reasoning if report.equilibrium else None
            },
            "historical_calibration": [
                {
                    "player_name": c.player_name,
                    "behavior_type": c.behavior_type,
                    "historical_frequency": c.historical_frequency,
                    "consistency_score": c.consistency_score,
                    "prediction_confidence": c.prediction_confidence
                }
                for c in report.historical_calibration
            ],
            "commitment_checks": [
                {
                    "player_name": c.player_name,
                    "commitment_type": c.commitment_type,
                    "total_score": c.total_score,
                    "credibility_level": c.credibility_level,
                    "analysis": c.analysis
                }
                for c in report.commitment_checks
            ],
            "signal_checks": [
                {
                    "player_name": c.player_name,
                    "signal_type": c.signal_type,
                    "signal_quality": c.signal_quality,
                    "analysis": c.analysis
                }
                for c in report.signal_checks
            ],
            "strategic_recommendation": report.strategic_recommendation,
            "confidence_level": report.confidence_level,
            "timestamp": report.timestamp
        }

    def to_json(self) -> str:
        """Export analysis as JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
