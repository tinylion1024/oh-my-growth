#!/usr/bin/env python3
"""Validate enriched weapon docs have the required quality sections and indexes."""

import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
WEAPON_FILES = sorted((ROOT_DIR / "knowledge" / "weapons").glob("**/weapons/*.md"))

REQUIRED_HEADINGS = (
    "## 玩法定位",
    "## 核心讲解",
    "## 关键要点",
    "## 深入讲解",
    "## 执行要点",
    "## 适用判断",
    "## 关键指标",
    "## 案例索引",
    "## 相关索引",
)


def validate_file(path: Path):
    issues = []
    content = path.read_text(encoding="utf-8")

    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            issues.append(f"missing heading: {heading}")

    if "category_id:" not in content.split("---", 2)[1]:
        issues.append("missing category_id in front matter")

    case_links = re.findall(r"## 案例索引(.*?)## 相关索引", content, re.DOTALL)
    if not case_links:
        issues.append("case index section not parseable")
    else:
        case_link_count = case_links[0].count("](")
        if case_link_count < 2:
            issues.append("case index should contain at least 2 links")

    related_links = re.findall(r"## 相关索引(.*)$", content, re.DOTALL)
    if not related_links:
        issues.append("related index section not parseable")
    else:
        related_link_count = related_links[0].count("](")
        if related_link_count < 4:
            issues.append("related index should contain at least 4 links")

    key_points = re.findall(r"## 关键要点(.*?)## 深入讲解", content, re.DOTALL)
    if not key_points:
        issues.append("key points section not parseable")
    else:
        bullet_count = len(re.findall(r"^- ", key_points[0], re.MULTILINE))
        if bullet_count < 4:
            issues.append("key points should contain at least 4 bullets")

    return issues


def main():
    failures = []
    for path in WEAPON_FILES:
        issues = validate_file(path)
        if issues:
            failures.append((path, issues))

    if failures:
        for path, issues in failures:
            print(f"❌ {path.relative_to(ROOT_DIR)}")
            for issue in issues:
                print(f"   - {issue}")
        return 1

    print(f"✅ All {len(WEAPON_FILES)} weapon docs passed quality validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
