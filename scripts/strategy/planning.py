#!/usr/bin/env python3
"""Planning module for strategy analysis.

This module contains methods for resource allocation, Kelly sizing, game theory, and projections.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

try:
    from ..gametheory_analysis import GameTheoryAnalysis, GameType
    from ..kelly_sizing import KellySizing
except ImportError:  # pragma: no cover - direct script compatibility.
    from gametheory_analysis import GameTheoryAnalysis, GameType
    from kelly_sizing import KellySizing

from .constants import STAGE_LABELS

if TYPE_CHECKING:
    from ..strategy_brain import StrategyOption


class PlanningBuilder:
    """Builder class for planning-related strategy components.

    Methods:
        - _build_kelly_allocation: Kelly criterion based allocation
        - _build_kelly_context: Context for Kelly sizing
        - _build_game_theory_analysis: Game theory competitive analysis
        - _build_failure_modes: Identify failure modes
        - _build_resource_allocation: Resource allocation recommendations
        - _build_review_trigger: Review trigger conditions
        - _build_caveats: Caveats and warnings
        - _build_current_state: Current state summary
        - _build_projection: Outcome projection
        - _build_decision_process: Decision process table
    """

    def __init__(self, brain: Any) -> None:
        """Initialize the builder with a reference to the StrategyBrain instance.

        Args:
            brain: The StrategyBrain instance to access its methods and attributes.
        """
        self.brain = brain

    def _build_kelly_context(self, context: Dict[str, Any], top_option: Optional["StrategyOption"]) -> Dict[str, Any]:
        """Build context for Kelly criterion sizing.

        Args:
            context: Strategy context.
            top_option: The top strategy option.

        Returns:
            Kelly context dictionary.
        """
        budget_amount = self.brain._parse_budget_amount(str(context.get("budget", "")))
        resource_clarity = "clear" if budget_amount > 0 else "partial" if context.get("team") else "unclear"
        probability_source = "expert" if context.get("history") or self.brain._get_experiment_log(context) else "guess"
        payoff_clarity = "clear" if context.get("metric") and context.get("goal") else "partial"
        downside_bound = "bounded" if top_option and top_option.guardrail_risk else "partial"
        feedback_mechanism = "yes" if context.get("metric") else "partial"
        return {
            "resource_pool": budget_amount,
            "resource_clarity": resource_clarity,
            "probability_source": probability_source,
            "payoff_clarity": payoff_clarity,
            "downside_bound": downside_bound,
            "repeatability": "repeatable",
            "feedback_mechanism": feedback_mechanism,
            "uncertainty_level": "high" if not context.get("history") else "normal",
        }

    def _build_kelly_allocation(
        self,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        posterior: float,
    ) -> Optional[Dict[str, Any]]:
        """Build Kelly criterion based allocation recommendation.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            posterior: Posterior probability from Bayesian analysis.

        Returns:
            Kelly allocation dictionary or None.
        """
        if not top_option or not context.get("budget"):
            return None

        budget_amount = self.brain._parse_budget_amount(str(context.get("budget", "")))
        if budget_amount <= 0:
            return None

        impact_map = {"High": 1.5, "Medium": 1.0, "Low": 0.6}
        effort_map = {"Low": 0.35, "Medium": 0.60, "High": 0.90}
        ks = KellySizing(risk_profile="moderate")
        kelly_context = self._build_kelly_context(context, top_option)
        binary_result = ks.binary_kelly(
            win_prob=max(0.05, min(0.95, posterior)),
            win_amount=impact_map.get(top_option.impact, 1.0) * 100,
            loss_amount=effort_map.get(top_option.effort, 0.6) * 100,
        )
        readiness = ks.decision_readiness(kelly_context)
        recommended_fraction, _ = binary_result.get_recommended(kelly_context["uncertainty_level"])
        capped_fraction = ks.apply_exposure_cap(recommended_fraction)

        metric = self.brain._primary_metric(context)
        action_package = ks.create_action_package(
            kelly_fraction=capped_fraction,
            resource_pool=budget_amount,
            opportunity_name=top_option.name,
            metrics=[metric],
            add_conditions=[
                f"{metric} 连续两周改善，且 {top_option.guardrail_risk or '约束线未恶化'}",
            ],
            stop_conditions=[
                f"{metric} 没有改善，或 {top_option.guardrail_risk or '实验副作用明显'}",
            ],
        )
        return {
            "budget_amount": budget_amount,
            "full_kelly": round(binary_result.full_kelly, 4),
            "recommended_ratio": round(capped_fraction, 4),
            "recommended_ratio_text": f"{capped_fraction:.1%} 风险预算",
            "allocation_amount": round(action_package.allocation, 2),
            "allocation_text": f"建议先投入约 {action_package.allocation:,.0f} 元",
            "readiness_score": readiness.score,
            "readiness_status": readiness.status.value,
            "add_condition": action_package.add_conditions[0] if action_package.add_conditions else "达到正向信号再加仓",
            "stop_condition": action_package.stop_conditions[0] if action_package.stop_conditions else "核心指标未改善则停止",
            "metrics": action_package.metrics,
        }

    def _build_game_theory_analysis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
    ) -> Optional[Dict[str, Any]]:
        """Build game theory competitive analysis.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.

        Returns:
            Game theory analysis dictionary or None.
        """
        competitor = str(context.get("competitor", "")).strip()
        market = str(context.get("market_structure", "")).strip().lower()
        query_text = f"{query} {context.get('goal', '')}".lower()
        explicit_competition_signal = any(
            keyword in market or keyword in query_text
            for keyword in ["竞品", "价格", "降价", "pricing", "竞争", "price war", "竞争对手"]
        )
        trigger = bool(competitor or market or explicit_competition_signal)
        if not trigger or not top_option:
            return None

        competitor_name = competitor or "竞争对手"
        game_type = (
            GameType.TWO_SIDED_MARKET
            if any(word in market for word in ["平台", "双边", "marketplace"]) or self.brain._business_model_kind(context) in {"marketplace", "local-services"}
            else GameType.PRISONER_DILEMMA
        )
        gta = GameTheoryAnalysis(game_type=game_type)
        gta.set_players(["我方", competitor_name])
        gta.set_strategies(
            {
                "我方": [f"押注{top_option.name}", "保守试探"],
                competitor_name: ["快速跟进", "观察不动"],
            }
        )

        impact_value = {"High": 12, "Medium": 8, "Low": 4}.get(top_option.impact, 6)
        effort_cost = {"Low": 2, "Medium": 4, "High": 6}.get(top_option.effort, 4)
        payoffs = {
            (f"押注{top_option.name}", "快速跟进"): {"我方": impact_value - effort_cost - 2, competitor_name: 4},
            (f"押注{top_option.name}", "观察不动"): {"我方": impact_value + 3, competitor_name: -3},
            ("保守试探", "快速跟进"): {"我方": 1, competitor_name: 5},
            ("保守试探", "观察不动"): {"我方": 3, competitor_name: 2},
        }
        payoff_types = {combo: {"我方": "estimated", competitor_name: "estimated"} for combo in payoffs}
        gta.build_payoff_matrix(payoffs, payoff_types=payoff_types)

        history_data = []
        for item in self.brain._get_experiment_log(context):
            if "竞争" in str(item.get("name", "")) or "定价" in str(item.get("name", "")):
                history_data.append(
                    {
                        "player_name": competitor_name,
                        "behavior_type": "follow_up",
                        "frequency": 0.7,
                        "consistency": 0.6,
                        "last_observed": str(item.get("outcome", "")),
                        "reference_class": "challenger",
                    }
                )
        if history_data:
            gta.calibrate_with_history(history_data)

        report = gta.analyze()
        equilibrium = report.equilibrium
        posture = "先发试探，准备应对跟进" if equilibrium and equilibrium.strategy_profile and "快速跟进" in equilibrium.strategy_profile else "主动推进，抢先建立优势"
        game_type_label = "平台博弈" if game_type == GameType.TWO_SIDED_MARKET else "竞争反应博弈"
        return {
            "game_type": report.game_type,
            "game_type_label": game_type_label,
            "competitor": competitor_name,
            "posture": posture,
            "recommendation": report.strategic_recommendation,
            "confidence": report.confidence_level,
            "equilibrium": list(equilibrium.strategy_profile) if equilibrium else [],
        }

    def _build_failure_modes(
        self,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, str]]:
        """Build failure modes analysis.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            List of failure mode dictionaries.
        """
        def load_failure_doc(path_str: str) -> Optional[Dict[str, str]]:
            try:
                from pathlib import Path

                # planning.py is in scripts/strategy/, so we need parent.parent.parent to get project root
                doc_path = Path(__file__).resolve().parent.parent.parent / path_str
            except Exception:
                return None
            if not doc_path.exists():
                return None
            content = doc_path.read_text(encoding="utf-8").strip()
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            title = ""
            summary = ""
            for idx, line in enumerate(lines):
                if line.startswith("## "):
                    title = line[3:].strip()
                    for candidate in lines[idx + 1:]:
                        if candidate.startswith("## "):
                            break
                        if not candidate.startswith("-") and not candidate.startswith("#"):
                            summary = candidate
                            break
                    break
            if not title:
                return None
            return {"title": title, "summary": summary or "需要结合原文查看失效条件。", "file": path_str}

        if results and results.get("failures"):
            docs = []
            for failure in results["failures"]:
                metadata = failure.get("metadata", {})
                file_path = metadata.get("file", "")
                loaded = load_failure_doc(f"knowledge/{file_path}" if file_path and not file_path.startswith("knowledge/") else file_path)
                if loaded:
                    docs.append(loaded)
                else:
                    docs.append(
                        {
                            "title": failure.get("name", ""),
                            "summary": metadata.get("summary", "") or "需要结合原文查看失效条件。",
                            "file": file_path,
                        }
                    )
            if docs:
                return docs[:3]

        if top_option and top_option.failure_refs:
            docs = []
            for ref in top_option.failure_refs:
                loaded = load_failure_doc(ref)
                if loaded:
                    docs.append(loaded)
            if docs:
                return docs[:3]

        problem = context.get("problem_type", "")
        category = top_option.category if top_option else ""
        mapping: Dict[str, List[Dict[str, str]]] = {
            "acquisition": [
                {
                    "title": "广撒渠道导致样本污染",
                    "summary": "还没验证主转化链路时同时铺太多渠道，最后无法判断哪个动作真的有效。",
                    "file": "knowledge/failures/acquisition-anti-patterns.md",
                },
                {
                    "title": "低质量流量掩盖真实增长",
                    "summary": "补贴、薅羊毛或低意向流量会抬高新增，但无法转成高质量留存。",
                    "file": "knowledge/failures/acquisition-anti-patterns.md",
                },
            ],
            "referral": [
                {
                    "title": "高补贴裂变换来低质量用户",
                    "summary": "如果分享动机来自补贴而不是价值，裂变会放大噪音而不是放大产品力。",
                    "file": "knowledge/failures/referral-failure-modes.md",
                },
                {
                    "title": "裂变链路过长导致流失",
                    "summary": "分享路径每多一步，都会显著抬高中途流失和作弊空间。",
                    "file": "knowledge/failures/referral-failure-modes.md",
                },
            ],
            "retention": [
                {
                    "title": "用激励制造假留存",
                    "summary": "短期刺激可以抬高回访，但不会形成持续价值和真实习惯。",
                    "file": "knowledge/failures/retention-failure-modes.md",
                },
                {
                    "title": "同时改太多机制导致无法归因",
                    "summary": "留存问题需要单点验证，否则很难判断哪个动作真的有效。",
                    "file": "knowledge/failures/retention-failure-modes.md",
                },
            ],
        }
        modes = mapping.get(problem, [])
        if category == "paid-ads":
            modes.append(
                {
                    "title": "投放扩量早于转化验证",
                    "summary": "素材、人群和落地页未稳前扩预算，CAC 很容易快速失控。",
                    "file": "knowledge/failures/acquisition-anti-patterns.md",
                }
            )
        return modes[:3]

    def _build_resource_allocation(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        """Build resource allocation recommendations.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            Dictionary with increase, decrease, protect recommendations.
        """
        option_name = top_option.name if top_option else "主抓手"
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        increase = f"把产品/增长/运营资源优先向「{option_name}」倾斜。"
        if top_case:
            increase += f" 案例「{top_case['name']}」说明该方向更接近当前阶段的可复制主路径。"
        decrease = "压缩低优先级活动、分散试错和非核心项目。"
        if top_theory:
            decrease += f" 理论「{top_theory['name']}」提示不要同时分散验证过多机制。"
        protect = f"保护 {self.brain._primary_metric(context)} 的数据监控与复盘节奏。"
        if top_option and top_option.guardrail_risk:
            protect += f" 同时重点监控约束线风险：{top_option.guardrail_risk}。"
        return {
            "increase": increase,
            "decrease": decrease,
            "protect": protect,
        }

    def _build_review_trigger(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, str]:
        """Build review trigger conditions.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.
            protection_controls: Protection control items.

        Returns:
            Dictionary with time, signal, evidence.
        """
        metric = self.brain._primary_metric(context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        signal = f"{metric} 没有趋势改善，或出现明显副作用"
        if top_option and top_option.guardrail_risk:
            signal += f"，尤其是 {top_option.guardrail_risk}"

        evidence = "实验面板中的过程指标与主指标数据 (observed)"
        if top_case or top_theory:
            parts = []
            if top_case:
                parts.append(f"对照案例「{top_case['name']}」的关键动作是否落地")
            if top_theory:
                parts.append(f"核查理论「{top_theory['name']}」要求的机制是否成立")
            for control in protection_controls[:2]:
                parts.append(f"检查保护措施是否避免「{control['risk']}」")
            evidence = "；".join(parts) + " (observed)"
        return {
            "time": "7-14 天后复盘一次，30 天后决定是否放大",
            "signal": signal,
            "evidence": evidence,
        }

    def _build_caveats(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build caveats and warnings.

        Args:
            top_option: The top strategy option.
            context: Strategy context.

        Returns:
            List of caveat strings.
        """
        caveats = []
        if top_option:
            caveats.append(f"警告：{top_option.key_risk}")
        caveats.append("不确定：如果关键指标基线不准，当前优先级判断会偏差。")
        if not context.get("history") and not self.brain._get_experiment_log(context):
            caveats.append("警告：历史尝试信息缺失，可能重复踩同样的坑。")
        return caveats

    def _build_current_state(
        self,
        context: Dict[str, str],
        results: Dict[str, Any],
    ) -> Dict[str, Union[List[str], str]]:
        """Build current state summary.

        Args:
            context: Strategy context.
            results: Retrieval results.

        Returns:
            Dictionary with goal, stage, constraints, resources, facts.
        """
        facts = []
        profile = self.brain._get_company_profile(context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        if context.get("metric"):
            facts.append(f"{context['metric']} (observed)")
        else:
            facts.append(f"{self.brain._primary_metric(context)} 尚未提供现值 (assumed)")
        if context.get("goal"):
            facts.append(f"目标：{context['goal']} (observed)")
        if profile.get("company_name"):
            facts.append(f"公司：{profile['company_name']} (observed)")
        if profile.get("business_model"):
            facts.append(f"商业模式：{profile['business_model']} (observed)")
        if context.get("budget"):
            facts.append(f"预算：{context['budget']} (observed)")
        else:
            facts.append("预算上限待补充 (estimated)")
        if context.get("history"):
            facts.append(f"历史尝试：{context['history']} (observed)")
        else:
            experiment_log = self.brain._get_experiment_log(context)
            if experiment_log:
                facts.append(f"历史实验数：{len(experiment_log)} (observed)")
            else:
                facts.append("历史尝试信息缺失 (assumed)")
        if top_case:
            facts.append(f"当前最相近案例：{top_case['name']}，可作为外部参照 (observed)")
        if top_theory:
            facts.append(f"当前主要解释框架：{top_theory['name']} (observed)")

        return {
            "goal": context.get("goal", f"围绕 {self.brain._primary_metric(context)} 找到当前主抓手"),
            "stage": STAGE_LABELS.get(context.get("stage", ""), context.get("stage", "未明确")),
            "constraints": context.get("constraints", "预算/人力/时间窗口待补充"),
            "resources": context.get("team", "默认最小跨职能团队"),
            "facts": facts,
        }

    def _build_projection(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        """Build outcome projection.

        Args:
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            Dictionary with probability, assumption, evidence.
        """
        metric = self.brain._primary_metric(context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        evidence = "参考相似案例与当前阶段匹配度较高 (observed)"
        if top_case or top_theory:
            parts = []
            if top_case:
                parts.append(f"案例「{top_case['name']}」相似度={top_case['score']:.2f}")
            if top_theory:
                parts.append(f"理论「{top_theory['name']}」相关度={top_theory['score']:.2f}")
            evidence = "；".join(parts) + " (observed)"

        assumption = "实验动作能触达真实用户动机，且执行范围足够聚焦 (assumed)"
        if top_theory and top_theory.get("highlights"):
            assumption = f"实验动作要满足「{top_theory['name']}」强调的原则：{top_theory['highlights'][0]} (assumed)"

        probability = f"{metric} 在 2-4 周内出现可观察改善的概率中等偏高 (estimated)"
        if top_option and top_option.support_bonus > top_option.risk_penalty:
            probability = f"{metric} 在 2-4 周内出现可观察改善的概率中等偏高，且证据支持强于失效风险 (estimated)"
        return {
            "probability": probability,
            "assumption": assumption,
            "evidence": evidence,
        }

    def _build_decision_process(self, options: List["StrategyOption"]) -> Dict[str, List[Dict]]:
        """Build decision process table.

        Args:
            options: List of strategy options.

        Returns:
            Dictionary with table and why_not lists.
        """
        rows = []
        why_not = []
        for option in options[:3]:
            goal_impact = 5 if option.impact == "High" else 3 if option.impact == "Medium" else 1
            leverage = 5 if option.score >= 6 else 4 if option.score >= 5 else 3
            stage_fit = max(1, round(option.stage_fit * 5))
            resource_fit = max(1, round(option.resource_fit * 5))
            rows.append(
                {
                    "name": option.name,
                    "goal_impact": goal_impact,
                    "leverage": leverage,
                    "stage_fit": stage_fit,
                    "resource_fit": resource_fit,
                    "total": round(option.score, 2),
                }
            )
        for option in options[1:3]:
            support_hint = option.evidence_support[0] if option.evidence_support else "当前上下文下缺少更强直接证据"
            risk_hint = option.risk_signals[0] if option.risk_signals else option.key_risk
            why_not.append(
                {
                    "name": option.name,
                    "reason": (
                        f"{risk_hint}；阶段匹配={option.stage_fit:.2f}，旅程匹配={option.journey_fit:.2f}，"
                        f"资源匹配={option.resource_fit:.2f}，资源画像匹配={option.resource_profile_fit:.2f}；"
                        f"支持证据：{support_hint}"
                    ),
                }
            )
        return {"table": rows, "why_not": why_not}
