#!/usr/bin/env python3
"""Lightweight test runner using only the Python standard library."""

import argparse
import importlib.util
import traceback
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import List

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_DIR = ROOT_DIR / "tests"
RESULTS_DIR = TEST_DIR / "results"


@dataclass
class TestOutcome:
    module: str
    test_name: str
    passed: bool
    error: str = ""


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load test module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover_tests(module: ModuleType):
    for name in dir(module):
        if name.startswith("test_"):
            candidate = getattr(module, name)
            if callable(candidate):
                yield name, candidate


def write_report(outcomes: List[TestOutcome], report_path: Path):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    passed = sum(1 for outcome in outcomes if outcome.passed)
    failed = len(outcomes) - passed
    pass_rate = (passed / len(outcomes) * 100) if outcomes else 0.0

    lines = [
        "# Test Report",
        "",
        "## Summary",
        "",
        f"- Total Tests: {len(outcomes)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Pass Rate: {pass_rate:.1f}%",
        "",
        "## Details",
        "",
    ]

    for outcome in outcomes:
        status = "PASSED" if outcome.passed else "FAILED"
        lines.append(f"- `{outcome.module}::{outcome.test_name}` - {status}")
        if outcome.error:
            lines.append("")
            lines.append("```text")
            lines.append(outcome.error.rstrip())
            lines.append("```")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run repository test modules.")
    parser.add_argument(
        "--report",
        default="",
        help="Optional markdown report output path",
    )
    args = parser.parse_args()

    outcomes: List[TestOutcome] = []
    for test_file in sorted(TEST_DIR.glob("test_*.py")):
        module = load_module(test_file)
        for test_name, test_callable in discover_tests(module):
            try:
                test_callable()
                outcomes.append(TestOutcome(test_file.name, test_name, True))
                print(f"✅ {test_file.name}::{test_name}")
            except Exception:
                outcomes.append(
                    TestOutcome(
                        test_file.name,
                        test_name,
                        False,
                        traceback.format_exc(),
                    )
                )
                print(f"❌ {test_file.name}::{test_name}")

    if args.report:
        write_report(outcomes, Path(args.report))

    failed = [outcome for outcome in outcomes if not outcome.passed]
    print("")
    print(f"Total: {len(outcomes)}  Passed: {len(outcomes) - len(failed)}  Failed: {len(failed)}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
