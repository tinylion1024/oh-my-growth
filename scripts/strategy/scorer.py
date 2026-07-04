"""Strategy scoring methods for prioritizing options.

This module contains methods that calculate scores, adjustments, and
penalties for strategy options.
"""

from typing import Any, Dict, List, Optional, Tuple

from .constants import PROBLEM_TO_METRICS, STAGE_LABELS
from .utils import normalize_text


class StrategyScorer:
    """Handles scoring and prioritization of strategy options."""

    def __init__(self, brain: Any):
        """Initialize with reference to the strategy brain.

        Args:
            brain: StrategyBrain instance to access its properties and methods.
        """
        self.brain = brain

    def _get_company_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract company profile from context."""
        payload = context.get("company_profile", {})
        return payload if isinstance(payload, dict) else {}

    def _metric_alignment_adjustment(
        self,
        category: str,
        context: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """Calculate bonus based on metric alignment."""
        metric_text = normalize_text(" ".join([str(context.get("metric", "")), str(context.get("goal", ""))]))
        if not metric_text:
            return 0.0, []

        category_tokens = {
            "b2b-sales": ["线索", "高意向", "demo", "成交", "成单", "商机"],
            "plg": ["首次价值", "激活", "试用", "onboarding", "产品使用", "转化"],
            "content-growth": ["内容", "seo", "搜索", "自然流量", "品牌搜索"],
            "brand": ["品牌", "心智", "品牌搜索"],
            "viral-referral": ["分享", "邀请", "传播", "k 因子"],
            "retention": ["留存", "复购", "回访", "活跃"],
            "community": ["社区", "核心用户", "供给密度", "履约"],
            "cold-start": ["首批用户", "种子用户", "订单", "履约", "撮合"],
            "monetization": ["收入", "付费", "升级", "订阅", "arpu", "arppu"],
            "paid-ads": ["cac", "投放", "点击", "获客成本"],
        }
        bonus = 0.0
        notes: List[str] = []
        hits = sum(1 for token in category_tokens.get(category, []) if token in metric_text)
        if hits:
            bonus += min(0.55, 0.22 + hits * 0.11)
            notes.append("当前主指标直接要求这类动作贡献结果")
        return bonus, notes[:1]

    def _framework_alignment_adjustment(
        self,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, List[str], List[str]]:
        """Calculate bonus based on framework alignment."""
        stage_fit = float(metadata.get("stage_fit", 0.0))
        journey_fit = float(metadata.get("journey_fit", 0.0))
        resource_fit = float(metadata.get("resource_fit", 0.0))
        resource_profile_fit = float(metadata.get("resource_profile_fit", resource_fit))
        growth_process = metadata.get("growth_process", "")
        current_process = context.get("growth_process", "")

        bonus = 0.0
        support_notes: List[str] = []
        risk_notes: List[str] = []

        bonus += (stage_fit - 0.55) * 0.95
        bonus += (journey_fit - 0.55) * 0.8
        bonus += (resource_fit - 0.5) * 0.35
        bonus += (resource_profile_fit - 0.5) * 0.55
        if growth_process and growth_process == current_process:
            bonus += 0.18
            support_notes.append("主业务过程与当前问题一致")

        if stage_fit >= 0.8:
            support_notes.append("阶段匹配度高")
        elif stage_fit <= 0.35:
            risk_notes.append("阶段不够匹配")
        if journey_fit >= 0.8:
            support_notes.append("旅程节点对得上")
        elif journey_fit <= 0.35:
            risk_notes.append("旅程节点不够对齐")
        if resource_profile_fit >= 0.75:
            support_notes.append("资源画像更适合当前团队")
        elif resource_profile_fit <= 0.35:
            risk_notes.append("资源画像偏重，不适合当前团队")

        return bonus, support_notes[:3], risk_notes[:3]

    def _guardrail_adjustment_for_option(
        self,
        category: str,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """Calculate penalty based on guardrail constraints."""
        guardrail_penalty = float(metadata.get("guardrail_penalty", 0.0))
        guardrail_risk = str(metadata.get("guardrail_risk", ""))
        problem = context.get("problem_type", "")
        notes: List[str] = []

        if guardrail_penalty > 0:
            notes.append(f"当前约束线与该方向的已知风险冲突：{guardrail_risk}")

        if problem == "acquisition" and category == "paid-ads":
            guardrail_penalty += 0.08
            notes.append("获客阶段要优先控制 CAC 和高意向转化质量")
        if problem == "retention" and category in {"viral-referral", "paid-ads"}:
            guardrail_penalty += 0.06
            notes.append("当前重点是留存，不应先用拉新动作掩盖主价值问题")
        if problem == "monetization" and "留存" in guardrail_risk:
            guardrail_penalty += 0.08
            notes.append("当前变现动作必须服从留存 guardrail")

        return guardrail_penalty, notes[:2]

    def _top_case_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get the top case from results."""
        cases = results.get("cases", [])
        return cases[0] if cases else None

    def _top_theory_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get the top theory from results."""
        theories = results.get("theories", [])
        return theories[0] if theories else None

    def _evidence_adjustments_for_option(
        self,
        metadata: Dict[str, Any],
        results: Dict[str, Any],
        context: Dict[str, str],
    ) -> Tuple[float, float, List[str], List[str]]:
        """Calculate adjustments based on evidence from cases and theories."""
        support_bonus = 0.0
        risk_penalty = 0.0
        support_notes: List[str] = []
        risk_notes: List[str] = []

        growth_process = metadata.get("growth_process", "")
        journey_stage = metadata.get("journey_stage", "")
        failure_refs = set(metadata.get("failure_refs", []))
        problem = context.get("problem_type", "")

        for case in results.get("cases", [])[:3]:
            case_meta = case.get("metadata", {})
            if case_meta.get("growth_process") == growth_process:
                support_bonus += 0.12
                support_notes.append(f"案例「{case['name']}」支持该业务过程")
            if case_meta.get("journey_stage") == journey_stage:
                support_bonus += 0.08
                support_notes.append(f"案例「{case['name']}」命中同一旅程节点")

        for theory in results.get("theories", [])[:2]:
            theory_meta = theory.get("metadata", {})
            if theory_meta.get("growth_process") == growth_process:
                support_bonus += 0.1
                support_notes.append(f"理论「{theory['name']}」能解释该机制成立条件")
            if theory_meta.get("journey_stage") == journey_stage:
                support_bonus += 0.06

        for failure in results.get("failures", [])[:2]:
            failure_meta = failure.get("metadata", {})
            failure_file = failure_meta.get("file", "")
            normalized_failure_file = (
                f"knowledge/{failure_file}" if failure_file and not failure_file.startswith("knowledge/") else failure_file
            )
            if normalized_failure_file in failure_refs:
                risk_penalty += 0.28
                risk_notes.append(f"失败模式「{failure['name']}」与当前玩法直接相关")
            if failure_meta.get("journey_stage") == journey_stage:
                risk_penalty += 0.06
            if problem in failure_meta.get("problem_types", []):
                risk_penalty += 0.05

        return support_bonus, risk_penalty, support_notes[:3], risk_notes[:3]

    def _method_pack_adjustment_for_option(
        self,
        category: str,
        results: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """Boost options that are part of the top operating-system method packs."""
        bonus = 0.0
        notes: List[str] = []
        for index, pack in enumerate(results.get("method_packs", [])[:2]):
            metadata = pack.get("metadata", {})
            categories = set(metadata.get("categories", []))
            related_weapons = set(metadata.get("related_weapons", []))
            if category not in categories and category not in related_weapons:
                continue
            bonus += 0.38 if index == 0 else 0.18
            highlights = pack.get("highlights", [])
            rule = highlights[0] if highlights else metadata.get("resource_profile", "")
            notes.append(f"增长操作系统「{pack['name']}」要求优先按「{rule}」组织实验")
        return bonus, notes[:2]

    def _business_model_adjustment(
        self,
        category: str,
        context: Dict[str, str],
    ) -> Tuple[float, List[str]]:
        """Calculate bonus based on business model alignment."""
        profile = self._get_company_profile(context)
        business_model = str(profile.get("business_model", "")).lower()
        industry = str(context.get("industry", "")).lower()
        bonus = 0.0
        notes: List[str] = []

        if any(token in business_model for token in ["b2b", "sales-led", "sales led", "销售驱动"]):
            if category == "b2b-sales":
                bonus += 0.6
                notes.append("当前业务形态是 sales-led B2B，应优先考虑线索与销售漏斗")
            if category == "cold-start":
                bonus -= 0.2

        if industry == "local-services" or any(
            token in business_model for token in ["local services", "本地生活", "到店", "上门", "同城", "配送", "外卖", "出行"]
        ):
            if category in {"cold-start", "community"}:
                bonus += 0.22
                notes.append("当前业务依赖单城密度与履约体验，应优先考虑地面运营和区域验证")
            if category in {"paid-ads", "viral-referral"}:
                bonus -= 0.08

        if industry == "marketplace" or any(token in business_model for token in ["marketplace", "双边", "平台"]):
            if category in {"community", "viral-referral"}:
                bonus += 0.18
                notes.append("当前业务是双边/平台型，需优先考虑供需两侧协同")
            if category == "cold-start":
                bonus -= 0.05

        if industry == "ai":
            if category in {"content-growth", "plg"}:
                bonus += 0.14
                notes.append("AI 冷启动更适合先验证内容分发或产品自解释能力")

        return bonus, notes[:2]

    def _constraint_adjustment_for_option(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
        context: Dict[str, str],
    ) -> Tuple[float, List[str]]:
        """Calculate penalty based on explicit constraints."""
        constraints_text = " ".join(
            str(context.get(key, "")) for key in ["constraints", "history", "goal", "team", "budget"]
        ).lower()
        penalty = 0.0
        notes: List[str] = []

        if any(token in constraints_text for token in ["不能依赖付费投放", "不做投放", "不能投广告", "不投广告", "no paid ads"]):
            if category == "paid-ads":
                penalty += 0.9
                notes.append("当前约束明确排除了付费投放")

        if any(token in constraints_text for token in ["不能用高补贴", "不做补贴", "不能烧钱裂变", "不能高激励"]):
            if category == "viral-referral":
                penalty += 0.75
                notes.append("当前约束不允许高补贴或高激励裂变")

        if any(token in constraints_text for token in ["不能扩招聘", "不能加人", "1人", "单人", "小团队"]):
            if metadata.get("effort") == "High":
                penalty += 0.45
                notes.append("当前团队与人力约束不支持高复杂度动作")
            elif metadata.get("effort") == "Medium":
                penalty += 0.15
                notes.append("当前团队规模要求优先考虑更轻量动作")

        if any(token in constraints_text for token in ["不能伤害留存", "不能影响留存", "不能破坏留存", "不能伤害核心留存"]):
            if category == "monetization" and weapon_name in {"限时优惠", "强付费墙", "付费墙", "年付折扣"}:
                penalty += 0.5
                notes.append("当前约束要求变现动作不能以牺牲留存为代价")

        return penalty, notes[:2]

    def _option_why_now(self, category: str, effort: str, impact: str, stage: str) -> str:
        """Generate the 'why now' explanation for an option."""
        stage_text = STAGE_LABELS.get(stage, "当前阶段")
        return f"{stage_text}下，{category}方向的预期影响为{impact}，执行复杂度为{effort}，更适合先作为主验证动作。"

    def _option_risk(self, category: str, stage: str) -> str:
        """Generate risk description for an option."""
        if category == "viral-referral":
            return "如果产品价值和分享动机不足，裂变会带来低质量流量。"
        if category == "paid-ads":
            return "在转化链路未稳前放大投放，容易让 CAC 失控。"
        if category == "plg":
            return "如果首次价值达成太慢，PLG 玩法会变成空转。"
        if category == "retention":
            return "如果主价值没立住，留存机制只会制造短期假活跃。"
        return f"{STAGE_LABELS.get(stage, '当前阶段')}需要控制试错范围，避免高投入动作先行。"

    def _primary_metric(self, context: Dict[str, str]) -> str:
        """Get the primary metric for the context."""
        if context.get("metric"):
            return context["metric"]
        problem = context.get("problem_type", "")
        return PROBLEM_TO_METRICS.get(problem, ["核心增长指标"])[0]

    def _prioritize_options(self, results: Dict[str, Any], context: Dict[str, str]) -> List[Any]:
        """Prioritize and score strategy options from results."""
        try:
            from ..strategy_brain import StrategyOption
        except ImportError:  # pragma: no cover - direct script compatibility.
            from strategy_brain import StrategyOption

        options: List[StrategyOption] = []
        problem = context.get("problem_type", "")
        stage = context.get("stage", "")
        industry = context.get("industry", "")
        weapons = results.get("weapons", [])

        impact_score = {"High": 3.0, "Medium": 2.0, "Low": 1.0}
        effort_penalty = {"Low": 0.2, "Medium": 0.7, "High": 1.2}
        category_fit = {
            "acquisition": {"cold-start": 1.2, "plg": 1.0, "content-growth": 0.8, "paid-ads": 0.5, "b2b-sales": 0.55},
            "activation": {"plg": 1.2, "retention": 0.8, "community": 0.6},
            "retention": {"retention": 1.2, "community": 0.8, "plg": 0.6},
            "monetization": {"monetization": 1.2, "plg": 0.8, "b2b-sales": 0.5},
            "referral": {"viral-referral": 1.2, "plg": 0.7, "community": 0.6},
        }

        for weapon in weapons:
            metadata = weapon["metadata"]
            category = metadata["category"]
            category_name = metadata.get("category_name", category)
            base_score = weapon["score"] * 2.5
            fit_bonus = category_fit.get(problem, {}).get(category, 0.2)
            impact_bonus = impact_score.get(metadata["impact"], 1.0)
            effort_cost = effort_penalty.get(metadata["effort"], 0.8)

            if industry == "saas" and category == "plg":
                fit_bonus += 0.3
            if stage == "0-1" and category == "cold-start":
                fit_bonus += 0.3
            if stage == "10-100" and category == "paid-ads":
                fit_bonus += 0.2
            history_adjustment, history_note = self.brain.history._history_score_adjustment(category, weapon["name"], context)
            history_condition_penalty, history_condition_note = self.brain.history._history_failure_condition_adjustment(
                category,
                weapon["name"],
                metadata,
                context,
            )
            metric_bonus, metric_notes = self._metric_alignment_adjustment(category, context)
            business_model_bonus, business_model_notes = self._business_model_adjustment(category, context)
            framework_bonus, framework_support_notes, framework_risk_notes = self._framework_alignment_adjustment(
                metadata, context
            )
            support_bonus, risk_penalty, support_notes, risk_notes = self._evidence_adjustments_for_option(
                metadata, results, context
            )
            method_pack_bonus, method_pack_notes = self._method_pack_adjustment_for_option(category, results)
            constraint_penalty, constraint_notes = self._constraint_adjustment_for_option(
                category, weapon["name"], metadata, context
            )
            guardrail_penalty, guardrail_notes = self._guardrail_adjustment_for_option(category, metadata, context)

            score = (
                base_score
                + fit_bonus
                + impact_bonus
                + metric_bonus
                + business_model_bonus
                + framework_bonus
                + support_bonus
                + method_pack_bonus
                - effort_cost
                - risk_penalty
                - constraint_penalty
                - history_condition_penalty
                - guardrail_penalty
                + history_adjustment
            )
            why_now = self._option_why_now(category, metadata["effort"], metadata["impact"], stage)
            key_risk = self._option_risk(category, stage)
            if history_adjustment > 0 and history_note:
                why_now = f"{why_now} {history_note}"
            if history_adjustment < 0 and history_note:
                key_risk = f"{key_risk} {history_note}"
            if history_condition_note:
                key_risk = f"{key_risk} {history_condition_note}。"
            if metric_notes:
                why_now = f"{why_now} {'；'.join(metric_notes)}。"
            if business_model_notes:
                why_now = f"{why_now} {'；'.join(business_model_notes)}。"
            if framework_support_notes:
                why_now = f"{why_now} {'；'.join(framework_support_notes[:2])}。"
            if support_notes:
                why_now = f"{why_now} {'；'.join(support_notes[:2])}。"
            if method_pack_notes:
                why_now = f"{why_now} {'；'.join(method_pack_notes)}。"
            if framework_risk_notes:
                key_risk = f"{key_risk} {'；'.join(framework_risk_notes[:2])}。"
            if risk_notes:
                key_risk = f"{key_risk} {'；'.join(risk_notes[:2])}。"
            if constraint_notes:
                key_risk = f"{key_risk} {'；'.join(constraint_notes)}。"
            if guardrail_notes:
                key_risk = f"{key_risk} {'；'.join(guardrail_notes)}。"
            options.append(
                StrategyOption(
                    name=weapon["name"],
                    category=category,
                    category_name=category_name,
                    score=score,
                    effort=metadata["effort"],
                    impact=metadata["impact"],
                    evidence_tier=metadata["evidence_tier"],
                    why_now=why_now,
                    key_risk=key_risk,
                    stage_fit=metadata.get("stage_fit", 0.0),
                    resource_fit=metadata.get("resource_fit", 0.0),
                    journey_fit=metadata.get("journey_fit", 0.0),
                    resource_profile_fit=metadata.get("resource_profile_fit", metadata.get("resource_fit", 0.0)),
                    journey_stage=metadata.get("journey_stage", ""),
                    marketplace_side=metadata.get("marketplace_side", ""),
                    guardrail_risk=metadata.get("guardrail_risk", ""),
                    resource_profile=metadata.get("resource_profile", ""),
                    failure_refs=metadata.get("failure_refs", []),
                    evidence_support=support_notes,
                    risk_signals=risk_notes,
                    support_bonus=round(support_bonus, 2),
                    risk_penalty=round(risk_penalty, 2),
                    constraint_penalty=round(constraint_penalty, 2),
                    framework_bonus=round(framework_bonus, 2),
                    metric_bonus=round(metric_bonus, 2),
                    history_adjustment=round(history_adjustment, 2),
                    history_condition_penalty=round(history_condition_penalty, 2),
                    explicit_guardrail_penalty=round(guardrail_penalty, 2),
                    method_pack_bonus=round(method_pack_bonus, 2),
                )
            )

        options.sort(key=lambda item: item.score, reverse=True)
        return options
