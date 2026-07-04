#!/usr/bin/env python3
"""Game Theory Analysis - Compatibility wrapper.

This module provides backward compatibility by re-exporting from the gametheory package.
"""

try:
    from .gametheory import (
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
        find_nash_equilibrium,
        find_dominated_strategies,
        calibrate_with_history,
        check_commitment_credibility,
        check_signal_quality,
        GameTheoryAnalysis,
    )
except ImportError:  # pragma: no cover - direct script compatibility.
    from gametheory import (
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
        find_nash_equilibrium,
        find_dominated_strategies,
        calibrate_with_history,
        check_commitment_credibility,
        check_signal_quality,
        GameTheoryAnalysis,
    )


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
        irreversibility=15,
        observability=18,
        cost=10,
        consistency=12,
        incentive=8
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
