#!/usr/bin/env python3
"""
Report Contract Verification Script

Verifies that output reports comply with the report contract defined in
references/report-contract.md.

Usage:
    python verify_report.py --input report.md --output verification.json

Reference: references/report-contract.md
"""

import json
import argparse
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Severity(Enum):
    ERROR = "error"      # 必须修复
    WARNING = "warning"  # 应该修复
    INFO = "info"        # 建议修复


@dataclass
class ValidationIssue:
    section: str
    severity: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    valid: bool
    score: float  # 0-100
    issues: List[Dict]
    sections_found: List[str]
    sections_missing: List[str]
    fact_markers: Dict[str, int]


# Required sections from report-contract.md
REQUIRED_SECTIONS = [
    {
        "id": "conclusion",
        "user_title": "先看结论",
        "patterns": ["## 先看结论", "## 结论", "## 建议", "## 执行摘要"],
        "required_content": ["目标", "理由", "置信度", "行动"]
    },
    {
        "id": "current_state",
        "user_title": "先把现状说清楚",
        "patterns": ["## 先把现状说清楚", "## 现状", "## 当前状态", "## 背景"],
        "required_content": ["目标", "阶段", "约束", "资源"]
    },
    {
        "id": "clarity_assessment",
        "user_title": "现状够不够清楚",
        "patterns": ["## 现状够不够清楚", "## 清晰度", "## 清晰度评估"],
        "required_content": ["评分", "诊断"]
    },
    {
        "id": "decision_process",
        "user_title": "判断过程",
        "patterns": ["## 判断过程", "## 决策过程", "## 分析过程"],
        "required_content": ["方案", "对比", "评分"]
    },
    {
        "id": "recommendation",
        "user_title": "推荐方案",
        "patterns": ["## 推荐方案", "## 推荐", "## 建议"],
        "required_content": ["方案", "理由", "路径"]
    },
    {
        "id": "resource_allocation",
        "user_title": "时间、精力、资源应该怎么重新分配",
        "patterns": [
            "## 时间、精力、资源应该怎么重新分配",
            "## 资源分配",
            "## 资源配置"
        ],
        "required_content": ["主攻", "次要", "监控"]
    },
    {
        "id": "actions",
        "user_title": "接下来怎么做",
        "patterns": ["## 接下来怎么做", "## 行动", "## 下一步", "## 行动计划"],
        "required_content": ["行动", "负责人", "期限"]
    },
    {
        "id": "projection",
        "user_title": "做完以后可能怎样",
        "patterns": ["## 做完以后可能怎样", "## 预期", "## 预测", "## 投影"],
        "required_content": ["概率", "假设", "证据"]
    },
    {
        "id": "review_trigger",
        "user_title": "什么时候回头看",
        "patterns": ["## 什么时候回头看", "## 复盘", "## 回顾", "## 检查点"],
        "required_content": ["时间", "信号", "证据"]
    },
    {
        "id": "caveats",
        "user_title": "注意事项",
        "patterns": ["## 注意事项", "## 警告", "## 风险提示", "## 限制"],
        "required_content": ["警告", "不确定"]
    }
]

# Fact marker patterns
FACT_MARKERS = {
    "observed": r"\(observed\)|（已观察）|（实测）|（数据）",
    "estimated": r"\(estimated\)|（估算）|（预估）|（约）",
    "assumed": r"\(assumed\)|（假设）|（推测）|（假定）"
}

# Title mappings for user-friendly names
TITLE_MAPPINGS = {
    "主要矛盾": "最关键的卡点",
    "次要矛盾": "先不主攻，但要盯住",
    "矛盾主要方面": "现在最影响局面的一侧",
    "因果链": "为什么这样做会有效",
    "概率推演": "做完以后可能怎样",
    "监控阈值": "什么时候回头看",
    "内因": "你能直接改变的",
    "外因": "你只能影响或等待的"
}


def extract_sections(content: str) -> Dict[str, str]:
    """Extract sections from markdown content."""
    sections = {}

    # Split by ## headers
    parts = re.split(r'\n## ', content)

    for part in parts[1:]:  # Skip content before first ##
        lines = part.strip().split('\n')
        if lines:
            title = lines[0].strip()
            body = '\n'.join(lines[1:]) if len(lines) > 1 else ""
            sections[title] = body

    return sections


def find_section_match(
    section_title: str,
    extracted_sections: Dict[str, str]
) -> Optional[Tuple[str, str]]:
    """Find matching section from extracted sections."""
    # Direct match
    if section_title in extracted_sections:
        return (section_title, extracted_sections[section_title])

    # Check patterns
    for section_def in REQUIRED_SECTIONS:
        if section_def["id"] in section_title.lower().replace("_", ""):
            for pattern in section_def["patterns"]:
                clean_pattern = pattern.replace("## ", "")
                if clean_pattern in extracted_sections:
                    return (clean_pattern, extracted_sections[clean_pattern])

    return None


def check_fact_markers(content: str) -> Dict[str, int]:
    """Count fact markers in content."""
    counts = {}

    for marker_type, pattern in FACT_MARKERS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        counts[marker_type] = len(matches)

    return counts


def check_content_requirements(
    content: str,
    required_content: List[str]
) -> List[str]:
    """Check if required content keywords are present."""
    missing = []

    for keyword in required_content:
        if keyword.lower() not in content.lower():
            missing.append(keyword)

    return missing


def apply_title_mappings(content: str) -> str:
    """Apply user-friendly title mappings."""
    result = content
    for old_title, new_title in TITLE_MAPPINGS.items():
        result = result.replace(old_title, new_title)
    return result


def verify_report(content: str) -> ValidationResult:
    """Main verification function."""
    issues = []
    sections_found = []
    sections_missing = []

    # Extract sections
    extracted = extract_sections(content)

    # Check each required section
    for section_def in REQUIRED_SECTIONS:
        found = False

        for pattern in section_def["patterns"]:
            clean_pattern = pattern.replace("## ", "")
            if clean_pattern in extracted:
                found = True
                sections_found.append(section_def["user_title"])

                # Check content requirements
                section_content = extracted[clean_pattern]
                missing_content = check_content_requirements(
                    section_content,
                    section_def["required_content"]
                )

                if missing_content:
                    issues.append(asdict(ValidationIssue(
                        section=section_def["user_title"],
                        severity=Severity.WARNING.value,
                        message=f"缺少关键内容: {', '.join(missing_content)}",
                        suggestion=f"添加: {', '.join(missing_content)}"
                    )))
                break

        if not found:
            sections_missing.append(section_def["user_title"])
            issues.append(asdict(ValidationIssue(
                section=section_def["user_title"],
                severity=Severity.ERROR.value,
                message="缺少必选章节",
                suggestion=f"添加章节: {section_def['patterns'][0]}"
            )))

    # Check fact markers
    fact_counts = check_fact_markers(content)
    total_facts = sum(fact_counts.values())

    if total_facts == 0:
        issues.append(asdict(ValidationIssue(
            section="全局",
            severity=Severity.WARNING.value,
            message="未发现事实标记 (observed/estimated/assumed)",
            suggestion="为关键事实添加标记，如: 月活用户 120 万 (observed)"
        )))

    # Check for title mappings
    mapped_content = apply_title_mappings(content)
    if mapped_content != content:
        # Some academic terms were found
        pass  # This is OK, just noting

    # Calculate score
    total_sections = len(REQUIRED_SECTIONS)
    found_sections = len(sections_found)
    section_score = (found_sections / total_sections) * 70

    # Fact marker score
    fact_score = min(30, total_facts * 5)

    # Deduct for errors/warnings
    error_count = sum(1 for i in issues if i["severity"] == "error")
    warning_count = sum(1 for i in issues if i["severity"] == "warning")

    total_score = section_score + fact_score - (error_count * 10) - (warning_count * 3)
    total_score = max(0, min(100, total_score))

    # Determine validity
    valid = error_count == 0 and found_sections >= total_sections * 0.8

    return ValidationResult(
        valid=valid,
        score=round(total_score, 1),
        issues=issues,
        sections_found=sections_found,
        sections_missing=sections_missing,
        fact_markers=fact_counts
    )


def main():
    parser = argparse.ArgumentParser(
        description="Verify report contract compliance"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input markdown report file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output JSON file for verification results"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown"],
        default="json",
        help="Output format"
    )

    args = parser.parse_args()

    # Read input
    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    # Perform verification
    result = verify_report(content)

    # Write output
    output_data = asdict(result)

    if args.format == "markdown":
        md = f"""# 报告验证结果

## 总体评分: {result.score}/100

## 状态: {'✅ 通过' if result.valid else '❌ 未通过'}

## 章节检查

### 已找到 ({len(result.sections_found)}/{len(REQUIRED_SECTIONS)})
"""
        for section in result.sections_found:
            md += f"- ✅ {section}\n"

        if result.sections_missing:
            md += f"\n### 缺失\n"
            for section in result.sections_missing:
                md += f"- ❌ {section}\n"

        md += f"\n## 事实标记统计\n\n"
        for marker, count in result.fact_markers.items():
            md += f"- {marker}: {count} 处\n"

        if result.issues:
            md += "\n## 问题列表\n\n"
            for issue in result.issues:
                icon = "❌" if issue["severity"] == "error" else "⚠️"
                md += f"{icon} **[{issue['section']}]** {issue['message']}\n"
                if issue.get("suggestion"):
                    md += f"   → 建议: {issue['suggestion']}\n"

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Verification complete. Score: {result.score}/100")
    if result.valid:
        print("✅ Report passes validation")
    else:
        print("❌ Report needs fixes")


if __name__ == "__main__":
    main()
