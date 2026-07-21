#!/usr/bin/env python3
"""Strategy-brain layer that turns retrieval into operator-friendly recommendations."""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from .bayesian_decision import BayesianDecision
    from .gametheory_analysis import GameTheoryAnalysis, GameType
    from .kelly_sizing import KellySizing
    from .knowledge_retriever import KnowledgeRetriever
    from .strategy.constants import (
        PROBLEM_LABELS,
        STAGE_FRAMEWORK,
        PROBLEM_TO_PROCESS,
        PROBLEM_TO_JOURNEY,
        CATEGORY_ACTIONS,
        CATEGORY_AVOIDS,
    )
    from .strategy.builder import StrategyBuilder
    from .strategy.formatter import StrategyFormatter
    from .strategy.history import StrategyHistory
    from .strategy.scorer import StrategyScorer
except ImportError:  # pragma: no cover - direct script compatibility.
    from bayesian_decision import BayesianDecision
    from gametheory_analysis import GameTheoryAnalysis, GameType
    from kelly_sizing import KellySizing
    from knowledge_retriever import KnowledgeRetriever
    from strategy.constants import (
        PROBLEM_LABELS,
        STAGE_FRAMEWORK,
        PROBLEM_TO_PROCESS,
        PROBLEM_TO_JOURNEY,
        CATEGORY_ACTIONS,
        CATEGORY_AVOIDS,
    )
    from strategy.builder import StrategyBuilder
    from strategy.formatter import StrategyFormatter
    from strategy.history import StrategyHistory
    from strategy.scorer import StrategyScorer

# Keep local references for backward compatibility (deprecated, will be removed)
# All constants are now imported from strategy.constants


@dataclass
class StrategyOption:
    name: str
    category: str
    category_name: str
    score: float
    effort: str
    impact: str
    evidence_tier: str
    why_now: str
    key_risk: str
    stage_fit: float = 0.0
    resource_fit: float = 0.0
    journey_fit: float = 0.0
    resource_profile_fit: float = 0.0
    journey_stage: str = ""
    marketplace_side: str = ""
    guardrail_risk: str = ""
    resource_profile: str = ""
    failure_refs: List[str] = field(default_factory=list)
    evidence_support: List[str] = field(default_factory=list)
    risk_signals: List[str] = field(default_factory=list)
    support_bonus: float = 0.0
    risk_penalty: float = 0.0
    constraint_penalty: float = 0.0
    framework_bonus: float = 0.0
    metric_bonus: float = 0.0
    history_adjustment: float = 0.0
    history_condition_penalty: float = 0.0
    explicit_guardrail_penalty: float = 0.0
    method_pack_bonus: float = 0.0


class StrategyBrain:
    """Generate operator-oriented strategy recommendations from the retrieval layer."""

    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()
        self.builder = StrategyBuilder(self)
        self.history = StrategyHistory(self)
        self.scorer = StrategyScorer(self)
        self.formatter = StrategyFormatter(self)

    def _build_retrieval_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy method for backward compatibility with tests."""
        return self.builder._build_retrieval_context(context)

    def _get_experiment_log(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Proxy method for backward compatibility with builder."""
        return self.history._get_experiment_log(context)

    def _history_repeat_risk_prompts(self, context: Dict[str, Any]) -> List[str]:
        """Proxy method for backward compatibility with builder."""
        return self.history._history_repeat_risk_prompts(context)

    def analyze(self, query: str, context: Dict[str, str], mode: str = "assess") -> Dict:
        working_context = self.builder._build_retrieval_context(context)
        results = self.retriever.retrieve(
            query,
            working_context,
            case_limit=5,
            weapon_limit=6,
            theory_limit=3,
            method_pack_limit=3,
        )
        options = self._prioritize_options(results, working_context)
        top_option = options[0] if options else None
        decision_text, confidence_label, posterior = self.builder._build_confidence(query, working_context, results, top_option)
        decision_process = self.builder._build_decision_process(options)
        actions = self.builder._build_actions(query, working_context, top_option, results)
        growth_process = self.builder._build_growth_process(working_context)
        north_star = self.builder._build_north_star(working_context)
        evidence_chain = self.builder._build_evidence_chain(results, top_option, working_context)
        memory_summary = self.builder._build_memory_summary(working_context)
        kelly_allocation = self.builder._build_kelly_allocation(working_context, top_option, posterior)
        game_theory = self.builder._build_game_theory_analysis(query, working_context, top_option)
        failure_modes = self.builder._build_failure_modes(working_context, top_option, results)
        protection_controls = self.history._history_protection_controls(working_context, top_option)
        return {
            "query": query,
            "mode": mode,
            "context_summary": self.builder._build_context_summary(working_context),
            "problem_label": PROBLEM_LABELS.get(working_context.get("problem_type", ""), "增长"),
            "stage_diagnosis": self.builder._build_stage_diagnosis(working_context),
            "growth_process": growth_process,
            "north_star": north_star,
            "journey_focus": self.builder._build_journey_focus(working_context),
            "marketplace_diagnosis": self.builder._build_marketplace_diagnosis(query, working_context, top_option, results),
            "local_services_diagnosis": self.builder._build_local_services_diagnosis(query, working_context, top_option, results),
            "business_model_diagnosis": self.builder._build_business_model_diagnosis(query, working_context, top_option, results),
            "measurement_notes": self.builder._build_measurement_notes(working_context, top_option, north_star, growth_process),
            "evidence_chain": evidence_chain,
            "memory_summary": memory_summary,
            "kelly_allocation": kelly_allocation,
            "game_theory": game_theory,
            "failure_modes": failure_modes,
            "protection_controls": protection_controls,
            "decision_line": self.builder._build_decision_line(query, working_context, top_option, decision_text, confidence_label),
            "core_tension": self.builder._build_core_tension(query, working_context, top_option, evidence_chain, results),
            "why_now": self.builder._build_why_now(working_context, top_option, results, evidence_chain),
            "priorities": options[:3],
            "do_now": self.builder._build_do_now(top_option, working_context),
            "avoid_now": self.builder._build_avoid_now(top_option, working_context),
            "experiment": self.builder._build_experiment(query, working_context, top_option, results, protection_controls),
            "decision_process": decision_process,
            "resource_allocation": self.builder._build_resource_allocation(working_context, top_option, results),
            "actions": actions,
            "projection": self.builder._build_projection(working_context, top_option, results),
            "review_trigger": self.builder._build_review_trigger(working_context, top_option, results, protection_controls),
            "caveats": self.builder._build_caveats(top_option, working_context),
            "missing_info": self.builder._build_missing_info(working_context),
            "reference_cases": results["cases"][:3],
            "reference_theories": results["theories"][:2],
            "reference_failures": results.get("failures", [])[:2],
            "reference_method_packs": results.get("method_packs", [])[:3],
            "decision_text": decision_text,
            "confidence_label": confidence_label,
            "confidence_score": posterior,
            "current_state": self.builder._build_current_state(working_context, results),
        }

    def to_json(self, analysis: Dict) -> str:
        """Serialize an analysis payload with StrategyOption objects expanded."""
        serializable = analysis.copy()
        serializable["priorities"] = [option.__dict__ for option in analysis["priorities"]]
        return json.dumps(serializable, ensure_ascii=False, indent=2)

    def to_report_markdown(self, analysis: Dict, clarity_score: float, clarity_level: str, can_proceed: bool) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_report_markdown(analysis, clarity_score, clarity_level, can_proceed)

    def to_executive_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_executive_markdown(analysis)

    def to_assess_markdown(
        self,
        analysis: Dict,
        clarity_score: float,
        clarity_level: str,
        can_proceed: bool,
    ) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_assess_markdown(analysis, clarity_score, clarity_level, can_proceed)

    def to_design_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_design_markdown(analysis)

    def to_weekly_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_weekly_markdown(analysis)

    def to_experiment_card_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_experiment_card_markdown(analysis)

    def to_share_markdown(self, analysis: Dict) -> str:
        """Render a concise, public-safe experiment snapshot."""
        return self.formatter.to_share_markdown(analysis)

    def to_decision_memo_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_decision_memo_markdown(analysis)

    def to_qbr_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_qbr_markdown(analysis)

    def to_fast_scan_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_fast_scan_markdown(analysis)

    def to_brd_markdown(self, analysis: Dict) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_brd_markdown(analysis)

    def build_learning_path(self, query: str, context: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
        """Build a lightweight learning path around the retrieval results."""
        working_context = self.builder._build_retrieval_context(context)
        results = self.retriever.retrieve(
            query,
            working_context,
            case_limit=3,
            weapon_limit=4,
            theory_limit=3,
            method_pack_limit=3,
        )
        analysis = self.analyze(query, working_context, mode="learn")
        guide_map = {
            "acquisition": [
                {"name": "阶段判断", "file": "knowledge/guides/stage-diagnosis.md"},
                {"name": "AIDA 转化模型", "file": "knowledge/guides/aida-model.md"},
                {"name": "归因与身份识别", "file": "knowledge/guides/attribution-and-identity.md"},
            ],
            "retention": [
                {"name": "用户旅程诊断", "file": "knowledge/guides/user-journey-diagnosis.md"},
                {"name": "北极星指标", "file": "knowledge/guides/north-star-metrics.md"},
                {"name": "实验设计", "file": "knowledge/guides/experiment-design.md"},
            ],
            "monetization": [
                {"name": "北极星指标", "file": "knowledge/guides/north-star-metric.md"},
                {"name": "增长策略环", "file": "knowledge/guides/growth-loop.md"},
                {"name": "实验设计", "file": "knowledge/guides/experiment-design.md"},
            ],
            "referral": [
                {"name": "用户旅程诊断", "file": "knowledge/guides/user-journey-diagnosis.md"},
                {"name": "增长策略环", "file": "knowledge/guides/growth-loop.md"},
                {"name": "归因与身份识别", "file": "knowledge/guides/attribution-and-identity.md"},
            ],
        }
        guides = guide_map.get(context.get("problem_type", ""), guide_map["acquisition"])
        business_model_diag = analysis.get("business_model_diagnosis")

        def case_reason(item: Dict[str, Any]) -> str:
            meta = item.get("metadata", {})
            return (
                f"阶段匹配={meta.get('stage_fit', 0):.2f}，"
                f"旅程匹配={meta.get('journey_fit', 0):.2f}，"
                f"资源匹配={meta.get('resource_fit', 0):.2f}，"
                f"公司类型={meta.get('company_type', 'general')}"
            )

        def theory_reason(item: Dict[str, Any]) -> str:
            meta = item.get("metadata", {})
            return (
                f"主业务过程={meta.get('growth_process', '增长经营')}，"
                f"旅程={meta.get('journey_stage', '待补充')}，"
                f"资源匹配={meta.get('resource_fit', 0):.2f}"
            )

        def weapon_reason(item: Dict[str, Any]) -> str:
            meta = item.get("metadata", {})
            return (
                f"类别={meta.get('category_name', meta.get('category', ''))}，"
                f"阶段匹配={meta.get('stage_fit', 0):.2f}，"
                f"旅程匹配={meta.get('journey_fit', 0):.2f}，"
                f"资源画像匹配={meta.get('resource_profile_fit', meta.get('resource_fit', 0)):.2f}"
            )

        return {
            "guides": guides,
            "business_model_diagnosis": business_model_diag,
            "theories": [
                {
                    "name": item["name"],
                    "file": item["metadata"].get("file", ""),
                    "reason": theory_reason(item),
                }
                for item in results["theories"]
            ],
            "method_packs": [
                {
                    "name": item["name"],
                    "file": item["metadata"].get("file", ""),
                    "reason": "；".join(item.get("highlights", [])),
                }
                for item in results.get("method_packs", [])
            ],
            "cases": [
                {
                    "name": item["name"],
                    "id": item["id"],
                    "reason": case_reason(item),
                }
                for item in results["cases"]
            ],
            "weapons": [
                {
                    "name": item["name"],
                    "category": item["metadata"].get("category_name", ""),
                    "reason": weapon_reason(item),
                }
                for item in results["weapons"]
            ],
        }

    def to_learning_markdown(self, query: str, context: Dict[str, str]) -> str:
        """Proxy method for formatter."""
        return self.formatter.to_learning_markdown(query, context)

    def _business_model_kind(self, context: Dict[str, Any]) -> str:
        profile = self._get_company_profile(context)
        business_model = str(profile.get("business_model", "")).lower()
        industry = str(context.get("industry", "")).lower()

        if industry == "local-services" or any(
            token in business_model for token in ["local services", "本地生活", "到店", "上门", "同城", "配送", "外卖", "出行"]
        ):
            return "local-services"
        if industry == "marketplace" or any(token in business_model for token in ["marketplace", "双边", "平台"]):
            return "marketplace"
        if industry == "ai" or any(token in business_model for token in ["ai", "agent", "copilot"]):
            return "ai"
        if any(token in business_model for token in ["b2b", "sales-led", "sales led", "销售驱动"]):
            return "b2b-sales-led"
        return "general"

    def _local_services_density_focus(self, query: str, context: Dict[str, Any]) -> str:
        text = " ".join(
            [
                query,
                str(context.get("goal", "")),
                str(context.get("metric", "")),
                str(context.get("constraints", "")),
            ]
        ).lower()
        if any(token in text for token in ["多城", "扩城", "多个城市", "全国铺开", "城市扩张"]):
            return "先在单城打透供给、需求和履约密度，再决定是否扩城。"
        if any(token in text for token in ["供给", "商家", "骑手", "运力", "履约能力", "供给侧"]):
            return "先补稳定供给和履约能力，再放大需求端拉新。"
        if any(token in text for token in ["需求", "用户", "买家", "拉新", "到店客流", "需求侧"]):
            return "先验证区域内真实需求密度，再逐步补供给与履约。"
        return "先在单城/单区域把供给质量、需求密度和履约体验打穿，再决定放大。"

    def _marketplace_liquidity_focus(self, query: str, context: Dict[str, Any]) -> str:
        text = " ".join(
            [
                query,
                str(context.get("goal", "")),
                str(context.get("metric", "")),
                str(context.get("constraints", "")),
            ]
        ).lower()
        if any(marker in text for marker in ["先补需求侧", "先做需求侧", "需求侧优先", "先拉需求", "先做需求"]):
            return "先补需求侧密度，再验证供给侧承接能力。"
        if any(marker in text for marker in ["先补供给侧", "先做供给侧", "供给侧优先", "先拉供给", "先做供给"]):
            return "先补供给侧流动性，再验证需求侧响应。"

        supply_hits = sum(
            1 for token in ["供给", "商家", "司机", "创作者", "房东", "seller", "supply"]
            if token in text
        )
        demand_hits = sum(
            1 for token in ["需求", "买家", "乘客", "租客", "buyer", "demand"]
            if token in text
        )
        if demand_hits > supply_hits:
            return "先补需求侧密度，再验证供给侧承接能力。"
        if supply_hits > demand_hits:
            return "先补供给侧流动性，再验证需求侧响应。"
        return "先判断哪一侧更稀缺、哪一侧更决定首批有效撮合，再把单边流动性做出来。"

    def _parse_budget_amount(self, budget_text: str) -> float:
        if not budget_text:
            return 0.0
        normalized = str(budget_text).replace(",", "").replace("，", "").strip().lower()
        match = None
        import re

        for pattern in [r"(\d+(?:\.\d+)?)\s*万", r"(\d+(?:\.\d+)?)\s*k", r"(\d+(?:\.\d+)?)"]:
            match = re.search(pattern, normalized)
            if match:
                value = float(match.group(1))
                if "万" in pattern:
                    return value * 10000
                if "k" in pattern and "k" in normalized:
                    return value * 1000
                return value
        return 0.0

    def _normalize_text(self, text: Any) -> str:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._normalize_text(text)

    def _get_company_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._get_company_profile(context)

    def _metric_alignment_adjustment(
        self,
        category: str,
        context: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._metric_alignment_adjustment(category, context)

    def _framework_alignment_adjustment(
        self,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, List[str], List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._framework_alignment_adjustment(metadata, context)

    def _guardrail_adjustment_for_option(
        self,
        category: str,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._guardrail_adjustment_for_option(category, metadata, context)

    def _top_case_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._top_case_reference(results)

    def _top_theory_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._top_theory_reference(results)

    def _evidence_adjustments_for_option(
        self,
        metadata: Dict[str, Any],
        results: Dict[str, Any],
        context: Dict[str, str],
    ) -> Tuple[float, float, List[str], List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._evidence_adjustments_for_option(metadata, results, context)

    def _business_model_adjustment(
        self,
        category: str,
        context: Dict[str, str],
    ) -> Tuple[float, List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._business_model_adjustment(category, context)

    def _constraint_adjustment_for_option(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
        context: Dict[str, str],
    ) -> Tuple[float, List[str]]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._constraint_adjustment_for_option(category, weapon_name, metadata, context)

    def _prioritize_options(self, results: Dict[str, Any], context: Dict[str, str]) -> List[StrategyOption]:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._prioritize_options(results, context)

    def _option_why_now(self, category: str, effort: str, impact: str, stage: str) -> str:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._option_why_now(category, effort, impact, stage)

    def _option_risk(self, category: str, stage: str) -> str:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._option_risk(category, stage)

    def _primary_metric(self, context: Dict[str, str]) -> str:
        """Proxy method for backward compatibility with scorer."""
        return self.scorer._primary_metric(context)
