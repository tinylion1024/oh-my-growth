#!/usr/bin/env python3
"""Experiment module for strategy analysis.

This module contains methods for building experiment designs and action items.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from strategy.constants import CATEGORY_ACTIONS, CATEGORY_AVOIDS

if TYPE_CHECKING:
    from strategy_brain import StrategyOption


class ExperimentBuilder:
    """Builder class for experiment-related strategy components.

    Methods:
        - _build_experiment: Build experiment hypothesis and steps
        - _build_actions: Build action items
        - _build_do_now: Build immediate action items
        - _build_avoid_now: Build items to avoid
        - _build_missing_info: Identify missing information
    """

    def __init__(self, brain: Any) -> None:
        """Initialize the builder with a reference to the StrategyBrain instance.

        Args:
            brain: The StrategyBrain instance to access its methods and attributes.
        """
        self.brain = brain

    def _build_experiment(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, Union[List[str], str]]:
        """Build experiment design.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.
            protection_controls: Protection control items.

        Returns:
            Dictionary with hypothesis, steps, success_signals, stop_signals.
        """
        metric = self.brain._primary_metric(context)
        if top_option is None:
            return {
                "hypothesis": "先补信息后再设计实验。",
                "steps": ["补齐目标、现状、资源、约束。"],
                "success_signals": [f"明确 {metric} 的当前值和目标值。"],
                "stop_signals": ["关键事实仍不清楚，暂停继续扩展方案。"],
            }

        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        case_highlight = ""
        if top_case and top_case.get("highlights"):
            case_highlight = top_case["highlights"][0]
        theory_highlight = ""
        if top_theory and top_theory.get("highlights"):
            theory_highlight = top_theory["highlights"][0]

        hypothesis = f"如果优先推进「{top_option.name}」，则在 2 周内能显著改善 {metric}。"
        if top_case or top_theory:
            evidence_bits = []
            if top_case:
                evidence_bits.append(f"参考案例「{top_case['name']}」")
            if top_theory:
                evidence_bits.append(f"遵循理论「{top_theory['name']}」")
            hypothesis = f"{hypothesis} {'，'.join(evidence_bits)} 的成立条件。"

        steps = [
            f"定义单一实验对象：围绕「{query}」只验证一个关键动作。",
            f"设计最小上线版本，控制在 {top_option.effort} 级别工作量。",
            f"每天追踪 {metric} 与次级过程指标，7-14 天内复盘。",
        ]
        if case_highlight:
            steps.insert(1, f"把案例「{top_case['name']}」中的做法「{case_highlight}」转成当前业务可执行版本。")
        if theory_highlight:
            steps.append(f"实验设计优先遵循「{top_theory['name']}」中的原则：{theory_highlight}。")
        for control in protection_controls[:2]:
            steps.append(f"保护措施：针对「{control['risk']}」，{control['control']}")

        success_signals = [
            f"{metric} 出现持续改善趋势。",
            "至少一个过程指标明显上升，且没有引发明显副作用。",
        ]
        if top_case:
            success_signals.append(f"关键过程指标开始接近案例「{top_case['name']}」对应的可复制动作。")
        for control in protection_controls[:2]:
            success_signals.append(f"保护指标成立：{control['guardrail']}。")

        stop_signals = [
            "用户质量明显下滑或核心留存受损。",
            "实验期间需要额外扩预算/扩团队才能成立。",
        ]
        if top_theory:
            stop_signals.append(f"如果连「{top_theory['name']}」要求的基础机制都无法成立，应停止继续放大。")
        for control in protection_controls[:2]:
            stop_signals.append(f"复发保护：{control['stop']}。")

        return {
            "hypothesis": hypothesis,
            "steps": steps,
            "success_signals": success_signals,
            "stop_signals": stop_signals,
        }

    def _build_do_now(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build immediate action items.

        Args:
            top_option: The top strategy option.
            context: Strategy context.

        Returns:
            List of immediate action strings.
        """
        if top_option is None:
            return ["先补齐当前目标、阶段、约束和已有尝试，再进入策略判断。"]

        base_actions = CATEGORY_ACTIONS.get(top_option.category, [])
        metric = self.brain._primary_metric(context)
        if self.brain._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            return [
                self.brain._local_services_density_focus("", context),
                "优先选一个城市、一个区域或一个核心场景，把供给质量、需求密度和履约体验一起跑通。",
                f"所有动作都围绕「{metric}」和有效履约闭环设计验证。",
            ]
        if self.brain._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            return [
                self.brain._marketplace_liquidity_focus("", context),
                "优先用人工运营或定向激励把单边密度做出来，再验证另一侧的自然响应。",
                f"所有动作都围绕「{metric}」和单边流动性设计验证闭环。",
            ]
        return base_actions[:2] + [f"所有动作都围绕「{metric}」设计单一验证闭环。"][:1]

    def _build_avoid_now(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build items to avoid.

        Args:
            top_option: The top strategy option.
            context: Strategy context.

        Returns:
            List of items to avoid.
        """
        if top_option is None:
            return ["不要在信息不足时同时推进多个增长方向。"]

        stage = context.get("stage", "")
        avoid_list = CATEGORY_AVOIDS.get(top_option.category, []).copy()
        if self.brain._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            avoid_list = [
                "不要多城同时铺开。",
                "不要在履约体验没稳前用大补贴硬拉量。",
            ] + avoid_list
        if self.brain._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            avoid_list = [
                "不要同时大规模补贴供需两侧。",
                "不要在两侧都没有流动性前追求全面开放。",
            ] + avoid_list
        for item in self.brain._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            avoid_repeat = str(item.get("avoid_repeat", item.get("lesson", ""))).strip()
            if outcome in {"failed", "stop", "stopped", "negative"} and avoid_repeat:
                avoid_list.append(f"不要重复历史失败模式：{avoid_repeat}")
            elif outcome in {"failed", "stop", "stopped", "negative"}:
                failure_prompts = self.brain._history_repeat_risk_prompts({"experiment_log": {"experiments": [item]}})
                if failure_prompts:
                    avoid_list.append(failure_prompts[0].replace("这次准备如何避免历史失败条件：", "不要重演历史失败条件："))
        if stage == "0-1":
            avoid_list.append("不要先追求规模化自动化，把人肉验证做透更重要。")
        if context.get("problem_type") == "monetization":
            avoid_list.append("不要把短期收入目标压过核心产品价值。")
        return avoid_list[:3]

    def _build_missing_info(self, context: Dict[str, str]) -> List[str]:
        """Identify missing information in context.

        Args:
            context: Strategy context.

        Returns:
            List of missing information prompts.
        """
        prompts = []
        if not context.get("metric"):
            prompts.append("当前最关键指标的现值和目标值")
        if not context.get("budget"):
            prompts.append("预算上限")
        if not context.get("team"):
            prompts.append("可投入的人力角色和数量")
        if not context.get("history") and not self.brain._get_experiment_log(context):
            prompts.append("过去做过哪些尝试，效果如何")
        elif self.brain._get_experiment_log(context):
            prompts.extend(self.brain._history_repeat_risk_prompts(context))
        if not context.get("constraints"):
            prompts.append("当前不能突破的业务/产品/合规约束")
        if not self.brain._get_company_profile(context):
            prompts.append("公司画像：目标用户、商业模式和当前组织能力")
        if self.brain._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            prompts.append("单城供给质量、需求密度、履约成功率和区域空档点")
        if self.brain._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            prompts.append("供给侧与需求侧当前密度、转化和空档点")
        return prompts

    def _build_actions(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Build action items with owners, deadlines, and acceptance criteria.

        Args:
            query: The strategy query.
            context: Strategy context.
            top_option: The top strategy option.
            results: Retrieval results.

        Returns:
            List of action item dictionaries.
        """
        option_name = top_option.name if top_option else "主策略验证"
        metric = self.brain._primary_metric(context)
        top_case = self.brain._top_case_reference(results)
        top_theory = self.brain._top_theory_reference(results)
        first_acceptance = f"明确实验范围、关键指标和停止条件，围绕 {metric} 建立追踪面板"
        first_change = "把分散的策略讨论收敛为单一主抓手验证"
        second_acceptance = f"{metric} 出现趋势变化，且能解释驱动因素"
        second_change = "验证策略是否真能推动主要矛盾的一侧"

        if top_case:
            first_acceptance += f"，并把案例「{top_case['name']}」的关键动作翻译成当前业务版本"
            first_change += f"，优先借鉴「{top_case['name']}」的可复制部分"
        if top_theory:
            second_acceptance += f"，同时验证是否满足「{top_theory['name']}」的成立条件"
            second_change += "，而不是只看表面指标"
        return [
            {
                "name": f"{option_name} 最小实验设计",
                "owner": "增长负责人",
                "deadline": "本周内",
                "resources": "产品/运营/数据各 1 人",
                "acceptance": first_acceptance,
                "change": first_change,
            },
            {
                "name": f"{option_name} 上线与监控",
                "owner": "产品经理或增长 PM",
                "deadline": "两周内",
                "resources": "最小实现资源 + 每日数据回看",
                "acceptance": second_acceptance,
                "change": second_change,
            },
        ]
