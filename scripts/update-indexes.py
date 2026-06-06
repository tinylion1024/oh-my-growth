#!/usr/bin/env python3
"""Synchronize index metadata and enrich weapon descriptions from source files."""

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT_DIR / "knowledge" / "indexes"
WEAPON_SOURCE_DIR = ROOT_DIR / "knowledge" / "weapons"


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


def sync_cases_index():
    path = INDEX_DIR / "cases-index.json"
    payload = load_json(path)
    payload["metadata"]["total_cases"] = len(payload.get("cases", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload["metadata"]["total_cases"]


def sync_weapons_index():
    path = INDEX_DIR / "weapons-index.json"
    payload = load_json(path)

    source_by_id = {}
    for markdown_file in WEAPON_SOURCE_DIR.glob("**/weapons/*.md"):
        front_matter = parse_front_matter(markdown_file)
        weapon_id = str(front_matter.get("id", "")).strip()
        if not weapon_id:
            continue
        source_by_id[weapon_id] = front_matter

    category_counter = Counter()
    for weapon in payload.get("weapons", []):
        weapon_id = str(weapon.get("id", ""))
        source = source_by_id.get(weapon_id, {})
        if source.get("description"):
            weapon["description"] = source["description"]
        category_counter[weapon.get("category", "")] += 1

    for category in payload.get("categories", []):
        category["count"] = category_counter.get(category.get("id", ""), 0)

    payload["metadata"]["total_weapons"] = len(payload.get("weapons", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload["metadata"]["total_weapons"]


def sync_theories_index():
    path = INDEX_DIR / "theories-index.json"
    payload = load_json(path)
    payload["metadata"]["total_theories"] = len(payload.get("theories", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload["metadata"]["total_theories"]


def main():
    case_count = sync_cases_index()
    weapon_count = sync_weapons_index()
    theory_count = sync_theories_index()
    print(
        f"Indexes updated: {case_count} cases, {weapon_count} weapons, {theory_count} theories"
    )


if __name__ == "__main__":
    main()
