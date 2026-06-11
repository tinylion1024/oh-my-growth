#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def run_script(path):
    return subprocess.run(
        [sys.executable, path],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_update_indexes_and_validate_indexes():
    enrich_result = run_script("scripts/enrich-weapons.py")
    assert enrich_result.returncode == 0, enrich_result.stderr
    assert "Enriched 111 weapon docs" in enrich_result.stdout

    update_result = run_script("scripts/update-indexes.py")
    assert update_result.returncode == 0, update_result.stderr
    assert "Indexes updated:" in update_result.stdout

    weapons_payload = json.loads((ROOT_DIR / "knowledge/indexes/weapons-index.json").read_text(encoding="utf-8"))
    assert all(weapon.get("file") for weapon in weapons_payload["weapons"])
    assert all("growth_process" in weapon for weapon in weapons_payload["weapons"])
    assert all("journey_stage" in weapon for weapon in weapons_payload["weapons"])
    assert all("marketplace_side" in weapon for weapon in weapons_payload["weapons"])
    assert all("failure_refs" in weapon for weapon in weapons_payload["weapons"])
    assert {weapon["category"] for weapon in weapons_payload["weapons"]} == {
        "cold-start",
        "viral-referral",
        "content-growth",
        "community",
        "plg",
        "retention",
        "monetization",
        "paid-ads",
        "brand",
        "b2b-sales",
    }

    cases_payload = json.loads((ROOT_DIR / "knowledge/indexes/cases-index.json").read_text(encoding="utf-8"))
    assert all("growth_process" in case for case in cases_payload["cases"])
    assert all("journey_stage" in case for case in cases_payload["cases"])
    assert all("marketplace_side" in case for case in cases_payload["cases"])
    assert all("failure_refs" in case for case in cases_payload["cases"])
    assert any(case.get("company_type") == "marketplace" and case.get("marketplace_side") for case in cases_payload["cases"])
    assert any(case.get("company_type") == "local-services" for case in cases_payload["cases"])

    theories_payload = json.loads((ROOT_DIR / "knowledge/indexes/theories-index.json").read_text(encoding="utf-8"))
    assert all("growth_process" in theory for theory in theories_payload["theories"])
    assert all("journey_stage" in theory for theory in theories_payload["theories"])
    assert all("marketplace_side" in theory for theory in theories_payload["theories"])
    assert all("failure_refs" in theory for theory in theories_payload["theories"])

    failures_payload = json.loads((ROOT_DIR / "knowledge/indexes/failures-index.json").read_text(encoding="utf-8"))
    assert failures_payload["metadata"]["total_failures"] >= 3
    assert all("problem_types" in failure for failure in failures_payload["failures"])
    assert all("summary" in failure for failure in failures_payload["failures"])

    readme_content = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
    assert "[DeepSeek（深度求索）- AI开源突围战](<./knowledge/cases/china/deepseek.md>)" in readme_content
    assert "[Beta邀请制](<./knowledge/weapons/01-cold-start/weapons/007-Beta邀请制.md>)" in readme_content
    assert "[Landing Page注册](<./knowledge/weapons/01-cold-start/weapons/008-Landing Page注册.md>)" in readme_content

    validate_weapons_result = run_script("scripts/validate-weapons.py")
    assert validate_weapons_result.returncode == 0, validate_weapons_result.stdout + validate_weapons_result.stderr
    assert "weapon docs passed quality validation" in validate_weapons_result.stdout

    validate_result = run_script("scripts/validate-indexes.py")
    assert validate_result.returncode == 0, validate_result.stdout + validate_result.stderr
    assert "All indexes validated successfully" in validate_result.stdout


def test_validate_agents_without_external_yaml_dependency():
    result = run_script("scripts/validate-agents.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All agents validated successfully" in result.stdout


def test_validate_docs_checks_structure_and_links():
    result = run_script("scripts/validate-docs.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Documentation structure and links validated successfully" in result.stdout


def test_growth_framework_guides_exist_and_are_sanitized():
    expected_guides = {
        "README.md",
        "stage-diagnosis.md",
        "north-star-metric.md",
        "user-journey-diagnosis.md",
        "growth-loop.md",
        "experiment-design.md",
        "attribution-and-identity.md",
    }
    guides_dir = ROOT_DIR / "knowledge" / "guides"
    assert expected_guides.issubset({path.name for path in guides_dir.iterdir() if path.is_file()})

    public_paths = [
        ROOT_DIR / "README.md",
        ROOT_DIR / "SKILL.md",
        ROOT_DIR / "references",
        ROOT_DIR / "knowledge" / "guides",
        ROOT_DIR / "knowledge" / "modules",
    ]

    for base in public_paths:
        if base.is_file():
            contents = base.read_text(encoding="utf-8")
            assert "UGS-P" not in contents
            assert "UGS" not in contents
            continue

        for path in base.rglob("*.md"):
            contents = path.read_text(encoding="utf-8")
            assert "UGS-P" not in contents, path
            assert "UGS" not in contents, path


def test_failure_mode_guides_exist():
    failures_dir = ROOT_DIR / "knowledge" / "failures"
    expected = {
        "README.md",
        "acquisition-anti-patterns.md",
        "referral-failure-modes.md",
        "retention-failure-modes.md",
    }
    assert failures_dir.exists()
    assert expected.issubset({path.name for path in failures_dir.iterdir() if path.is_file()})
