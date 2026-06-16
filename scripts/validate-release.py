#!/usr/bin/env python3
"""Validate release metadata and public command contracts."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from cli import AUXILIARY_COMMANDS, PRIMARY_COMMANDS, SCENARIO_COMMANDS  # noqa: E402


def extract_version(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^\s*version\s*[:=]\s*[\"']?([^\"'\s]+)", content)
    if not match:
        raise ValueError(f"missing version field: {path.relative_to(ROOT_DIR)}")
    return match.group(1)


def count_scripted_checks() -> int:
    total = 0
    for path in sorted((ROOT_DIR / "tests").glob("test_*.py")):
        module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        total += sum(
            1
            for node in module.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    return total


def main() -> int:
    issues = []
    version = (ROOT_DIR / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads((ROOT_DIR / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != version:
        issues.append(f"manifest.json version {manifest.get('version')} != {version}")

    scripted_checks = count_scripted_checks()
    testing = manifest.get("testing", {})
    if testing.get("scripted_checks") != scripted_checks:
        issues.append(
            f"manifest.json scripted_checks {testing.get('scripted_checks')} != {scripted_checks}"
        )
    if testing.get("pass_rate") != f"{scripted_checks}/{scripted_checks}":
        issues.append("manifest.json pass_rate is inconsistent with discovered tests")

    versioned_files = [
        ROOT_DIR / "pyproject.toml",
        ROOT_DIR / "SKILL.md",
        ROOT_DIR / "openclaw" / "SKILL.md",
        ROOT_DIR / "hermes" / "SKILL.md",
        *sorted((ROOT_DIR / "skills").glob("*.md")),
    ]
    for path in versioned_files:
        try:
            file_version = extract_version(path)
        except ValueError as error:
            issues.append(str(error))
            continue
        if file_version != version:
            issues.append(f"{path.relative_to(ROOT_DIR)} version {file_version} != {version}")

    commands = PRIMARY_COMMANDS + AUXILIARY_COMMANDS + SCENARIO_COMMANDS
    expected_skill_names = {f"omg-{command}" for command in commands}
    actual_skill_names = {path.stem for path in (ROOT_DIR / "skills").glob("*.md")}
    if actual_skill_names != expected_skill_names:
        issues.append(
            "command skill set mismatch: "
            f"missing={sorted(expected_skill_names - actual_skill_names)}, "
            f"extra={sorted(actual_skill_names - expected_skill_names)}"
        )

    install_script = (ROOT_DIR / "scripts" / "install.sh").read_text(encoding="utf-8")
    if f"version: {version}" not in install_script:
        issues.append("scripts/install.sh fallback skill version is inconsistent")
    for command in commands:
        if f'"{command}"' not in install_script:
            issues.append(f"scripts/install.sh is missing command {command}")
    if "/oh-my-growth " in install_script or re.search(r"/omg\s+[a-z]", install_script):
        issues.append("scripts/install.sh fallback docs use legacy command syntax")

    for path in [ROOT_DIR / "README.md", ROOT_DIR / "README_CN.md"]:
        content = path.read_text(encoding="utf-8")
        if f"version-{version}-blue" not in content:
            issues.append(f"{path.name} version badge is inconsistent")
        if f"tests-{scripted_checks}%2F{scripted_checks}%20passed" not in content:
            issues.append(f"{path.name} test badge is inconsistent")
        for command in commands:
            if f"`/omg-{command}`" not in content:
                issues.append(f"{path.name} is missing `/omg-{command}`")

    if issues:
        print("❌ Release metadata validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print(f"✅ Release metadata validated successfully (v{version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
