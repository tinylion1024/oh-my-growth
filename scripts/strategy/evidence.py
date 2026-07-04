#!/usr/bin/env python3
"""Evidence module for strategy analysis.

This module contains methods for building evidence chains, confidence, and decision lines.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

try:
    from ..bayesian_decision import BayesianDecision
except ImportError:  # pragma: no cover - direct script compatibility.
    from bayesian_decision import BayesianDecision

from .constants import PROBLEM_LABELS, STAGE_FRAMEWORK, STAGE_LABELS

if TYPE_CHECKING:
    from ..strategy_brain import StrategyOption


class EvidenceBuilder:
    """Builder class for evidence-related strategy components.

    Methods:
        - _build_evidence_chain: Build chain of supporting/opposing evidence
        - _build_confidence: Calculate Bayesian confidence
        - _build_decision_line: Build the main decision statement
        - _build_core_tension: Identify core tension in strategy
        - _build_why_now: Explain why this strategy now
    """

    def __init__(self, brain: Any) -> None:
        """Initialize the builder with a reference to the StrategyBrain instance.

        Args:
            brain: The StrategyBrain instance to access its methods and attributes.
        """
        self.brain = brain

    def _build_evidence_chain(
        self,
        results: Dict,
        top_option: Optional["StrategyOption"],
        context: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Build evidence chain from cases, theories, and failures.

        Args:
            results: Retrieval results with cases, theories, failures.
            top_option: The top strategy option.
            context: Strategy context.

        Returns:
            List of evidence items with type_label, name, why, evidence_tier.
        """
        chain: List[Dict[str, str]] = []
        requested_journey = context.get("journey_stage", "")
        if top_option:
            chain.append(
                {
                    "type_label": "玩法",
                    "name": top_option.name,
                    "why": (
                        f"在「{top_option.journey_stage or '核心旅程'}」节点的匹配度达 {top_option.journey_fit:.2f}，"
                        f"资源画像匹配度 {top_option.resource_profile_fit:.2f}。目前已识别的支持证据包括「{'；'.join(top_option.evidence_support[:1])}」。"
                        + (f" 需警惕约束线风险：{top_option.guardrail_risk}。" if top_option.guardrail_risk else "")
                    ),
                    "evidence_tier": top_option.evidence_tier,
                }
            )
        for pack in results.get("method_packs", [])[:1]:
            metadata = pack.get("metadata", {})
            highlights = pack.get("highlights", [])
            chain.append(
                {
                    "type_label": "操作系统",
                    "name": pack["name"],
                    "why": (
                        f"该方法包覆盖「{metadata.get('journey_stage', '核心旅程')}」节点，"
                        f"阶段匹配度 {metadata.get('stage_fit', 0):.2f}，资源匹配度 {metadata.get('resource_fit', 0):.2f}。"
                        + (f" 关键规则：{highlights[0]}" if highlights else "")
                    ),
                    "evidence_tier": metadata.get("evidence_tier", "C"),
                }
            )
        for case in results["cases"][:2]:
            chain.append(
                {
                    "type_label": "案例",
                    "name": case["name"],
                    "why": (
                        f"该案例在「{case['metadata'].get('journey_stage', '相应旅程')}」中展现了可复用的增长路径，相似度为 {case['score']:.2f}。"
                        + (f" 关键可复制点：{case['highlights'][0]}。" if case.get("highlights") else "")
                    ),
                    "evidence_tier": case["metadata"].get("evidence_tier", "C"),
                }
            )
        for theory in results["theories"][:1]:
            chain.append(
                {
                    "type_label": "理论",
                    "name": theory["name"],
                    "why": (
                        f"理论提供了底层机制的支撑（相关度 {theory['score']:.2f}），重点解释了「{theory['metadata'].get('growth_process', '主业务过程')}」的运作逻辑。"
                        + (f" 核心准则：{theory['highlights'][0]}。" if theory.get("highlights") else "")
                    ),
                    "evidence_tier": theory["metadata"].get("evidence_tier", "B"),
                }
            )
        for failure in results.get("failures", [])[:1]:
            chain.append(
                {
                    "type_label": "反例",
                    "name": failure["name"],
                    "why": (
                        f"警告：检测到与当前决策相似的失败模式「{failure['metadata'].get('summary', '待补充')}」。"
                        f"在「{failure['metadata'].get('journey_stage', '对应旅程')}」中存在失效风险。"
                    ),
                    "evidence_tier": "C",
                }
            )
        return chain

    def _build_confidence(
        self,
        query: str,
        context: Dict[str, str],
        results: Dict,
        top_option: Optional["StrategyOption"],
    ) -> Tuple[Dict[str, str], str, float]:
        """Build Bayesian confidence assessment.

        Args:
            query: The strategy query.
            context: Strategy context.
            results: Retrieval results.
            top_option: The top strategy option.

        Returns:
            Tuple of (decision_text dict, confidence_label, posterior probability).
        """
        bd = BayesianDecision()
        hypothesis = f"当前阶段优先聚焦 {top_option.name if top_option else '核心增长动作'} 是更优策略"
        bd.set_hypothesis(hypothesis)
        prior = 0.30 + min(0.25, 0.05 * len([value for value in context.values() if value]))
        bd.set_prior(prior, rationale=f"基于当前上下文和问题描述：{query}")

        for case in results["cases"][:3]:
            bd.add_evidence(case["name"], case["metadata"]["evidence_tier"], "support")
        for theory in results["theories"][:2]:
            bd.add_evidence(theory["name"], theory["metadata"]["evidence_tier"], "support")
        if top_option:
            bd.add_evidence(top_option.name, top_option.evidence_tier, "support")
        for failure in results.get("failures", [])[:1]:
            bd.add_evidence(f"反例：{failure['name']}", "C", "oppose")
        if top_option and (top_option.constraint_penalty > 0.2 or top_option.explicit_guardrail_penalty > 0.1):
            bd.add_evidence(f"{top_option.name} 的约束线风险", "D", "oppose")

        posterior = bd.update()
        decision_text = bd.get_decision_text()
        return decision_text, decision_text["confidence"], posterior

    def _build_decision_line(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        decision_text: Dict[str, str],
        confidence_label: str,
    ) -> str:
        """Build the main decision line statement.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            decision_text: Decision text from Bayesian analysis.
            confidence_label: Confidence label.

        Returns:
            Decision line string.
        """
        if top_option is None:
            return f"当前问题「{query}」信息仍偏少，先补关键现状，再做策略判断。"

        stage = STAGE_LABELS.get(context.get("stage", ""), context.get("stage", "当前阶段"))
        return (
            f"{decision_text['action']}：在{stage}优先押注「{top_option.name}」作为主抓手，"
            f"先验证能否带动{PROBLEM_LABELS.get(context.get('problem_type', ''), '核心指标')}，置信度{confidence_label}。"
        )

    def _build_core_tension(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        evidence_chain: List[Dict[str, str]],
        results: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build core tension analysis.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            evidence_chain: Evidence chain items.
            results: Retrieval results.

        Returns:
            Core tension string.
        """
        problem = context.get("problem_type", "")
        stage = context.get("stage", "")
        evidence_parts: List[str] = []

        top_case = self.brain._top_case_reference(results) if results else None
        top_theory = self.brain._top_theory_reference(results) if results else None

        if top_case:
            case_highlights = top_case.get("highlights")
            case_insight = case_highlights[0] if case_highlights else "先抓住可复制主路径"
            evidence_parts.append(f"案例「{top_case['name']}」提供的关键洞察是「{case_insight}」")
        if top_theory:
            theory_highlights = top_theory.get("highlights")
            theory_insight = theory_highlights[0] if theory_highlights else "要先验证机制成立条件"
            evidence_parts.append(f"遵循理论「{top_theory['name']}」的核心原则「{theory_insight}」")

        evidence_hint = "；".join(evidence_parts) + "，" if evidence_parts else ""
        if self.brain._business_model_kind(context) == "local-services" and problem == "acquisition":
            density_focus = self.brain._local_services_density_focus(query, context)
            return (
                f"{evidence_hint}核心矛盾不是先铺更多城市或渠道，而是先在单城/单区域做出稳定供给、需求和履约密度；"
                f"{density_focus}"
            )
        if self.brain._business_model_kind(context) == "marketplace" and problem == "acquisition":
            liquidity_focus = self.brain._marketplace_liquidity_focus(query, context)
            return (
                f"{evidence_hint}核心矛盾不是同时拉满供给和需求，而是先判断哪一侧更稀缺、"
                f"哪一侧更决定首批有效撮合；{liquidity_focus}"
            )
        if problem == "acquisition" and stage == "0-1":
            return f"{evidence_hint}现在的核心矛盾不是渠道不够多，而是还没有找到可复制、低成本拿到高意向首批用户的主路径。"
        if problem == "retention":
            return f"{evidence_hint}核心矛盾不是玩法不够花，而是用户在关键留存节点没有持续获得回访理由。"
        if problem == "monetization":
            return f"{evidence_hint}核心矛盾不是缺少收费点，而是尚未验证用户愿意为什么价值付费，以及付费动作会不会伤留存。"
        if problem == "referral":
            return f"{evidence_hint}核心矛盾不是裂变玩法少，而是当前产品价值和分享动机是否强到足以支撑低摩擦传播。"
        option_name = top_option.name if top_option else "主策略"
        return f"当前问题「{query}」要先收敛主抓手，避免同时推进太多方向；建议围绕「{option_name}」建立第一轮验证。"

    def _build_why_now(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict,
        evidence_chain: List[Dict[str, str]],
    ) -> List[str]:
        """Build reasons why this strategy should be executed now.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.
            evidence_chain: Evidence chain items.

        Returns:
            List of reason strings.
        """
        reasons = []
        if top_option:
            reasons.append(
                f"首选「{top_option.name}」是因为它在当前资源和阶段约束下具有最高的落地确定性。其画像匹配度达 {top_option.resource_profile_fit:.2f}，"
                f"且与目标旅程节点「{top_option.journey_stage or '核心路径'}」高度契合。"
            )
            if top_option.evidence_support:
                reasons.append(f"该判断得到了以下直接证据的支持：{'；'.join(top_option.evidence_support[:2])}。")
            if top_option.metric_bonus > 0:
                reasons.append(f"由于该方向与当前主指标「{self.brain._primary_metric(context)}」直接关联，我们显式提升了其优先级。")
            if top_option.risk_signals:
                reasons.append(f"需要警惕的潜在风险或失效信号是：{'；'.join(top_option.risk_signals[:1])}。")

        top_case = self.brain._top_case_reference(results)
        if top_case:
            case_reason = f"案例「{top_case['name']}」提供了极其相似的场景证据（相似度 {top_case['score']:.2f}）"
            if top_case.get("highlights"):
                case_reason += f"，其成功的关键动作「{top_case['highlights'][0]}」具备直接迁移价值。"
            reasons.append(case_reason)

        top_theory = self.brain._top_theory_reference(results)
        if top_theory:
            theory_reason = f"从增长底层逻辑看，理论「{top_theory['name']}」解释了为什么在当前阶段必须优先关注「{top_theory['metadata'].get('growth_process', '主业务过程')}」"
            if top_theory.get("highlights"):
                theory_reason += f"，并给出了「{top_theory['highlights'][0]}」作为执行准则。"
            reasons.append(theory_reason)

        if context.get("stage"):
            stage_label = STAGE_LABELS.get(context["stage"], context["stage"])
            stage_focus = STAGE_FRAMEWORK.get(context["stage"], {}).get("focus", "快速验证")
            reasons.append(f"考虑到当前处于 {stage_label} 阶段，决策重心应放在「{stage_focus}」上。")

        profile = self.brain._get_company_profile(context)
        if profile.get("target_user"):
            reasons.append(f"基于目标用户群「{profile['target_user']}」的行为特征，该策略更有利于在核心触点产生真实价值。")

        if top_option and top_option.explicit_guardrail_penalty > 0:
            reasons.append(f"注意：虽然该策略被推荐，但由于触及约束线（扣分 {top_option.explicit_guardrail_penalty:.2f}），执行时必须严格遵守保护措施。")

        return reasons
