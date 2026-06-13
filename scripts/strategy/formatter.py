#!/usr/bin/env python3
"""Output formatting methods for strategy analysis results."""

import json
from typing import Any, Dict, List, Optional


class StrategyFormatter:
    """Format strategy analysis results into various output formats."""

    def __init__(self, brain: Any):
        """Initialize formatter with reference to StrategyBrain instance.

        Args:
            brain: StrategyBrain instance for accessing helper methods
        """
        self.brain = brain

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
        top_case = self.brain._top_case_reference(
            {
                "cases": analysis.get("reference_cases", []),
                "theories": analysis.get("reference_theories", []),
            }
        )
        top_theory = self.brain._top_theory_reference(
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

    def to_learning_markdown(self, query: str, context: Dict[str, str]) -> str:
        """Render a learning-path response."""
        path = self.brain.build_learning_path(query, context)
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
