#!/usr/bin/env python3
"""Strategy-brain layer that turns retrieval into operator-friendly recommendations."""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from bayesian_decision import BayesianDecision
from gametheory_analysis import GameTheoryAnalysis, GameType
from kelly_sizing import KellySizing
from knowledge_retriever import KnowledgeRetriever

# Import constants from strategy module
from strategy.constants import (
    PROBLEM_LABELS,
    STAGE_LABELS,
    STAGE_FRAMEWORK,
    PROBLEM_TO_PROCESS,
    PROBLEM_TO_JOURNEY,
    CATEGORY_ACTIONS,
    CATEGORY_AVOIDS,
    PROBLEM_TO_METRICS,
)

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


class StrategyBrain:
    """Generate operator-oriented strategy recommendations from the retrieval layer."""

    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()

    def analyze(self, query: str, context: Dict[str, str], mode: str = "assess") -> Dict:
        working_context = self._build_retrieval_context(context)
        results = self.retriever.retrieve(query, working_context, case_limit=5, weapon_limit=6, theory_limit=3)
        options = self._prioritize_options(results, working_context)
        top_option = options[0] if options else None
        decision_text, confidence_label, posterior = self._build_confidence(query, working_context, results, top_option)
        decision_process = self._build_decision_process(options)
        actions = self._build_actions(query, working_context, top_option, results)
        growth_process = self._build_growth_process(working_context)
        north_star = self._build_north_star(working_context)
        evidence_chain = self._build_evidence_chain(results, top_option, working_context)
        memory_summary = self._build_memory_summary(working_context)
        kelly_allocation = self._build_kelly_allocation(working_context, top_option, posterior)
        game_theory = self._build_game_theory_analysis(query, working_context, top_option)
        failure_modes = self._build_failure_modes(working_context, top_option, results)
        protection_controls = self._history_protection_controls(working_context, top_option)
        return {
            "query": query,
            "mode": mode,
            "context_summary": self._build_context_summary(working_context),
            "problem_label": PROBLEM_LABELS.get(working_context.get("problem_type", ""), "增长"),
            "stage_diagnosis": self._build_stage_diagnosis(working_context),
            "growth_process": growth_process,
            "north_star": north_star,
            "journey_focus": self._build_journey_focus(working_context),
            "marketplace_diagnosis": self._build_marketplace_diagnosis(query, working_context, top_option, results),
            "local_services_diagnosis": self._build_local_services_diagnosis(query, working_context, top_option, results),
            "business_model_diagnosis": self._build_business_model_diagnosis(query, working_context, top_option, results),
            "measurement_notes": self._build_measurement_notes(working_context, top_option, north_star, growth_process),
            "evidence_chain": evidence_chain,
            "memory_summary": memory_summary,
            "kelly_allocation": kelly_allocation,
            "game_theory": game_theory,
            "failure_modes": failure_modes,
            "protection_controls": protection_controls,
            "decision_line": self._build_decision_line(query, working_context, top_option, decision_text, confidence_label),
            "core_tension": self._build_core_tension(query, working_context, top_option, evidence_chain, results),
            "why_now": self._build_why_now(working_context, top_option, results, evidence_chain),
            "priorities": options[:3],
            "do_now": self._build_do_now(top_option, working_context),
            "avoid_now": self._build_avoid_now(top_option, working_context),
            "experiment": self._build_experiment(query, working_context, top_option, results, protection_controls),
            "decision_process": decision_process,
            "resource_allocation": self._build_resource_allocation(working_context, top_option, results),
            "actions": actions,
            "projection": self._build_projection(working_context, top_option, results),
            "review_trigger": self._build_review_trigger(working_context, top_option, results, protection_controls),
            "caveats": self._build_caveats(top_option, working_context),
            "missing_info": self._build_missing_info(working_context),
            "reference_cases": results["cases"][:3],
            "reference_theories": results["theories"][:2],
            "reference_failures": results.get("failures", [])[:2],
            "decision_text": decision_text,
            "confidence_label": confidence_label,
            "confidence_score": posterior,
            "current_state": self._build_current_state(working_context, results),
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
            f"- **阶段判断**：{analysis['stage_diagnosis']['current_stage']}，{analysis['stage_diagnosis']['focus']}",
            f"- **主业务过程**：{analysis['growth_process']['name']}",
            f"- **北极星指标**：{analysis['north_star']['metric']}",
            f"- **约束线**：{analysis['north_star']['guardrail']}",
            f"- **旅程卡点**：{analysis['journey_focus']['stage']}",
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
                "## 增长框架定位",
                "",
                f"- **当前阶段**：{analysis['stage_diagnosis']['current_stage']}",
                f"- **阶段重点**：{analysis['stage_diagnosis']['focus']}",
                f"- **主业务过程**：{analysis['growth_process']['name']}，{analysis['growth_process']['focus']}",
                f"- **北极星指标**：{analysis['north_star']['metric']}",
                f"- **约束线**：{analysis['north_star']['guardrail']}",
                f"- **旅程卡点**：{analysis['journey_focus']['stage']}，{analysis['journey_focus']['focus']}",
            ]
        )
        if analysis.get("business_model_diagnosis"):
            lines.extend(
                [
                    f"- **业务形态判断**：{analysis['business_model_diagnosis']['label']}，{analysis['business_model_diagnosis']['focus']}",
                    f"- **运行规则**：{analysis['business_model_diagnosis']['rule']}",
                ]
            )
        lines.extend(["", "## 判断依据", ""])
        for item in analysis["evidence_chain"]:
            lines.append(
                f"- **{item['type_label']}**：{item['name']} · {item['why']} · 证据={item['evidence_tier']}"
            )

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
                "### 数据与归因要求",
                "",
            ]
        )
        for item in analysis["measurement_notes"]:
            lines.append(f"- {item}")

        lines.extend(
            [
                "",
                "### 为什么不是其他选项",
                "",
            ]
        )
        for item in analysis["decision_process"]["why_not"]:
            lines.append(f"- **不是 {item['name']}**：{item['reason']}")
        if analysis.get("game_theory"):
            lines.extend(
                [
                    "",
                    "### 竞争/平台判断",
                    "",
                    f"- **场景**：{analysis['game_theory']['game_type_label']}",
                    f"- **建议姿态**：{analysis['game_theory']['posture']}",
                    f"- **分析结论**：{analysis['game_theory']['recommendation']}",
                ]
            )
        if analysis.get("failure_modes"):
            lines.extend(["", "### 共性失败陷阱", ""])
            for item in analysis["failure_modes"]:
                lines.append(f"- **{item['title']}**：{item['summary']}")

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
            f"**阶段判断**：{analysis['stage_diagnosis']['current_stage']}，{analysis['growth_process']['name']}",
            "",
            f"**北极星**：{analysis['north_star']['metric']}（约束线：{analysis['north_star']['guardrail']}）",
            "",
            f"**核心矛盾**：{analysis['core_tension']}",
            "",
            f"**优先级**：{top_names}",
            "",
            "**这周拍板**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[10:10] = [
                f"**业务形态判断**：{analysis['business_model_diagnosis']['label']}，{analysis['business_model_diagnosis']['focus']}",
                "",
            ]
        for item in analysis["do_now"][:3]:
            lines.append(f"- {item}")
        lines.extend(["", "**先别做**："])
        for item in analysis["avoid_now"][:2]:
            lines.append(f"- {item}")
        lines.extend(["", f"**置信度**：{analysis['confidence_label']} ({analysis['confidence_score']:.2f})"])
        if analysis.get("kelly_allocation"):
            lines.extend(
                [
                    "",
                    f"**预算建议**：{analysis['kelly_allocation']['recommended_ratio_text']}，"
                    f"{analysis['kelly_allocation']['allocation_text']}",
                ]
            )
        if analysis.get("game_theory"):
            lines.extend(
                [
                    "",
                    f"**竞争/平台姿态**：{analysis['game_theory']['posture']}",
                ]
            )
        return "\n".join(lines)

    def to_assess_markdown(
        self,
        analysis: Dict,
        clarity_score: float,
        clarity_level: str,
        can_proceed: bool,
    ) -> str:
        """Opportunity assessment before entering a deeper strategy mode."""
        next_command = "diagnose"
        if can_proceed and clarity_score >= 75 and analysis["priorities"]:
            next_command = "design"

        top_names = " / ".join(option.name for option in analysis["priorities"][:3]) if analysis["priorities"] else "待补充"
        lines = [
            "## Opportunity Assess",
            "",
            f"**当前判断**：{'可以进入下一步策略分析' if can_proceed else '先补关键信息，再进入策略分析'}",
            f"**清晰度评分**：{clarity_score:.0f}/100（{clarity_level}）",
            f"**问题归类**：{analysis['stage_diagnosis']['current_stage']} / {analysis['growth_process']['name']} / {analysis['journey_focus']['stage']}",
            f"**当前最像的主抓手**：{top_names}",
            "",
            "**为什么值得继续看**：",
        ]
        for reason in analysis["why_now"][:3]:
            lines.append(f"- {reason}")
        lines.extend(["", "**已经具备的依据**："])
        for item in analysis["evidence_chain"][:3]:
            lines.append(f"- {item['type_label']}：{item['name']}，{item['why']}")
        lines.extend(["", "**还缺什么**："])
        for item in analysis["missing_info"][:4]:
            lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "**建议下一步**：",
                f"- 先运行：`python scripts/cli.py {next_command} \"{analysis['query']}\" ...`",
                f"- 先盯住：{analysis['north_star']['metric']}（约束线：{analysis['north_star']['guardrail']}）",
            ]
        )
        return "\n".join(lines)

    def to_design_markdown(self, analysis: Dict) -> str:
        """Strategy-design output focused on implementation shape instead of diagnosis breadth."""
        top_option = analysis["priorities"][0] if analysis["priorities"] else None
        p0 = analysis["priorities"][:1]
        p1 = analysis["priorities"][1:3]
        top_case = self._top_case_reference(
            {
                "cases": analysis.get("reference_cases", []),
                "theories": analysis.get("reference_theories", []),
            }
        )
        top_theory = self._top_theory_reference(
            {
                "cases": analysis.get("reference_cases", []),
                "theories": analysis.get("reference_theories", []),
            }
        )
        lines = [
            "## Strategy Design",
            "",
            f"**设计主题**：{analysis['query']}",
            f"**主策略方向**：{analysis['decision_line']}",
            "",
            "**推荐玩法组合**：",
            "",
            "### P0 - 核心玩法",
        ]
        for option in p0:
            lines.append(
                f"- {option.name}（{option.category_name}）: 阶段匹配={option.stage_fit:.2f}，"
                f"旅程匹配={option.journey_fit:.2f}，资源画像匹配={option.resource_profile_fit:.2f}"
            )
        lines.extend(["", "### P1 - 辅助玩法"])
        for index, option in enumerate(p1):
            why_not = analysis["decision_process"]["why_not"][index]["reason"] if index < len(analysis["decision_process"]["why_not"]) else option.key_risk
            lines.append(
                f"- {option.name}（{option.category_name}）: 为什么不是 P0 = {why_not}"
            )
        lines.extend(
            [
                "",
                "### 组合协同",
                f"- 当前先围绕「{top_option.name if top_option else '主抓手'}」做主验证，其他玩法只承担放大或辅助，不单独开新战线。",
                "",
                "## 设计原则",
            ]
        )
        for reason in analysis["why_now"][:3]:
            lines.append(f"- {reason}")
        lines.extend(["", "## 实施路径"])
        for action in analysis["actions"]:
            lines.append(
                f"- {action['name']}：负责人={action['owner']}，期限={action['deadline']}，验收={action['acceptance']}"
            )
        lines.extend(
            [
                "",
                "## 关键指标",
                f"- 北极星：{analysis['north_star']['metric']}",
                f"- 旅程卡点：{analysis['journey_focus']['stage']} / {analysis['journey_focus']['focus']}",
                f"- 约束线：{analysis['north_star']['guardrail']}",
                "",
                "## 数据与归因要求",
            ]
        )
        for item in analysis["measurement_notes"]:
            lines.append(f"- {item}")
        lines.extend(["", "## 证据依据"])
        for item in analysis["evidence_chain"][:4]:
            lines.append(f"- {item['type_label']}：{item['name']}，{item['why']}")
        if top_case or top_theory:
            lines.extend(["", "## 理论 / 案例支撑"])
            if top_case:
                lines.append(f"- 案例：{top_case['name']}")
            if top_theory:
                lines.append(f"- 理论：{top_theory['name']}")
        return "\n".join(lines)

    def to_weekly_markdown(self, analysis: Dict) -> str:
        """Weekly operating brief for growth owners."""
        action = analysis["actions"][0] if analysis["actions"] else {
            "name": "待确认",
            "owner": "增长负责人",
            "deadline": "本周内",
            "acceptance": "待补充",
        }
        lines = [
            "## Weekly Brief",
            "",
            f"**本周判断**：{analysis['decision_line']}",
            "",
            f"**本周主抓手**：{analysis['priorities'][0].name if analysis['priorities'] else '待确认'}",
            f"**北极星**：{analysis['north_star']['metric']}",
            f"**本周负责人**：{action['owner']}",
            f"**本周截止**：{action['deadline']}",
            "",
            "**这周要做**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[8:8] = [
                f"**业务形态提醒**：{analysis['business_model_diagnosis']['focus']}",
                "",
            ]
        for item in analysis["do_now"][:3]:
            lines.append(f"- {item}")
        lines.extend(["", "**这周不要做**："])
        for item in analysis["avoid_now"][:3]:
            lines.append(f"- {item}")
        lines.extend(["", "**复盘检查点**："])
        lines.append(f"- 验收标准：{action['acceptance']}")
        lines.append(f"- 回看信号：{analysis['review_trigger']['signal']}")
        if analysis.get("protection_controls"):
            lines.append("- 复发保护：")
            for item in analysis["protection_controls"][:2]:
                lines.append(f"- 防止{item['risk']}：{item['guardrail']}")
        if analysis.get("kelly_allocation"):
            lines.extend(
                [
                    "",
                    "**预算动作**：",
                    f"- 当前建议：{analysis['kelly_allocation']['recommended_ratio_text']}，{analysis['kelly_allocation']['allocation_text']}",
                    f"- 加仓条件：{analysis['kelly_allocation']['add_condition']}",
                    f"- 停止条件：{analysis['kelly_allocation']['stop_condition']}",
                ]
            )
        if analysis.get("game_theory"):
            lines.extend(
                [
                    "",
                    "**竞争/平台提醒**：",
                    f"- {analysis['game_theory']['recommendation']}",
                ]
            )
        if analysis.get("failure_modes"):
            lines.extend(["", "**共性失败陷阱**："])
            for item in analysis["failure_modes"][:2]:
                lines.append(f"- {item['title']}：{item['summary']}")
        if analysis["memory_summary"]:
            lines.extend(["", "**历史提醒**："])
            for item in analysis["memory_summary"][:3]:
                lines.append(f"- {item}")
        return "\n".join(lines)

    def to_experiment_card_markdown(self, analysis: Dict) -> str:
        """Compact experiment card for execution."""
        action = analysis["actions"][0] if analysis["actions"] else {
            "name": "待确认",
            "owner": "增长负责人",
            "deadline": "本周内",
            "resources": "待补充",
        }
        lines = [
            "## Experiment Card",
            "",
            f"**实验名称**：{action['name']}",
            f"**假设**：{analysis['experiment']['hypothesis']}",
            f"**主指标**：{analysis['north_star']['metric']}",
            f"**负责人**：{action['owner']}",
            f"**期限**：{action['deadline']}",
            f"**资源**：{action['resources']}",
            "",
            "**步骤**：",
        ]
        for step in analysis["experiment"]["steps"]:
            lines.append(f"- {step}")
        lines.extend(["", "**成功信号**："])
        for signal in analysis["experiment"]["success_signals"]:
            lines.append(f"- {signal}")
        lines.extend(["", "**停止信号**："])
        for signal in analysis["experiment"]["stop_signals"]:
            lines.append(f"- {signal}")
        if analysis.get("protection_controls"):
            lines.extend(["", "**复发保护措施**："])
            for item in analysis["protection_controls"][:2]:
                lines.append(f"- 风险={item['risk']}：{item['control']}")
        if analysis.get("kelly_allocation"):
            lines.extend(
                [
                    "",
                    "**预算建议**：",
                    f"- 推荐比例：{analysis['kelly_allocation']['recommended_ratio_text']}",
                    f"- 建议投入：{analysis['kelly_allocation']['allocation_text']}",
                    f"- 加仓条件：{analysis['kelly_allocation']['add_condition']}",
                    f"- 停止条件：{analysis['kelly_allocation']['stop_condition']}",
                ]
            )
        if analysis.get("failure_modes"):
            lines.extend(["", "**失败陷阱**："])
            for item in analysis["failure_modes"][:2]:
                lines.append(f"- {item['title']}：{item['summary']}")
        if analysis["memory_summary"]:
            lines.extend(["", "**历史提醒**："])
            for item in analysis["memory_summary"][:2]:
                lines.append(f"- {item}")
        return "\n".join(lines)

    def to_decision_memo_markdown(self, analysis: Dict) -> str:
        """Decision memo optimized for review and approval."""
        top_name = analysis["priorities"][0].name if analysis["priorities"] else "待确认"
        lines = [
            "## Decision Memo",
            "",
            f"**决策请求**：是否在当前阶段优先投入「{top_name}」。",
            "",
            f"**一句话判断**：{analysis['decision_line']}",
            "",
            "**做这个决定的依据**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[5:5] = [
                f"**{analysis['business_model_diagnosis']['label']}判断**：",
                f"- 当前侧重点：{analysis['business_model_diagnosis']['focus']}",
                f"- 运行规则：{analysis['business_model_diagnosis']['rule']}",
                "",
            ]
        for item in analysis["evidence_chain"]:
            lines.append(f"- {item['type_label']}：{item['name']}，{item['why']}")
        lines.extend(["", "**不做其他选项的原因**："])
        for item in analysis["decision_process"]["why_not"]:
            lines.append(f"- {item['name']}：{item['reason']}")
        lines.extend(["", "**需要批准的动作**："])
        for action in analysis["actions"]:
            lines.append(f"- {action['name']}（负责人={action['owner']}，期限={action['deadline']}）")
        if analysis.get("kelly_allocation"):
            lines.extend(
                [
                    "",
                    "**预算建议**：",
                    f"- 推荐投入：{analysis['kelly_allocation']['allocation_text']}",
                    f"- 推荐比例：{analysis['kelly_allocation']['recommended_ratio_text']}",
                    f"- Kelly 准备度：{analysis['kelly_allocation']['readiness_score']}/100（{analysis['kelly_allocation']['readiness_status']}）",
                ]
            )
        if analysis.get("game_theory"):
            lines.extend(
                [
                    "",
                    "**竞争/平台判断**：",
                    f"- {analysis['game_theory']['recommendation']}",
                ]
            )
        if analysis.get("failure_modes"):
            lines.extend(["", "**失败陷阱**："])
            for item in analysis["failure_modes"][:2]:
                lines.append(f"- {item['title']}：{item['summary']}")
        if analysis.get("protection_controls"):
            lines.extend(["", "**复发保护**："])
            for item in analysis["protection_controls"][:2]:
                lines.append(f"- 风险={item['risk']}；保护线={item['guardrail']}；停止条件={item['stop']}")
        if analysis["memory_summary"]:
            lines.extend(["", "**组织历史约束**："])
            for item in analysis["memory_summary"][:3]:
                lines.append(f"- {item}")
        return "\n".join(lines)

    def to_qbr_markdown(self, analysis: Dict) -> str:
        """Quarterly business review style summary."""
        top_name = analysis["priorities"][0].name if analysis["priorities"] else "待确认"
        lines = [
            "## QBR Summary",
            "",
            f"**季度主题**：围绕「{top_name}」修正当前增长主路径。",
            "",
            f"**经营判断**：{analysis['decision_line']}",
            f"**阶段定位**：{analysis['stage_diagnosis']['current_stage']} / {analysis['growth_process']['name']}",
            f"**北极星**：{analysis['north_star']['metric']}",
            "",
            "**季度优先事项**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[7:7] = [
                f"**业务形态判断**：{analysis['business_model_diagnosis']['label']} / {analysis['business_model_diagnosis']['focus']}",
                "",
            ]
        for item in analysis["do_now"][:3]:
            lines.append(f"- {item}")
        lines.extend(["", "**季度风险**："])
        for item in analysis["caveats"][:3]:
            lines.append(f"- {item}")
        if analysis.get("kelly_allocation"):
            lines.extend(
                [
                    "",
                    "**预算分配建议**：",
                    f"- 当前建议：{analysis['kelly_allocation']['recommended_ratio_text']}，{analysis['kelly_allocation']['allocation_text']}",
                    f"- 加仓条件：{analysis['kelly_allocation']['add_condition']}",
                    f"- 停止条件：{analysis['kelly_allocation']['stop_condition']}",
                ]
            )
        if analysis.get("game_theory"):
            lines.extend(
                [
                    "",
                    "**竞争/平台姿态**：",
                    f"- {analysis['game_theory']['posture']}",
                    f"- {analysis['game_theory']['recommendation']}",
                ]
            )
        if analysis.get("failure_modes"):
            lines.extend(["", "**失败陷阱**："])
            for item in analysis["failure_modes"][:3]:
                lines.append(f"- {item['title']}：{item['summary']}")
        return "\n".join(lines)

    def to_fast_scan_markdown(self, analysis: Dict) -> str:
        """Compact recommendation for early-stage screening."""
        lines = [
            "## Fast Scan",
            "",
            f"**建议**：{analysis['decision_line']}",
            "",
            "**理由**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[4:4] = [
                f"**业务形态判断**：{analysis['business_model_diagnosis']['focus']}",
                "",
            ]
        for reason in analysis["why_now"][:3]:
            lines.append(f"- {reason}")
        lines.extend(["", "**风险**："])
        for item in analysis["caveats"][:2]:
            lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "**下一步**：",
                f"- {analysis['actions'][0]['name']}",
                "",
                f"**置信度**：{analysis['confidence_label']} ({analysis['confidence_score']:.2f})",
            ]
        )
        return "\n".join(lines)

    def to_brd_markdown(self, analysis: Dict) -> str:
        """Render a lighter-weight decision BRD from strategy analysis."""
        top_name = analysis["priorities"][0].name if analysis["priorities"] else "待确认"
        lines = [
            f"# {analysis['query']} - 增长决策BRD",
            "",
            "## 1. 执行摘要",
            "",
            analysis["decision_line"],
            "",
            "## 2. 业务问题与机会",
            "",
            f"- **阶段**：{analysis['stage_diagnosis']['current_stage']}",
            f"- **主业务过程**：{analysis['growth_process']['name']}",
            f"- **北极星指标**：{analysis['north_star']['metric']}",
            f"- **约束线**：{analysis['north_star']['guardrail']}",
            f"- **核心矛盾**：{analysis['core_tension']}",
            "",
            "## 3. 核心策略",
            "",
            f"- **主抓手**：{top_name}",
            "- **为什么现在做**：",
        ]
        if analysis.get("business_model_diagnosis"):
            lines[13:13] = [
                f"- **业务形态判断**：{analysis['business_model_diagnosis']['label']}，{analysis['business_model_diagnosis']['focus']}",
                f"- **业务形态规则**：{analysis['business_model_diagnosis']['rule']}",
            ]
        for reason in analysis["why_now"]:
            lines.append(f"  - {reason}")
        lines.extend(["", "## 4. 风险与反对意见", ""])
        for item in analysis["decision_process"]["why_not"]:
            lines.append(f"- **备选不优先**：{item['name']}，因为{item['reason']}")
        for item in analysis["caveats"][:2]:
            lines.append(f"- **主要风险**：{item}")
        if analysis.get("game_theory"):
            lines.append(f"- **竞争/平台判断**：{analysis['game_theory']['recommendation']}")
        if analysis.get("failure_modes"):
            for item in analysis["failure_modes"][:2]:
                lines.append(f"- **失败陷阱**：{item['title']}，{item['summary']}")
        lines.extend(["", "## 5. 证据依据", ""])
        for item in analysis["evidence_chain"]:
            lines.append(
                f"- **{item['type_label']}**：{item['name']} · {item['why']} · 证据={item['evidence_tier']}"
            )
        lines.extend(["", "## 6. 下一步行动", ""])
        for action in analysis["actions"]:
            lines.append(
                f"- **{action['name']}**：负责人={action['owner']}，期限={action['deadline']}，验收={action['acceptance']}"
            )
        return "\n".join(lines)

    def build_learning_path(self, query: str, context: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
        """Build a lightweight learning path around the retrieval results."""
        working_context = self._build_retrieval_context(context)
        results = self.retriever.retrieve(query, working_context, case_limit=3, weapon_limit=4, theory_limit=3)
        analysis = self.analyze(query, working_context, mode="learn")
        guide_map = {
            "acquisition": [
                {"name": "阶段判断", "file": "knowledge/guides/stage-diagnosis.md"},
                {"name": "AIDA 转化模型", "file": "knowledge/guides/aida-model.md"},
                {"name": "归因与身份识别", "file": "knowledge/guides/attribution-and-identity.md"},
            ],
            "retention": [
                {"name": "用户旅程诊断", "file": "knowledge/guides/user-journey-diagnosis.md"},
                {"name": "北极星指标", "file": "knowledge/guides/north-star-metric.md"},
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
        """Render a learning-path response."""
        path = self.build_learning_path(query, context)
        lines = [
            "## Learning Path",
            "",
            f"**主题**：{query}",
            "",
            "**建议先读的方法指南**：",
        ]
        if path.get("business_model_diagnosis"):
            lines[4:4] = [
                f"**业务形态判断**：{path['business_model_diagnosis']['label']}，{path['business_model_diagnosis']['focus']}",
                "",
            ]
        for guide in path["guides"]:
            lines.append(f"- {guide['name']}（{guide['file']}）")
        lines.extend(["", "**相关理论**："])
        for theory in path["theories"]:
            lines.append(f"- {theory['name']}（{theory['file']}）: {theory['reason']}")
        lines.extend(["", "**先看这些案例**："])
        for case in path["cases"]:
            lines.append(f"- {case['name']}：{case['reason']}")
        lines.extend(["", "**建议对照的玩法**："])
        for weapon in path["weapons"]:
            lines.append(f"- {weapon['name']}（{weapon['category']}）: {weapon['reason']}")
        return "\n".join(lines)

    def _build_stage_diagnosis(self, context: Dict[str, str]) -> Dict[str, str]:
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
        problem = context.get("problem_type", "")
        name, focus = PROBLEM_TO_PROCESS.get(problem, ("增长经营", "先判断问题更偏新增还是偏价值深耕。"))
        return {
            "name": name,
            "focus": focus,
            "reason": f"当前问题更接近{PROBLEM_LABELS.get(problem, '增长')}，因此优先按{name}处理。",
        }

    def _build_north_star(self, context: Dict[str, str]) -> Dict[str, str]:
        metric = self._primary_metric(context)
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

    def _build_retrieval_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        working_context = dict(context)
        if not working_context.get("growth_process"):
            working_context["growth_process"] = self._build_growth_process(working_context)["name"]
        if not working_context.get("journey_stage"):
            working_context["journey_stage"] = self._build_journey_focus(working_context)["stage"]
        if not working_context.get("metric"):
            working_context["metric"] = self._primary_metric(working_context)
        return working_context

    def _build_journey_focus(self, context: Dict[str, str]) -> Dict[str, str]:
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

    def _build_measurement_notes(
        self,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        north_star: Dict[str, str],
        growth_process: Dict[str, str],
    ) -> List[str]:
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
        if self._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            notes.append("至少拆出单城供给活跃、需求密度、有效履约订单数和履约成功率，避免只看拉新量。")
        if self._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            notes.append("至少拆出供给侧活跃、需求侧活跃、有效撮合数三段漏斗，判断先补哪一侧。")
        experiment_log = self._get_experiment_log(context)
        if experiment_log:
            notes.append("历史实验口径要与本轮实验保持一致，避免换指标后误判改进。")
        return notes

    def _get_company_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        payload = context.get("company_profile", {})
        return payload if isinstance(payload, dict) else {}

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

    def _get_experiment_log(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        payload = context.get("experiment_log", {})
        if isinstance(payload, dict):
            experiments = payload.get("experiments", [])
            if isinstance(experiments, list):
                return [item for item in experiments if isinstance(item, dict)]
        return []

    def _build_memory_summary(self, context: Dict[str, Any]) -> List[str]:
        summary: List[str] = []
        profile = self._get_company_profile(context)
        if profile:
            name = profile.get("company_name") or profile.get("product_name") or "当前项目"
            business_model = profile.get("business_model", "业务模式待补充")
            team = profile.get("team") or context.get("team") or "团队规模待补充"
            summary.append(f"{name} 当前按「{business_model}」经营，团队资源={team}。")
            if profile.get("target_user"):
                summary.append(f"当前核心目标用户：{profile['target_user']}。")
        for item in self._get_experiment_log(context)[:3]:
            name = str(item.get("name", "未命名实验"))
            outcome = str(item.get("outcome", item.get("status", "结果待定")))
            lesson = str(item.get("lesson", "")).strip()
            detail = f"历史实验「{name}」结果={outcome}"
            if lesson:
                detail += f"，教训={lesson}"
            summary.append(detail + "。")
        return summary

    def _build_marketplace_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        if self._business_model_kind(context) != "marketplace" or context.get("problem_type") != "acquisition":
            return None

        side_focus = self._marketplace_liquidity_focus(query, context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        if self._business_model_kind(context) != "local-services" or context.get("problem_type") != "acquisition":
            return None

        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
        return {
            "focus": self._local_services_density_focus(query, context),
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
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        kind = self._business_model_kind(context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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

    def _build_kelly_context(self, context: Dict[str, Any], top_option: Optional[StrategyOption]) -> Dict[str, Any]:
        budget_amount = self._parse_budget_amount(str(context.get("budget", "")))
        resource_clarity = "clear" if budget_amount > 0 else "partial" if context.get("team") else "unclear"
        probability_source = "expert" if context.get("history") or self._get_experiment_log(context) else "guess"
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

    def _build_game_theory_analysis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional[StrategyOption],
    ) -> Optional[Dict[str, Any]]:
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
            if any(word in market for word in ["平台", "双边", "marketplace"]) or self._business_model_kind(context) in {"marketplace", "local-services"}
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
        for item in self._get_experiment_log(context):
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
        top_option: Optional[StrategyOption],
        results: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, str]]:
        def load_failure_doc(path_str: str) -> Optional[Dict[str, str]]:
            try:
                from pathlib import Path

                doc_path = Path(__file__).resolve().parent.parent / path_str
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

    def _build_kelly_allocation(
        self,
        context: Dict[str, Any],
        top_option: Optional[StrategyOption],
        posterior: float,
    ) -> Optional[Dict[str, Any]]:
        if not top_option or not context.get("budget"):
            return None

        budget_amount = self._parse_budget_amount(str(context.get("budget", "")))
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

        metric = self._primary_metric(context)
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

    def _history_score_adjustment(self, category: str, weapon_name: str, context: Dict[str, Any]) -> Tuple[float, str]:
        adjustments = 0.0
        notes: List[str] = []
        normalized_name = weapon_name.lower()
        for item in self._get_experiment_log(context):
            exp_category = str(item.get("category", "")).strip()
            exp_name = str(item.get("name", "")).strip().lower()
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            lesson = str(item.get("lesson", "")).strip()
            same_track = exp_category == category or (exp_name and exp_name in normalized_name) or (normalized_name and normalized_name in exp_name)
            if not same_track:
                continue
            if outcome in {"failed", "stop", "stopped", "negative"}:
                adjustments -= 1.0
                notes.append(f"历史上同方向做过但未跑通：{lesson or exp_name or exp_category}")
            elif outcome in {"success", "succeeded", "positive", "validated"}:
                adjustments += 0.45
                notes.append(f"历史上同方向已有正向信号：{lesson or exp_name or exp_category}")
        return adjustments, "；".join(notes[:2])

    def _history_repeat_risk_prompts(self, context: Dict[str, Any]) -> List[str]:
        prompts: List[str] = []
        readable = self._failure_tag_labels()
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [
                    str(item.get("name", "")),
                    str(item.get("lesson", "")),
                    str(item.get("avoid_repeat", "")),
                ]
            )
            tags = self._failure_condition_tags(failure_text)
            if not tags:
                continue
            prompts.append("这次准备如何避免历史失败条件：" + "、".join(readable[tag] for tag in tags[:3]))
        return prompts[:2]

    def _history_protection_controls(
        self,
        context: Dict[str, Any],
        top_option: Optional[StrategyOption],
    ) -> List[Dict[str, str]]:
        controls: List[Dict[str, str]] = []
        readable = self._failure_tag_labels()
        control_map = {
            "low_quality_users": {
                "control": "只统计高意向样本，拆开流量量与高意向转化率，不用总新增替代真实质量。",
                "guardrail": "高意向转化率 / 激活率不能继续下滑",
                "stop": "新增上涨但高意向转化或激活继续恶化时立即停",
            },
            "activation_drop": {
                "control": "把首次价值达成率设成首个过程指标，先验证核心动作，不同时改多处 onboarding。",
                "guardrail": "首次价值达成率不能低于当前基线",
                "stop": "曝光或注册上涨但首次价值达成率不升反降时立即停",
            },
            "retention_damage": {
                "control": "主实验之外单独监控 7 日 / 30 日留存，禁止用短期刺激替代真实回访。",
                "guardrail": "7 日 / 30 日留存不能恶化",
                "stop": "短期指标改善但留存或复访连续恶化时立即停",
            },
            "cac_loss": {
                "control": "预算拆成小批次，先验证单渠道单位经济性，再决定是否加仓。",
                "guardrail": "CAC 不能超出当前可接受区间",
                "stop": "样本量尚小但 CAC 已明显失控时立即停",
            },
            "subsidy_abuse": {
                "control": "把补贴和激励限定在小样本白名单，不让补贴直接决定传播动机。",
                "guardrail": "补贴成本和作弊率不能失控",
                "stop": "需要持续加大补贴才能维持指标时立即停",
            },
            "diffuse_execution": {
                "control": "一次只改一个主机制，实验期间锁定其他变量，保证可归因。",
                "guardrail": "实验窗口内不允许并行改多个主机制",
                "stop": "一旦并行改动过多导致无法归因，本轮实验作废",
            },
            "lead_quality": {
                "control": "把线索数和高意向线索/成单率分开看，先验证 ICP 与线索质量。",
                "guardrail": "高意向线索率和 demo-to-close 不能继续下滑",
                "stop": "线索数上涨但成交效率继续恶化时立即停",
            },
        }

        option_tags = set(self._option_failure_condition_tags(top_option.category, top_option.name, {
            "guardrail_risk": top_option.guardrail_risk,
            "resource_profile": top_option.resource_profile,
        })) if top_option else set()
        problem_relevant_tags = {
            "acquisition": {"low_quality_users", "cac_loss", "lead_quality", "activation_drop"},
            "activation": {"activation_drop", "diffuse_execution"},
            "retention": {"retention_damage", "diffuse_execution"},
            "monetization": {"retention_damage", "cac_loss"},
            "referral": {"low_quality_users", "subsidy_abuse", "activation_drop"},
        }.get(str(context.get("problem_type", "")), set())
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [str(item.get("name", "")), str(item.get("lesson", "")), str(item.get("avoid_repeat", ""))]
            )
            failure_tags = self._failure_condition_tags(failure_text)
            tags = [tag for tag in failure_tags if not option_tags or tag in option_tags]
            if not tags:
                tags = [tag for tag in failure_tags if tag in problem_relevant_tags]
            for tag in tags[:2]:
                if tag not in control_map:
                    continue
                controls.append(
                    {
                        "risk": readable[tag],
                        "control": control_map[tag]["control"],
                        "guardrail": control_map[tag]["guardrail"],
                        "stop": control_map[tag]["stop"],
                    }
                )

        deduped: List[Dict[str, str]] = []
        seen = set()
        for item in controls:
            key = item["risk"]
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        return deduped[:3]

    def _normalize_text(self, text: Any) -> str:
        return " ".join(str(text).lower().replace("_", " ").replace("-", " ").split())

    def _failure_condition_tags(self, text: str) -> List[str]:
        normalized = self._normalize_text(text)
        mapping = {
            "low_quality_users": ["低质量用户", "低质量流量", "羊毛", "薅羊毛", "意向低"],
            "activation_drop": ["激活低", "激活偏低", "首次价值", "转化偏低", "转化低", "试用激活"],
            "retention_damage": ["留存低", "留存偏低", "伤害留存", "假留存", "假活跃", "回访低"],
            "cac_loss": ["cac", "获客成本", "成本高", "投放失控", "预算失控"],
            "subsidy_abuse": ["高补贴", "补贴", "高激励", "激励滥用"],
            "diffuse_execution": ["无法归因", "同时做太多", "太分散", "多机制同时"],
            "lead_quality": ["线索质量", "高意向线索", "成交低", "成单低", "demo"],
        }
        tags = [tag for tag, keywords in mapping.items() if any(keyword in normalized for keyword in keywords)]
        return tags

    def _failure_tag_labels(self) -> Dict[str, str]:
        return {
            "low_quality_users": "低质量用户/流量",
            "activation_drop": "激活不成立",
            "retention_damage": "留存受损或假留存",
            "cac_loss": "CAC/预算失控",
            "subsidy_abuse": "高补贴或激励滥用",
            "diffuse_execution": "动作过多导致无法归因",
            "lead_quality": "线索质量不足",
        }

    def _option_failure_condition_tags(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
    ) -> List[str]:
        source = " ".join(
            [
                category,
                weapon_name,
                str(metadata.get("guardrail_risk", "")),
                str(metadata.get("resource_profile", "")),
            ]
        )
        tags = set(self._failure_condition_tags(source))
        category_defaults = {
            "viral-referral": {"low_quality_users", "subsidy_abuse"},
            "paid-ads": {"cac_loss", "low_quality_users"},
            "plg": {"activation_drop"},
            "retention": {"retention_damage", "diffuse_execution"},
            "monetization": {"retention_damage"},
            "b2b-sales": {"lead_quality"},
        }
        tags.update(category_defaults.get(category, set()))
        return list(tags)

    def _history_failure_condition_adjustment(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, str]:
        option_tags = set(self._option_failure_condition_tags(category, weapon_name, metadata))
        if not option_tags:
            return 0.0, ""

        penalty = 0.0
        notes: List[str] = []
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [
                    str(item.get("name", "")),
                    str(item.get("lesson", "")),
                    str(item.get("avoid_repeat", "")),
                ]
            )
            failure_tags = set(self._failure_condition_tags(failure_text))
            overlap = option_tags & failure_tags
            if not overlap:
                continue
            penalty += 0.35
            readable = self._failure_tag_labels()
            notes.append("历史失败条件重复：" + "、".join(readable[tag] for tag in sorted(overlap)))
        return min(0.9, penalty), "；".join(notes[:2])

    def _metric_alignment_adjustment(
        self,
        category: str,
        context: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        metric_text = self._normalize_text(" ".join([str(context.get("metric", "")), str(context.get("goal", ""))]))
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

    def _build_context_summary(self, context: Dict[str, str]) -> str:
        parts = []
        profile = self._get_company_profile(context)
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

    def _build_evidence_chain(
        self,
        results: Dict,
        top_option: Optional[StrategyOption],
        context: Dict[str, Any],
    ) -> List[Dict[str, str]]:
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

    def _top_case_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        cases = results.get("cases", [])
        return cases[0] if cases else None

    def _top_theory_reference(self, results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        theories = results.get("theories", [])
        return theories[0] if theories else None

    def _build_core_tension(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        evidence_chain: List[Dict[str, str]],
        results: Optional[Dict[str, Any]] = None,
    ) -> str:
        problem = context.get("problem_type", "")
        stage = context.get("stage", "")
        evidence_parts: List[str] = []

        top_case = self._top_case_reference(results) if results else None
        top_theory = self._top_theory_reference(results) if results else None

        if top_case:
            case_highlights = top_case.get("highlights")
            case_insight = case_highlights[0] if case_highlights else "先抓住可复制主路径"
            evidence_parts.append(f"案例「{top_case['name']}」提供的关键洞察是「{case_insight}」")
        if top_theory:
            theory_highlights = top_theory.get("highlights")
            theory_insight = theory_highlights[0] if theory_highlights else "要先验证机制成立条件"
            evidence_parts.append(f"遵循理论「{top_theory['name']}」的核心原则「{theory_insight}」")

        evidence_hint = "；".join(evidence_parts) + "，" if evidence_parts else ""
        if self._business_model_kind(context) == "local-services" and problem == "acquisition":
            density_focus = self._local_services_density_focus(query, context)
            return (
                f"{evidence_hint}核心矛盾不是先铺更多城市或渠道，而是先在单城/单区域做出稳定供给、需求和履约密度；"
                f"{density_focus}"
            )
        if self._business_model_kind(context) == "marketplace" and problem == "acquisition":
            liquidity_focus = self._marketplace_liquidity_focus(query, context)
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
        return f"当前问题“{query}”要先收敛主抓手，避免同时推进太多方向；建议围绕「{option_name}」建立第一轮验证。"

    def _build_why_now(
        self,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        results: Dict,
        evidence_chain: List[Dict[str, str]],
    ) -> List[str]:
        reasons = []
        if top_option:
            reasons.append(
                f"首选「{top_option.name}」是因为它在当前资源和阶段约束下具有最高的落地确定性。其画像匹配度达 {top_option.resource_profile_fit:.2f}，"
                f"且与目标旅程节点「{top_option.journey_stage or '核心路径'}」高度契合。"
            )
            if top_option.evidence_support:
                reasons.append(f"该判断得到了以下直接证据的支持：{'；'.join(top_option.evidence_support[:2])}。")
            if top_option.metric_bonus > 0:
                reasons.append(f"由于该方向与当前主指标「{self._primary_metric(context)}」直接关联，我们显式提升了其优先级。")
            if top_option.risk_signals:
                reasons.append(f"需要警惕的潜在风险或失效信号是：{'；'.join(top_option.risk_signals[:1])}。")

        top_case = self._top_case_reference(results)
        if top_case:
            case_reason = f"案例「{top_case['name']}」提供了极其相似的场景证据（相似度 {top_case['score']:.2f}）"
            if top_case.get("highlights"):
                case_reason += f"，其成功的关键动作「{top_case['highlights'][0]}」具备直接迁移价值。"
            reasons.append(case_reason)

        top_theory = self._top_theory_reference(results)
        if top_theory:
            theory_reason = f"从增长底层逻辑看，理论「{top_theory['name']}」解释了为什么在当前阶段必须优先关注「{top_theory['metadata'].get('growth_process', '主业务过程')}」"
            if top_theory.get("highlights"):
                theory_reason += f"，并给出了「{top_theory['highlights'][0]}」作为执行准则。"
            reasons.append(theory_reason)

        if context.get("stage"):
            stage_label = STAGE_LABELS.get(context["stage"], context["stage"])
            stage_focus = STAGE_FRAMEWORK.get(context["stage"], {}).get("focus", "快速验证")
            reasons.append(f"考虑到当前处于 {stage_label} 阶段，决策重心应放在「{stage_focus}」上。")

        profile = self._get_company_profile(context)
        if profile.get("target_user"):
            reasons.append(f"基于目标用户群「{profile['target_user']}」的行为特征，该策略更有利于在核心触点产生真实价值。")

        if top_option and top_option.explicit_guardrail_penalty > 0:
            reasons.append(f"注意：虽然该策略被推荐，但由于触及约束线（扣分 {top_option.explicit_guardrail_penalty:.2f}），执行时必须严格遵守保护措施。")

        return reasons

    def _evidence_adjustments_for_option(
        self,
        metadata: Dict[str, Any],
        results: Dict[str, Any],
        context: Dict[str, str],
    ) -> Tuple[float, float, List[str], List[str]]:
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

    def _business_model_adjustment(
        self,
        category: str,
        context: Dict[str, str],
    ) -> Tuple[float, List[str]]:
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

    def _prioritize_options(self, results: Dict[str, Any], context: Dict[str, str]) -> List[StrategyOption]:
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
            history_adjustment, history_note = self._history_score_adjustment(category, weapon["name"], context)
            history_condition_penalty, history_condition_note = self._history_failure_condition_adjustment(
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
        if self._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            return [
                self._local_services_density_focus("", context),
                "优先选一个城市、一个区域或一个核心场景，把供给质量、需求密度和履约体验一起跑通。",
                f"所有动作都围绕「{metric}」和有效履约闭环设计验证。",
            ]
        if self._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            return [
                self._marketplace_liquidity_focus("", context),
                "优先用人工运营或定向激励把单边密度做出来，再验证另一侧的自然响应。",
                f"所有动作都围绕「{metric}」和单边流动性设计验证闭环。",
            ]
        return base_actions[:2] + [f"所有动作都围绕「{metric}」设计单一验证闭环。"][:1]

    def _build_avoid_now(self, top_option: Optional[StrategyOption], context: Dict[str, str]) -> List[str]:
        if top_option is None:
            return ["不要在信息不足时同时推进多个增长方向。"]

        stage = context.get("stage", "")
        avoid_list = CATEGORY_AVOIDS.get(top_option.category, []).copy()
        if self._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            avoid_list = [
                "不要多城同时铺开。",
                "不要在履约体验没稳前用大补贴硬拉量。",
            ] + avoid_list
        if self._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            avoid_list = [
                "不要同时大规模补贴供需两侧。",
                "不要在两侧都没有流动性前追求全面开放。",
            ] + avoid_list
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            avoid_repeat = str(item.get("avoid_repeat", item.get("lesson", ""))).strip()
            if outcome in {"failed", "stop", "stopped", "negative"} and avoid_repeat:
                avoid_list.append(f"不要重复历史失败模式：{avoid_repeat}")
            elif outcome in {"failed", "stop", "stopped", "negative"}:
                failure_prompts = self._history_repeat_risk_prompts({"experiment_log": {"experiments": [item]}})
                if failure_prompts:
                    avoid_list.append(failure_prompts[0].replace("这次准备如何避免历史失败条件：", "不要重演历史失败条件："))
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
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, Union[List[str], str]]:
        metric = self._primary_metric(context)
        if top_option is None:
            return {
                "hypothesis": "先补信息后再设计实验。",
                "steps": ["补齐目标、现状、资源、约束。"],
                "success_signals": [f"明确 {metric} 的当前值和目标值。"],
                "stop_signals": ["关键事实仍不清楚，暂停继续扩展方案。"],
            }

        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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
            f"定义单一实验对象：围绕“{query}”只验证一个关键动作。",
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

    def _build_missing_info(self, context: Dict[str, str]) -> List[str]:
        prompts = []
        if not context.get("metric"):
            prompts.append("当前最关键指标的现值和目标值")
        if not context.get("budget"):
            prompts.append("预算上限")
        if not context.get("team"):
            prompts.append("可投入的人力角色和数量")
        if not context.get("history") and not self._get_experiment_log(context):
            prompts.append("过去做过哪些尝试，效果如何")
        elif self._get_experiment_log(context):
            prompts.extend(self._history_repeat_risk_prompts(context))
        if not context.get("constraints"):
            prompts.append("当前不能突破的业务/产品/合规约束")
        if not self._get_company_profile(context):
            prompts.append("公司画像：目标用户、商业模式和当前组织能力")
        if self._business_model_kind(context) == "local-services" and context.get("problem_type") == "acquisition":
            prompts.append("单城供给质量、需求密度、履约成功率和区域空档点")
        if self._business_model_kind(context) == "marketplace" and context.get("problem_type") == "acquisition":
            prompts.append("供给侧与需求侧当前密度、转化和空档点")
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

    def _build_resource_allocation(
        self,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        option_name = top_option.name if top_option else "主抓手"
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
        increase = f"把产品/增长/运营资源优先向「{option_name}」倾斜。"
        if top_case:
            increase += f" 案例「{top_case['name']}」说明该方向更接近当前阶段的可复制主路径。"
        decrease = "压缩低优先级活动、分散试错和非核心项目。"
        if top_theory:
            decrease += f" 理论「{top_theory['name']}」提示不要同时分散验证过多机制。"
        protect = f"保护 {self._primary_metric(context)} 的数据监控与复盘节奏。"
        if top_option and top_option.guardrail_risk:
            protect += f" 同时重点监控约束线风险：{top_option.guardrail_risk}。"
        return {
            "increase": increase,
            "decrease": decrease,
            "protect": protect,
        }

    def _build_actions(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        option_name = top_option.name if top_option else "主策略验证"
        metric = self._primary_metric(context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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

    def _build_projection(
        self,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        metric = self._primary_metric(context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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

    def _build_review_trigger(
        self,
        context: Dict[str, str],
        top_option: Optional[StrategyOption],
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, str]:
        metric = self._primary_metric(context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
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

    def _build_caveats(self, top_option: Optional[StrategyOption], context: Dict[str, str]) -> List[str]:
        caveats = []
        if top_option:
            caveats.append(f"警告：{top_option.key_risk}")
        caveats.append("不确定：如果关键指标基线不准，当前优先级判断会偏差。")
        if not context.get("history") and not self._get_experiment_log(context):
            caveats.append("警告：历史尝试信息缺失，可能重复踩同样的坑。")
        return caveats

    def _build_current_state(
        self,
        context: Dict[str, str],
        results: Dict[str, Any],
    ) -> Dict[str, Union[List[str], str]]:
        facts = []
        profile = self._get_company_profile(context)
        top_case = self._top_case_reference(results)
        top_theory = self._top_theory_reference(results)
        if context.get("metric"):
            facts.append(f"{context['metric']} (observed)")
        else:
            facts.append(f"{self._primary_metric(context)} 尚未提供现值 (assumed)")
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
            experiment_log = self._get_experiment_log(context)
            if experiment_log:
                facts.append(f"历史实验数：{len(experiment_log)} (observed)")
            else:
                facts.append("历史尝试信息缺失 (assumed)")
        if top_case:
            facts.append(f"当前最相近案例：{top_case['name']}，可作为外部参照 (observed)")
        if top_theory:
            facts.append(f"当前主要解释框架：{top_theory['name']} (observed)")

        return {
            "goal": context.get("goal", f"围绕 {self._primary_metric(context)} 找到当前主抓手"),
            "stage": STAGE_LABELS.get(context.get("stage", ""), context.get("stage", "未明确")),
            "constraints": context.get("constraints", "预算/人力/时间窗口待补充"),
            "resources": context.get("team", "默认最小跨职能团队"),
            "facts": facts,
        }
