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

FAILURE_INDEX_FILE_BY_NAME = {
    "acquisition-anti-patterns.md": "获客反模式",
    "referral-failure-modes.md": "裂变失败模式",
    "retention-failure-modes.md": "留存失败模式",
}

PROBLEM_TO_PROCESS = {
    "acquisition": "用户获取",
    "activation": "用户深耕",
    "retention": "用户深耕",
    "monetization": "用户深耕",
    "referral": "用户获取",
}

PROBLEM_TO_JOURNEY = {
    "acquisition": "认知/到达",
    "activation": "注册/激活",
    "retention": "留存",
    "monetization": "付费",
    "referral": "分享",
}

WEAPON_INDEX_ENRICHMENT = {
    "cold-start": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["0-1"],
        "marketplace_side": "",
        "resource_profile": "低预算、创始人驱动、跨职能小团队",
        "guardrail_risk": "需要警惕低质量流量替代真实增长",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "viral-referral": {
        "growth_process": "用户获取",
        "journey_stage": "分享",
        "stage_fit": ["0-1", "1-10"],
        "marketplace_side": "",
        "resource_profile": "需要产品、增长、风控协同",
        "guardrail_risk": "需要警惕激励滥用和低质量用户",
        "failure_refs": ["knowledge/failures/referral-failure-modes.md"],
    },
    "content-growth": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["0-1", "1-10"],
        "marketplace_side": "",
        "resource_profile": "内容与分发并重，持续产能要求高",
        "guardrail_risk": "需要警惕曝光上涨但高意向转化不改善",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "community": {
        "growth_process": "用户深耕",
        "journey_stage": "留存",
        "stage_fit": ["1-10", "10-100"],
        "marketplace_side": "",
        "resource_profile": "运营密集，需要长期维护",
        "guardrail_risk": "需要警惕社区活跃替代真实留存",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "plg": {
        "growth_process": "用户深耕",
        "journey_stage": "注册/激活",
        "stage_fit": ["0-1", "1-10"],
        "marketplace_side": "",
        "resource_profile": "产品与工程驱动，实验节奏要求高",
        "guardrail_risk": "需要警惕功能堆叠但首次价值达成不改善",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "retention": {
        "growth_process": "用户深耕",
        "journey_stage": "留存",
        "stage_fit": ["1-10", "10-100"],
        "marketplace_side": "",
        "resource_profile": "产品、运营、数据共同驱动",
        "guardrail_risk": "需要警惕假留存和多机制同时变更",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "monetization": {
        "growth_process": "用户深耕",
        "journey_stage": "付费",
        "stage_fit": ["1-10", "10-100"],
        "marketplace_side": "",
        "resource_profile": "商业化与体验平衡，数据口径要求高",
        "guardrail_risk": "需要警惕短期收入伤害长期留存",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "paid-ads": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["1-10", "10-100"],
        "marketplace_side": "",
        "resource_profile": "预算密集，需要稳定归因和投放优化",
        "guardrail_risk": "需要警惕 CAC 失控和扩量早于转化验证",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "brand": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["10-100"],
        "marketplace_side": "",
        "resource_profile": "中长期投入，需要跨团队协同",
        "guardrail_risk": "需要警惕品牌曝光无法回到高意向转化",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "b2b-sales": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["1-10", "10-100"],
        "marketplace_side": "",
        "resource_profile": "销售驱动，需要线索与转化流程协同",
        "guardrail_risk": "需要警惕线索数掩盖真实成交质量",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
}

WEAPON_MARKETPLACE_SIDE_BY_ID = {
    "1": "supply",
    "2": "supply",
    "4": "supply",
    "6": "demand",
    "7": "demand",
    "8": "demand",
    "10": "liquidity",
    "11": "liquidity",
    "12": "liquidity",
    "23": "liquidity",
    "24": "liquidity",
}

THEORY_INDEX_ENRICHMENT = {
    "growth-hacking": {
        "growth_process": "增长经营",
        "journey_stage": "注册/激活",
        "stage_fit": ["0-1", "1-10"],
        "company_type": "general",
        "resource_profile": "需要稳定实验节奏、基础数据和跨职能协作",
        "failure_refs": [
            "knowledge/failures/acquisition-anti-patterns.md",
            "knowledge/failures/retention-failure-modes.md",
        ],
    },
    "plg": {
        "growth_process": "用户深耕",
        "journey_stage": "注册/激活",
        "stage_fit": ["0-1", "1-10"],
        "company_type": "saas",
        "resource_profile": "产品、工程、增长密切协作，依赖核心价值快速达成",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "network-effects": {
        "growth_process": "用户获取",
        "journey_stage": "分享",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "marketplace",
        "marketplace_side": "liquidity",
        "resource_profile": "平台型资源配置，重视供需两侧协同和临界规模",
        "failure_refs": ["knowledge/failures/referral-failure-modes.md"],
    },
    "content-growth": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["0-1", "1-10"],
        "company_type": "general",
        "resource_profile": "持续内容产能和分发能力要求高",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "community-growth": {
        "growth_process": "用户深耕",
        "journey_stage": "留存",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "general",
        "resource_profile": "需要长期运营、人群分层和核心用户机制",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "brand-growth": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["10-100"],
        "company_type": "general",
        "resource_profile": "品牌预算、中长期投入、跨团队内容与传播协同",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "viral-growth": {
        "growth_process": "用户获取",
        "journey_stage": "分享",
        "stage_fit": ["0-1", "1-10"],
        "company_type": "general",
        "resource_profile": "产品、增长、风控协同，要求低摩擦分享体验",
        "failure_refs": ["knowledge/failures/referral-failure-modes.md"],
    },
    "performance-marketing": {
        "growth_process": "用户获取",
        "journey_stage": "认知/到达",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "general",
        "resource_profile": "预算密集，要求稳定归因、创意与落地页协同",
        "failure_refs": ["knowledge/failures/acquisition-anti-patterns.md"],
    },
    "gamification": {
        "growth_process": "用户深耕",
        "journey_stage": "留存",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "general",
        "resource_profile": "需要行为设计、数据分析和节奏控制",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "flywheel": {
        "growth_process": "增长经营",
        "journey_stage": "留存",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "general",
        "resource_profile": "需要跨职能系统化协作和长期反馈回路",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "business-models": {
        "growth_process": "用户深耕",
        "journey_stage": "付费",
        "stage_fit": ["1-10", "10-100"],
        "company_type": "general",
        "resource_profile": "需要收入模型设计、实验能力和留存约束意识",
        "failure_refs": ["knowledge/failures/retention-failure-modes.md"],
    },
    "growthhackers": {
        "growth_process": "增长经营",
        "journey_stage": "注册/激活",
        "stage_fit": ["0-1", "1-10"],
        "company_type": "general",
        "resource_profile": "偏增长团队方法论，需要实验文化和快速执行",
        "failure_refs": [
            "knowledge/failures/acquisition-anti-patterns.md",
            "knowledge/failures/retention-failure-modes.md",
        ],
    },
}


def derive_marketplace_side(case: dict, company_type: str) -> str:
    if company_type not in {"marketplace", "local-services"}:
        return ""

    tactics = " ".join(case.get("tags", {}).get("tactics", []))
    summary = case.get("summary", "")
    replicable = " ".join(case.get("replicable_points", []))
    text = f"{tactics} {summary} {replicable}".lower()

    supply_hits = sum(
        1 for token in ["供给", "商家", "司机", "房东", "创作者", "入驻", "库存", "seller", "host", "driver"]
        if token in text
    )
    demand_hits = sum(
        1 for token in ["需求", "买家", "乘客", "房客", "游客", "用户", "buyer", "rider", "guest"]
        if token in text
    )

    if supply_hits and supply_hits > demand_hits:
        return "supply"
    if demand_hits and demand_hits > supply_hits:
        return "demand"
    return "liquidity"


def derive_case_fields(case: dict) -> dict:
    tags = case.get("tags", {})
    problems = tags.get("problem", []) or []
    stages = tags.get("stage", []) or []
    industries = tags.get("industry", []) or []
    business_models = tags.get("business_model", []) or []
    tactics = tags.get("tactics", []) or []
    name = case.get("name", "")
    summary = case.get("summary", "")
    derived_text = f"{name} {' '.join(tactics)} {summary}".lower()

    primary_problem = problems[0] if problems else ""
    growth_process = PROBLEM_TO_PROCESS.get(primary_problem, "增长经营")
    journey_stage = PROBLEM_TO_JOURNEY.get(primary_problem, "用户旅程待明确")

    company_type = "general"
    if "saas" in industries:
        company_type = "saas"
    elif any(
        token in derived_text
        for token in ["本地生活", "外卖", "到店", "上门", "同城", "配送", "履约", "出行", "即时零售", "local service"]
    ):
        company_type = "local-services"
    elif "marketplace" in industries:
        company_type = "marketplace"
    elif "ecommerce" in industries:
        company_type = "ecommerce"
    elif "ai" in industries:
        company_type = "ai"
    elif any(token in tactics for token in ["平台", "双边市场"]):
        company_type = "marketplace"

    if company_type in {"marketplace", "local-services"} and not primary_problem:
        growth_process = "用户获取"
        journey_stage = "认知/到达"

    failure_refs = []
    if "acquisition" in problems or "referral" in problems:
        failure_refs.append("knowledge/failures/acquisition-anti-patterns.md")
    if "referral" in problems:
        failure_refs.append("knowledge/failures/referral-failure-modes.md")
    if "retention" in problems or "activation" in problems or "monetization" in problems:
        failure_refs.append("knowledge/failures/retention-failure-modes.md")

    resource_profile = "资料不足，需结合案例原文判断"
    if company_type == "local-services":
        resource_profile = "需要单城/单区域运营、供给履约协同和线下执行能力"
    elif company_type == "marketplace" or "platform" in business_models:
        resource_profile = "平台型增长，需要供给与需求两侧协同"
    elif "saas" in industries:
        resource_profile = "偏产品和销售协同，重视高意向线索与留存"
    elif "ecommerce" in industries:
        resource_profile = "流量、转化、复购和供应链联动明显"

    marketplace_side = derive_marketplace_side(case, company_type)

    return {
        "growth_process": growth_process,
        "journey_stage": journey_stage,
        "stage_fit": stages,
        "company_type": company_type,
        "marketplace_side": marketplace_side,
        "resource_profile": resource_profile,
        "failure_refs": failure_refs,
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
    for case in payload.get("cases", []):
        case.update(derive_case_fields(case))
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
        enrichment = WEAPON_INDEX_ENRICHMENT.get(weapon.get("category", ""), {})
        weapon.update(enrichment)
        weapon["marketplace_side"] = WEAPON_MARKETPLACE_SIDE_BY_ID.get(weapon_id, weapon.get("marketplace_side", ""))
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
    for theory in payload.get("theories", []):
        theory_id = theory.get("id", "")
        enrichment = THEORY_INDEX_ENRICHMENT.get(theory_id, {})
        theory.update(enrichment)
        theory.setdefault("marketplace_side", "")
    payload["metadata"]["total_theories"] = len(payload.get("theories", []))
    payload["metadata"]["last_updated"] = str(date.today())
    write_json(path, payload)
    return payload


def sync_failures_index():
    path = INDEX_DIR / "failures-index.json"
    failure_docs = sorted((ROOT_DIR / "knowledge" / "failures").glob("*.md"))

    entries = []
    for doc_path in failure_docs:
        if doc_path.name == "README.md":
            continue

        if "acquisition" in doc_path.name:
            growth_process = "用户获取"
            journey_stage = "认知/到达"
            problem_types = ["acquisition"]
        elif "referral" in doc_path.name:
            growth_process = "用户获取"
            journey_stage = "分享"
            problem_types = ["referral"]
        else:
            growth_process = "用户深耕"
            journey_stage = "留存"
            problem_types = ["retention", "activation", "monetization"]

        content = doc_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        summary = ""
        warning_signals = []
        suggestions = []
        current_bucket = None
        for line in lines[1:]:
            if line == "常见信号：":
                current_bucket = warning_signals
                continue
            if line == "建议：":
                current_bucket = suggestions
                continue
            if line.startswith("## "):
                continue
            if line.startswith("-") and current_bucket is not None:
                current_bucket.append(line.lstrip("- ").strip())
                continue
            if not summary and not line.startswith("#"):
                summary = line

        entries.append(
            {
                "id": doc_path.stem,
                "name": FAILURE_INDEX_FILE_BY_NAME.get(doc_path.name, doc_path.stem),
                "file": str(doc_path.relative_to(ROOT_DIR / "knowledge")),
                "growth_process": growth_process,
                "journey_stage": journey_stage,
                "problem_types": problem_types,
                "summary": summary or "用于提醒当前策略的常见失效条件与反模式。",
                "warning_signals": warning_signals[:3],
                "suggestions": suggestions[:3],
            }
        )

    payload = {
        "metadata": {
            "version": "1.0.0",
            "last_updated": str(date.today()),
            "total_failures": len(entries),
        },
        "failures": entries,
    }
    write_json(path, payload)
    return payload


def main():
    cases_payload = sync_cases_index()
    weapons_payload = sync_weapons_index()
    theories_payload = sync_theories_index()
    failures_payload = sync_failures_index()
    sync_readme_indexes(cases_payload, weapons_payload)

    case_count = cases_payload["metadata"]["total_cases"]
    weapon_count = weapons_payload["metadata"]["total_weapons"]
    theory_count = theories_payload["metadata"]["total_theories"]
    failure_count = failures_payload["metadata"]["total_failures"]
    print(
        f"Indexes updated: {case_count} cases, {weapon_count} weapons, {theory_count} theories, {failure_count} failures"
    )


if __name__ == "__main__":
    main()
