#!/usr/bin/env python3
"""Kelly Sizing - Compatibility wrapper.

This module provides backward compatibility by re-exporting from the kelly package.
"""

try:
    from .kelly import (
        DecisionReadinessStatus,
        KellySuitability,
        BinaryKellyResult,
        Scenario,
        ScenarioKellyResult,
        FractionalKellyResult,
        DecisionReadinessResult,
        ActionPackage,
        KellyAllocationReport,
        binary_kelly,
        scenario_kelly,
        fractional_kelly,
        decision_readiness,
        assess_kelly_suitability,
        KellySizing,
    )
except ImportError:  # pragma: no cover - direct script compatibility.
    from kelly import (
        DecisionReadinessStatus,
        KellySuitability,
        BinaryKellyResult,
        Scenario,
        ScenarioKellyResult,
        FractionalKellyResult,
        DecisionReadinessResult,
        ActionPackage,
        KellyAllocationReport,
        binary_kelly,
        scenario_kelly,
        fractional_kelly,
        decision_readiness,
        assess_kelly_suitability,
        KellySizing,
    )


def main():
    """Demo: Kelly Sizing for growth experiment"""

    print("=" * 60)
    print("Kelly 资源分配示例：邀请裂变实验")
    print("=" * 60)

    # Initialize
    ks = KellySizing(risk_profile="moderate")

    # Example 1: Binary Kelly
    print("\n📊 场景 1: 二元机会")
    print("-" * 40)

    result = ks.binary_kelly(
        win_prob=0.60,
        win_amount=100,
        loss_amount=30
    )

    print(f"成功概率: {result.win_probability:.0%}")
    print(f"净赔率: {result.net_odds:.2f}")
    print(f"边缘: {result.edge:.2f}")
    print(f"Full Kelly: {result.full_kelly:.1%}")
    print(f"Half Kelly: {result.half_kelly:.1%}")
    print(f"Quarter Kelly: {result.quarter_kelly:.1%}")

    recommended, desc = result.get_recommended("normal")
    print(f"\n推荐: {recommended:.1%} ({desc})")

    # Example 2: Scenario Kelly
    print("\n📊 场景 2: 多场景机会")
    print("-" * 40)

    scenarios = [
        {"outcome": "大成功", "return_rate": 2.0, "probability": 0.20},
        {"outcome": "小成功", "return_rate": 0.5, "probability": 0.30},
        {"outcome": "持平", "return_rate": 0.0, "probability": 0.30},
        {"outcome": "失败", "return_rate": -0.5, "probability": 0.20},
    ]

    scenario_result = ks.scenario_kelly(scenarios)

    print(f"最优比例: {scenario_result.optimal_fraction:.1%}")
    print(f"Half Kelly: {scenario_result.half_kelly:.1%}")
    print(f"Quarter Kelly: {scenario_result.quarter_kelly:.1%}")
    print(f"期望对数增长: {scenario_result.expected_log_growth:.4f}")

    # Example 3: Fractional Kelly
    print("\n📊 场景 3: 分数 Kelly")
    print("-" * 40)

    frac_result = ks.fractional_kelly(0.40, fraction=0.5)

    print(f"原始 Kelly: {frac_result.original_kelly:.1%}")
    print(f"分数: {frac_result.fraction:.1%}")
    print(f"调整后: {frac_result.adjusted_kelly:.1%}")
    print(f"增长效率: {frac_result.growth_efficiency:.1%}")
    print(f"风险降低: {frac_result.risk_reduction:.1%}")

    # Example 4: Decision Readiness
    print("\n📊 场景 4: 决策准备度")
    print("-" * 40)

    context = {
        "resource_pool": 1000000,
        "resource_clarity": "clear",
        "probability_source": "expert",
        "payoff_clarity": "partial",
        "downside_bound": "bounded",
        "repeatability": "repeatable",
        "feedback_mechanism": "yes",
    }

    readiness = ks.decision_readiness(context)

    print(f"总分: {readiness.score}")
    print(f"状态: {readiness.status.value}")
    print(f"\n维度得分:")
    for dim, score in readiness.dimensions.items():
        print(f"  - {dim}: {score}")

    if readiness.gaps:
        print(f"\n信息缺口:")
        for gap in readiness.gaps:
            print(f"  - {gap}")

    if readiness.recommendations:
        print(f"\n建议:")
        for rec in readiness.recommendations:
            print(f"  - {rec}")

    # Example 5: Full Report
    print("\n" + "=" * 60)
    print("完整 Kelly 分配报告")
    print("=" * 60)

    full_context = {
        "resource_pool": 800000,
        "protected_reserve": 200000,
        "risk_budget": 800000,
        "resource_clarity": "clear",
        "probability_source": "expert",
        "payoff_clarity": "partial",
        "downside_bound": "bounded",
        "repeatability": "repeatable",
        "feedback_mechanism": "yes",
        "uncertainty_level": "normal",
        "assumptions": ["用户有足够动机邀请", "激励成本可控"],
        "assumption_sources": {
            "用户有足够动机邀请": "assumed",
            "激励成本可控": "estimated"
        }
    }

    action_pkg = ks.create_action_package(
        kelly_fraction=result.half_kelly,
        resource_pool=800000,
        opportunity_name="邀请裂变 MVP",
        metrics=["病毒系数", "CAC", "新用户留存率"],
        add_conditions=["病毒系数 > 0.5 且 CAC < 50元"],
        stop_conditions=["病毒系数 < 0.3 或 CAC > 80元"]
    )

    report = ks.generate_full_report(
        opportunity_name="邀请裂变实验",
        kelly_result=result,
        context=full_context,
        action_package=action_pkg
    )

    print(ks.to_json(report))


if __name__ == "__main__":
    main()
