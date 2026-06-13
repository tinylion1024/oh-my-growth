"""Nash equilibrium calculation methods.

This module contains methods for finding Nash equilibria and dominated strategies.
"""

from typing import List, Dict, Tuple, Optional
from itertools import product

from gametheory.types import (
    Player,
    Strategy,
    PayoffCell,
    EquilibriumResult,
    EquilibriumType,
)


def get_strategy_combinations(
    players: List[Player],
    strategies: Dict[str, List[Strategy]]
) -> List[Tuple[str, ...]]:
    """Generate all possible strategy combinations."""
    if not strategies:
        return []

    player_names = [p.name for p in players]
    strategy_lists = [strategies[name] for name in player_names]
    strategy_names = [[s.name for s in strats] for strats in strategy_lists]

    return list(product(*strategy_names))


def find_best_response(
    player_idx: int,
    other_strategies: Tuple[str, ...],
    players: List[Player],
    strategies: Dict[str, List[Strategy]],
    payoff_matrix: Dict[Tuple[str, ...], PayoffCell]
) -> Tuple[str, float]:
    """
    Find the best response for a player given others' strategies.

    Args:
        player_idx: Index of the player in players list
        other_strategies: Strategies chosen by other players
        players: List of all players
        strategies: Dict of strategies for each player
        payoff_matrix: The payoff matrix

    Returns:
        Tuple of (best_strategy_name, best_payoff)
    """
    player_name = players[player_idx].name
    player_strategies = [s.name for s in strategies[player_name]]

    best_strategy = None
    best_payoff = float('-inf')

    for strategy in player_strategies:
        # Build the full strategy combination
        combo = list(other_strategies)
        combo.insert(player_idx, strategy)
        combo = tuple(combo)

        if combo in payoff_matrix:
            payoff = payoff_matrix[combo].payoffs.get(player_name, 0)
            if payoff > best_payoff:
                best_payoff = payoff
                best_strategy = strategy

    return best_strategy, best_payoff


def find_nash_equilibrium(
    players: List[Player],
    strategies: Dict[str, List[Strategy]],
    payoff_matrix: Dict[Tuple[str, ...], PayoffCell]
) -> List[EquilibriumResult]:
    """
    Find all Nash equilibria in pure strategies.

    A Nash equilibrium is a strategy profile where no player
    can improve their payoff by unilaterally changing their strategy.

    Returns:
        List of equilibrium results
    """
    if not payoff_matrix:
        raise ValueError("Payoff matrix not built. Call build_payoff_matrix() first.")

    equilibrium_results = []
    all_combos = get_strategy_combinations(players, strategies)

    for combo in all_combos:
        is_nash = True
        reasoning_parts = []

        # Check if any player wants to deviate
        for player_idx, player in enumerate(players):
            # Get current payoff
            current_payoff = payoff_matrix[combo].payoffs.get(player.name, 0)

            # Get strategies of other players
            other_strategies = tuple(
                combo[i] for i in range(len(combo)) if i != player_idx
            )

            # Find best response
            best_strategy, best_payoff = find_best_response(
                player_idx, other_strategies, players, strategies, payoff_matrix
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
            is_pareto = is_pareto_optimal(combo, players, payoff_matrix, all_combos)

            result = EquilibriumResult(
                equilibrium_type=EquilibriumType.NASH.value,
                strategy_profile=combo,
                payoffs=payoff_matrix[combo].payoffs.copy(),
                is_pareto_optimal=is_pareto,
                reasoning="; ".join(reasoning_parts)
            )

            equilibrium_results.append(result)

    # Check uniqueness
    if len(equilibrium_results) == 1:
        equilibrium_results[0].is_unique = True
    else:
        for eq in equilibrium_results:
            eq.is_unique = False

    return equilibrium_results


def is_pareto_optimal(
    combo: Tuple[str, ...],
    players: List[Player],
    payoff_matrix: Dict[Tuple[str, ...], PayoffCell],
    all_combos: List[Tuple[str, ...]]
) -> bool:
    """Check if a strategy combination is Pareto optimal."""
    current_payoffs = payoff_matrix[combo].payoffs

    for other_combo in all_combos:
        if other_combo == combo:
            continue

        other_payoffs = payoff_matrix[other_combo].payoffs

        # Check if other_combo Pareto dominates combo
        all_better_or_equal = True
        some_better = False

        for player in players:
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


def find_dominated_strategies(
    players: List[Player],
    strategies: Dict[str, List[Strategy]],
    payoff_matrix: Dict[Tuple[str, ...], PayoffCell]
) -> Dict[str, List[str]]:
    """
    Find all strictly dominated strategies for each player.

    A strategy is strictly dominated if another strategy always
    gives a better payoff regardless of what other players do.

    Returns:
        Dict mapping player name to list of dominated strategy names
    """
    dominated = {player.name: [] for player in players}
    all_combos = get_strategy_combinations(players, strategies)

    for player_idx, player in enumerate(players):
        player_strategies = [s.name for s in strategies[player.name]]

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

                        if alt_combo in payoff_matrix:
                            strategy_payoff = payoff_matrix[combo].payoffs.get(player.name, 0)
                            other_payoff = payoff_matrix[alt_combo].payoffs.get(player.name, 0)

                            if other_payoff <= strategy_payoff:
                                always_better = False
                                break

                if always_better:
                    dominated[player.name].append(strategy)
                    break

    return dominated
