#!/usr/bin/env python3
"""Knowledge Retriever - Compatibility wrapper.

This module provides backward compatibility by re-exporting from the retriever package.
"""

try:
    from .retriever import (
        BASE_DIR,
        STAGE_ALIASES,
        normalize_stage,
        normalize_text,
        tokenize,
        compute_similarity,
        expand_query,
        build_query_tokens,
        context_business_model,
        context_business_model_kind,
        context_marketplace_side_focus,
        context_preferred_categories,
        context_preferred_theories,
        problem_to_categories,
        problem_to_theories,
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
        search_cases,
        search_weapons,
        search_theories,
        search_failures,
        search_method_packs,
        SearchResult,
        KnowledgeRetriever,
    )
except ImportError:  # pragma: no cover - direct script compatibility.
    from retriever import (
        BASE_DIR,
        STAGE_ALIASES,
        normalize_stage,
        normalize_text,
        tokenize,
        compute_similarity,
        expand_query,
        build_query_tokens,
        context_business_model,
        context_business_model_kind,
        context_marketplace_side_focus,
        context_preferred_categories,
        context_preferred_theories,
        problem_to_categories,
        problem_to_theories,
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
        search_cases,
        search_weapons,
        search_theories,
        search_failures,
        search_method_packs,
        SearchResult,
        KnowledgeRetriever,
    )


def main():
    """测试检索功能"""
    retriever = KnowledgeRetriever()

    # 测试用例
    test_queries = [
        {
            'query': 'SaaS产品如何获取首批用户',
            'context': {'industry': 'saas', 'problem_type': 'acquisition', 'stage': '0-1'}
        },
        {
            'query': '如何提升用户留存率',
            'context': {'industry': 'education', 'problem_type': 'retention', 'stage': '1-10'}
        },
        {
            'query': '设计裂变机制',
            'context': {'problem_type': 'referral'}
        }
    ]

    for test in test_queries:
        print(f"\n查询: {test['query']}")
        print(f"上下文: {test.get('context', {})}")
        print("-" * 50)

        results = retriever.retrieve(test['query'], test.get('context'))

        print(f"\n案例 ({len(results['cases'])} 个):")
        for case in results['cases']:
            print(f"  - {case['name']} (分数: {case['score']:.2f}, 证据等级: {case['metadata']['evidence_tier']})")

        print(f"\n玩法 ({len(results['weapons'])} 个):")
        for weapon in results['weapons']:
            print(f"  - {weapon['name']} (分数: {weapon['score']:.2f}, 难度: {weapon['metadata']['effort']}, 影响: {weapon['metadata']['impact']})")

        print(f"\n理论 ({len(results['theories'])} 个):")
        for theory in results['theories']:
            print(f"  - {theory['name']} (分数: {theory['score']:.2f})")


if __name__ == "__main__":
    main()
