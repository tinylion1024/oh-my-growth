#!/usr/bin/env python3
"""
Current-State Clarity Assessment Script

Assesses the clarity of the current state across 7 dimensions and outputs
follow-up questions when clarity is insufficient.

Usage:
    python assess_clarity.py --input state.json --output assessment.json

Reference: references/current-state-clarity.md
"""

import json
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ClarityLevel(Enum):
    INSUFFICIENT = "insufficient"  # 0-54: 无法开始诊断，必须先澄清
    WORKABLE = "workable"          # 55-74: 可以开始诊断，边做边澄清
    CLEAR = "clear"                # 75-100: 可以深入诊断


@dataclass
class DimensionScore:
    dimension: str
    weight: int
    score: int  # 0-100
    weighted_score: float
    evidence: List[str]
    missing: List[str]


@dataclass
class ClarityAssessment:
    total_score: float
    level: str
    dimensions: List[Dict]
    hard_requirements_met: bool
    blocking_issues: List[str]
    follow_up_questions: List[Dict]
    can_proceed: bool


# Dimension definitions with weights
DIMENSIONS = {
    "goal_success": {
        "weight": 20,
        "description": "目标与成功标准",
        "questions": [
            "目标是什么？(observed/estimated/assumed)",
            "成功标准是什么？如何衡量？",
            "目标是否可量化、有时限？"
        ],
        "hard_requirement": True
    },
    "facts_evidence": {
        "weight": 20,
        "description": "事实与证据",
        "questions": [
            "有哪些已验证的事实？(observed)",
            "有哪些估算值？依据是什么？(estimated)",
            "有哪些假设？风险是什么？(assumed)"
        ],
        "hard_requirement": True
    },
    "stage": {
        "weight": 12,
        "description": "阶段判断",
        "questions": [
            "产品/业务处于什么阶段？",
            "阶段判断的依据是什么？",
            "阶段的关键特征是否明确？"
        ],
        "hard_requirement": False
    },
    "scarce_resources": {
        "weight": 12,
        "description": "稀缺资源",
        "questions": [
            "最稀缺的资源是什么？",
            "资源约束是什么？",
            "资源如何分配？"
        ],
        "hard_requirement": False
    },
    "hard_constraints": {
        "weight": 12,
        "description": "硬约束",
        "questions": [
            "有哪些不可逾越的约束？",
            "约束的来源是什么？",
            "约束是否可验证？"
        ],
        "hard_requirement": False
    },
    "stakeholders": {
        "weight": 8,
        "description": "利益相关者",
        "questions": [
            "关键决策者是谁？",
            "利益相关者的诉求是什么？",
            "是否有冲突的利益？"
        ],
        "hard_requirement": False
    },
    "repeated_patterns": {
        "weight": 8,
        "description": "重复模式",
        "questions": [
            "是否出现过类似问题？",
            "之前的解决方案是什么？",
            "有什么经验教训？"
        ],
        "hard_requirement": False
    }
}


def assess_dimension(dimension_name: str, input_data: Dict) -> DimensionScore:
    """Assess a single dimension based on input data."""
    dim_config = DIMENSIONS[dimension_name]

    # Get dimension data from input
    dim_data = input_data.get("dimensions", {}).get(dimension_name, {})

    # Calculate score based on provided evidence
    evidence = dim_data.get("evidence", [])
    missing = []

    # Score based on evidence quality and completeness
    if len(evidence) == 0:
        score = 0
        missing = dim_config["questions"]
    elif len(evidence) == 1:
        score = 40
        missing = dim_config["questions"][1:]
    elif len(evidence) == 2:
        score = 70
        missing = dim_config["questions"][2:]
    else:
        score = min(100, 70 + (len(evidence) - 2) * 10)
        missing = []

    # Override score if provided
    if "score" in dim_data:
        score = dim_data["score"]

    weighted_score = score * dim_config["weight"] / 100

    return DimensionScore(
        dimension=dimension_name,
        weight=dim_config["weight"],
        score=score,
        weighted_score=weighted_score,
        evidence=evidence,
        missing=missing
    )


def determine_level(total_score: float) -> ClarityLevel:
    """Determine clarity level based on total score."""
    if total_score < 55:
        return ClarityLevel.INSUFFICIENT
    elif total_score < 75:
        return ClarityLevel.WORKABLE
    else:
        return ClarityLevel.CLEAR


def check_hard_requirements(dimensions: List[DimensionScore]) -> Tuple[bool, List[str]]:
    """Check if hard requirements are met."""
    blocking = []

    for dim in dimensions:
        dim_config = DIMENSIONS[dim.dimension]
        if dim_config["hard_requirement"] and dim.score < 50:
            blocking.append(
                f"{dim_config['description']} (得分: {dim.score}/100) - 必须达到50分以上"
            )

    return len(blocking) == 0, blocking


def generate_follow_up_questions(
    dimensions: List[DimensionScore],
    level: ClarityLevel
) -> List[Dict]:
    """Generate follow-up questions based on missing information."""
    questions = []

    # Sort dimensions by weight (priority) and score (need)
    sorted_dims = sorted(
        dimensions,
        key=lambda d: (-DIMENSIONS[d.dimension]["weight"], d.score)
    )

    for dim in sorted_dims:
        if dim.score < 70 and dim.missing:
            # Add up to 2 questions per dimension
            for q in dim.missing[:2]:
                questions.append({
                    "dimension": dim.dimension,
                    "dimension_name": DIMENSIONS[dim.dimension]["description"],
                    "question": q,
                    "priority": "high" if dim.score < 40 else "medium"
                })

    # Limit to 5 questions total
    return questions[:5]


def assess_clarity(input_data: Dict) -> ClarityAssessment:
    """Main assessment function."""
    # Assess each dimension
    dimension_scores = [
        assess_dimension(dim_name, input_data)
        for dim_name in DIMENSIONS.keys()
    ]

    # Calculate total score
    total_score = sum(d.weighted_score for d in dimension_scores)

    # Determine level
    level = determine_level(total_score)

    # Check hard requirements
    hard_req_met, blocking = check_hard_requirements(dimension_scores)

    # Generate follow-up questions
    follow_up = generate_follow_up_questions(dimension_scores, level)

    # Determine if can proceed
    can_proceed = (
        level != ClarityLevel.INSUFFICIENT and
        hard_req_met
    )

    return ClarityAssessment(
        total_score=round(total_score, 1),
        level=level.value,
        dimensions=[asdict(d) for d in dimension_scores],
        hard_requirements_met=hard_req_met,
        blocking_issues=blocking,
        follow_up_questions=follow_up,
        can_proceed=can_proceed
    )


def main():
    parser = argparse.ArgumentParser(
        description="Assess current-state clarity"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input JSON file with state data"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output JSON file for assessment results"
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
        input_data = json.load(f)

    # Perform assessment
    result = assess_clarity(input_data)

    # Write output
    output_data = asdict(result)

    if args.format == "markdown":
        # Generate markdown report
        md = f"""# 现状清晰度评估

## 总分: {result.total_score}/100

## 等级: {result.level.upper()}

## 各维度评分

| 维度 | 权重 | 得分 | 加权得分 | 状态 |
|------|------|------|----------|------|
"""
        for dim in result.dimensions:
            status = "✅" if dim["score"] >= 70 else "⚠️" if dim["score"] >= 40 else "❌"
            md += f"| {DIMENSIONS[dim['dimension']]['description']} | {dim['weight']} | {dim['score']} | {dim['weighted_score']:.1f} | {status} |\n"

        if result.blocking_issues:
            md += "\n## 阻塞问题\n\n"
            for issue in result.blocking_issues:
                md += f"- ❌ {issue}\n"

        if result.follow_up_questions:
            md += "\n## 追问建议\n\n"
            for i, q in enumerate(result.follow_up_questions, 1):
                md += f"{i}. **[{q['dimension_name']}]** {q['question']}\n"

        md += f"\n## 结论\n\n"
        if result.can_proceed:
            md += "✅ 可以开始诊断\n"
        else:
            md += "❌ 需要先澄清现状\n"

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Assessment complete. Score: {result.total_score}/100 ({result.level})")
    if not result.can_proceed:
        print("⚠️  Cannot proceed - need to clarify current state first")


if __name__ == "__main__":
    main()
