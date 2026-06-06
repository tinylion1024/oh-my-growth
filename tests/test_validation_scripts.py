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
