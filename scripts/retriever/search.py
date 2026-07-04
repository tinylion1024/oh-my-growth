"""Search methods for knowledge retrieval.

This module contains methods for searching cases, weapons, theories, failures,
and method packs.
"""

from typing import Dict, List, Optional

from .types import (
    normalize_stage,
    SearchResult,
)
from .context import (
    normalize_text,
    tokenize,
    compute_similarity,
    build_query_tokens,
    context_business_model_kind,
    context_marketplace_side_focus,
    context_preferred_categories,
    context_preferred_theories,
    problem_to_process,
    problem_to_journey,
    category_stage_fit,
    category_journey_fit,
    resource_fit,
    resource_profile_fit,
    metric_category_focus,
    metric_theory_focus,
    guardrail_penalty,
    guardrail_risk,
    case_stage_fit,
    case_journey_fit,
)


def search_cases(
    cases: List[Dict],
    query: str,
    context: Optional[Dict] = None,
    limit: int = 5
) -> List[SearchResult]:
    """搜索案例"""
    if context is None:
        context = {}

    query_tokens = build_query_tokens(query, context)
    problem = context.get('problem_type', '').lower()
    journey_stage = context.get("journey_stage", "") or problem_to_journey(problem)
    growth_process = context.get("growth_process", "") or problem_to_process(problem)
    marketplace_side_focus = context_marketplace_side_focus(query, context)
    business_model_kind = context_business_model_kind(context)
    metric_focus = metric_category_focus(context)
    stage = normalize_stage(context.get('stage', ''))

    results = []

    for case in cases:
        doc_text = ' '.join([
            case.get('name', ''),
            case.get('summary', ''),
            case.get('region', ''),
            ' '.join(case.get('tags', {}).get('tactics', [])),
            ' '.join(case.get('tags', {}).get('industry', [])),
            ' '.join(case.get('tags', {}).get('problem', [])),
            ' '.join(case.get('replicable_points', []))
        ])
        doc_tokens = tokenize(doc_text)

        score = compute_similarity(query_tokens, doc_tokens)

        industry = context.get('industry', '').lower()
        case_industries = case.get('tags', {}).get('industry', [])
        if industry in case_industries:
            score += 0.3

        case_problems = case.get('tags', {}).get('problem', [])
        if problem in case_problems:
            score += 0.2

        if case.get("growth_process") == growth_process:
            score += 0.08

        case_stages = case.get('stage_fit', []) or case.get('tags', {}).get('stage', [])
        if stage in case_stages:
            score += 0.15

        stage_fit = case_stage_fit(case, stage)
        score += stage_fit * 0.15

        journey_fit = case_journey_fit(case, journey_stage, problem)
        score += journey_fit * 0.08
        resource_fit_score = resource_profile_fit(case.get("resource_profile", ""), context)
        score += resource_fit_score * 0.06

        company_type = case.get("company_type", "")
        marketplace_side = case.get("marketplace_side", "")
        if business_model_kind == "local-services":
            if company_type == "local-services":
                score += 0.2
            elif company_type == "marketplace":
                score += 0.08
        elif industry == "marketplace" or company_type == "marketplace":
            if company_type == "marketplace":
                score += 0.14
            elif company_type == "local-services":
                score += 0.12
        if business_model_kind in {"marketplace", "local-services"}:
            if marketplace_side == marketplace_side_focus:
                score += 0.12
            elif marketplace_side == "liquidity":
                score += 0.08
            elif marketplace_side_focus in {"supply", "demand"} and marketplace_side in {"supply", "demand"}:
                score -= 0.06
        case_text = normalize_text(" ".join(case.get("replicable_points", [])))
        if "b2b-sales" in metric_focus and any(token in case_text for token in ["线索", "demo", "成交"]):
            score += 0.08
        if "content-growth" in metric_focus and any(token in case_text for token in ["内容", "seo", "搜索"]):
            score += 0.06
        if "retention" in metric_focus and any(token in case_text for token in ["留存", "复购", "活跃"]):
            score += 0.06

        if score > 0:
            results.append(SearchResult(
                id=case.get('id', ''),
                name=case.get('name', ''),
                type='case',
                score=round(min(1.5, score), 4),
                highlights=case.get('replicable_points', [])[:3],
                metadata={
                    'region': case.get('region', ''),
                    'evidence_tier': case.get('evidence_tier', 'C'),
                    'confidence': case.get('confidence', 0.75),
                    'growth_process': case.get('growth_process', growth_process),
                    'journey_stage': case.get('journey_stage', journey_stage),
                    'stage_fit': round(stage_fit, 2),
                    'resource_fit': round(resource_fit_score, 2),
                    'journey_fit': round(journey_fit, 2),
                    'company_type': company_type,
                    'marketplace_side': marketplace_side,
                    'resource_profile': case.get('resource_profile', ''),
                    'failure_refs': case.get('failure_refs', []),
                }
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def search_weapons(
    weapons: List[Dict],
    weapon_categories: Dict[str, str],
    weapon_details: Dict[str, Dict[str, str]],
    query: str,
    context: Optional[Dict] = None,
    limit: int = 5
) -> List[SearchResult]:
    """搜索玩法"""
    if context is None:
        context = {}

    query_tokens = build_query_tokens(query, context)
    problem = context.get('problem_type', '').lower()
    stage = normalize_stage(context.get("stage", ""))
    journey_stage = context.get("journey_stage", "") or problem_to_journey(problem)
    growth_process = context.get("growth_process", "") or problem_to_process(problem)
    business_model_kind = context_business_model_kind(context)
    metric_focus = metric_category_focus(context)

    results = []

    for weapon in weapons:
        weapon_id = str(weapon.get("id", ""))
        weapon_detail = weapon_details.get(weapon_id, {})
        category_id = weapon.get("category", "")
        category_name = weapon_categories.get(category_id, "")
        description = weapon.get("description") or weapon_detail.get("description", "")

        doc_text = ' '.join([
            weapon.get('name', ''),
            description,
            category_id,
            category_name,
            weapon_detail.get("category_label", ""),
        ])
        doc_tokens = tokenize(doc_text)

        score = compute_similarity(query_tokens, doc_tokens)

        if category_id in context_preferred_categories(context, problem):
            score += 0.35
        if category_id in metric_focus:
            score += 0.16

        if context.get("industry", "").lower() == "saas" and category_id == "plg":
            score += 0.12
        business_model = context_business_model_kind(context)
        if business_model_kind == "b2b-sales-led" and category_id == "b2b-sales":
            score += 0.22
        if business_model_kind == "marketplace" and category_id in {"community", "viral-referral"}:
            score += 0.14
        if business_model_kind == "local-services" and category_id in {"cold-start", "community"}:
            score += 0.16
        if business_model_kind == "ai" and category_id in {"content-growth", "plg"}:
            score += 0.12

        indexed_stage_fit = weapon.get("stage_fit", [])
        stage_fit = 1.0 if stage and stage in indexed_stage_fit else category_stage_fit(category_id, stage)
        score += stage_fit * 0.18

        indexed_journey = weapon.get("journey_stage", "")
        journey_fit = 1.0 if indexed_journey == journey_stage else category_journey_fit(category_id, journey_stage)
        score += journey_fit * 0.16

        resource_fit_score = resource_fit(weapon.get('effort', 'Medium'), context)
        score += resource_fit_score * 0.1
        profile_fit = resource_profile_fit(weapon.get("resource_profile", ""), context)
        score += profile_fit * 0.08

        if weapon.get("growth_process") == growth_process:
            score += 0.08

        marketplace_side = weapon.get("marketplace_side", "")
        if business_model_kind == "local-services":
            if marketplace_side in {"supply", "liquidity"}:
                score += 0.12
            elif marketplace_side == "demand" and stage == "0-1":
                score -= 0.08
        if business_model_kind in {"marketplace", "local-services"} and marketplace_side:
            side_focus = context_marketplace_side_focus(query, context)
            if marketplace_side == side_focus:
                score += 0.16
            elif marketplace_side == "liquidity":
                score += 0.08
            elif side_focus in {"supply", "demand"} and marketplace_side in {"supply", "demand"}:
                score -= 0.05
        guardrail_penalty_score = guardrail_penalty(
            weapon.get('guardrail_risk', guardrail_risk(category_id, problem)),
            context,
        )
        score -= guardrail_penalty_score

        if score > 0:
            results.append(SearchResult(
                id=weapon_id,
                name=weapon.get('name', ''),
                type='weapon',
                score=round(score, 4),
                highlights=[description or category_name or category_id],
                metadata={
                    'category': category_id,
                    'category_name': category_name,
                    'effort': weapon.get('effort', 'Medium'),
                    'impact': weapon.get('impact', 'Medium'),
                    'evidence_tier': weapon.get('evidence_tier', 'C'),
                    'file': weapon_detail.get("file", ""),
                    'growth_process': weapon.get('growth_process', growth_process),
                    'journey_stage': weapon.get('journey_stage', journey_stage),
                    'stage_fit': round(stage_fit, 2),
                    'resource_fit': round(resource_fit_score, 2),
                    'resource_profile_fit': round(profile_fit, 2),
                    'journey_fit': round(journey_fit, 2),
                    'marketplace_side': marketplace_side,
                    'guardrail_risk': weapon.get('guardrail_risk', guardrail_risk(category_id, problem)),
                    'guardrail_penalty': round(guardrail_penalty_score, 2),
                    'resource_profile': weapon.get('resource_profile', ''),
                    'failure_refs': weapon.get('failure_refs', []),
                }
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def search_theories(
    theories: List[Dict],
    query: str,
    context: Optional[Dict] = None,
    limit: int = 3
) -> List[SearchResult]:
    """搜索理论"""
    if context is None:
        context = {}

    query_tokens = build_query_tokens(query, context)
    problem = context.get("problem_type", "").lower()
    growth_process = context.get("growth_process", "") or problem_to_process(problem)
    journey_stage = context.get("journey_stage", "") or problem_to_journey(problem)
    stage = context.get("stage", "")
    marketplace_side_focus = context_marketplace_side_focus(query, context)
    business_model_kind = context_business_model_kind(context)
    metric_theory_focus_set = metric_theory_focus(context)

    results = []

    for theory in theories:
        doc_text = ' '.join([
            theory.get('id', ''),
            theory.get('name', ''),
            theory.get('core_question', ''),
            ' '.join(theory.get('core_principles', [])),
            ' '.join(theory.get('applicable_scenarios', [])),
            ' '.join(theory.get('key_tactics', [])),
        ])
        doc_tokens = tokenize(doc_text)

        score = compute_similarity(query_tokens, doc_tokens)
        if theory.get("id", "") in context_preferred_theories(context, problem):
            score += 0.25
        if theory.get("id", "") in metric_theory_focus_set:
            score += 0.12
        if theory.get("growth_process") == growth_process:
            score += 0.08

        business_model = context_business_model_kind(context)
        if business_model_kind == "b2b-sales-led" and theory.get("id", "") in {"business-models", "plg"}:
            score += 0.15
        if business_model_kind in {"marketplace", "local-services"} and theory.get("id", "") in {"network-effects", "flywheel"}:
            score += 0.18
        if business_model_kind == "ai" and theory.get("id", "") in {"content-growth", "plg"}:
            score += 0.12

        indexed_journey = theory.get("journey_stage", "")
        journey_fit = 1.0 if indexed_journey == journey_stage else 0.35
        score += journey_fit * 0.08

        indexed_stage_fit = theory.get("stage_fit", [])
        stage_fit = 1.0 if stage and stage in indexed_stage_fit else 0.4
        score += stage_fit * 0.06
        resource_fit_score = resource_profile_fit(theory.get("resource_profile", ""), context)
        score += resource_fit_score * 0.08

        if business_model_kind == "local-services":
            if theory.get("id", "") in {"network-effects", "flywheel"}:
                score += 0.06
            if theory.get("company_type", "") == "local-services":
                score += 0.12
        elif context.get("industry", "").lower() == "marketplace" or "marketplace" in business_model:
            if theory.get("company_type", "") == "marketplace":
                score += 0.12
        if business_model_kind in {"marketplace", "local-services"}:
            if theory.get("marketplace_side", "") == marketplace_side_focus:
                score += 0.1
            elif theory.get("marketplace_side", "") == "liquidity":
                score += 0.06
            elif marketplace_side_focus in {"supply", "demand"} and theory.get("marketplace_side", "") in {"supply", "demand"}:
                score -= 0.04

        if score > 0:
            results.append(SearchResult(
                id=theory.get('id', ''),
                name=theory.get('name', ''),
                type='theory',
                score=round(min(1.5, score), 4),
                highlights=theory.get('core_principles', [])[:3],
                metadata={
                    'evidence_tier': theory.get('evidence_tier', 'B'),
                    'file': theory.get('file', ''),
                    'growth_process': theory.get('growth_process', growth_process),
                    'journey_stage': theory.get('journey_stage', journey_stage),
                    'stage_fit': round(stage_fit, 2),
                    'resource_fit': round(resource_fit_score, 2),
                    'journey_fit': round(journey_fit, 2),
                    'company_type': theory.get('company_type', ''),
                    'marketplace_side': theory.get('marketplace_side', ''),
                    'resource_profile': theory.get('resource_profile', ''),
                    'failure_refs': theory.get('failure_refs', []),
                }
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def search_failures(
    failures: List[Dict],
    query: str,
    context: Optional[Dict] = None,
    limit: int = 2
) -> List[SearchResult]:
    """Search failure modes and anti-patterns."""
    if context is None:
        context = {}

    query_tokens = build_query_tokens(query, context)
    problem = context.get("problem_type", "").lower()
    growth_process = context.get("growth_process", "") or problem_to_process(problem)
    journey_stage = context.get("journey_stage", "") or problem_to_journey(problem)

    results = []
    for failure in failures:
        doc_text = " ".join([
            failure.get("id", ""),
            failure.get("name", ""),
            failure.get("summary", ""),
            " ".join(failure.get("warning_signals", [])),
            " ".join(failure.get("suggestions", [])),
        ])
        doc_tokens = tokenize(doc_text)

        score = compute_similarity(query_tokens, doc_tokens)
        if problem in failure.get("problem_types", []):
            score += 0.28
        if failure.get("growth_process") == growth_process:
            score += 0.08

        indexed_journey = failure.get("journey_stage", "")
        journey_fit = 1.0 if indexed_journey == journey_stage else 0.35
        score += journey_fit * 0.08

        if score > 0:
            results.append(SearchResult(
                id=failure.get("id", ""),
                name=failure.get("name", ""),
                type="failure",
                score=min(1.0, score),
                highlights=failure.get("warning_signals", [])[:2] or [failure.get("summary", "")],
                metadata={
                    "file": failure.get("file", ""),
                    "growth_process": failure.get("growth_process", growth_process),
                    "journey_stage": failure.get("journey_stage", journey_stage),
                    "problem_types": failure.get("problem_types", []),
                    "summary": failure.get("summary", ""),
                    "suggestions": failure.get("suggestions", [])[:2],
                    "journey_fit": round(journey_fit, 2),
                }
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def search_method_packs(
    method_packs: List[Dict],
    query: str,
    context: Optional[Dict] = None,
    limit: int = 3
) -> List[SearchResult]:
    """Search absorbed marketing-growth method packs."""
    if context is None:
        context = {}

    query_tokens = build_query_tokens(query, context)
    problem = context.get("problem_type", "").lower()
    stage = normalize_stage(context.get("stage", ""))
    journey_stage = context.get("journey_stage", "") or problem_to_journey(problem)
    growth_process = context.get("growth_process", "") or problem_to_process(problem)
    preferred_categories = context_preferred_categories(context, problem)
    metric_focus = metric_category_focus(context)

    results = []
    for pack in method_packs:
        categories = set(pack.get("categories", []))
        doc_text = " ".join([
            pack.get("id", ""),
            pack.get("name", ""),
            pack.get("summary", ""),
            " ".join(pack.get("domains", [])),
            " ".join(pack.get("problem_types", [])),
            " ".join(pack.get("categories", [])),
            " ".join(pack.get("canonical_questions", [])),
            " ".join(pack.get("decision_rules", [])),
            " ".join(pack.get("experiment_shapes", [])),
            " ".join(pack.get("guardrails", [])),
        ])
        doc_tokens = tokenize(doc_text)

        score = compute_similarity(query_tokens, doc_tokens)
        if problem in pack.get("problem_types", []):
            score += 0.3
        if categories & preferred_categories:
            score += 0.22
        if categories & metric_focus:
            score += 0.12
        if pack.get("growth_process") == growth_process:
            score += 0.08

        indexed_stage_fit = pack.get("stage_fit", [])
        stage_fit = 1.0 if stage and stage in indexed_stage_fit else 0.35
        score += stage_fit * 0.12

        indexed_journey = pack.get("journey_stage", "")
        journey_fit = 1.0 if indexed_journey == journey_stage else 0.35
        score += journey_fit * 0.1

        resource_fit_score = resource_profile_fit(pack.get("resource_profile", ""), context)
        score += resource_fit_score * 0.08

        if score > 0:
            results.append(SearchResult(
                id=pack.get("id", ""),
                name=pack.get("name", ""),
                type="method_pack",
                score=round(min(1.5, score), 4),
                highlights=pack.get("decision_rules", [])[:2] or [pack.get("summary", "")],
                metadata={
                    "file": pack.get("file", ""),
                    "domains": pack.get("domains", []),
                    "categories": pack.get("categories", []),
                    "problem_types": pack.get("problem_types", []),
                    "source_skills": pack.get("source_skills", []),
                    "growth_process": pack.get("growth_process", growth_process),
                    "journey_stage": indexed_journey or journey_stage,
                    "stage_fit": round(stage_fit, 2),
                    "journey_fit": round(journey_fit, 2),
                    "resource_fit": round(resource_fit_score, 2),
                    "resource_profile": pack.get("resource_profile", ""),
                    "guardrails": pack.get("guardrails", [])[:3],
                    "experiment_shapes": pack.get("experiment_shapes", [])[:3],
                    "related_weapons": pack.get("related_weapons", []),
                    "related_failures": pack.get("related_failures", []),
                    "evidence_tier": pack.get("evidence_tier", "C"),
                }
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]
