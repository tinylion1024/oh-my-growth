#!/usr/bin/env python3

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from strategy_brain import StrategyBrain


FIXTURES_PATH = Path(__file__).parent / "fixtures" / "strategy-golden-scenarios.json"


def load_scenarios():
    return json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))


def run_scenario(scenario):
    return StrategyBrain().analyze(
        scenario["query"],
        scenario["context"],
        mode="diagnose",
    )


def test_golden_scenarios_expected_top_categories():
    for scenario in load_scenarios():
        analysis = run_scenario(scenario)
        top_priority = analysis["priorities"][0]
        assert (
            top_priority.category == scenario["expected_top_category"]
        ), f"{scenario['id']}: expected top category {scenario['expected_top_category']}, got {top_priority.category}"
        assert (
            analysis["growth_process"]["name"] == scenario["expected_growth_process"]
        ), f"{scenario['id']}: expected growth process {scenario['expected_growth_process']}, got {analysis['growth_process']['name']}"


def test_golden_scenarios_forbidden_categories_absent_from_priorities():
    for scenario in load_scenarios():
        analysis = run_scenario(scenario)
        categories = {item.category for item in analysis["priorities"]}
        forbidden = set(scenario.get("forbidden_priority_categories", []))
        assert not (
            categories & forbidden
        ), f"{scenario['id']}: forbidden categories appeared in priorities: {categories & forbidden}"


def test_golden_scenarios_emit_required_guardrail_signals():
    for scenario in load_scenarios():
        analysis = run_scenario(scenario)
        combined_text = " ".join(
            [
                analysis["decision_line"],
                analysis["core_tension"],
                " ".join(analysis["avoid_now"]),
                " ".join(analysis["caveats"]),
                analysis["north_star"]["guardrail"],
                analysis["review_trigger"]["signal"],
            ]
        )
        for signal in scenario.get("required_text_signals", []):
            assert signal in combined_text, f"{scenario['id']}: missing required signal: {signal}"
