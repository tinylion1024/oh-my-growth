#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from knowledge_retriever import KnowledgeRetriever
from strategy_brain import StrategyBrain


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


def test_b2b_sales_led_context_surfaces_b2b_sales_with_journey_fit():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "B2B 销售驱动型 SaaS 应该先扩销售还是先修线索质量",
        {
            "industry": "saas",
            "problem_type": "acquisition",
            "stage": "1-10",
            "company_profile": {"business_model": "b2b sales-led saas"},
        },
        case_limit=3,
        weapon_limit=8,
        theory_limit=2,
    )

    b2b_weapons = [item for item in results["weapons"] if item["metadata"]["category"] == "b2b-sales"]
    assert b2b_weapons, "Expected B2B sales-led context to surface b2b-sales weapons"
    assert b2b_weapons[0]["metadata"]["journey_fit"] >= 0.9


def test_marketplace_supply_query_prefers_marketplace_cases_with_side_metadata():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "Marketplace 冷启动先补供给侧还是需求侧",
        {
            "industry": "marketplace",
            "problem_type": "acquisition",
            "stage": "0-1",
            "company_profile": {"business_model": "marketplace"},
            "goal": "突破首批有效撮合",
            "metric": "有效撮合数",
        },
        case_limit=5,
        weapon_limit=5,
        theory_limit=3,
    )

    assert results["cases"], "Expected marketplace cases"
    assert any(item["metadata"]["company_type"] == "marketplace" for item in results["cases"])
    assert any(item["metadata"]["marketplace_side"] in {"supply", "liquidity"} for item in results["cases"])
    assert any(item["metadata"]["marketplace_side"] == "liquidity" for item in results["theories"])


def test_marketplace_side_focus_changes_case_ranking_bias():
    retriever = KnowledgeRetriever()
    common_context = {
        "industry": "marketplace",
        "problem_type": "acquisition",
        "stage": "0-1",
        "company_profile": {"business_model": "marketplace"},
        "metric": "有效撮合数",
        "goal": "突破首批有效撮合",
    }
    supply_results = retriever.retrieve(
        "Marketplace 冷启动先补供给侧还是需求侧",
        common_context,
        case_limit=3,
        weapon_limit=3,
        theory_limit=2,
    )
    demand_results = retriever.retrieve(
        "Marketplace 冷启动先补需求侧还是供给侧",
        common_context,
        case_limit=3,
        weapon_limit=3,
        theory_limit=2,
    )

    assert supply_results["cases"] and demand_results["cases"]
    supply_side = supply_results["cases"][0]["metadata"]["marketplace_side"]
    demand_side = demand_results["cases"][0]["metadata"]["marketplace_side"]
    assert supply_side in {"supply", "liquidity"}
    assert demand_side in {"demand", "liquidity"}
    assert supply_side != demand_side or demand_side == "liquidity"


def test_marketplace_side_focus_changes_weapon_ranking_bias():
    retriever = KnowledgeRetriever()
    common_context = {
        "industry": "marketplace",
        "problem_type": "acquisition",
        "stage": "0-1",
        "company_profile": {"business_model": "marketplace"},
        "metric": "有效撮合数",
        "goal": "突破首批有效撮合",
        "constraints": "不能同时大规模补贴两侧",
    }
    supply_results = retriever.retrieve(
        "Marketplace 冷启动先补供给侧还是需求侧",
        common_context,
        case_limit=3,
        weapon_limit=5,
        theory_limit=2,
    )
    demand_results = retriever.retrieve(
        "Marketplace 冷启动先补需求侧还是供给侧",
        common_context,
        case_limit=3,
        weapon_limit=5,
        theory_limit=2,
    )

    assert supply_results["weapons"] and demand_results["weapons"]
    assert supply_results["weapons"][0]["metadata"]["marketplace_side"] in {"supply", "liquidity"}
    assert demand_results["weapons"][0]["metadata"]["marketplace_side"] in {"demand", "liquidity"}


def test_local_services_context_prefers_local_service_cases():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "本地生活平台冷启动应该先铺多城还是先打透单城",
        {
            "industry": "local-services",
            "problem_type": "acquisition",
            "stage": "0-1",
            "company_profile": {"business_model": "local services marketplace"},
            "metric": "有效履约订单数",
            "goal": "在单城跑通供需和履约闭环",
            "constraints": "不能多城同时烧钱补贴",
        },
        case_limit=5,
        weapon_limit=5,
        theory_limit=2,
    )

    assert results["cases"], "Expected local-services cases"
    assert results["cases"][0]["metadata"]["company_type"] in {"local-services", "marketplace"}
    assert any(item["metadata"]["company_type"] == "local-services" for item in results["cases"])
    assert results["weapons"][0]["metadata"]["category"] in {"cold-start", "community"}
    assert results["weapons"][0]["metadata"]["marketplace_side"] in {"supply", "liquidity", ""}


def test_journey_stage_changes_weapon_fit_metadata():
    retriever = KnowledgeRetriever()

    reach_results = retriever.retrieve(
        "如何提升注册转化",
        {
            "industry": "saas",
            "problem_type": "acquisition",
            "stage": "0-1",
            "journey_stage": "认知/到达",
        },
        case_limit=2,
        weapon_limit=3,
        theory_limit=1,
    )
    share_results = retriever.retrieve(
        "如何提升注册转化",
        {
            "industry": "saas",
            "problem_type": "acquisition",
            "stage": "0-1",
            "journey_stage": "分享",
        },
        case_limit=2,
        weapon_limit=3,
        theory_limit=1,
    )

    assert reach_results["weapons"], "Expected reach-oriented weapon recommendations"
    assert share_results["weapons"], "Expected share-oriented weapon recommendations"
    assert reach_results["weapons"][0]["metadata"]["journey_fit"] != share_results["weapons"][0]["metadata"]["journey_fit"]


def test_weapon_results_include_indexed_failure_refs_and_profiles():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "我们要不要做邀请裂变",
        {"problem_type": "referral", "stage": "1-10"},
        case_limit=2,
        weapon_limit=3,
        theory_limit=1,
    )

    assert results["weapons"], "Expected weapon recommendations"
    top_weapon = results["weapons"][0]
    assert top_weapon["metadata"]["growth_process"] in {"用户获取", "用户深耕"}
    assert top_weapon["metadata"]["failure_refs"], "Expected failure refs from index"
    assert top_weapon["metadata"]["resource_profile"], "Expected resource profile from index"
    assert "resource_profile_fit" in top_weapon["metadata"]


def test_theory_results_include_enriched_schema_fields():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "SaaS 产品如何通过产品自增长",
        {"industry": "saas", "problem_type": "activation", "stage": "1-10"},
        case_limit=2,
        weapon_limit=2,
        theory_limit=3,
    )

    assert results["theories"], "Expected theory recommendations"
    top_theory = results["theories"][0]
    assert top_theory["metadata"]["growth_process"] in {"用户获取", "用户深耕", "增长经营"}
    assert top_theory["metadata"]["journey_stage"]
    assert isinstance(top_theory["metadata"]["failure_refs"], list)
    assert "resource_fit" in top_theory["metadata"]


def test_small_team_context_prefers_low_budget_resource_profiles():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "如何提升注册转化",
        {
            "industry": "saas",
            "problem_type": "acquisition",
            "stage": "0-1",
            "budget": "5000元",
            "team": "1人",
            "constraints": "不能依赖付费投放",
        },
        case_limit=2,
        weapon_limit=5,
        theory_limit=2,
    )

    assert results["weapons"], "Expected weapon recommendations"
    top_weapon = results["weapons"][0]
    assert top_weapon["metadata"]["category"] == "cold-start"
    assert top_weapon["metadata"]["resource_profile_fit"] >= 0.9


def test_paid_ads_retrieval_carries_guardrail_penalty_when_constraints_conflict():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "如何快速放大投放获客",
        {
            "industry": "saas",
            "problem_type": "acquisition",
            "stage": "10-100",
            "budget": "5000元",
            "team": "1人",
            "constraints": "不能依赖付费投放，预算有限",
        },
        case_limit=2,
        weapon_limit=10,
        theory_limit=2,
    )

    paid_ads = [item for item in results["weapons"] if item["metadata"]["category"] == "paid-ads"]
    assert paid_ads, "Expected paid-ads options to remain retrievable for contrast"
    assert paid_ads[0]["metadata"]["guardrail_penalty"] > 0


def test_failure_results_are_retrievable_for_referral_context():
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(
        "我们要不要做邀请裂变",
        {"problem_type": "referral", "stage": "1-10", "journey_stage": "分享"},
        case_limit=2,
        weapon_limit=2,
        theory_limit=1,
        failure_limit=2,
    )

    assert results["failures"], "Expected failure-mode recommendations"
    top_failure = results["failures"][0]
    assert "referral" in top_failure["metadata"]["problem_types"]
    assert top_failure["metadata"]["journey_stage"] == "分享"


def test_marketing_growth_method_packs_are_retrievable_by_growth_problem():
    retriever = KnowledgeRetriever()

    seo_results = retriever.retrieve(
        "我们的网站搜索流量很少，需要做 SEO 和 AEO 获客",
        {"industry": "saas", "problem_type": "acquisition", "stage": "1-10"},
        case_limit=1,
        weapon_limit=1,
        theory_limit=1,
        method_pack_limit=3,
    )
    seo_pack_ids = {item["id"] for item in seo_results["method_packs"]}
    assert "seo-aeo-growth-system" in seo_pack_ids
    assert seo_results["method_packs"][0]["metadata"]["source_skills"]
    assert seo_results["method_packs"][0]["metadata"]["related_weapons"]
    assert seo_results["method_packs"][0]["metadata"]["related_failures"]

    geo_results = retriever.retrieve(
        "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率",
        {"industry": "saas", "problem_type": "acquisition", "stage": "10-100"},
        case_limit=1,
        weapon_limit=1,
        theory_limit=1,
        method_pack_limit=3,
    )
    geo_pack_ids = {item["id"] for item in geo_results["method_packs"]}
    assert "geo-llm-discovery-system" in geo_pack_ids

    cro_results = retriever.retrieve(
        "落地页访问不少，但是注册和试用转化率很低，想做 CRO",
        {"industry": "saas", "problem_type": "activation", "stage": "1-10"},
        case_limit=1,
        weapon_limit=1,
        theory_limit=1,
        method_pack_limit=3,
    )
    cro_pack_ids = {item["id"] for item in cro_results["method_packs"]}
    assert "conversion-rate-optimization-system" in cro_pack_ids

    ads_results = retriever.retrieve(
        "Meta 和 Google 广告 CPA 太高，创意测试没有结论",
        {"industry": "ecommerce", "problem_type": "acquisition", "stage": "10-100"},
        case_limit=1,
        weapon_limit=1,
        theory_limit=1,
        method_pack_limit=3,
    )
    ads_pack_ids = {item["id"] for item in ads_results["method_packs"]}
    assert "paid-acquisition-creative-system" in ads_pack_ids


def test_method_pack_shapes_geo_diagnosis_experiment_and_evidence():
    analysis = StrategyBrain().analyze(
        "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率",
        {"industry": "saas", "problem_type": "acquisition", "stage": "10-100"},
        mode="diagnose",
    )

    assert analysis["reference_method_packs"][0]["id"] == "geo-llm-discovery-system"
    assert any(item["type_label"] == "操作系统" for item in analysis["evidence_chain"])
    assert any("GEO/LLM 发现系统" in step for step in analysis["experiment"]["steps"])
    assert any("方法包停止线" in signal for signal in analysis["experiment"]["stop_signals"])
    assert analysis["priorities"][0].method_pack_bonus > 0
