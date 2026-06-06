#!/usr/bin/env python3
"""Synchronize indexes and refresh README knowledge navigation blocks."""

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT_DIR / "knowledge" / "indexes"
WEAPON_SOURCE_DIR = ROOT_DIR / "knowledge" / "weapons"
README_PATH = ROOT_DIR / "README.md"
KNOWLEDGE_ROOT = ROOT_DIR / "knowledge"

CASE_INDEX_START = "<!-- AUTO-CASE-INDEX:START -->"
CASE_INDEX_END = "<!-- AUTO-CASE-INDEX:END -->"
WEAPON_INDEX_START = "<!-- AUTO-WEAPON-INDEX:START -->"
WEAPON_INDEX_END = "<!-- AUTO-WEAPON-INDEX:END -->"

CASE_REGION_TITLES = {
    "china": "中国案例",
    "overseas": "海外案例",
    "vertical": "垂直行业案例",
}

WEAPON_CATEGORY_BY_DIR = {
    "01-cold-start": "cold-start",
    "02-viral-referral": "viral-referral",
    "03-content-growth": "content-growth",
    "04-community": "community",
    "05-plg": "plg",
    "06-retention": "retention",
    "07-monetization": "monetization",
    "08-paid-ads": "paid-ads",
    "09-brand": "brand",
    "10-b2b-sales": "b2b-sales",
}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def parse_front_matter(path: Path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}

    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def replace_section(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    if not pattern.search(content):
        raise ValueError(f"Missing README marker pair: {start_marker} ... {end_marker}")
    return pattern.sub(replacement, content, count=1)


def markdown_link(label: str, target: str) -> str:
    return f"[{label}](<{target}>)"


def render_case_index(cases_payload):
    cases = cases_payload.get("cases", [])
    lines = [CASE_INDEX_START]

    for region_id in ["china", "overseas", "vertical"]:
        region_cases = sorted(
            [case for case in cases if case.get("region") == region_id],
            key=lambda item: item.get("name", ""),
        )
        title = CASE_REGION_TITLES[region_id]
        lines.extend(
            [
                "<details>",
                f"<summary>{title}（{len(region_cases)}）</summary>",
                "",
            ]
        )
        for case in region_cases:
            tactics = "、".join(case.get("tags", {}).get("tactics", [])[:3])
            suffix = f" · {case.get('evidence_tier', 'N/A')}级证据"
            if tactics:
                suffix += f" · {tactics}"
            target = f"./knowledge/{case['file']}"
            lines.append(f"- {markdown_link(case['name'], target)}{suffix}")
        lines.extend(["", "</details>", ""])

    lines.append(CASE_INDEX_END)
    return "\n".join(lines)


def render_weapon_index(weapons_payload):
    categories = weapons_payload.get("categories", [])
    weapons = weapons_payload.get("weapons", [])
    lines = [WEAPON_INDEX_START]

    for category in categories:
        category_id = category["id"]
        category_name = category["name"]
        category_weapons = sorted(
            [weapon for weapon in weapons if weapon.get("category") == category_id],
            key=lambda item: int(item.get("id", 0)),
        )
        lines.extend(
            [
                "<details>",
                f"<summary>{category_name}（{len(category_weapons)}）</summary>",
                "",
            ]
        )
        for weapon in category_weapons:
            file_path = weapon.get("file")
            label = weapon["name"]
            if file_path:
                label = markdown_link(label, f"./knowledge/{file_path}")
            effort = weapon.get("effort", "N/A")
            impact = weapon.get("impact", "N/A")
            evidence_tier = weapon.get("evidence_tier", "N/A")
            lines.append(
                f"- {label} · {effort} effort · {impact} impact · {evidence_tier}级证据"
            )
        lines.extend(["", "</details>", ""])

    lines.append(WEAPON_INDEX_END)
    return "\n".join(lines)


def sync_readme_indexes(cases_payload, weapons_payload):
    content = README_PATH.read_text(encoding="utf-8")
    content = replace_section(
        content,
        CASE_INDEX_START,
        CASE_INDEX_END,
        render_case_index(cases_payload),
    )
    content = replace_section(
        content,
        WEAPON_INDEX_START,
        WEAPON_INDEX_END,
        render_weapon_index(weapons_payload),
    )
    README_PATH.write_text(content, encoding="utf-8")


def sync_cases_index():
    path = INDEX_DIR / "cases-index.json"
    payload = load_json(path)
    payload["metadata"]["total_cases"] = len(payload.get("cases", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload


def sync_weapons_index():
    path = INDEX_DIR / "weapons-index.json"
    payload = load_json(path)

    source_by_id = {}
    for markdown_file in WEAPON_SOURCE_DIR.glob("**/weapons/*.md"):
        front_matter = parse_front_matter(markdown_file)
        weapon_id = str(front_matter.get("id", "")).strip()
        if not weapon_id:
            continue
        source_by_id[weapon_id] = {
            "front_matter": front_matter,
            "file": markdown_file.relative_to(KNOWLEDGE_ROOT).as_posix(),
            "category": WEAPON_CATEGORY_BY_DIR.get(markdown_file.parent.parent.name, ""),
        }

    category_counter = Counter()
    for weapon in payload.get("weapons", []):
        weapon_id = str(weapon.get("id", ""))
        source = source_by_id.get(weapon_id, {})
        front_matter = source.get("front_matter", {})
        if front_matter.get("name"):
            weapon["name"] = front_matter["name"]
        if front_matter.get("description"):
            weapon["description"] = front_matter["description"]
        if source.get("file"):
            weapon["file"] = source["file"]
        if source.get("category"):
            weapon["category"] = source["category"]
        category_counter[weapon.get("category", "")] += 1

    for category in payload.get("categories", []):
        category["count"] = category_counter.get(category.get("id", ""), 0)

    payload["metadata"]["total_weapons"] = len(payload.get("weapons", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload


def sync_theories_index():
    path = INDEX_DIR / "theories-index.json"
    payload = load_json(path)
    payload["metadata"]["total_theories"] = len(payload.get("theories", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload


def main():
    cases_payload = sync_cases_index()
    weapons_payload = sync_weapons_index()
    theories_payload = sync_theories_index()
    sync_readme_indexes(cases_payload, weapons_payload)

    case_count = cases_payload["metadata"]["total_cases"]
    weapon_count = weapons_payload["metadata"]["total_weapons"]
    theory_count = theories_payload["metadata"]["total_theories"]
    print(
        f"Indexes updated: {case_count} cases, {weapon_count} weapons, {theory_count} theories"
    )


if __name__ == "__main__":
    main()
