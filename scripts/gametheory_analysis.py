#!/usr/bin/env python3
"""
Game Theory Analysis Module for Growth Master Skill

Provides game theory analysis for strategic decision making including
Nash equilibrium calculation, payoff matrix construction, and historical
behavior calibration.

Usage:
    from gametheory_analysis import GameTheoryAnalysis

    gta = GameTheoryAnalysis()
    gta.set_players(["我方", "竞争对手"])
    gta.set_strategies({
        "我方": ["降价", "不降价"],
        "竞争对手": ["跟进降价", "不跟进"]
    })
    gta.build_payoff_matrix(payoffs)
    nash = gta.find_nash_equilibrium()
    result = gta.analyze()
"""

import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal, Tuple, Any
from enum import Enum
from datetime import datetime
from itertools import product


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

    # Commitment credibility weights
    COMMITMENT_WEIGHTS = {
        "irreversibility": 0.25,
        "observability": 0.20,
        "cost": 0.25,
        "consistency": 0.15,
        "incentive": 0.15
    }

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
        """
        Set game participants.

        Args:
            players: List of player names

        Example:
            gta.set_players(["我方", "竞争对手"])
        """
        self.players = [Player(name=name) for name in players]

    def set_player_details(
        self,
        name: str,
        player_type: str = "competitor",
        objectives: List[str] = None,
        historical_behavior: Dict[str, Any] = None,
        rationality_score: float = 0.8
    ) -> None:
        """
        Set detailed player information.

        Args:
            name: Player name
            player_type: Type of player (competitor, customer, supplier, regulator)
            objectives: List of player objectives
            historical_behavior: Dict of historical behaviors
            rationality_score: How rationally the player behaves (0-1)
        """
        for player in self.players:
            if player.name == name:
                player.player_type = player_type
                player.objectives = objectives or []
                player.historical_behavior = historical_behavior or {}
                player.rationality_score = rationality_score
                break

    def set_strategies(self, strategies: Dict[str, List[str]]) -> None:
        """
        Set available strategies for each player.

        Args:
            strategies: Dict mapping player name to list of strategy names

        Example:
            gta.set_strategies({
                "我方": ["降价", "不降价"],
                "竞争对手": ["跟进降价", "不跟进"]
            })
        """
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
        """
        Set detailed strategy information.

        Args:
            player_name: Player name
            strategy_name: Strategy name
            description: Strategy description
            cost: Cost of implementing this strategy
            is_commitment: Whether this is a commitment strategy
            commitment_type: Type of commitment (burning_bridge, reputation, contract, investment)
        """
        if player_name in self.strategies:
            for strategy in self.strategies[player_name]:
                if strategy.name == strategy_name:
                    strategy.description = description
                    strategy.cost = cost
                    strategy.is_commitment = is_commitment
                    strategy.commitment_type = commitment_type
                    break

    def set_timing(self, timing: TimingType, order: List[str] = None) -> None:
        """
        Set game timing structure.

        Args:
            timing: SIMULTANEOUS or SEQUENTIAL
            order: Player order for sequential games
        """
        self.timing = timing
        self._player_order = order

    def set_information(self, info_type: InformationType) -> None:
        """
        Set information structure.

        Args:
            info_type: COMPLETE or INCOMPLETE
        """
        self.information = info_type

    def build_payoff_matrix(
        self,
        payoffs: Dict[Tuple[str, ...], Dict[str, float]],
        payoff_types: Dict[Tuple[str, ...], Dict[str, str]] = None,
        notes: Dict[Tuple[str, ...], str] = None
    ) -> Dict[Tuple[str, ...], PayoffCell]:
        """
        Build the payoff matrix.

        Args:
            payoffs: Dict mapping strategy combination to payoff dict
                     e.g., {("降价", "跟进"): {"我方": -5, "竞争对手": -5}}
            payoff_types: Dict mapping strategy combination to type dict
                          e.g., {("降价", "跟进"): {"我方": "estimated"}}
            notes: Additional notes for each cell

        Returns:
            The constructed payoff matrix

        Example:
            gta.build_payoff_matrix({
                ("降价", "跟进"): {"我方": -5, "竞争对手": -5},
                ("降价", "不跟进"): {"我方": 15, "竞争对手": -10},
                ("不降价", "跟进"): {"我方": -8, "竞争对手": 12},
                ("不降价", "不跟进"): {"我方": 0, "竞争对手": 0}
            })
        """
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

    def _get_strategy_combinations(self) -> List[Tuple[str, ...]]:
        """Generate all possible strategy combinations"""
        if not self.strategies:
            return []

        player_names = [p.name for p in self.players]
        strategy_lists = [self.strategies[name] for name in player_names]
        strategy_names = [[s.name for s in strategies] for strategies in strategy_lists]

        return list(product(*strategy_names))

    def _find_best_response(self, player_idx: int, other_strategies: Tuple[str, ...]) -> Tuple[str, float]:
        """
        Find the best response for a player given others' strategies.

        Args:
            player_idx: Index of the player in self.players
            other_strategies: Strategies chosen by other players

        Returns:
            Tuple of (best_strategy_name, best_payoff)
        """
        player_name = self.players[player_idx].name
        player_strategies = [s.name for s in self.strategies[player_name]]

        best_strategy = None
        best_payoff = float('-inf')

        for strategy in player_strategies:
            # Build the full strategy combination
            combo = list(other_strategies)
            combo.insert(player_idx, strategy)
            combo = tuple(combo)

            if combo in self.payoff_matrix:
                payoff = self.payoff_matrix[combo].payoffs.get(player_name, 0)
                if payoff > best_payoff:
                    best_payoff = payoff
                    best_strategy = strategy

        return best_strategy, best_payoff

    def find_nash_equilibrium(self) -> List[EquilibriumResult]:
        """
        Find all Nash equilibria in pure strategies.

        A Nash equilibrium is a strategy profile where no player
        can improve their payoff by unilaterally changing their strategy.

        Returns:
            List of equilibrium results
        """
        if not self.payoff_matrix:
            raise ValueError("Payoff matrix not built. Call build_payoff_matrix() first.")

        self.equilibrium_results = []
        all_combos = self._get_strategy_combinations()

        for combo in all_combos:
            is_nash = True
            reasoning_parts = []

            # Check if any player wants to deviate
            for player_idx, player in enumerate(self.players):
                # Get current payoff
                current_payoff = self.payoff_matrix[combo].payoffs.get(player.name, 0)

                # Get strategies of other players
                other_strategies = tuple(
                    combo[i] for i in range(len(combo)) if i != player_idx
                )

                # Find best response
                best_strategy, best_payoff = self._find_best_response(
                    player_idx, other_strategies
                )

                current_strategy = combo[player_idx]

                if best_payoff > current_payoff:
                    is_nash = False
                    break
                else:
                    reasoning_parts.append(
                        f"{player.name}: {current_strategy}是最佳响应"
                    )

            if is_nash:
                # Check if Pareto optimal
                is_pareto = self._is_pareto_optimal(combo)

                result = EquilibriumResult(
                    equilibrium_type=EquilibriumType.NASH.value,
                    strategy_profile=combo,
                    payoffs=self.payoff_matrix[combo].payoffs.copy(),
                    is_pareto_optimal=is_pareto,
                    reasoning="; ".join(reasoning_parts)
                )

                self.equilibrium_results.append(result)

        # Check uniqueness
        if len(self.equilibrium_results) == 1:
            self.equilibrium_results[0].is_unique = True
        else:
            for eq in self.equilibrium_results:
                eq.is_unique = False

        return self.equilibrium_results

    def _is_pareto_optimal(self, combo: Tuple[str, ...]) -> bool:
        """Check if a strategy combination is Pareto optimal"""
        current_payoffs = self.payoff_matrix[combo].payoffs
        all_combos = self._get_strategy_combinations()

        for other_combo in all_combos:
            if other_combo == combo:
                continue

            other_payoffs = self.payoff_matrix[other_combo].payoffs

            # Check if other_combo Pareto dominates combo
            all_better_or_equal = True
            some_better = False

            for player in self.players:
                other_p = other_payoffs.get(player.name, 0)
                current_p = current_payoffs.get(player.name, 0)

                if other_p < current_p:
                    all_better_or_equal = False
                    break
                elif other_p > current_p:
                    some_better = True

            if all_better_or_equal and some_better:
                return False

        return True

    def find_dominated_strategies(self) -> Dict[str, List[str]]:
        """
        Find all strictly dominated strategies for each player.

        A strategy is strictly dominated if another strategy always
        gives a better payoff regardless of what other players do.

        Returns:
            Dict mapping player name to list of dominated strategy names
        """
        dominated = {player.name: [] for player in self.players}
        all_combos = self._get_strategy_combinations()

        for player_idx, player in enumerate(self.players):
            player_strategies = [s.name for s in self.strategies[player.name]]

            for strategy in player_strategies:
                for other_strategy in player_strategies:
                    if strategy == other_strategy:
                        continue

                    # Check if other_strategy dominates strategy
                    always_better = True

                    for combo in all_combos:
                        if combo[player_idx] == strategy:
                            # Build alternative combo with other_strategy
                            alt_combo = list(combo)
                            alt_combo[player_idx] = other_strategy
                            alt_combo = tuple(alt_combo)

                            if alt_combo in self.payoff_matrix:
                                strategy_payoff = self.payoff_matrix[combo].payoffs.get(player.name, 0)
                                other_payoff = self.payoff_matrix[alt_combo].payoffs.get(player.name, 0)

                                if other_payoff <= strategy_payoff:
                                    always_better = False
                                    break

                    if always_better:
                        dominated[player.name].append(strategy)
                        break

        return dominated

    def calibrate_with_history(self, history_data: List[Dict[str, Any]]) -> List[HistoricalCalibration]:
        """
        Calibrate predictions using historical behavior data.

        Args:
            history_data: List of historical behavior records
                Each record should have:
                - player_name: str
                - behavior_type: str (e.g., "price_war", "follow_discount")
                - frequency: float (0-1, how often they exhibit this behavior)
                - last_observed: str (date or description)
                - consistency: float (0-1, how consistent the behavior is)
                - reference_class: str (e.g., "market_leader", "challenger")

        Returns:
            List of historical calibration records
        """
        self.historical_calibration = []

        for record in history_data:
            player_name = record.get("player_name", "")

            # Find matching player
            player = next((p for p in self.players if p.name == player_name), None)
            if not player:
                continue

            # Calculate prediction confidence based on frequency and consistency
            frequency = record.get("frequency", 0.5)
            consistency = record.get("consistency", 0.5)
            prediction_confidence = frequency * consistency

            calibration = HistoricalCalibration(
                player_name=player_name,
                behavior_type=record.get("behavior_type", ""),
                historical_frequency=frequency,
                last_observed=record.get("last_observed", ""),
                consistency_score=consistency,
                reference_class=record.get("reference_class", ""),
                prediction_confidence=prediction_confidence
            )

            self.historical_calibration.append(calibration)

            # Update player's historical behavior
            player.historical_behavior[record.get("behavior_type", "")] = {
                "frequency": frequency,
                "consistency": consistency,
                "last_observed": record.get("last_observed", "")
            }

        return self.historical_calibration

    def get_predicted_behavior(self, player_name: str, behavior_type: str) -> Tuple[float, str]:
        """
        Get predicted behavior probability for a player.

        Args:
            player_name: Player to predict
            behavior_type: Type of behavior to predict

        Returns:
            Tuple of (probability, confidence_level)
        """
        for calibration in self.historical_calibration:
            if calibration.player_name == player_name and calibration.behavior_type == behavior_type:
                confidence = calibration.prediction_confidence

                if confidence >= 0.75:
                    level = ConfidenceLevel.HIGH.value
                elif confidence >= 0.50:
                    level = ConfidenceLevel.MEDIUM.value
                else:
                    level = ConfidenceLevel.LOW.value

                return confidence, level

        return 0.5, ConfidenceLevel.LOW.value

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
        """
        Check the credibility of a player's commitment.

        Args:
            player_name: Player making the commitment
            commitment_type: Type of commitment (burning_bridge, reputation, contract, investment)
            irreversibility: Score 0-25
            observability: Score 0-20
            cost: Score 0-25
            consistency: Score 0-15
            incentive: Score 0-15

        Returns:
            CommitmentCheck result
        """
        total_score = irreversibility + observability + cost + consistency + incentive

        if total_score >= 75:
            credibility_level = CommitmentCredibility.HIGH.value
        elif total_score >= 50:
            credibility_level = CommitmentCredibility.MEDIUM.value
        else:
            credibility_level = CommitmentCredibility.LOW.value

        analysis_parts = []
        if irreversibility >= 20:
            analysis_parts.append("承诺高度不可逆")
        elif irreversibility < 10:
            analysis_parts.append("承诺容易撤销")

        if observability >= 15:
            analysis_parts.append("对手可清楚观察到")
        elif observability < 10:
            analysis_parts.append("承诺可观察性低")

        if cost >= 20:
            analysis_parts.append("违约成本很高")
        elif cost < 10:
            analysis_parts.append("违约成本低")

        analysis = "; ".join(analysis_parts) if analysis_parts else "承诺可信度一般"

        check = CommitmentCheck(
            player_name=player_name,
            commitment_type=commitment_type,
            irreversibility_score=irreversibility,
            observability_score=observability,
            cost_score=cost,
            consistency_score=consistency,
            incentive_score=incentive,
            total_score=total_score,
            credibility_level=credibility_level,
            analysis=analysis
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
        """
        Check the quality of a signal.

        Args:
            player_name: Player sending the signal
            signal_type: Type of signal (separating, pooling, semi_separating)
            cost_to_mimic: Score 0-1 (how costly for low-type to mimic)
            observability: Score 0-1 (how observable the signal is)
            consistency: Score 0-1 (consistency with history)
            verifiability: Score 0-1 (how verifiable the signal is)

        Returns:
            SignalCheck result
        """
        avg_quality = (cost_to_mimic + observability + consistency + verifiability) / 4

        if avg_quality >= 0.75:
            quality = "high"
        elif avg_quality >= 0.50:
            quality = "medium"
        else:
            quality = "low"

        analysis_parts = []
        if cost_to_mimic >= 0.7:
            analysis_parts.append("低成本类型难以模仿")
        elif cost_to_mimic < 0.3:
            analysis_parts.append("容易被低成本类型模仿")

        if signal_type == "separating":
            analysis_parts.append("分离信号，可区分类型")
        elif signal_type == "pooling":
            analysis_parts.append("混同信号，无法区分类型")

        analysis = "; ".join(analysis_parts) if analysis_parts else "信号质量一般"

        check = SignalCheck(
            player_name=player_name,
            signal_type=signal_type,
            cost_to_mimic=cost_to_mimic,
            observability=observability,
            consistency=consistency,
            verifiability=verifiability,
            signal_quality=quality,
            analysis=analysis
        )

        self.signal_checks.append(check)
        return check

    def analyze(self) -> GameReport:
        """
        Perform comprehensive game theory analysis.

        Returns:
            Complete game theory analysis report
        """
        # Find Nash equilibrium if not already done
        if not self.equilibrium_results:
            self.find_nash_equilibrium()

        # Get best equilibrium
        equilibrium = self.equilibrium_results[0] if self.equilibrium_results else None

        # Generate strategic recommendation
        recommendation = self._generate_recommendation(equilibrium)

        # Determine confidence level
        confidence = self._determine_confidence_level()

        # Build report
        report = GameReport(
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

        return report

    def _generate_recommendation(self, equilibrium: Optional[EquilibriumResult]) -> str:
        """Generate strategic recommendation based on analysis"""
        if not equilibrium:
            return "无法确定纳什均衡，建议收集更多信息"

        parts = []

        # Main recommendation based on equilibrium
        strategy_parts = []
        for i, player in enumerate(self.players):
            strategy = equilibrium.strategy_profile[i]
            strategy_parts.append(f"{player.name}: {strategy}")

        parts.append(f"纳什均衡策略组合: ({', '.join(strategy_parts)})")

        # Payoff analysis
        payoff_parts = []
        for player_name, payoff in equilibrium.payoffs.items():
            payoff_parts.append(f"{player_name}: {payoff:+.1f}")
        parts.append(f"均衡收益: {', '.join(payoff_parts)}")

        # Pareto optimality
        if equilibrium.is_pareto_optimal:
            parts.append("此均衡是帕累托最优的")
        else:
            parts.append("此均衡不是帕累托最优，存在双赢可能")

        # Historical calibration influence
        if self.historical_calibration:
            cal_parts = []
            for cal in self.historical_calibration:
                if cal.prediction_confidence >= 0.6:
                    cal_parts.append(
                        f"{cal.player_name}历史行为预测置信度: {cal.prediction_confidence:.0%}"
                    )
            if cal_parts:
                parts.append("历史校准: " + "; ".join(cal_parts))

        # Commitment credibility
        for check in self.commitment_checks:
            parts.append(
                f"{check.player_name}承诺可信度: {check.credibility_level} ({check.total_score}分)"
            )

        # Signal quality
        for check in self.signal_checks:
            parts.append(
                f"{check.player_name}信号质量: {check.signal_quality}"
            )

        return "\n".join(parts)

    def _determine_confidence_level(self) -> str:
        """Determine overall confidence level for the analysis"""
        score = 0.0
        factors = 0

        # Factor 1: Equilibrium uniqueness
        if self.equilibrium_results:
            if len(self.equilibrium_results) == 1:
                score += 0.3
            else:
                score += 0.15
            factors += 1

        # Factor 2: Historical calibration
        if self.historical_calibration:
            avg_confidence = sum(c.prediction_confidence for c in self.historical_calibration) / len(self.historical_calibration)
            score += avg_confidence * 0.3
            factors += 1

        # Factor 3: Payoff matrix quality
        observed_count = sum(
            1 for cell in self.payoff_matrix.values()
            if any(t == "observed" for t in cell.payoff_type.values())
        )
        if self.payoff_matrix:
            observed_ratio = observed_count / len(self.payoff_matrix)
            score += observed_ratio * 0.2
            factors += 1

        # Factor 4: Commitment credibility
        if self.commitment_checks:
            avg_credibility = sum(c.total_score for c in self.commitment_checks) / len(self.commitment_checks)
            score += (avg_credibility / 100) * 0.2
            factors += 1

        if factors == 0:
            return ConfidenceLevel.LOW.value

        avg_score = score / factors

        if avg_score >= 0.75:
            return ConfidenceLevel.HIGH.value
        elif avg_score >= 0.50:
            return ConfidenceLevel.MEDIUM.value
        else:
            return ConfidenceLevel.LOW.value

    def to_dict(self) -> Dict:
        """Export analysis as dictionary"""
        report = self.analyze()

        return {
            "game_type": report.game_type,
            "players": report.players,
            "strategies": report.strategies,
            "payoff_matrix": {
                str(k): v for k, v in report.payoff_matrix.items()
            },
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
        """Export analysis as JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def main():
    """Demo: Game theory analysis for pricing decision"""

    print("=" * 60)
    print("博弈论分析示例：SaaS 定价决策")
    print("=" * 60)

    # Initialize
    gta = GameTheoryAnalysis()

    # Set players
    gta.set_players(["我方", "竞争对手"])
    gta.set_player_details(
        name="我方",
        player_type="market_leader",
        objectives=["保持市场份额", "维持利润率"]
    )
    gta.set_player_details(
        name="竞争对手",
        player_type="challenger",
        objectives=["扩大市场份额"],
        rationality_score=0.9
    )

    # Set strategies
    gta.set_strategies({
        "我方": ["降价10%", "不降价"],
        "竞争对手": ["跟进降价", "不跟进"]
    })

    # Build payoff matrix
    print("\n📊 构建收益矩阵:")
    gta.build_payoff_matrix(
        payoffs={
            ("降价10%", "跟进降价"): {"我方": -5, "竞争对手": -5},
            ("降价10%", "不跟进"): {"我方": 15, "竞争对手": -10},
            ("不降价", "跟进降价"): {"我方": -8, "竞争对手": 12},
            ("不降价", "不跟进"): {"我方": 0, "竞争对手": 0}
        },
        payoff_types={
            ("降价10%", "跟进降价"): {"我方": "estimated", "竞争对手": "estimated"},
            ("降价10%", "不跟进"): {"我方": "assumed", "竞争对手": "assumed"},
            ("不降价", "跟进降价"): {"我方": "estimated", "竞争对手": "assumed"},
            ("不降价", "不跟进"): {"我方": "observed", "竞争对手": "observed"}
        }
    )

    for combo, cell in gta.payoff_matrix.items():
        print(f"  {combo}: {cell.payoffs} ({cell.payoff_type.get('我方', 'unknown')})")

    # Find Nash equilibrium
    print("\n🎯 纳什均衡分析:")
    equilibria = gta.find_nash_equilibrium()

    for eq in equilibria:
        print(f"  策略组合: {eq.strategy_profile}")
        print(f"  收益: {eq.payoffs}")
        print(f"  帕累托最优: {eq.is_pareto_optimal}")
        print(f"  推理: {eq.reasoning}")

    # Find dominated strategies
    print("\n🔍 被占优策略:")
    dominated = gta.find_dominated_strategies()
    for player, strategies in dominated.items():
        if strategies:
            print(f"  {player}: {strategies}")
        else:
            print(f"  {player}: 无")

    # Historical calibration
    print("\n📈 历史行为校准:")
    gta.calibrate_with_history([
        {
            "player_name": "竞争对手",
            "behavior_type": "follow_discount",
            "frequency": 0.9,
            "last_observed": "2024-01",
            "consistency": 0.85,
            "reference_class": "challenger"
        },
        {
            "player_name": "竞争对手",
            "behavior_type": "initiate_price_war",
            "frequency": 0.1,
            "last_observed": "从未",
            "consistency": 0.95,
            "reference_class": "challenger"
        }
    ])

    for cal in gta.historical_calibration:
        print(f"  {cal.player_name} - {cal.behavior_type}:")
        print(f"    历史频率: {cal.historical_frequency:.0%}")
        print(f"    一致性: {cal.consistency_score:.0%}")
        print(f"    预测置信度: {cal.prediction_confidence:.0%}")

    # Check commitment credibility
    print("\n🔒 承诺可信性检验:")
    gta.check_commitment_credibility(
        player_name="我方",
        commitment_type="price_promise",
        irreversibility=15,  # 可撤销但有一定成本
        observability=18,    # 公开声明
        cost=10,             # 违约有一定成本
        consistency=12,      # 历史上一致
        incentive=8          # 与激励基本一致
    )

    for check in gta.commitment_checks:
        print(f"  {check.player_name} ({check.commitment_type}):")
        print(f"    总分: {check.total_score}/100")
        print(f"    可信度: {check.credibility_level}")
        print(f"    分析: {check.analysis}")

    # Get predicted behavior
    prob, level = gta.get_predicted_behavior("竞争对手", "follow_discount")
    print(f"\n🔮 行为预测:")
    print(f"  竞争对手跟进降价概率: {prob:.0%} ({level})")

    # Generate full report
    print("\n" + "=" * 60)
    print("完整分析报告:")
    print("=" * 60)
    print(gta.to_json())


if __name__ == "__main__":
    main()
