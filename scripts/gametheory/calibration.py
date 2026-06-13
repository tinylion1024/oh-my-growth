"""Historical calibration, commitment credibility, and signal quality methods.

This module contains methods for calibrating predictions with historical data,
checking commitment credibility, and analyzing signal quality.
"""

from typing import List, Dict, Tuple, Any

from gametheory.types import (
    Player,
    HistoricalCalibration,
    CommitmentCheck,
    SignalCheck,
    CommitmentCredibility,
    ConfidenceLevel,
)


# Commitment credibility weights
COMMITMENT_WEIGHTS = {
    "irreversibility": 0.25,
    "observability": 0.20,
    "cost": 0.25,
    "consistency": 0.15,
    "incentive": 0.15
}


def calibrate_with_history(
    players: List[Player],
    history_data: List[Dict[str, Any]]
) -> List[HistoricalCalibration]:
    """
    Calibrate predictions using historical behavior data.

    Args:
        players: List of game participants
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
    calibration_results = []

    for record in history_data:
        player_name = record.get("player_name", "")

        # Find matching player
        player = next((p for p in players if p.name == player_name), None)
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

        calibration_results.append(calibration)

        # Update player's historical behavior
        player.historical_behavior[record.get("behavior_type", "")] = {
            "frequency": frequency,
            "consistency": consistency,
            "last_observed": record.get("last_observed", "")
        }

    return calibration_results


def get_predicted_behavior(
    historical_calibration: List[HistoricalCalibration],
    player_name: str,
    behavior_type: str
) -> Tuple[float, str]:
    """
    Get predicted behavior probability for a player.

    Args:
        historical_calibration: List of calibration records
        player_name: Player to predict
        behavior_type: Type of behavior to predict

    Returns:
        Tuple of (probability, confidence_level)
    """
    for calibration in historical_calibration:
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

    return CommitmentCheck(
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


def check_signal_quality(
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

    return SignalCheck(
        player_name=player_name,
        signal_type=signal_type,
        cost_to_mimic=cost_to_mimic,
        observability=observability,
        consistency=consistency,
        verifiability=verifiability,
        signal_quality=quality,
        analysis=analysis
    )


def generate_recommendation(
    equilibrium: Any,
    players: List[Player],
    historical_calibration: List[HistoricalCalibration],
    commitment_checks: List[CommitmentCheck],
    signal_checks: List[SignalCheck]
) -> str:
    """Generate strategic recommendation based on analysis."""
    if not equilibrium:
        return "无法确定纳什均衡，建议收集更多信息"

    parts = []

    # Main recommendation based on equilibrium
    strategy_parts = []
    for i, player in enumerate(players):
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
    if historical_calibration:
        cal_parts = []
        for cal in historical_calibration:
            if cal.prediction_confidence >= 0.6:
                cal_parts.append(
                    f"{cal.player_name}历史行为预测置信度: {cal.prediction_confidence:.0%}"
                )
        if cal_parts:
            parts.append("历史校准: " + "; ".join(cal_parts))

    # Commitment credibility
    for check in commitment_checks:
        parts.append(
            f"{check.player_name}承诺可信度: {check.credibility_level} ({check.total_score}分)"
        )

    # Signal quality
    for check in signal_checks:
        parts.append(
            f"{check.player_name}信号质量: {check.signal_quality}"
        )

    return "\n".join(parts)


def determine_confidence_level(
    equilibrium_results: List[Any],
    historical_calibration: List[HistoricalCalibration],
    payoff_matrix: Dict,
    commitment_checks: List[CommitmentCheck]
) -> str:
    """Determine overall confidence level for the analysis."""
    score = 0.0
    factors = 0

    # Factor 1: Equilibrium uniqueness
    if equilibrium_results:
        if len(equilibrium_results) == 1:
            score += 0.3
        else:
            score += 0.15
        factors += 1

    # Factor 2: Historical calibration
    if historical_calibration:
        avg_confidence = sum(c.prediction_confidence for c in historical_calibration) / len(historical_calibration)
        score += avg_confidence * 0.3
        factors += 1

    # Factor 3: Payoff matrix quality
    from gametheory.types import PayoffCell
    observed_count = sum(
        1 for cell in payoff_matrix.values()
        if isinstance(cell, PayoffCell) and any(t == "observed" for t in cell.payoff_type.values())
    )
    if payoff_matrix:
        observed_ratio = observed_count / len(payoff_matrix)
        score += observed_ratio * 0.2
        factors += 1

    # Factor 4: Commitment credibility
    if commitment_checks:
        avg_credibility = sum(c.total_score for c in commitment_checks) / len(commitment_checks)
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
