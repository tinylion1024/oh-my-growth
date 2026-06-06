#!/usr/bin/env python3
"""Strategy-brain layer that turns retrieval into operator-friendly recommendations."""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from bayesian_decision import BayesianDecision
from knowledge_retriever import KnowledgeRetriever

PROBLEM_LABELS = {
    "acquisition": "获客",
    "activation": "激活",
    "retention": "留存",
    "monetization": "变现",
    "referral": "裂变",
}

STAGE_LABELS = {
    "0-1": "冷启动",
    "1-10": "增长期",
    "10-100": "规模化",
}

CATEGORY_ACTIONS = {
    "cold-start": ["先集中拿到 20-50 个高意向种子用户", "优先验证转介绍或高触达渠道是否能稳定出单"],
    "viral-referral": ["只设计一个低摩擦分享触点", "先跑奖励成本可控的双边激励实验"],
    "content-growth": ["先围绕单一高意图关键词做内容闭环", "把内容产出绑定到注册或留资动作"],
    "community": ["先识别核心用户群并建立固定反馈场景", "让社区承担分发和留存，而不是只做运营热闹"],
    "plg": ["先缩短首次价值到达时间", "优先做能自传播的产品节点，而不是大而全功能"],
    "retention": ["只盯一个关键留存节点", "先用提醒、习惯、回流机制验证复访提升"],
    "monetization": ["先明确付费触发点", "优先做不伤害核心留存的轻量商业化实验"],
    "paid-ads": ["先小预算验证创意和人群", "没有自然转化基础前不要放大预算"],
    "brand": ["只围绕一个品牌心智重复投入", "品牌动作必须绑定长期获客或转化假设"],
    "b2b-sales": ["先提高高意向线索密度", "把销售动作拆成可复盘的话术和漏斗"],
}

CATEGORY_AVOIDS = {
    "cold-start": ["不要一开始就铺太多渠道", "不要先做重工程的大系统"],
    "viral-referral": ["不要先上复杂裂变玩法", "不要用高补贴换来低质量用户"],
    "content-growth": ["不要同时做太多内容形态", "不要只做曝光不设计转化路径"],
    "community": ["不要把社区活跃误当成增长结果", "不要一开始就追求大规模社区运营"],
    "plg": ["不要先做复杂功能矩阵", "不要用销售动作掩盖产品体验问题"],
    "retention": ["不要同时改太多留存机制", "不要在主价值未成立前堆激励"],
    "monetization": ["不要先用强打扰付费墙", "不要为了短期收入破坏长期留存"],
    "paid-ads": ["不要在素材和转化路径未验证前扩量", "不要让 CAC 脱离 LTV 讨论"],
    "brand": ["不要把品牌动作当短期拉新速效药", "不要做没有复用价值的一次性 campaign"],
    "b2b-sales": ["不要只盯线索数不看成交路径", "不要过早扩销售团队而不修转化漏斗"],
}

PROBLEM_TO_METRICS = {
    "acquisition": ["新增高意向用户数", "获客成本/CAC", "首周激活率"],
    "activation": ["首个关键动作转化率", "首次价值达成率", "激活到留存转化率"],
    "retention": ["7日/30日留存", "复访频次", "流失召回率"],
    "monetization": ["付费转化率", "ARPU/ARPPU", "升级率"],
    "referral": ["分享率", "邀请转化率", "K 因子"],
}


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


class StrategyBrain:
    """Generate operator-oriented strategy recommendations from the retrieval layer."""

    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()

    def analyze(self, query: str, context: Dict[str, str], mode: str = "assess") -> Dict:
        results = self.retriever.retrieve(query, context, case_limit=5, weapon_limit=6, theory_limit=3)
        options = self._prioritize_options(results["weapons"], context)
        top_option = options[0] if options else None
        decision_text, confidence_label, posterior = self._build_confidence(query, context, results, top_option)
        decision_process = self._build_decision_process(options)
        actions = self._build_actions(query, context, top_option)
        return {
            "query": query,
            "mode": mode,
            "context_summary": self._build_context_summary(context),
            "problem_label": PROBLEM_LABELS.get(context.get("problem_type", ""), "增长"),
            "decision_line": self._build_decision_line(query, context, top_option, decision_text, confidence_label),
            "core_tension": self._build_core_tension(query, context, top_option),
            "why_now": self._build_why_now(context, top_option, results),
            "priorities": options[:3],
            "do_now": self._build_do_now(top_option, context),
            "avoid_now": self._build_avoid_now(top_option, context),
            "experiment": self._build_experiment(query, context, top_option),
            "decision_process": decision_process,
            "resource_allocation": self._build_resource_allocation(context, top_option),
            "actions": actions,
            "projection": self._build_projection(context),
            "review_trigger": self._build_review_trigger(context),
            "caveats": self._build_caveats(top_option, context),
            "missing_info": self._build_missing_info(context),
            "reference_cases": results["cases"][:3],
            "reference_theories": results["theories"][:2],
            "decision_text": decision_text,
            "confidence_label": confidence_label,
            "confidence_score": posterior,
            "current_state": self._build_current_state(context),
        }

    def to_json(self, analysis: Dict) -> str:
        """Serialize an analysis payload with StrategyOption objects expanded."""
        serializable = analysis.copy()
        serializable["priorities"] = [option.__dict__ for option in analysis["priorities"]]
        return json.dumps(serializable, ensure_ascii=False, indent=2)

    def to_report_markdown(self, analysis: Dict, clarity_score: float, clarity_level: str, can_proceed: bool) -> str:
        """Render a decision memo that matches the report contract."""
        priorities = analysis["priorities"]
        top_name = priorities[0].name if priorities else "待确认"
        missing_info = analysis["missing_info"] or ["暂无"]
        current_state = analysis["current_state"]
        actions = analysis["actions"]
        projection = analysis["projection"]
        review = analysis["review_trigger"]

        lines = [
            "## 先看结论",
            "",
            f"**最该先解决**：围绕「{top_name}」先验证主增长矛盾。",
            "",
            f"**为什么是它**：{analysis['decision_line']}",
            "",
            f"**置信度**：{analysis['confidence_label']}",
            "",
            f"**第一个行动**：{actions[0]['name']}（负责人：{actions[0]['owner']}，期限：{actions[0]['deadline']}）",
            "",
            "## 先把现状说清楚",
            "",
            f"- **目标**：{current_state['goal']}",
            f"- **阶段**：{current_state['stage']}",
            f"- **约束**：{current_state['constraints']}",
            f"- **资源**：{current_state['resources']}",
            "- **关键事实**：",
        ]
        for fact in current_state["facts"]:
            lines.append(f"  - {fact}")

        lines.extend(
            [
                "",
                "## 现状够不够清楚",
                "",
                f"**清晰度评分**：{clarity_score}/100",
                "",
                f"**清晰度等级**：{clarity_level}",
                "",
                f"**是否可以诊断**：{'是' if can_proceed else '否'}",
                "",
                "**缺失信息**：",
            ]
        )
        for item in missing_info:
            lines.append(f"- {item}")

        lines.extend(
            [
                "",
                "**追问问题**：",
            ]
        )
        for index, item in enumerate(missing_info[:3], 1):
            lines.append(f"{index}. 请补充：{item}")

        lines.extend(
            [
                "",
                "## 判断过程",
                "",
                "### 候选方案对比",
                "",
                "| 候选 | 目标影响 | 杠杆效应 | 阶段匹配 | 资源约束 | 总分 |",
                "|-----|---------|---------|---------|---------|-----|",
            ]
        )
        for row in analysis["decision_process"]["table"]:
            lines.append(
                f"| {row['name']} | {row['goal_impact']} | {row['leverage']} | {row['stage_fit']} | {row['resource_fit']} | {row['total']} |"
            )

        lines.extend(
            [
                "",
                f"### 为什么是 {top_name}",
                "",
                analysis["core_tension"],
                "",
                "### 为什么不是其他选项",
                "",
            ]
        )
        for item in analysis["decision_process"]["why_not"]:
            lines.append(f"- **不是 {item['name']}**：{item['reason']}")

        lines.extend(
            [
                "",
                "## 推荐方案",
                "",
                f"**方案名称**：{top_name}",
                "",
                "**核心理由**：",
            ]
        )
        for index, reason in enumerate(analysis["why_now"], 1):
            lines.append(f"{index}. {reason}")
        lines.extend(["", "**实施路径**："])
        for index, step in enumerate(analysis["experiment"]["steps"], 1):
            lines.append(f"{index}. {step}")

        lines.extend(
            [
                "",
                "## 时间、精力、资源应该怎么重新分配",
                "",
                "**分配原则**：清晰时果断倾斜",
                "",
                "| 分配桶 | 份额 | 含义 |",
                "|-------|-----|------|",
                "| 主攻主要矛盾 | 60% | 资源优先押注主抓手 |",
                "| 压缩次要矛盾 | 20% | 保持必要止损动作 |",
                "| 证据与监控 | 20% | 跟踪实验和风险信号 |",
                "",
                "**具体建议**：",
                f"- **应该增加**：{analysis['resource_allocation']['increase']}",
                f"- **应该减少**：{analysis['resource_allocation']['decrease']}",
                f"- **应该保护**：{analysis['resource_allocation']['protect']}",
                "",
                "## 接下来怎么做",
                "",
            ]
        )
        for action in actions:
            lines.extend(
                [
                    f"### 行动：{action['name']}",
                    "",
                    f"- **负责人**：{action['owner']}",
                    f"- **期限**：{action['deadline']}",
                    f"- **资源**：{action['resources']}",
                    f"- **验收标准**：{action['acceptance']}",
                    f"- **改变什么**：{action['change']}",
                    "",
                ]
            )
        lines.extend(["### 应该停止或推迟的事", ""])
        for item in analysis["avoid_now"]:
            lines.append(f"- {item}：避免分散资源")

        lines.extend(
            [
                "",
                "## 做完以后可能怎样",
                "",
                f"- **概率**：{projection['probability']}",
                f"- **假设**：{projection['assumption']}",
                f"- **证据**：{projection['evidence']}",
                "",
                "## 什么时候回头看",
                "",
                f"- **时间**：{review['time']}",
                f"- **信号**：{review['signal']}",
                f"- **证据**：{review['evidence']}",
                "",
                "## 注意事项",
                "",
            ]
        )
        for item in analysis["caveats"]:
            lines.append(f"- {item}")
        return "\n".join(lines)

    def to_executive_markdown(self, analysis: Dict) -> str:
        """Shorter leadership-oriented summary."""
        priorities = analysis["priorities"]
        top_names = " > ".join(option.name for option in priorities[:3]) if priorities else "待补充"
        lines = [
            "## 董事会/负责人摘要",
            "",
            f"**一句话判断**：{analysis['decision_line']}",
            "",
            f"**核心矛盾**：{analysis['core_tension']}",
            "",
            f"**优先级**：{top_names}",
            "",
            "**这周拍板**：",
        ]
        for item in analysis["do_now"][:3]:
            lines.append(f"- {item}")
        lines.extend(["", "**先别做**："])
        for item in analysis["avoid_now"][:2]:
            lines.append(f"- {item}")
        lines.extend(["", f"**置信度**：{analysis['confidence_label']} ({analysis['confidence_score']:.2f})"])
        return "\n".join(lines)

    def _build_context_summary(self, context: Dict[str, str]) -> str:
        parts = []
        if context.get("industry"):
            parts.append(f"行业={context['industry']}")
        if context.get("stage"):
            parts.append(f"阶段={STAGE_LABELS.get(context['stage'], context['stage'])}")
        if context.get("problem_type"):
            parts.append(f"问题={PROBLEM_LABELS.get(context['problem_type'], context['problem_type'])}")
        if context.get("goal"):
            parts.append(f"目标={context['goal']}")
        return "，".join(parts) if parts else "上下文待补充"

    def _build_confidence(
        self,
        query: str,
        context: Dict[str, str],
        results: Dict,
        top_option: Optional[StrategyOption],
    ) -> Tuple[Dict[str, str], str, float]:
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

        posterior = bd.update()
        decision_text = bd.get_decision_text()
        return decision_text, decision_text["confidence"], posterior

    def _build_decision_line(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        decision_text: Dict[str, str],
        confidence_label: str,
    ) -> str:
        if top_option is None:
            return f"当前问题“{query}”信息仍偏少，先补关键现状，再做策略判断。"

        stage = STAGE_LABELS.get(context.get("stage", ""), context.get("stage", "当前阶段"))
        return (
            f"{decision_text['action']}：在{stage}优先押注「{top_option.name}」作为主抓手，"
            f"先验证能否带动{PROBLEM_LABELS.get(context.get('problem_type', ''), '核心指标')}，置信度{confidence_label}。"
        )

    def _build_core_tension(self, query: str, context: Dict[str, str], top_option: Optional[StrategyOption]) -> str:
        problem = context.get("problem_type", "")
        stage = context.get("stage", "")
        if problem == "acquisition" and stage == "0-1":
            return "现在的核心矛盾不是渠道不够多，而是还没有找到可复制、低成本拿到高意向首批用户的主路径。"
        if problem == "retention":
            return "核心矛盾不是玩法不够花，而是用户在关键留存节点没有持续获得回访理由。"
        if problem == "monetization":
            return "核心矛盾不是缺少收费点，而是尚未验证用户愿意为什么价值付费，以及付费动作会不会伤留存。"
        if problem == "referral":
            return "核心矛盾不是裂变玩法少，而是当前产品价值和分享动机是否强到足以支撑低摩擦传播。"
        option_name = top_option.name if top_option else "主策略"
        return f"当前问题“{query}”要先收敛主抓手，避免同时推进太多方向；建议围绕「{option_name}」建立第一轮验证。"

    def _build_why_now(self, context: Dict[str, str], top_option: Optional[StrategyOption], results: Dict) -> List[str]:
        reasons = []
        if top_option:
            reasons.append(
                f"主策略「{top_option.name}」兼顾影响和复杂度，当前排序得分 {top_option.score:.2f}。"
            )
        if results["cases"]:
            reasons.append(f"已有 {len(results['cases'][:3])} 个相关案例可提供可复制证据。")
        if context.get("stage"):
            reasons.append(f"当前处于{STAGE_LABELS.get(context['stage'], context['stage'])}，更适合先做可快速验证的动作。")
        return reasons

    def _prioritize_options(self, weapons: List[Dict], context: Dict[str, str]) -> List[StrategyOption]:
        options: List[StrategyOption] = []
        problem = context.get("problem_type", "")
        stage = context.get("stage", "")
        industry = context.get("industry", "")

        impact_score = {"High": 3.0, "Medium": 2.0, "Low": 1.0}
        effort_penalty = {"Low": 0.2, "Medium": 0.7, "High": 1.2}
        category_fit = {
            "acquisition": {"cold-start": 1.2, "plg": 1.0, "content-growth": 0.8, "paid-ads": 0.5},
            "activation": {"plg": 1.2, "retention": 0.8, "community": 0.6},
            "retention": {"retention": 1.2, "community": 0.8, "plg": 0.6},
            "monetization": {"monetization": 1.2, "plg": 0.8, "b2b-sales": 0.7},
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

            score = base_score + fit_bonus + impact_bonus - effort_cost
            why_now = self._option_why_now(category, metadata["effort"], metadata["impact"], stage)
            key_risk = self._option_risk(category, stage)
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
                )
            )

        options.sort(key=lambda item: item.score, reverse=True)
        return options

    def _option_why_now(self, category: str, effort: str, impact: str, stage: str) -> str:
        stage_text = STAGE_LABELS.get(stage, "当前阶段")
        return f"{stage_text}下，{category}方向的预期影响为{impact}，执行复杂度为{effort}，更适合先作为主验证动作。"

    def _option_risk(self, category: str, stage: str) -> str:
        if category == "viral-referral":
            return "如果产品价值和分享动机不足，裂变会带来低质量流量。"
        if category == "paid-ads":
            return "在转化链路未稳前放大投放，容易让 CAC 失控。"
        if category == "plg":
            return "如果首次价值达成太慢，PLG 玩法会变成空转。"
        if category == "retention":
            return "如果主价值没立住，留存机制只会制造短期假活跃。"
        return f"{STAGE_LABELS.get(stage, '当前阶段')}需要控制试错范围，避免高投入动作先行。"

    def _build_do_now(self, top_option: Optional[StrategyOption], context: Dict[str, str]) -> List[str]:
        if top_option is None:
            return ["先补齐当前目标、阶段、约束和已有尝试，再进入策略判断。"]

        base_actions = CATEGORY_ACTIONS.get(top_option.category, [])
        metric = self._primary_metric(context)
        return base_actions[:2] + [f"所有动作都围绕「{metric}」设计单一验证闭环。"][:1]

    def _build_avoid_now(self, top_option: Optional[StrategyOption], context: Dict[str, str]) -> List[str]:
        if top_option is None:
            return ["不要在信息不足时同时推进多个增长方向。"]

        stage = context.get("stage", "")
        avoid_list = CATEGORY_AVOIDS.get(top_option.category, []).copy()
        if stage == "0-1":
            avoid_list.append("不要先追求规模化自动化，把人肉验证做透更重要。")
        if context.get("problem_type") == "monetization":
            avoid_list.append("不要把短期收入目标压过核心产品价值。")
        return avoid_list[:3]

    def _build_experiment(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
    ) -> Dict[str, Union[List[str], str]]:
        metric = self._primary_metric(context)
        if top_option is None:
            return {
                "hypothesis": "先补信息后再设计实验。",
                "steps": ["补齐目标、现状、资源、约束。"],
                "success_signals": [f"明确 {metric} 的当前值和目标值。"],
                "stop_signals": ["关键事实仍不清楚，暂停继续扩展方案。"],
            }

        return {
            "hypothesis": f"如果优先推进「{top_option.name}」，则在 2 周内能显著改善 {metric}。",
            "steps": [
                f"定义单一实验对象：围绕“{query}”只验证一个关键动作。",
                f"设计最小上线版本，控制在 {top_option.effort} 级别工作量。",
                f"每天追踪 {metric} 与次级过程指标，7-14 天内复盘。",
            ],
            "success_signals": [
                f"{metric} 出现持续改善趋势。",
                "至少一个过程指标明显上升，且没有引发明显副作用。",
            ],
            "stop_signals": [
                "用户质量明显下滑或核心留存受损。",
                "实验期间需要额外扩预算/扩团队才能成立。",
            ],
        }

    def _build_missing_info(self, context: Dict[str, str]) -> List[str]:
        prompts = []
        if not context.get("metric"):
            prompts.append("当前最关键指标的现值和目标值")
        if not context.get("budget"):
            prompts.append("预算上限")
        if not context.get("team"):
            prompts.append("可投入的人力角色和数量")
        if not context.get("history"):
            prompts.append("过去做过哪些尝试，效果如何")
        if not context.get("constraints"):
            prompts.append("当前不能突破的业务/产品/合规约束")
        return prompts

    def _primary_metric(self, context: Dict[str, str]) -> str:
        if context.get("metric"):
            return context["metric"]
        problem = context.get("problem_type", "")
        return PROBLEM_TO_METRICS.get(problem, ["核心增长指标"])[0]

    def _build_decision_process(self, options: List[StrategyOption]) -> Dict[str, List[Dict]]:
        rows = []
        why_not = []
        for option in options[:3]:
            goal_impact = 5 if option.impact == "High" else 3 if option.impact == "Medium" else 1
            leverage = 5 if option.score >= 6 else 4 if option.score >= 5 else 3
            stage_fit = 5 if "更适合先作为主验证动作" in option.why_now else 3
            resource_fit = 5 if option.effort == "Low" else 3 if option.effort == "Medium" else 2
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
            why_not.append({"name": option.name, "reason": option.key_risk})
        return {"table": rows, "why_not": why_not}

    def _build_resource_allocation(self, context: Dict[str, str], top_option: Optional[StrategyOption]) -> Dict[str, str]:
        option_name = top_option.name if top_option else "主抓手"
        return {
            "increase": f"把产品/增长/运营资源优先向「{option_name}」倾斜。",
            "decrease": "压缩低优先级活动、分散试错和非核心项目。",
            "protect": f"保护 {self._primary_metric(context)} 的数据监控与复盘节奏。",
        }

    def _build_actions(self, query: str, context: Dict[str, str], top_option: Optional[StrategyOption]) -> List[Dict[str, str]]:
        option_name = top_option.name if top_option else "主策略验证"
        metric = self._primary_metric(context)
        return [
            {
                "name": f"{option_name} 最小实验设计",
                "owner": "增长负责人",
                "deadline": "本周内",
                "resources": "产品/运营/数据各 1 人",
                "acceptance": f"明确实验范围、关键指标和停止条件，围绕 {metric} 建立追踪面板",
                "change": "把分散的策略讨论收敛为单一主抓手验证",
            },
            {
                "name": f"{option_name} 上线与监控",
                "owner": "产品经理或增长 PM",
                "deadline": "两周内",
                "resources": "最小实现资源 + 每日数据回看",
                "acceptance": f"{metric} 出现趋势变化，且能解释驱动因素",
                "change": "验证策略是否真能推动主要矛盾的一侧",
            },
        ]

    def _build_projection(self, context: Dict[str, str]) -> Dict[str, str]:
        metric = self._primary_metric(context)
        return {
            "probability": f"{metric} 在 2-4 周内出现可观察改善的概率中等偏高 (estimated)",
            "assumption": "实验动作能触达真实用户动机，且执行范围足够聚焦 (assumed)",
            "evidence": "参考相似案例与当前阶段匹配度较高 (observed)",
        }

    def _build_review_trigger(self, context: Dict[str, str]) -> Dict[str, str]:
        metric = self._primary_metric(context)
        return {
            "time": "7-14 天后复盘一次，30 天后决定是否放大",
            "signal": f"{metric} 没有趋势改善，或出现明显副作用",
            "evidence": "实验面板中的过程指标与主指标数据 (observed)",
        }

    def _build_caveats(self, top_option: Optional[StrategyOption], context: Dict[str, str]) -> List[str]:
        caveats = []
        if top_option:
            caveats.append(f"警告：{top_option.key_risk}")
        caveats.append("不确定：如果关键指标基线不准，当前优先级判断会偏差。")
        if not context.get("history"):
            caveats.append("警告：历史尝试信息缺失，可能重复踩同样的坑。")
        return caveats

    def _build_current_state(self, context: Dict[str, str]) -> Dict[str, Union[List[str], str]]:
        facts = []
        if context.get("metric"):
            facts.append(f"{context['metric']} (observed)")
        else:
            facts.append(f"{self._primary_metric(context)} 尚未提供现值 (assumed)")
        if context.get("goal"):
            facts.append(f"目标：{context['goal']} (observed)")
        if context.get("budget"):
            facts.append(f"预算：{context['budget']} (observed)")
        else:
            facts.append("预算上限待补充 (estimated)")
        if context.get("history"):
            facts.append(f"历史尝试：{context['history']} (observed)")
        else:
            facts.append("历史尝试信息缺失 (assumed)")

        return {
            "goal": context.get("goal", f"围绕 {self._primary_metric(context)} 找到当前主抓手"),
            "stage": STAGE_LABELS.get(context.get("stage", ""), context.get("stage", "未明确")),
            "constraints": context.get("constraints", "预算/人力/时间窗口待补充"),
            "resources": context.get("team", "默认最小跨职能团队"),
            "facts": facts,
        }
