#!/usr/bin/env python3
"""Validate markdown structure, local links, and mode consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from cli import AUXILIARY_COMMANDS, PRIMARY_COMMANDS, SCENARIO_COMMANDS, VIEW_CHOICES  # noqa: E402

MARKDOWN_ROOTS = [
    ROOT_DIR / "README.md",
    ROOT_DIR / "SKILL.md",
    ROOT_DIR / "references",
    ROOT_DIR / "knowledge" / "failures",
    ROOT_DIR / "tests" / "README.md",
    ROOT_DIR / "tests" / "e2e" / "README.md",
    ROOT_DIR / "tests" / "e2e" / "test-scenarios.md",
]
IGNORED_PREFIXES = ("http://", "https://", "mailto:", "#", "plugin://")
PRIMARY_DOC_FILES = [
    ROOT_DIR / "README.md",
    ROOT_DIR / "SKILL.md",
    ROOT_DIR / "tests" / "README.md",
    ROOT_DIR / "tests" / "e2e" / "README.md",
    ROOT_DIR / "tests" / "e2e" / "test-scenarios.md",
]
LEGACY_UNSUPPORTED_MODES = {"audit"}


def iter_markdown_files() -> List[Path]:
    files: List[Path] = []
    for item in MARKDOWN_ROOTS:
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            files.extend(sorted(item.rglob("*.md")))
    return files


def check_fenced_blocks(path: Path, content: str, issues: List[str]) -> None:
    if content.count("```") % 2 != 0:
        issues.append(f"{path}: unbalanced fenced code blocks")


def check_heading_order(path: Path, content: str, issues: List[str]) -> None:
    if path.name == "README.md":
        return
    previous = 0
    for line in content.splitlines():
        match = re.match(r"^(#{1,6})\s+\S", line)
        if not match:
            continue
        level = len(match.group(1))
        if previous and level > previous + 2:
            issues.append(f"{path}: heading jumps from H{previous} to H{level}")
            return
        previous = level


def check_local_links(path: Path, content: str, issues: List[str]) -> None:
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    for raw_target in links:
        target = raw_target.strip().strip("<>")
        if target.startswith(IGNORED_PREFIXES):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        if target.endswith(".svg") and target.startswith("./"):
            continue
        target_path = (path.parent / target).resolve()
        if not target_path.exists():
            issues.append(f"{path}: broken local link -> {raw_target}")


def check_mode_consistency(issues: List[str]) -> None:
    readme = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
    skill = (ROOT_DIR / "SKILL.md").read_text(encoding="utf-8")
    for command in PRIMARY_COMMANDS:
        if f"`{command}`" not in readme:
            issues.append(f"README.md: missing command reference `{command}`")
    for command in AUXILIARY_COMMANDS:
        if f"`{command}`" not in readme and command != "validate":
            issues.append(f"README.md: missing auxiliary command reference `{command}`")
    for view in ["weekly", "experiment-card", "decision-memo", "qbr"]:
        if f"`{view}`" not in readme:
            issues.append(f"README.md: missing view reference `{view}`")
    if "## 七个核心入口" not in skill:
        issues.append("SKILL.md: expected '## 七个核心入口'")
    if "### 七个核心入口" not in readme:
        issues.append("README.md: expected '### 七个核心入口'")

    allowed_modes = set(PRIMARY_COMMANDS + AUXILIARY_COMMANDS + SCENARIO_COMMANDS + VIEW_CHOICES)
    for path in PRIMARY_DOC_FILES:
        content = path.read_text(encoding="utf-8")
        for legacy_mode in LEGACY_UNSUPPORTED_MODES:
            if re.search(rf"`{re.escape(legacy_mode)}`|\b{re.escape(legacy_mode)}\b", content):
                issues.append(f"{path.relative_to(ROOT_DIR)}: references unsupported legacy mode `{legacy_mode}`")
        for token in re.findall(r"`([a-z][a-z-]+)`", content):
            if token in {"json", "report", "operator", "executive"}:
                continue
            if token not in allowed_modes and token not in {"python", "growth"}:
                issues.append(f"{path.relative_to(ROOT_DIR)}: command/view `{token}` is not backed by the CLI contract")


def main() -> int:
    issues: List[str] = []
    for path in iter_markdown_files():
        content = path.read_text(encoding="utf-8")
        check_fenced_blocks(path, content, issues)
        check_heading_order(path, content, issues)
        check_local_links(path, content, issues)

    check_mode_consistency(issues)

    if issues:
        print("❌ Documentation validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("✅ Documentation structure and links validated successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
