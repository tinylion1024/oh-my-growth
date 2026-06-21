#!/usr/bin/env python3
"""Aggregate feedback logs into weekly insight reports."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List


ROOT_DIR = Path(__file__).resolve().parent.parent


def load_entries(feedback_dir: Path) -> List[Dict[str, Any]]:
    logs_dir = feedback_dir / "logs"
    scan_dirs = [logs_dir / "real"] if (logs_dir / "real").exists() else [logs_dir]
    entries: List[Dict[str, Any]] = []
    for scan_dir in scan_dirs:
        for path in sorted(scan_dir.rglob("*.json")):
            if path.name == "example-feedback.json":
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                entries.append(payload)
    return entries


def count_items(values: Iterable[str]) -> List[tuple[str, int]]:
    counter = Counter(item for item in values if item)
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))


def format_mode_table(entries: List[Dict[str, Any]]) -> str:
    bucket: Dict[str, List[int]] = defaultdict(list)
    for entry in entries:
        mode = str(entry.get("input_summary", {}).get("mode", "Unknown")).strip() or "Unknown"
        stars = int(entry.get("rating", {}).get("stars", 0) or 0)
        bucket[mode].append(stars)

    lines = ["| Mode | Count | Avg Stars |", "|------|------:|----------:|"]
    for mode, stars in sorted(bucket.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.append(f"| {mode} | {len(stars)} | {mean(stars):.1f} |")
    return "\n".join(lines)


def top_texts(entries: List[Dict[str, Any]], key_path: List[str], limit: int = 5) -> List[tuple[str, int]]:
    values: List[str] = []
    for entry in entries:
        current: Any = entry
        for key in key_path:
            if not isinstance(current, dict):
                current = {}
                break
            current = current.get(key, {})
        if isinstance(current, str):
            values.append(current.strip())
    return count_items(values)[:limit]


def build_weekly_report(entries: List[Dict[str, Any]], week: str) -> str:
    stars = [int(entry.get("rating", {}).get("stars", 0) or 0) for entry in entries if int(entry.get("rating", {}).get("stars", 0) or 0) > 0]
    helpful = sum(1 for entry in entries if bool(entry.get("qualitative", {}).get("will_act")))
    case_relevant = sum(1 for entry in entries if bool(entry.get("case_feedback", {}).get("relevant")))
    agent_counts = count_items(
        agent
        for entry in entries
        for agent in (entry.get("output_metadata", {}).get("agents_used", []) or [])
        if isinstance(agent, str)
    )
    suggestions = top_texts(entries, ["qualitative", "suggestions"])
    missing = top_texts(entries, ["qualitative", "missing_info"])

    lines = [
        f"# Feedback Weekly Report - {week}",
        "",
        "## Summary",
        "",
        f"- Total feedback: {len(entries)}",
        f"- Average stars: {mean(stars):.1f}" if stars else "- Average stars: n/a",
        f"- Will act rate: {helpful}/{len(entries)}",
        f"- Case relevance rate: {case_relevant}/{len(entries)}",
        "",
        "## By Mode",
        "",
        format_mode_table(entries),
        "",
        "## Top Suggestions",
        "",
    ]
    if suggestions:
        for text, count in suggestions:
            lines.append(f"- {text} ({count})")
    else:
        lines.append("- No suggestions recorded")

    lines.extend(["", "## Common Missing Info", ""])
    if missing:
        for text, count in missing:
            lines.append(f"- {text} ({count})")
    else:
        lines.append("- No missing-info entries recorded")

    lines.extend(["", "## Agent Usage", ""])
    if agent_counts:
        for agent, count in agent_counts[:6]:
            lines.append(f"- {agent} ({count})")
    else:
        lines.append("- No agent usage captured")

    return "\n".join(lines) + "\n"


def build_patterns_report(entries: List[Dict[str, Any]]) -> str:
    suggestion_counts = count_items(
        entry.get("qualitative", {}).get("suggestions", "").strip()
        for entry in entries
        if isinstance(entry.get("qualitative", {}).get("suggestions", ""), str)
    )
    missing_counts = count_items(
        entry.get("qualitative", {}).get("missing_info", "").strip()
        for entry in entries
        if isinstance(entry.get("qualitative", {}).get("missing_info", ""), str)
    )

    lines = [
        "# Feedback Patterns",
        "",
        "## Most Common Suggestions",
        "",
    ]
    if suggestion_counts:
        for text, count in suggestion_counts[:5]:
            lines.append(f"- {text} ({count})")
    else:
        lines.append("- No suggestion patterns found")

    lines.extend(["", "## Most Common Missing Info", ""])
    if missing_counts:
        for text, count in missing_counts[:5]:
            lines.append(f"- {text} ({count})")
    else:
        lines.append("- No missing-info patterns found")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate feedback logs into weekly reports.")
    parser.add_argument("--feedback-dir", default=str(ROOT_DIR / "feedback"))
    parser.add_argument("--output-dir", default=str(ROOT_DIR / "feedback" / "analysis"))
    parser.add_argument("--week", default="")
    args = parser.parse_args()

    feedback_dir = Path(args.feedback_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    entries = load_entries(feedback_dir)
    if not entries:
        print("No feedback entries found.")
        return 0

    week = args.week or f"{date.today().isocalendar().year}-W{date.today().isocalendar().week:02d}"
    weekly_report = output_dir / f"weekly-report-{week}.md"
    patterns_report = output_dir / "patterns.md"

    weekly_report.write_text(build_weekly_report(entries, week), encoding="utf-8")
    patterns_report.write_text(build_patterns_report(entries), encoding="utf-8")

    print(f"Feedback aggregated: {len(entries)} entries -> {weekly_report}")
    print(f"Patterns report -> {patterns_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
