#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from knowledge_retriever import KnowledgeRetriever


def test_referral_query_returns_weapons_and_theories():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "设计裂变机制",
        {"problem_type": "referral"},
        case_limit=3,
        weapon_limit=3,
        theory_limit=2,
    )

    assert results["weapons"], "Expected referral query to return weapon recommendations"
    assert results["theories"], "Expected referral query to return related theories"
    assert any(item["metadata"]["category"] == "viral-referral" for item in results["weapons"])


def test_saas_acquisition_prefers_plg_or_cold_start():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "SaaS产品如何获取首批用户",
        {"industry": "saas", "problem_type": "acquisition", "stage": "0-1"},
        case_limit=3,
        weapon_limit=5,
        theory_limit=2,
    )

    categories = {item["metadata"]["category"] for item in results["weapons"]}
    assert categories & {"plg", "cold-start"}, f"Unexpected categories: {categories}"
