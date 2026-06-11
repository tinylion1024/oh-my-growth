#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from strategy_brain import StrategyBrain


def test_early_stage_saas_acquisition_avoids_paid_ads_as_top_priority():
    analysis = StrategyBrain().analyze(
        "SaaS产品如何获取首批1000用户",
        {"industry": "saas", "stage": "0-1", "problem_type": "acquisition"},
        mode="diagnose",
    )

    assert analysis["priorities"], "Expected at least one strategy priority"
    assert analysis["priorities"][0].category != "paid-ads"


def test_referral_problem_is_classified_as_user_acquisition():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"industry": "saas", "stage": "1-10", "problem_type": "referral"},
        mode="diagnose",
    )

    assert analysis["growth_process"]["name"] == "用户获取"


def test_evidence_chain_surfaces_case_weapon_or_theory_support():
    analysis = StrategyBrain().analyze(
        "如何提升月活跃用户留存率",
        {"industry": "content", "stage": "1-10", "problem_type": "retention"},
        mode="diagnose",
    )

    assert analysis["evidence_chain"], "Expected evidence chain to be populated"
    assert any(item["type_label"] in {"玩法", "案例", "理论"} for item in analysis["evidence_chain"])


def test_journey_override_changes_retrieval_fit_metadata():
    brain = StrategyBrain()

    reach_analysis = brain.analyze(
        "如何提升注册转化",
        {
            "industry": "saas",
            "stage": "0-1",
            "problem_type": "acquisition",
            "journey_stage": "认知/到达",
        },
        mode="diagnose",
    )
    share_analysis = brain.analyze(
        "如何提升注册转化",
        {
            "industry": "saas",
            "stage": "0-1",
            "problem_type": "acquisition",
            "journey_stage": "分享",
        },
        mode="diagnose",
    )

    assert reach_analysis["evidence_chain"], "Expected evidence chain for reach analysis"
    assert share_analysis["evidence_chain"], "Expected evidence chain for share analysis"
    assert reach_analysis["evidence_chain"][0]["why"] != share_analysis["evidence_chain"][0]["why"]


def test_history_file_adds_repeat_failure_warning():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {
            "problem_type": "referral",
            "company_profile": {
                "company_name": "WriteFlow AI",
                "target_user": "内容团队和独立创作者",
            },
            "experiment_log": {
                "experiments": [
                    {
                        "name": "高补贴邀请裂变",
                        "category": "viral-referral",
                        "outcome": "failed",
                        "avoid_repeat": "不要再用高补贴直接拉低质量用户",
                    }
                ]
            },
        },
        mode="diagnose",
    )

    assert any("不要重复历史失败模式" in item for item in analysis["avoid_now"])
    assert any("WriteFlow AI" in item or "内容团队和独立创作者" in item for item in analysis["memory_summary"])


def test_budget_context_produces_kelly_allocation():
    analysis = StrategyBrain().analyze(
        "SaaS产品如何获取首批1000用户",
        {
            "industry": "saas",
            "stage": "0-1",
            "problem_type": "acquisition",
            "budget": "5万元",
            "metric": "新增高意向试用用户数",
            "goal": "拿到首批100个试用用户",
            "history": "做过种子用户外联，效果较好",
        },
        mode="diagnose",
    )

    assert analysis["kelly_allocation"] is not None
    assert analysis["kelly_allocation"]["budget_amount"] == 50000
    assert "风险预算" in analysis["kelly_allocation"]["recommended_ratio_text"]


def test_competitive_context_triggers_game_theory_layer():
    analysis = StrategyBrain().analyze(
        "如果竞品跟进我们的邀请机制怎么办",
        {
            "industry": "saas",
            "stage": "1-10",
            "problem_type": "referral",
            "competitor": "CompetitorX",
            "market_structure": "竞争激烈的平台市场",
        },
        mode="diagnose",
    )

    assert analysis["game_theory"] is not None
    assert analysis["game_theory"]["competitor"] == "CompetitorX"
    assert analysis["game_theory"]["game_type_label"] in {"平台博弈", "竞争反应博弈"}


def test_marketplace_without_competitive_context_does_not_trigger_game_theory():
    analysis = StrategyBrain().analyze(
        "Marketplace 冷启动时应该先补哪一侧供需",
        {
            "industry": "marketplace",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效撮合数",
            "goal": "突破首批供需匹配",
            "constraints": "不能同时大规模补贴两侧",
            "company_profile": {"business_model": "marketplace"},
        },
        mode="diagnose",
    )

    assert analysis["game_theory"] is None
    assert any("供给侧" in item or "需求侧" in item or "单边流动性" in item for item in analysis["do_now"])


def test_marketplace_demand_query_reflects_demand_side_focus():
    analysis = StrategyBrain().analyze(
        "Marketplace 冷启动先补需求侧还是供给侧",
        {
            "industry": "marketplace",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效撮合数",
            "goal": "突破首批有效撮合",
            "constraints": "不能同时大规模补贴两侧",
            "company_profile": {"business_model": "marketplace"},
        },
        mode="diagnose",
    )

    assert "先补需求侧密度" in analysis["core_tension"] or any("先补需求侧密度" in item for item in analysis["do_now"])


def test_marketplace_decision_memo_exposes_platform_side_diagnosis():
    brain = StrategyBrain()
    analysis = brain.analyze(
        "Marketplace 冷启动先补供给侧还是需求侧",
        {
            "industry": "marketplace",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效撮合数",
            "goal": "突破首批有效撮合",
            "constraints": "不能同时大规模补贴两侧",
            "company_profile": {"business_model": "marketplace"},
        },
        mode="diagnose",
    )

    assert analysis["marketplace_diagnosis"] is not None
    assert analysis["marketplace_diagnosis"]["side_focus"]
    memo = brain.to_decision_memo_markdown(analysis)
    assert "平台侧判断" in memo
    assert "运行规则" in memo


def test_local_services_query_prefers_single_city_density():
    analysis = StrategyBrain().analyze(
        "本地生活平台冷启动应该先铺多城还是先打透单城",
        {
            "industry": "local-services",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效履约订单数",
            "goal": "在单城跑通供需和履约闭环",
            "constraints": "不能多城同时烧钱补贴",
            "company_profile": {"business_model": "local services marketplace"},
        },
        mode="diagnose",
    )

    assert analysis["game_theory"] is None
    assert analysis["local_services_diagnosis"] is not None
    assert "单城" in analysis["core_tension"] or any("单城" in item for item in analysis["do_now"])


def test_local_services_decision_memo_exposes_operating_rule():
    brain = StrategyBrain()
    analysis = brain.analyze(
        "本地生活平台冷启动应该先铺多城还是先打透单城",
        {
            "industry": "local-services",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效履约订单数",
            "goal": "在单城跑通供需和履约闭环",
            "constraints": "不能多城同时烧钱补贴",
            "company_profile": {"business_model": "local services marketplace"},
        },
        mode="diagnose",
    )

    memo = brain.to_decision_memo_markdown(analysis)
    assert "本地生活判断" in memo
    assert "单城" in memo


def test_b2b_sales_led_business_model_diagnosis_is_explicit():
    brain = StrategyBrain()
    analysis = brain.analyze(
        "B2B 销售驱动型 SaaS 应该先扩销售还是先修线索质量",
        {
            "industry": "saas",
            "stage": "1-10",
            "problem_type": "acquisition",
            "metric": "高意向线索数",
            "goal": "提升成单效率",
            "constraints": "不能先扩销售团队",
            "company_profile": {"business_model": "b2b sales-led saas"},
        },
        mode="diagnose",
    )

    assert analysis["business_model_diagnosis"] is not None
    assert analysis["business_model_diagnosis"]["label"] == "B2B 销售驱动"
    executive = brain.to_executive_markdown(analysis)
    assert "业务形态判断" in executive
    assert "线索质量" in executive


def test_ai_cold_start_business_model_diagnosis_is_explicit():
    brain = StrategyBrain()
    analysis = brain.analyze(
        "AI 产品冷启动阶段应该先做内容获客还是产品内分享",
        {
            "industry": "ai",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "高意向试用数",
            "goal": "拿到首批稳定试用用户",
            "constraints": "团队很小，不能同时做内容矩阵和复杂分享机制",
            "company_profile": {"business_model": "ai copilot"},
        },
        mode="diagnose",
    )

    assert analysis["business_model_diagnosis"] is not None
    assert analysis["business_model_diagnosis"]["label"] == "AI 冷启动"
    fast_scan = brain.to_fast_scan_markdown(analysis)
    assert "业务形态判断" in fast_scan
    assert "首次价值达成" in fast_scan


def test_qbr_surfaces_business_model_diagnosis():
    brain = StrategyBrain()
    analysis = brain.analyze(
        "本地生活平台冷启动应该先铺多城还是先打透单城",
        {
            "industry": "local-services",
            "stage": "0-1",
            "problem_type": "acquisition",
            "metric": "有效履约订单数",
            "goal": "在单城跑通供需和履约闭环",
            "constraints": "不能多城同时烧钱补贴",
            "company_profile": {"business_model": "local services marketplace"},
        },
        mode="diagnose",
    )

    qbr = brain.to_qbr_markdown(analysis)
    assert "业务形态判断" in qbr
    assert "本地生活" in qbr


def test_referral_problem_includes_failure_modes():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"problem_type": "referral"},
        mode="diagnose",
    )

    assert analysis["failure_modes"], "Expected failure mode guidance"
    assert any("高补贴裂变" in item["title"] for item in analysis["failure_modes"])


def test_top_priority_carries_evidence_support_bonus():
    analysis = StrategyBrain().analyze(
        "SaaS产品如何获取首批1000用户",
        {"industry": "saas", "stage": "0-1", "problem_type": "acquisition"},
        mode="diagnose",
    )

    top_priority = analysis["priorities"][0]
    assert top_priority.support_bonus > 0
    assert top_priority.evidence_support
    assert any("支持" in item or "理论" in item or "案例" in item for item in top_priority.evidence_support)


def test_referral_priority_accumulates_failure_risk_penalty():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"industry": "saas", "stage": "1-10", "problem_type": "referral"},
        mode="diagnose",
    )

    top_priority = analysis["priorities"][0]
    assert top_priority.risk_penalty > 0
    assert top_priority.risk_signals
    assert "失败模式" in top_priority.risk_signals[0]


def test_why_not_reasons_now_include_evidence_and_risk_context():
    analysis = StrategyBrain().analyze(
        "如何提升月活跃用户留存率",
        {"industry": "content", "stage": "1-10", "problem_type": "retention"},
        mode="diagnose",
    )

    why_not = analysis["decision_process"]["why_not"]
    assert why_not
    assert any("支持证据" in item["reason"] for item in why_not)


def test_core_tension_references_case_or_theory_evidence():
    analysis = StrategyBrain().analyze(
        "SaaS产品如何获取首批1000用户",
        {"industry": "saas", "stage": "0-1", "problem_type": "acquisition"},
        mode="diagnose",
    )

    assert "案例「" in analysis["core_tension"] or "理论「" in analysis["core_tension"]


def test_experiment_design_reuses_case_or_theory_clues():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"industry": "saas", "stage": "1-10", "problem_type": "referral"},
        mode="diagnose",
    )

    experiment = analysis["experiment"]
    combined_text = " ".join([experiment["hypothesis"], *experiment["steps"], *experiment["success_signals"], *experiment["stop_signals"]])
    assert "案例「" in combined_text or "理论「" in combined_text


def test_resource_allocation_and_projection_reference_evidence():
    analysis = StrategyBrain().analyze(
        "如何提升月活跃用户留存率",
        {"industry": "content", "stage": "1-10", "problem_type": "retention"},
        mode="diagnose",
    )

    allocation = analysis["resource_allocation"]
    projection = analysis["projection"]
    assert "案例「" in allocation["increase"] or "理论「" in allocation["decrease"]
    assert "案例「" in projection["evidence"] or "理论「" in projection["evidence"]


def test_actions_reference_case_or_theory_clues():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"industry": "saas", "stage": "1-10", "problem_type": "referral"},
        mode="diagnose",
    )

    actions = analysis["actions"]
    assert actions
    combined = " ".join(item["acceptance"] + " " + item["change"] for item in actions)
    assert "案例「" in combined or "理论「" in combined


def test_review_trigger_uses_guardrail_and_evidence_reference():
    analysis = StrategyBrain().analyze(
        "我们要不要做邀请裂变",
        {"industry": "saas", "stage": "1-10", "problem_type": "referral"},
        mode="diagnose",
    )

    review = analysis["review_trigger"]
    assert "尤其是" in review["signal"]
    assert "案例「" in review["evidence"] or "理论「" in review["evidence"]


def test_current_state_lists_case_or_theory_as_observed_fact():
    analysis = StrategyBrain().analyze(
        "如何提升月活跃用户留存率",
        {"industry": "content", "stage": "1-10", "problem_type": "retention"},
        mode="diagnose",
    )

    facts = analysis["current_state"]["facts"]
    assert any("当前最相近案例" in fact or "当前主要解释框架" in fact for fact in facts)


def test_no_paid_ads_constraint_penalizes_paid_ads_direction():
    context = {
        "industry": "saas",
        "stage": "0-1",
        "problem_type": "acquisition",
        "constraints": "不能扩招聘，不能依赖付费投放",
        "budget": "5000元",
        "team": "1人",
    }
    brain = StrategyBrain()
    analysis = brain.analyze(
        "0-1 SaaS 在预算极低情况下是否该投广告",
        context,
        mode="diagnose",
    )

    categories = {item.category for item in analysis["priorities"]}
    assert "paid-ads" not in categories
    results = brain.retriever.retrieve(
        "0-1 SaaS 在预算极低情况下是否该投广告",
        context,
        case_limit=3,
        weapon_limit=20,
        theory_limit=2,
    )
    options = brain._prioritize_options(results, context)
    paid_ads_options = [item for item in options if item.category == "paid-ads"]
    assert paid_ads_options, "Expected paid-ads candidates to exist in the broader option set"
    assert all(item.constraint_penalty > 0 for item in paid_ads_options)


def test_no_high_incentive_constraint_penalizes_viral_referral_when_not_primary_problem():
    analysis = StrategyBrain().analyze(
        "内容产品当前留存很差，是否要靠高补贴裂变拉活",
        {
            "industry": "content",
            "stage": "1-10",
            "problem_type": "retention",
            "constraints": "不能用高补贴制造假活跃",
        },
        mode="diagnose",
    )

    assert analysis["priorities"][0].category == "retention"
    assert all(item.category != "viral-referral" for item in analysis["priorities"])


def test_retention_sensitive_constraint_penalizes_aggressive_monetization_variants():
    analysis = StrategyBrain().analyze(
        "变现压力很大时是否直接上强付费墙",
        {
            "industry": "saas",
            "stage": "1-10",
            "problem_type": "monetization",
            "constraints": "不能伤害核心留存",
            "metric": "付费转化率",
            "goal": "两个月内提升收入",
        },
        mode="diagnose",
    )

    for item in analysis["priorities"]:
        if item.name in {"限时优惠", "年付折扣"}:
            assert item.constraint_penalty > 0
