#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from cli import AUXILIARY_COMMANDS, PRIMARY_COMMANDS, SCENARIO_COMMANDS  # noqa: E402
from decision_tracking import collect_pending  # noqa: E402
from strategy_brain import StrategyBrain  # noqa: E402
from verify_report import verify_report  # noqa: E402

COMMANDS = PRIMARY_COMMANDS + AUXILIARY_COMMANDS + SCENARIO_COMMANDS
EXPECTED_VERSION = (ROOT_DIR / "VERSION").read_text(encoding="utf-8").strip()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_install_smoke_script_validates_all_plugin_platforms():
    result = run("scripts/smoke_install.py", "--platform", "all")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "claude install smoke passed" in result.stdout
    assert "hermes install smoke passed" in result.stdout
    assert "openclaw install smoke passed" in result.stdout


def test_platform_skill_contracts_match_cli_commands():
    expected = {f"/omg-{command}" for command in COMMANDS}
    for path in [ROOT_DIR / "SKILL.md", ROOT_DIR / "hermes" / "SKILL.md", ROOT_DIR / "openclaw" / "SKILL.md"]:
        content = path.read_text(encoding="utf-8")
        for trigger in expected:
            assert trigger in content, f"{path} missing {trigger}"

    for command in COMMANDS:
        skill_path = ROOT_DIR / "skills" / f"omg-{command}.md"
        assert skill_path.exists(), f"missing shortcut skill for {command}"
        content = skill_path.read_text(encoding="utf-8")
        assert f"name: omg-{command}" in content
        assert f"version: {EXPECTED_VERSION}" in content
        assert "parent: oh-my-growth" in content

    manifest = json.loads((ROOT_DIR / "manifest.json").read_text(encoding="utf-8"))
    for relative_path in manifest["entry_points"].values():
        assert (ROOT_DIR / relative_path).exists(), f"missing manifest entry point {relative_path}"
    for relative_path in manifest["structure"].values():
        assert (ROOT_DIR / relative_path).exists(), f"missing manifest structure path {relative_path}"


def assert_feedback_schema(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["feedback_id"]
    assert payload["timestamp"]
    assert payload["session_id"]
    assert payload["input_summary"]["mode"]
    assert payload["input_summary"]["problem_type"]
    assert 1 <= int(payload["rating"]["stars"]) <= 5
    assert payload["rating"]["usefulness"]
    assert isinstance(payload["qualitative"]["will_act"], bool)
    assert isinstance(payload["case_feedback"]["relevant"], bool)
    assert isinstance(payload["case_feedback"]["want_more"], bool)
    assert isinstance(payload["output_metadata"]["agents_used"], list)
    return payload


def test_feedback_sample_pool_is_seeded_and_schema_valid():
    assert (ROOT_DIR / "feedback" / "logs" / "real" / "README.md").exists()
    assert (ROOT_DIR / "feedback" / "analysis" / "README.md").exists()

    sample_paths = sorted((ROOT_DIR / "tests" / "fixtures" / "feedback").glob("valid-feedback-*.json"))
    sample_paths.append(ROOT_DIR / "feedback" / "logs" / "example-feedback.json")
    payloads = [assert_feedback_schema(path) for path in sample_paths]

    covered_modes = {payload["input_summary"]["mode"] for payload in payloads}
    covered_problems = {payload["input_summary"]["problem_type"] for payload in payloads}
    assert {"Fast Scan", "Decision BRD", "Strategy Design", "Weekly"} <= covered_modes
    assert {"acquisition", "retention", "monetization", "referral"} <= covered_problems


def test_decision_sample_pool_exercises_pending_and_tracked_states():
    assert (ROOT_DIR / "decisions" / "records" / "README.md").exists()
    assert (ROOT_DIR / "decisions" / "summary" / "README.md").exists()

    with tempfile.TemporaryDirectory() as tmp:
        decisions_dir = Path(tmp) / "decisions"
        (decisions_dir / "2026" / "01").mkdir(parents=True)
        shutil.copy2(
            ROOT_DIR / "tests" / "fixtures" / "decisions" / "decision-pending.md",
            decisions_dir / "2026" / "01" / "decision-20260101-pending.md",
        )
        shutil.copy2(
            ROOT_DIR / "tests" / "fixtures" / "decisions" / "decision-tracked.md",
            decisions_dir / "2026" / "01" / "decision-20260102-tracked.md",
        )
        shutil.copy2(
            ROOT_DIR / "tests" / "fixtures" / "decisions" / "decision-tracked-tracking.md",
            decisions_dir / "2026" / "01" / "decision-20260102-tracked-tracking.md",
        )

        pending = collect_pending(decisions_dir, today=date(2026, 6, 18), threshold_days=30)
        ids = {item.decision_id for item in pending}
        assert "decision-20260101-pending" in ids
        assert "decision-20260102-tracked" not in ids


def test_output_quality_fixtures_and_generated_report_gate():
    valid = verify_report((ROOT_DIR / "tests" / "fixtures" / "output-quality" / "report-valid-full.md").read_text(encoding="utf-8"))
    assert valid.valid is True
    assert valid.score >= 80

    invalid = verify_report((ROOT_DIR / "tests" / "fixtures" / "output-quality" / "report-missing-section.md").read_text(encoding="utf-8"))
    assert invalid.valid is False
    assert invalid.sections_missing

    analysis = StrategyBrain().analyze(
        "SaaS产品如何获取首批1000用户",
        {"industry": "saas", "stage": "0-1", "problem_type": "acquisition", "budget": "low"},
        mode="diagnose",
    )
    assert analysis["evidence_chain"]
    assert analysis["avoid_now"]
    assert analysis["experiment"]["success_signals"]
    assert analysis["experiment"]["stop_signals"]
    assert analysis["review_trigger"]["signal"]
