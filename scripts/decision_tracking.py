#!/usr/bin/env python3
"""Scan decision records and generate pending tracking reminders."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, List, Optional


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class DecisionItem:
    path: Path
    decision_id: str
    decision_date: date
    age_days: int
    tracking_path: Path


def parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        return {}
    lines = content.splitlines()
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def parse_date(path: Path, frontmatter: dict[str, str]) -> Optional[date]:
    raw = frontmatter.get("date")
    if raw:
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            pass
    match = re.search(r"decision-(\d{8})", path.name)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d").date()
    return None


def decision_id_for(path: Path, frontmatter: dict[str, str]) -> str:
    return frontmatter.get("decision_id") or path.stem


def iter_decision_files(decisions_dir: Path) -> Iterable[Path]:
    for path in sorted(decisions_dir.rglob("*.md")):
        if "templates" in path.parts or "summary" in path.parts:
            continue
        if path.name.endswith("-tracking.md") or path.name == "README.md":
            continue
        yield path


def collect_pending(decisions_dir: Path, today: date, threshold_days: int) -> List[DecisionItem]:
    pending: List[DecisionItem] = []
    for path in iter_decision_files(decisions_dir):
        content = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        decision_date = parse_date(path, frontmatter)
        if decision_date is None:
            continue
        tracking_path = path.with_name(f"{path.stem}-tracking.md")
        if tracking_path.exists():
            continue
        age_days = (today - decision_date).days
        if age_days >= threshold_days:
            pending.append(
                DecisionItem(
                    path=path,
                    decision_id=decision_id_for(path, frontmatter),
                    decision_date=decision_date,
                    age_days=age_days,
                    tracking_path=tracking_path,
                )
            )
    return sorted(pending, key=lambda item: (-item.age_days, item.path.name))


def render_report(items: List[DecisionItem], today: date, threshold_days: int) -> str:
    def display_path(path: Path) -> str:
        try:
            return str(path.relative_to(ROOT_DIR))
        except ValueError:
            return str(path)

    lines = [
        "# Pending Decision Tracking",
        "",
        f"- As of: {today.isoformat()}",
        f"- Threshold days: {threshold_days}",
        f"- Pending tracking: {len(items)}",
        "",
        "## Items",
        "",
    ]
    if not items:
        lines.append("- None")
        lines.extend(["", "Recommended next step: no pending tracking items."])
        return "\n".join(lines) + "\n"

    lines.extend(["| Decision ID | Decision Date | Age (days) | File |", "|---|---:|---:|---|"])
    for item in items:
        lines.append(
            f"| {item.decision_id} | {item.decision_date.isoformat()} | {item.age_days} | {display_path(item.path)} |"
        )
    lines.extend(
        [
            "",
            "Recommended next step: create a tracking note for the oldest pending decision first.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate pending decision tracking reminders.")
    parser.add_argument("--decisions-dir", default=str(ROOT_DIR / "decisions"))
    parser.add_argument("--output-file", default="")
    parser.add_argument("--today", default="")
    parser.add_argument("--threshold-days", type=int, default=30)
    args = parser.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    decisions_dir = Path(args.decisions_dir)
    pending = collect_pending(decisions_dir, today=today, threshold_days=args.threshold_days)
    report = render_report(pending, today=today, threshold_days=args.threshold_days)

    output_file = Path(args.output_file) if args.output_file else decisions_dir / "summary" / "pending-tracking.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report, encoding="utf-8")

    print(f"Pending tracking: {len(pending)}")
    print(f"Report written: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
