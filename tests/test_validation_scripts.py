#!/usr/bin/env python3

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
    update_result = run_script("scripts/update-indexes.py")
    assert update_result.returncode == 0, update_result.stderr
    assert "Indexes updated:" in update_result.stdout

    validate_result = run_script("scripts/validate-indexes.py")
    assert validate_result.returncode == 0, validate_result.stdout + validate_result.stderr
    assert "All indexes validated successfully" in validate_result.stdout


def test_validate_agents_without_external_yaml_dependency():
    result = run_script("scripts/validate-agents.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All agents validated successfully" in result.stdout
