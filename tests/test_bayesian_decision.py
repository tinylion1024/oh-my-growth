#!/usr/bin/env python3
"""
Test Bayesian Decision Module

Tests the Bayesian decision functionality for Growth Master Skill.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from bayesian_decision import (
    BayesianDecision,
    EvidenceTier,
    EvidenceDirection,
    DecisionAction,
)


def test_basic_bayesian_update():
    """Test basic Bayesian update with supporting evidence"""
    print("\n" + "=" * 60)
    print("Test 1: Basic Bayesian Update")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.35, rationale="有成功案例参考")

    print(f"Prior: {bd.get_posterior():.2f}")

    bd.add_evidence("Notion案例", "B", "support")
    posterior = bd.update()

    print(f"Evidence: Notion案例 (B, support)")
    print(f"Posterior: {posterior:.2f}")
    print(f"Decision: {bd.get_decision().value}")

    assert posterior > 0.35, "Posterior should increase with supporting evidence"
    assert bd.get_decision() in [DecisionAction.RUN_EXPERIMENT, DecisionAction.INVEST_NOW]

    print("✅ Test passed")


def test_opposing_evidence():
    """Test Bayesian update with opposing evidence"""
    print("\n" + "=" * 60)
    print("Test 2: Opposing Evidence")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.50)

    print(f"Prior: {bd.get_posterior():.2f}")

    bd.add_evidence("竞品失败案例", "B", "oppose")
    posterior = bd.update()

    print(f"Evidence: 竞品失败案例 (B, oppose)")
    print(f"Posterior: {posterior:.2f}")
    print(f"Decision: {bd.get_decision().value}")

    assert posterior < 0.50, "Posterior should decrease with opposing evidence"

    print("✅ Test passed")


def test_multiple_evidence():
    """Test Bayesian update with multiple evidence"""
    print("\n" + "=" * 60)
    print("Test 3: Multiple Evidence")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.30)

    print(f"Prior: {bd.get_posterior():.2f}")

    bd.add_evidence("Notion案例", "B", "support")
    bd.add_evidence("Dropbox案例", "B", "support")
    bd.add_evidence("SaaS行业报告", "B", "support")
    posterior = bd.update()

    print(f"Evidence: 3 supporting cases (B tier)")
    print(f"Posterior: {posterior:.2f}")
    print(f"Decision: {bd.get_decision().value}")
    print(f"Readiness Score: {bd.get_readiness_score()}")

    assert posterior > 0.30, "Posterior should increase"

    print("✅ Test passed")


def test_evidence_tiers():
    """Test different evidence tiers"""
    print("\n" + "=" * 60)
    print("Test 4: Evidence Tiers")
    print("=" * 60)

    results = {}

    for tier in ["A", "B", "C", "D"]:
        bd = BayesianDecision()
        bd.set_hypothesis("测试假设")
        bd.set_prior(0.30)
        bd.add_evidence(f"证据{tier}", tier, "support")
        posterior = bd.update()
        results[tier] = posterior

    print("Evidence tier impact:")
    for tier, posterior in results.items():
        update = EvidenceTier[tier].value
        print(f"  Tier {tier}: {0.30:.2f} → {posterior:.2f} (update: +{update:.2f})")

    # Verify tier A has largest impact
    assert results["A"] > results["B"] > results["C"] > results["D"]

    print("✅ Test passed")


def test_action_thresholds():
    """Test action threshold decisions"""
    print("\n" + "=" * 60)
    print("Test 5: Action Thresholds")
    print("=" * 60)

    test_cases = [
        (0.80, DecisionAction.INVEST_NOW),
        (0.60, DecisionAction.RUN_EXPERIMENT),
        (0.40, DecisionAction.COLLECT_EVIDENCE),
        (0.15, DecisionAction.STOP),
    ]

    for prior, expected_decision in test_cases:
        bd = BayesianDecision()
        bd.set_hypothesis("测试假设")
        bd.set_prior(prior)
        decision = bd.get_decision()
        print(f"Prior {prior:.2f} → Decision: {decision.value} (expected: {expected_decision.value})")
        assert decision == expected_decision, f"Expected {expected_decision.value}, got {decision.value}"

    print("✅ Test passed")


def test_high_risk_thresholds():
    """Test high-risk scenario thresholds"""
    print("\n" + "=" * 60)
    print("Test 6: High-Risk Thresholds")
    print("=" * 60)

    # Normal risk: 0.75 should be invest_now
    bd_normal = BayesianDecision(risk_level="normal")
    bd_normal.set_hypothesis("测试假设")
    bd_normal.set_prior(0.75)
    print(f"Normal risk, prior 0.75: {bd_normal.get_decision().value}")

    # High risk: 0.75 should be run_experiment (threshold raised to 0.85)
    bd_high = BayesianDecision(risk_level="high")
    bd_high.set_hypothesis("测试假设")
    bd_high.set_prior(0.75)
    print(f"High risk, prior 0.75: {bd_high.get_decision().value}")

    assert bd_normal.get_decision() == DecisionAction.INVEST_NOW
    assert bd_high.get_decision() == DecisionAction.RUN_EXPERIMENT

    print("✅ Test passed")


def test_iteration_log():
    """Test iteration logging"""
    print("\n" + "=" * 60)
    print("Test 7: Iteration Log")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.35)

    bd.add_evidence("Notion案例", "B", "support")
    bd.update()

    bd.log_round(
        remaining_gaps=["病毒系数未知"],
        next_questions=["用户邀请意愿有多强？"]
    )

    print(f"Rounds logged: {len(bd.iteration_log)}")
    print(f"Round 1 posterior: {bd.iteration_log[0].posterior:.2f}")
    print(f"Round 1 decision: {bd.iteration_log[0].decision}")

    assert len(bd.iteration_log) == 1
    assert bd.iteration_log[0].round_number == 1

    print("✅ Test passed")


def test_sensitivity_analysis():
    """Test sensitivity analysis generation"""
    print("\n" + "=" * 60)
    print("Test 8: Sensitivity Analysis")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.35)

    bd.add_evidence("Notion案例", "B", "support")
    bd.update()

    questions = bd.generate_sensitivity_questions()

    print("Sensitivity questions:")
    for q in questions:
        print(f"  - {q['question']}")

    assert len(questions) == 4

    print("✅ Test passed")


def test_json_export():
    """Test JSON export"""
    print("\n" + "=" * 60)
    print("Test 9: JSON Export")
    print("=" * 60)

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.35, rationale="有成功案例参考")

    bd.add_evidence("Notion案例", "B", "support", "Notion通过模板分享实现病毒增长")
    bd.update()

    json_output = bd.to_json()
    data = bd.to_dict()

    print(f"JSON length: {len(json_output)} chars")
    print(f"Hypothesis: {data['hypothesis']['statement']}")
    print(f"Posterior: {data['posterior']:.2f}")
    print(f"Decision: {data['decision']}")

    assert data["posterior"] > 0.35
    assert data["decision"] in ["invest_now", "run_experiment", "collect_evidence", "stop"]

    print("✅ Test passed")


def test_boundary_protection():
    """Test boundary protection (posterior clamped to 0.05-0.95)"""
    print("\n" + "=" * 60)
    print("Test 10: Boundary Protection")
    print("=" * 60)

    # Test upper bound
    bd_high = BayesianDecision()
    bd_high.set_hypothesis("测试假设")
    bd_high.set_prior(0.90)

    # Add multiple A-tier supporting evidence
    for i in range(5):
        bd_high.add_evidence(f"强证据{i}", "A", "support")
    posterior_high = bd_high.update()

    print(f"Prior 0.90 + 5 A-tier evidence → Posterior: {posterior_high:.2f}")
    assert posterior_high <= 0.95, "Posterior should be capped at 0.95"

    # Test lower bound
    bd_low = BayesianDecision()
    bd_low.set_hypothesis("测试假设")
    bd_low.set_prior(0.10)

    # Add multiple A-tier opposing evidence
    for i in range(5):
        bd_low.add_evidence(f"反对证据{i}", "A", "oppose")
    posterior_low = bd_low.update()

    print(f"Prior 0.10 + 5 A-tier opposing → Posterior: {posterior_low:.2f}")
    assert posterior_low >= 0.05, "Posterior should be floored at 0.05"

    print("✅ Test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Bayesian Decision Module Tests")
    print("=" * 60)

    tests = [
        test_basic_bayesian_update,
        test_opposing_evidence,
        test_multiple_evidence,
        test_evidence_tiers,
        test_action_thresholds,
        test_high_risk_thresholds,
        test_iteration_log,
        test_sensitivity_analysis,
        test_json_export,
        test_boundary_protection,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
