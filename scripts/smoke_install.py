#!/usr/bin/env python3
"""Smoke-test plugin installation artifacts for Claude Code, Hermes, and OpenClaw.

The checks intentionally avoid requiring the real host applications. They verify the
installable filesystem contract each platform consumes: skill metadata, shared
resources, command triggers, and a minimal CLI execution from the installed copy.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from cli import AUXILIARY_COMMANDS, PRIMARY_COMMANDS, SCENARIO_COMMANDS  # noqa: E402

COMMANDS = PRIMARY_COMMANDS + AUXILIARY_COMMANDS + SCENARIO_COMMANDS
EXPECTED_VERSION = (ROOT_DIR / "VERSION").read_text(encoding="utf-8").strip()
SHARED_DIRS = ["knowledge", "references", "scripts"]
SHARED_FILES = ["requirements.txt", "manifest.json"]


class SmokeError(AssertionError):
    """Raised when a smoke check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeError(message)


def require_path(path: Path, label: str) -> None:
    require(path.exists(), f"missing {label}: {path}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_cli_from_install(skill_dir: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "scripts/cli.py",
            "fast-scan",
            "test installation",
            "--industry",
            "saas",
            "--stage",
            "0-1",
            "--problem",
            "acquisition",
        ],
        cwd=skill_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    require("Fast Scan" in result.stdout, "installed CLI did not return fast-scan output")


def verify_trigger_contract(skill_file: Path, platform: str) -> None:
    content = read(skill_file)
    require(f"version: {EXPECTED_VERSION}" in content, f"{platform} skill version is not {EXPECTED_VERSION}")
    for command in COMMANDS:
        require(f"/omg-{command}" in content, f"{platform} skill missing trigger /omg-{command}")


def verify_shared_resources(skill_dir: Path, platform: str) -> None:
    require_path(skill_dir / "SKILL.md", f"{platform} SKILL.md")
    for dirname in SHARED_DIRS:
        require_path(skill_dir / dirname, f"{platform} {dirname}")
    require_path(skill_dir / "requirements.txt", f"{platform} requirements.txt")
    require_path(skill_dir / "manifest.json", f"{platform} manifest.json")
    run_cli_from_install(skill_dir)


def smoke_claude() -> None:
    with tempfile.TemporaryDirectory(prefix="omg-claude-home-") as home:
        env = os.environ.copy()
        env["HOME"] = home
        result = subprocess.run(
            ["bash", str(ROOT_DIR / "scripts" / "install.sh")],
            cwd=ROOT_DIR,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        require(result.returncode == 0, result.stdout + result.stderr)

        skills_root = Path(home) / ".claude" / "skills"
        skill_dir = skills_root / "oh-my-growth"
        alias = skills_root / "omg"
        verify_shared_resources(skill_dir, "claude")
        require(alias.is_symlink(), "Claude /omg alias is not a symlink")
        require(alias.resolve() == skill_dir.resolve(), "Claude /omg alias points to the wrong target")

        for command in COMMANDS:
            command_dir = skills_root / f"omg-{command}"
            require_path(command_dir / "SKILL.md", f"Claude shortcut /omg-{command}")
            shortcut = read(command_dir / "SKILL.md")
            require(f"/omg-{command}" in shortcut, f"Claude shortcut missing /omg-{command} docs")
            require_path(command_dir / "manifest.json", f"Claude shortcut /omg-{command} manifest.json")
            for dirname in ["knowledge", "scripts", "agents", "references"]:
                require((command_dir / dirname).is_symlink(), f"Claude shortcut /omg-{command} missing {dirname} symlink")


def copy_platform_package(platform: str, target: Path) -> Path:
    skill_dir = target / platform / "oh-my-growth"
    skill_dir.mkdir(parents=True)
    shutil.copy2(ROOT_DIR / platform / "SKILL.md", skill_dir / "SKILL.md")
    for dirname in SHARED_DIRS:
        shutil.copytree(ROOT_DIR / dirname, skill_dir / dirname)
    for filename in SHARED_FILES:
        shutil.copy2(ROOT_DIR / filename, skill_dir / filename)
    return skill_dir


def smoke_portable_platform(platform: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"omg-{platform}-") as tmp:
        skill_dir = copy_platform_package(platform, Path(tmp))
        verify_trigger_contract(skill_dir / "SKILL.md", platform)
        verify_shared_resources(skill_dir, platform)


def run(platforms: Iterable[str]) -> None:
    for platform in platforms:
        if platform == "claude":
            smoke_claude()
        elif platform in {"hermes", "openclaw"}:
            smoke_portable_platform(platform)
        else:
            raise SmokeError(f"unknown platform: {platform}")
        print(f"✅ {platform} install smoke passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test oh-my-growth plugin installation artifacts.")
    parser.add_argument(
        "--platform",
        choices=["all", "claude", "hermes", "openclaw"],
        default="all",
        help="Platform smoke test to run.",
    )
    args = parser.parse_args()

    platforms = ["claude", "hermes", "openclaw"] if args.platform == "all" else [args.platform]
    try:
        run(platforms)
    except SmokeError as error:
        print(f"❌ Install smoke failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
