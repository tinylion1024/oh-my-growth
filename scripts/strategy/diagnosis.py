#!/usr/bin/env python3
"""Diagnosis module for strategy analysis.

This module contains methods for diagnosing business context, stage, and journey focus.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from strategy.constants import (
    PROBLEM_LABELS,
    PROBLEM_TO_JOURNEY,
    PROBLEM_TO_PROCESS,
    STAGE_FRAMEWORK,
    STAGE_LABELS,
)

if TYPE_CHECKING:
    from strategy_brain import StrategyOption


class DiagnosisBuilder:
    """Builder class for diagnosis-related strategy components.

    Methods:
        - _build_stage_diagnosis: Analyze current business stage
        - _build_growth_process: Determine growth process focus
        - _build_north_star: Define north star metric and guardrails
        - _build_journey_focus: Determine user journey stage focus
        - _build_context_summary: Summarize context for display
        - _build_retrieval_context: Build context for retrieval
        - _build_memory_summary: Summarize company and experiment memory
        - _build_measurement_notes: Notes for measurement setup
        - _build_business_model_diagnosis: Diagnose by business model type
    """

    def __init__(self, brain: Any) -> None:
        """Initialize the builder with a reference to the StrategyBrain instance.

        Args:
            brain: The StrategyBrain instance to access its methods and attributes.
        """
        self.brain = brain

    def _build_stage_diagnosis(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build stage diagnosis with focus and reason.

        Args:
            context: Strategy context containing stage information.

        Returns:
            Dictionary with current_stage, focus, and reason.
        """
        stage = context.get("stage", "")
        frame = STAGE_FRAMEWORK.get(
            stage,
            {
                "name": STAGE_LABELS.get(stage, "阶段待明确"),
                "focus": "先明确当前阶段，再决定是否押注获客、留存还是变现。",
                "reason": "阶段不清会导致优先级判断失真。",
            },
        )
        return {
            "current_stage": frame["name"],
            "focus": frame["focus"],
            "reason": frame["reason"],
        }

    def _build_growth_process(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build growth process analysis.

        Args:
            context: Strategy context containing problem_type.

        Returns:
            Dictionary with name, focus, and reason.
        """
        problem = context.get("problem_type", "")
        name, focus = PROBLEM_TO_PROCESS.get(problem, ("增长经营", "先判断问题更偏新增还是偏价值深耕。"))
        return {
            "name": name,
            "focus": focus,
            "reason": f"当前问题更接近{PROBLEM_LABELS.get(problem, '增长')}，因此优先按{name}处理。",
        }

    def _build_north_star(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build north star metric with guardrails.

        Args:
            context: Strategy context containing problem_type.

        Returns:
            Dictionary with metric, guardrail, and reason.
        """
        metric = self.brain._primary_metric(context)
        problem = context.get("problem_type", "")
        guardrail_map = {
            "acquisition": "CAC 不失控，且首周激活率不下滑",
            "activation": "新增转化不能靠过度打扰或补贴硬拉",
            "retention": "提升复访时不能牺牲用户体验或制造假活跃",
            "monetization": "付费提升不能明显伤害留存和口碑",
            "referral": "邀请增长不能换来低质量用户或滥用",
        }
        return {
            "metric": metric,
            "guardrail": guardrail_map.get(problem, "不能破坏长期用户价值"),
            "reason": f"当前优先围绕 {metric} 配置资源，避免同时追太多指标。",
        }

    def _build_journey_focus(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build journey stage focus.

        Args:
            context: Strategy context containing journey_stage or problem_type.

        Returns:
            Dictionary with stage and focus.
        """
        if context.get("journey_stage"):
            stage = context["journey_stage"]
            focus_map = {
                "认知/到达": "当前先看用户如何接触到产品以及到达后的高意向转化是否成立。",
                "注册/激活": "当前先看用户是否在首次体验中完成关键动作并感知核心价值。",
                "留存": "当前先看用户为什么回来，以及为什么不回来。",
                "付费": "当前先看价值感知是否足以支撑付费和升级。",
                "分享": "当前先看用户是否有足够动机传播，以及接收方转化链路是否够短。",
            }
            return {
                "stage": stage,
                "focus": focus_map.get(stage, "先明确用户在哪一段断掉。"),
            }
        problem = context.get("problem_type", "")
        stage, focus = PROBLEM_TO_JOURNEY.get(problem, ("用户旅程待明确", "先明确用户在哪一段断掉。"))
        return {
            "stage": stage,
            "focus": focus,
        }

    def _build_context_summary(self, context: Dict[str, str]) -> str:
        """Build context summary for display.

        Args:
            context: Strategy context with company and problem info.

        Returns:
            Formatted summary string.
        """
        parts = []
        profile = self.brain._get_company_profile(context)
        if profile.get("company_name"):
            parts.append(f"公司={profile['company_name']}")
        if context.get("industry"):
            parts.append(f"行业={context['industry']}")
        if context.get("stage"):
            parts.append(f"阶段={STAGE_LABELS.get(context['stage'], context['stage'])}")
        if context.get("problem_type"):
            parts.append(f"问题={PROBLEM_LABELS.get(context['problem_type'], context['problem_type'])}")
        if context.get("goal"):
            parts.append(f"目标={context['goal']}")
        return "，".join(parts) if parts else "上下文待补充"

    def _build_retrieval_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for retrieval operations.

        Args:
            context: Strategy context.

        Returns:
            Enhanced context with growth_process, journey_stage, and metric.
        """
        working_context = dict(context)
        if not working_context.get("growth_process"):
            working_context["growth_process"] = self._build_growth_process(working_context)["name"]
        if not working_context.get("journey_stage"):
            working_context["journey_stage"] = self._build_journey_focus(working_context)["stage"]
        if not working_context.get("metric"):
            working_context["metric"] = self.brain._primary_metric(working_context)
        return working_context

    def _build_memory_summary(self, context: Dict[str, Any]) -> List[str]:
        """Build memory summary from company profile and experiment log.

        Args:
            context: Strategy context.

        Returns:
            List of summary strings.
        """
        summary: List[str] = []
        profile = self.brain._get_company_profile(context)
        if profile:
            name = profile.get("company_name") or profile.get("product_name") or "当前项目"
            business_model = profile.get("business_model", "业务模式待补充")
            team = profile.get("team") or context.get("team") or "团队规模待补充"
            summary.append(f"{name} 当前按「{business_model}」经营，团队资源={team}。")
            if profile.get("target_user"):
                summary.append(f"当前核心目标用户：{profile['target_user']}。")
        for item in self.brain._get_experiment_log(context)[:3]:
            name = str(item.get("name", "未命名实验"))
            outcome = str(item.get("outcome", item.get("status", "结果待定")))
            lesson = str(item.get("lesson", "")).strip()
            detail = f"历史实验「{name}」结果={outcome}"
            if lesson:
                detail += f"，教训={lesson}"
            summary.append(detail + "。")
        return summary

    def _build_measurement_notes(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        north_star: Dict[str, str],
        growth_process: Dict[str, str],
    ) -> List[str]:
        """Build measurement notes for experiment setup.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            north_star: North star configuration.
            growth_process: Growth process configuration.

        Returns:
            List of measurement note strings.
        """
        option_name = top_option.name if top_option else "当前主抓手"
        notes = [
            f"主指标统一围绕 {north_star['metric']}，并给出当前值、目标值和观察周期。",
            f"至少补一条约束线：{north_star['guardrail']}。",
            f"{growth_process['name']}相关动作需要能追踪到「{option_name}」前后指标变化。",
        ]
        if context.get("problem_type") in {"acquisition", "referral"}:
            notes.append("渠道、内容或分享动作至少要能做基础来源归因，避免只看总量。")
        else:
            notes.append("主价值动作、触达动作和留存/付费结果要使用同一口径复盘。")
        if self.brain._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            notes.append("至少拆出单城供给活跃、需求密度、有效履约订单数和履约成功率，避免只看拉新量。")
        if self.brain._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            notes.append("至少拆出供给侧活跃、需求侧活跃、有效撮合数三段漏斗，判断先补哪一侧。")
        experiment_log = self.brain._get_experiment_log(context)
        if experiment_log:
            notes.append("历史实验口径要与本轮实验保持一致，避免换指标后误判改进。")
        return notes

    def _build_marketplace_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build marketplace-specific diagnosis.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            Marketplace diagnosis dict or None.
        """
        if self.brain._business_model_kind(context) != "marketplace" or context.get("problem_type") != "acquisition":
            return None

        side_focus = self.brain._marketplace_liquidity_focus(query, context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        top_case_side = ""
        if top_case:
            top_case_side = top_case.get("metadata", {}).get("marketplace_side", "")

        return {
            "side_focus": side_focus,
            "top_case_side": top_case_side or "liquidity",
            "top_weapon_side": top_option.marketplace_side if top_option else "",
            "rule": "先做单边流动性，再观察另一侧是否自然跟进，避免两侧同时重补贴。",
            "evidence": (
                f"案例={top_case['name']}" if top_case else "案例待补充"
            ) + (
                f"；理论={top_theory['name']}" if top_theory else ""
            ),
        }

    def _build_local_services_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build local services-specific diagnosis.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            Local services diagnosis dict or None.
        """
        if self.brain._business_model_kind(context) != "local-services" or context.get("problem_type") != "acquisition":
            return None

        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        return {
            "focus": self.brain._local_services_density_focus(query, context),
            "rule": "先打透单城/单区域的供给、需求和履约，再考虑跨城扩张或大规模补贴。",
            "evidence": (
                f"案例={top_case['name']}" if top_case else "案例待补充"
            ) + (
                f"；理论={top_theory['name']}" if top_theory else ""
            ),
            "top_weapon": top_option.name if top_option else "",
        }

    def _build_business_model_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build business model-specific diagnosis.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            Business model diagnosis dict or None.
        """
        kind = self.brain._business_model_kind(context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        evidence = (f"案例={top_case['name']}" if top_case else "案例待补充") + (
            f"；理论={top_theory['name']}" if top_theory else ""
        )

        if kind == "marketplace" and context.get("problem_type") == "acquisition":
            diagnosis = self._build_marketplace_diagnosis(query, context, top_option, results)
            if diagnosis:
                return {
                    "label": "平台侧",
                    "focus": diagnosis["side_focus"],
                    "rule": diagnosis["rule"],
                    "evidence": diagnosis["evidence"],
                }

        if kind == "local-services" and context.get("problem_type") == "acquisition":
            diagnosis = self._build_local_services_diagnosis(query, context, top_option, results)
            if diagnosis:
                return {
                    "label": "本地生活",
                    "focus": diagnosis["focus"],
                    "rule": diagnosis["rule"],
                    "evidence": diagnosis["evidence"],
                }

        if kind == "b2b-sales-led" and context.get("problem_type") in {"acquisition", "monetization"}:
            return {
                "label": "B2B 销售驱动",
                "focus": "先修 ICP、线索质量和 demo-to-close 漏斗，再决定是否扩销售或放大渠道。",
                "rule": "不要先用扩人或扩渠道掩盖漏斗问题；先提高高意向线索质量和成交效率。",
                "evidence": evidence,
            }

        if kind == "ai" and context.get("problem_type") == "acquisition":
            return {
                "label": "AI 冷启动",
                "focus": "先让产品价值可被外部内容解释，并缩短首次价值达成，再考虑复杂分享机制或大投放。",
                "rule": "先验证内容分发与激活闭环，再决定是否加大传播或预算放量。",
                "evidence": evidence,
            }

        return None
