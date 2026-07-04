"""Kelly criterion calculation methods.

This module contains the core Kelly calculation functions for binary
and multi-scenario resource allocation.
"""

from math import log
from typing import List, Dict

from .types import (
    BinaryKellyResult,
    Scenario,
    ScenarioKellyResult,
    FractionalKellyResult,
)


def binary_kelly(
    win_prob: float,
    win_amount: float,
    loss_amount: float
) -> BinaryKellyResult:
    """
    Calculate Kelly fraction for binary outcome scenarios.

    Uses the classic Kelly formula: f* = (bp - q) / b
    where b = net odds, p = win probability, q = loss probability.

    Args:
        win_prob: Probability of winning (0.0 - 1.0)
        win_amount: Amount gained on win
        loss_amount: Amount lost on loss

    Returns:
        BinaryKellyResult with full and fractional Kelly values
    """
    # Validate inputs
    win_prob = max(0.0, min(1.0, win_prob))
    loss_amount = abs(loss_amount)  # Ensure positive

    # Calculate net odds (b)
    net_odds = win_amount / loss_amount if loss_amount > 0 else float('inf')

    # Loss probability (q)
    loss_prob = 1.0 - win_prob

    # Kelly formula: f* = (bp - q) / b
    if net_odds == float('inf'):
        # Infinite odds (no loss possible)
        full_kelly = 1.0
    else:
        # Standard Kelly calculation
        edge = (net_odds * win_prob) - loss_prob
        full_kelly = edge / net_odds if net_odds > 0 else 0.0

    # Ensure non-negative (no bet if edge is negative)
    full_kelly = max(0.0, full_kelly)

    # Calculate fractional Kelly values
    half_kelly = full_kelly * 0.5
    quarter_kelly = full_kelly * 0.25
    eighth_kelly = full_kelly * 0.125

    # Calculate edge and expected value
    edge = (net_odds * win_prob) - loss_prob
    expected_value = (win_prob * win_amount) - (loss_prob * loss_amount)

    return BinaryKellyResult(
        full_kelly=full_kelly,
        half_kelly=half_kelly,
        quarter_kelly=quarter_kelly,
        eighth_kelly=eighth_kelly,
        net_odds=net_odds,
        win_probability=win_prob,
        loss_probability=loss_prob,
        edge=edge,
        expected_value=expected_value
    )


def scenario_kelly(scenarios: List[Dict]) -> ScenarioKellyResult:
    """
    Calculate Kelly fraction for multiple outcome scenarios.

    Uses numerical optimization to maximize E[log(1 + f * r)]
    where r is the return rate for each scenario.

    Args:
        scenarios: List of scenario dicts with keys:
            - outcome: str (scenario name)
            - return_rate: float (e.g., 2.0 = 200% gain, -0.5 = 50% loss)
            - probability: float (0.0 - 1.0)
            - description: str (optional)

    Returns:
        ScenarioKellyResult with optimal fraction
    """
    # Convert to Scenario objects
    scenario_objs = []
    for s in scenarios:
        scenario_objs.append(Scenario(
            outcome=s.get("outcome", "unknown"),
            return_rate=s.get("return_rate", s.get("return", 0.0)),
            probability=s.get("probability", 0.0),
            description=s.get("description", "")
        ))

    # Normalize probabilities
    total_prob = sum(s.probability for s in scenario_objs)
    if total_prob > 0:
        for s in scenario_objs:
            s.probability /= total_prob

    def expected_log_growth(f: float) -> float:
        """Calculate expected log growth for given fraction f."""
        result = 0.0
        for scenario in scenario_objs:
            # Growth factor: 1 + f * return_rate
            growth_factor = 1.0 + f * scenario.return_rate
            # Avoid log of negative or zero
            if growth_factor <= 0:
                return float('inf')  # Penalize bankruptcy
            result -= scenario.probability * log(growth_factor)
        return result

    # Optimize with a bounded golden-section search to avoid external dependencies.
    lower, upper = 0.0, 2.0
    phi = (1 + 5 ** 0.5) / 2
    inv_phi = 1 / phi
    inv_phi_sq = inv_phi * inv_phi
    a, b = lower, upper
    h = b - a
    if h <= 1e-9:
        optimal_fraction = 0.0
        expected_log = 0.0
    else:
        n = 32
        c = a + inv_phi_sq * h
        d = a + inv_phi * h
        fc = expected_log_growth(c)
        fd = expected_log_growth(d)
        for _ in range(n):
            if fc < fd:
                b = d
                d = c
                fd = fc
                h = b - a
                c = a + inv_phi_sq * h
                fc = expected_log_growth(c)
            else:
                a = c
                c = d
                fc = fd
                h = b - a
                d = a + inv_phi * h
                fd = expected_log_growth(d)

        if fc < fd:
            optimal_fraction = c
            expected_log = -fc
        else:
            optimal_fraction = d
            expected_log = -fd

        if optimal_fraction < 0 or not (optimal_fraction == optimal_fraction):
            optimal_fraction = 0.0
            expected_log = 0.0

    return ScenarioKellyResult(
        optimal_fraction=optimal_fraction,
        half_kelly=optimal_fraction * 0.5,
        quarter_kelly=optimal_fraction * 0.25,
        expected_log_growth=expected_log,
        scenarios=scenario_objs,
        optimization_method="golden-section"
    )


def fractional_kelly(
    kelly_fraction: float,
    fraction: float = 0.5
) -> FractionalKellyResult:
    """
    Apply fractional Kelly adjustment.

    Fractional Kelly reduces position size to lower volatility
    while maintaining most of the growth rate.

    Args:
        kelly_fraction: Original Kelly fraction (full Kelly)
        fraction: Fraction to apply (0.5 = half Kelly)

    Returns:
        FractionalKellyResult with adjusted values
    """
    adjusted_kelly = kelly_fraction * fraction

    # Growth efficiency: approximate as fraction for small adjustments
    growth_efficiency = fraction * (2 - fraction)  # ~75% for half Kelly

    # Risk reduction: variance scales as fraction^2
    risk_reduction = 1.0 - (fraction ** 2)

    return FractionalKellyResult(
        original_kelly=kelly_fraction,
        fraction=fraction,
        adjusted_kelly=adjusted_kelly,
        growth_efficiency=growth_efficiency,
        risk_reduction=risk_reduction
    )
