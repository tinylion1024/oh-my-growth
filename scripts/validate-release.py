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


def load_index_count(index_name: str, payload_key: str, metadata_key: str) -> int:
    index_path = ROOT_DIR / "knowledge" / "indexes" / index_name
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    items = payload.get(payload_key, [])
    metadata_total = payload.get("metadata", {}).get(metadata_key)
    if metadata_total != len(items):
        raise ValueError(f"{index_name} metadata {metadata_key} {metadata_total} != {len(items)}")
    return len(items)


def main() -> int:
    issues = []
    version = (ROOT_DIR / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads((ROOT_DIR / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != version:
        issues.append(f"manifest.json version {manifest.get('version')} != {version}")

    expected_knowledge_counts = {
        "cases": load_index_count("cases-index.json", "cases", "total_cases"),
        "weapons": load_index_count("weapons-index.json", "weapons", "total_weapons"),
        "theories": load_index_count("theories-index.json", "theories", "total_theories"),
        "failures": load_index_count("failures-index.json", "failures", "total_failures"),
        "method_packs": load_index_count(
            "method-packs-index.json",
            "method_packs",
            "total_method_packs",
        ),
    }
    knowledge_base = manifest.get("knowledge_base", {})
    for key, expected in expected_knowledge_counts.items():
        if knowledge_base.get(key) != expected:
            issues.append(f"manifest.json knowledge_base.{key} {knowledge_base.get(key)} != {expected}")

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

    pyproject_content = (ROOT_DIR / "pyproject.toml").read_text(encoding="utf-8")
    if 'growth = "scripts.cli:main"' not in pyproject_content:
        issues.append("pyproject.toml is missing the public `growth` console script")
    if 'packages = [' not in pyproject_content or '"scripts"' not in pyproject_content:
        issues.append("pyproject.toml must explicitly package the scripts modules")
    if '"knowledge"' not in pyproject_content:
        issues.append("pyproject.toml must package the knowledge module")
    if "[tool.setuptools.package-data]" not in pyproject_content:
        issues.append("pyproject.toml must ship knowledge files as package data")

    release_check = (ROOT_DIR / "scripts" / "release-check.sh").read_text(encoding="utf-8")
    if "scripts/smoke_wheel.py" not in release_check:
        issues.append("release-check.sh must run the wheel smoke test")

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
    if "--platform" not in install_script:
        issues.append("scripts/install.sh is missing the platform selection contract")
    for platform in ["claude", "openclaw", "hermes"]:
        if platform not in install_script:
            issues.append(f"scripts/install.sh is missing platform {platform}")
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
        if path.name == "README.md":
            expected_phrases = [
                f"{expected_knowledge_counts['cases']} cases",
                f"{expected_knowledge_counts['weapons']} plays",
                f"{expected_knowledge_counts['method_packs']} method packs",
            ]
        else:
            expected_phrases = [
                f"{expected_knowledge_counts['cases']} 个案例",
                f"{expected_knowledge_counts['weapons']} 种玩法",
                f"{expected_knowledge_counts['method_packs']} 个增长方法包",
            ]
        for phrase in expected_phrases:
            if phrase not in content:
                issues.append(f"{path.name} is missing knowledge count phrase `{phrase}`")

    if issues:
        print("❌ Release metadata validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print(f"✅ Release metadata validated successfully (v{version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
