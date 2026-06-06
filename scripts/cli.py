#!/usr/bin/env python3
"""
Growth Master CLI
命令行接口，支持独立使用
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Union

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_retriever import KnowledgeRetriever
from assess_clarity import assess_clarity
from strategy_brain import StrategyBrain


def load_context_overrides(args) -> Dict[str, str]:
    """Load structured context overrides from JSON string or file."""
    merged: Dict[str, str] = {}
    if getattr(args, "context_json", ""):
        payload = json.loads(args.context_json)
        if not isinstance(payload, dict):
            raise ValueError("--context-json must decode to a JSON object")
        merged.update({str(key): str(value) for key, value in payload.items() if value is not None})

    if getattr(args, "context_file", ""):
        payload = json.loads(Path(args.context_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("--context-file must contain a JSON object")
        merged.update({str(key): str(value) for key, value in payload.items() if value is not None})

    return merged


def build_context(args) -> Dict[str, str]:
    """Build a normalized retrieval context from CLI arguments."""
    context = {}
    for source, target in [
        ("industry", "industry"),
        ("stage", "stage"),
        ("problem", "problem_type"),
        ("goal", "goal"),
        ("metric", "metric"),
        ("budget", "budget"),
        ("team", "team"),
        ("constraints", "constraints"),
        ("stakeholder", "stakeholder"),
        ("history", "history"),
    ]:
        value = getattr(args, source, "")
        if value:
            context[target] = value
    context.update(load_context_overrides(args))
    return context


def build_clarity_input(query: str, context: Dict[str, str]) -> Dict:
    """Translate lightweight CLI inputs into the clarity assessment schema."""
    has_basic_context = bool(context.get("industry") or context.get("problem_type"))
    dimensions: Dict[str, Dict[str, Union[List[str], int]]] = {}

    if query:
        goal_score = 80 if len(query) >= 8 else 60
        dimensions["goal_success"] = {
            "score": goal_score,
            "evidence": [f"问题描述: {query}"],
        }

    fact_evidence = [
        f"行业: {context['industry']}" for _ in [0] if context.get("industry")
    ] + [
        f"问题类型: {context['problem_type']}" for _ in [0] if context.get("problem_type")
    ] + [
        f"目标: {context['goal']}" for _ in [0] if context.get("goal")
    ] + [
        f"指标: {context['metric']}" for _ in [0] if context.get("metric")
    ]
    if fact_evidence or query:
        dimensions["facts_evidence"] = {
            "score": min(90, 50 + len(fact_evidence) * 15 + (10 if has_basic_context else 0)),
            "evidence": fact_evidence or [f"问题描述: {query}"],
        }

    if context.get("stage"):
        dimensions["stage"] = {
            "score": 80,
            "evidence": [f"业务阶段: {context['stage']}"],
        }

    resource_evidence = [
        f"预算: {context['budget']}" for _ in [0] if context.get("budget")
    ] + [
        f"团队: {context['team']}" for _ in [0] if context.get("team")
    ]
    if resource_evidence or has_basic_context:
        dimensions["scarce_resources"] = {
            "score": 70 if resource_evidence else 50,
            "evidence": resource_evidence or ["需进一步确认预算和团队配置"],
        }

    constraint_evidence = [
        f"约束: {context['constraints']}" for _ in [0] if context.get("constraints")
    ]
    if constraint_evidence or has_basic_context:
        dimensions["hard_constraints"] = {
            "score": 70 if constraint_evidence else 40,
            "evidence": constraint_evidence or ["默认存在时间/预算/资源约束，待补充"],
        }

    stakeholder_evidence = [
        f"关键相关方: {context['stakeholder']}" for _ in [0] if context.get("stakeholder")
    ]
    if stakeholder_evidence or has_basic_context:
        dimensions["stakeholders"] = {
            "score": 70 if stakeholder_evidence else 30,
            "evidence": stakeholder_evidence or ["默认存在决策方，待补充"],
        }

    history_evidence = [
        f"历史尝试: {context['history']}" for _ in [0] if context.get("history")
    ]
    if history_evidence or has_basic_context:
        dimensions["repeated_patterns"] = {
            "score": 70 if history_evidence else 30,
            "evidence": history_evidence or ["历史尝试信息缺失"],
        }

    return {"dimensions": dimensions}


def print_recommendations(questions):
    """Render follow-up questions when clarity is not enough."""
    if not questions:
        return
    print("\n建议补充:")
    for question in questions[:5]:
        print(f"  - [{question['dimension_name']}] {question['question']}")


def render_strategy_brain(title: str, analysis: Dict) -> None:
    """Render the strategy-brain output for operators."""
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f"\n上下文: {analysis['context_summary']}")

    print("\n【阶段判断】")
    print(f"  当前阶段: {analysis['stage_diagnosis']['current_stage']}")
    print(f"  主业务过程: {analysis['growth_process']['name']}")
    print(f"  北极星指标: {analysis['north_star']['metric']}")
    print(f"  约束线: {analysis['north_star']['guardrail']}")
    print(f"  用户旅程卡点: {analysis['journey_focus']['stage']} - {analysis['journey_focus']['focus']}")

    print("\n【一句话判断】")
    print(f"  {analysis['decision_line']}")

    print("\n【核心矛盾】")
    print(f"  {analysis['core_tension']}")

    print("\n【为什么现在做】")
    for reason in analysis["why_now"]:
        print(f"  • {reason}")

    print("\n【优先级排序】")
    for index, option in enumerate(analysis["priorities"], 1):
        print(f"  {index}. {option.name} ({option.category_name})")
        print(f"     得分: {option.score:.2f} | 难度: {option.effort} | 影响: {option.impact}")
        print(f"     为什么现在做: {option.why_now}")
        print(f"     主要风险: {option.key_risk}")

    print("\n【建议现在做】")
    for item in analysis["do_now"]:
        print(f"  • {item}")

    print("\n【建议先别做】")
    for item in analysis["avoid_now"]:
        print(f"  • {item}")

    print("\n【两周实验】")
    print(f"  假设: {analysis['experiment']['hypothesis']}")
    print("  步骤:")
    for step in analysis["experiment"]["steps"]:
        print(f"    - {step}")
    print("  成功信号:")
    for signal in analysis["experiment"]["success_signals"]:
        print(f"    - {signal}")
    print("  停止信号:")
    for signal in analysis["experiment"]["stop_signals"]:
        print(f"    - {signal}")

    if analysis["reference_cases"]:
        print("\n【参考案例】")
        for case in analysis["reference_cases"]:
            print(f"  • {case['name']} (证据等级: {case['metadata']['evidence_tier']})")

    if analysis["reference_theories"]:
        print("\n【理论支撑】")
        for theory in analysis["reference_theories"]:
            print(f"  • {theory['name']}")

    print("\n【数据与归因要求】")
    for item in analysis["measurement_notes"]:
        print(f"  • {item}")

    if analysis["missing_info"]:
        print("\n【还缺哪些信息】")
        for item in analysis["missing_info"]:
            print(f"  • {item}")

    print("\n" + "=" * 60)
    print(
        f"置信度: {analysis['confidence_label']} ({analysis['confidence_score']:.2f}) | "
        f"建议动作: {analysis['decision_text']['action']}"
    )
    print("=" * 60)


def render_strategy_output(title: str, analysis: Dict, view: str, clarity_score: float = 0.0, clarity_result: Dict = None) -> None:
    """Dispatch between operator/executive/report/json views."""
    if view == "json":
        print(StrategyBrain().to_json(analysis))
        return
    if view == "executive":
        print(StrategyBrain().to_executive_markdown(analysis))
        return
    if view == "report":
        clarity_level = clarity_result.level if clarity_result else "workable"
        can_proceed = clarity_result.can_proceed if clarity_result else True
        print(StrategyBrain().to_report_markdown(analysis, clarity_score, clarity_level, can_proceed))
        return
    render_strategy_brain(title, analysis)


def add_common_strategy_arguments(parser) -> None:
    """Attach shared strategy-brain arguments to a parser."""
    parser.add_argument('--industry', default='', help='行业类型')
    parser.add_argument('--stage', default='', help='业务阶段')
    parser.add_argument('--problem', default='', help='问题类型')
    parser.add_argument('--goal', default='', help='目标描述')
    parser.add_argument('--metric', default='', help='目标指标')
    parser.add_argument('--budget', default='', help='预算约束')
    parser.add_argument('--team', default='', help='团队约束')
    parser.add_argument('--constraints', default='', help='关键约束')
    parser.add_argument('--stakeholder', default='', help='关键相关方')
    parser.add_argument('--history', default='', help='历史尝试')
    parser.add_argument('--context-json', default='', help='补充结构化上下文 JSON 字符串')
    parser.add_argument('--context-file', default='', help='补充结构化上下文 JSON 文件')
    parser.add_argument(
        '--view',
        default='operator',
        choices=['operator', 'executive', 'report', 'json'],
        help='输出视图：执行版/负责人摘要/报告版/JSON',
    )


def cmd_assess(args):
    """评估增长机会"""
    context = build_context(args)

    clarity_result = assess_clarity(build_clarity_input(args.query, context))
    clarity_score = clarity_result.total_score if hasattr(clarity_result, 'total_score') else 0
    print("=" * 60)
    print("Growth Master - 评估模式")
    print("=" * 60)
    print(f"\n清晰度评分: {clarity_score}/100")

    if clarity_score < 55:
        print("状态: 信息不足，建议补充更多信息")
        print_recommendations(clarity_result.follow_up_questions)
        return 0

    analysis = StrategyBrain().analyze(args.query, context, mode="assess")
    render_strategy_output("Growth Master - 策略外脑评估", analysis, args.view, clarity_score, clarity_result)
    return 0


def cmd_design(args):
    """设计增长策略"""
    context = build_context(args)
    analysis = StrategyBrain().analyze(args.query, context, mode="design")
    render_strategy_output("Growth Master - 策略设计外脑", analysis, args.view)
    return 0


def cmd_diagnose(args):
    """完整的策略外脑诊断。"""
    context = build_context(args)
    clarity_result = assess_clarity(build_clarity_input(args.query, context))
    analysis = StrategyBrain().analyze(args.query, context, mode="diagnose")
    render_strategy_output(
        "Growth Master - 增长策略外脑",
        analysis,
        args.view,
        clarity_result.total_score,
        clarity_result,
    )
    return 0


def cmd_search(args):
    """搜索知识库"""
    retriever = KnowledgeRetriever()
    context = build_context(args)

    results = retriever.retrieve(
        args.query,
        context,
        case_limit=args.limit,
        weapon_limit=args.limit,
        theory_limit=args.limit // 2
    )

    output = {
        'query': args.query,
        'context': context,
        'results': results
    }

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n搜索: {args.query}")
        print("-" * 40)

        print(f"\n案例 ({len(results['cases'])} 个):")
        for case in results['cases']:
            print(f"  • {case['name']} (分数: {case['score']:.2f})")

        print(f"\n玩法 ({len(results['weapons'])} 个):")
        for weapon in results['weapons']:
            print(f"  • {weapon['name']} (分数: {weapon['score']:.2f})")

        print(f"\n理论 ({len(results['theories'])} 个):")
        for theory in results['theories']:
            print(f"  • {theory['name']}")
    return 0


def cmd_match(args):
    """优先匹配最相关案例。"""
    retriever = KnowledgeRetriever()
    context = build_context(args)
    results = retriever.retrieve(
        args.query,
        context,
        case_limit=args.limit,
        weapon_limit=max(1, min(args.limit, 3)),
        theory_limit=max(1, args.limit // 2),
    )

    print("=" * 60)
    print("Growth Master - 案例匹配模式")
    print("=" * 60)
    print(f"\n问题: {args.query}")

    print("\n【匹配案例】")
    for case in results["cases"]:
        print(f"  • {case['name']} (相似度: {case['score']:.2f}, 证据等级: {case['metadata']['evidence_tier']})")
        if case["highlights"]:
            print(f"    可借鉴: {case['highlights'][0][:50]}")

    if results["weapons"]:
        print("\n【可搭配玩法】")
        for weapon in results["weapons"][:3]:
            print(f"  • {weapon['name']} ({weapon['metadata'].get('category_name') or weapon['metadata']['category']})")

    if results["theories"]:
        print("\n【相关理论】")
        for theory in results["theories"][:2]:
            print(f"  • {theory['name']}")

    print("\n" + "=" * 60)
    return 0


def cmd_scenario(args):
    """Role/scenario-oriented shortcut for growth operators."""
    scenario_defaults = {
        "cold-start": {"problem": "acquisition", "stage": args.stage or "0-1", "title": "Growth Master - 冷启动外脑"},
        "retention": {"problem": "retention", "stage": args.stage or "1-10", "title": "Growth Master - 留存外脑"},
        "monetization": {"problem": "monetization", "stage": args.stage or "1-10", "title": "Growth Master - 变现外脑"},
        "referral": {"problem": "referral", "stage": args.stage or "1-10", "title": "Growth Master - 裂变外脑"},
    }
    defaults = scenario_defaults[args.command]
    if not getattr(args, "problem", ""):
        args.problem = defaults["problem"]
    if not getattr(args, "stage", ""):
        args.stage = defaults["stage"]

    context = build_context(args)
    clarity_result = assess_clarity(build_clarity_input(args.query, context))
    analysis = StrategyBrain().analyze(args.query, context, mode=args.command)
    render_strategy_output(defaults["title"], analysis, args.view, clarity_result.total_score, clarity_result)
    return 0


def cmd_validate(args):
    """验证报告"""
    from verify_report import verify_report

    report_path = Path(args.file)
    if not report_path.exists():
        print(f"文件不存在: {args.file}", file=sys.stderr)
        return 1

    result = verify_report(report_path.read_text(encoding="utf-8"))
    print(f"\n报告: {args.file}")
    print(f"评分: {result.score}/100")
    print(f"状态: {'✅ 通过' if result.valid else '❌ 未通过'}")

    if result.issues:
        print(f"\n问题 ({len(result.issues)} 个):")
        for issue in result.issues[:5]:
            print(f"  [{issue['severity']}] {issue['section']}: {issue['message']}")
    return 0 if result.valid else 1


def main():
    parser = argparse.ArgumentParser(
        description="Growth Master CLI - 智能增长顾问命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 评估增长机会
  growth assess "SaaS产品如何获取首批用户" --industry saas --stage 0-1

  # 设计增长策略
  growth design "如何提升用户留存" --industry education --problem retention

  # 外脑式诊断
  growth diagnose "SaaS产品如何获取首批1000用户" --industry saas --stage 0-1

  # 搜索知识库
  growth search "裂变机制" --limit 10

  # 匹配相关案例
  growth match "教育产品如何做裂变" --problem referral --limit 5

  # 验证报告
  growth validate report.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # assess 命令
    assess_parser = subparsers.add_parser('assess', help='评估增长机会')
    assess_parser.add_argument('query', help='问题描述')
    add_common_strategy_arguments(assess_parser)
    assess_parser.set_defaults(func=cmd_assess)

    # design 命令
    design_parser = subparsers.add_parser('design', help='设计增长策略')
    design_parser.add_argument('query', help='问题描述')
    add_common_strategy_arguments(design_parser)
    design_parser.set_defaults(func=cmd_design)

    # diagnose 命令
    diagnose_parser = subparsers.add_parser('diagnose', help='生成完整的策略外脑诊断')
    diagnose_parser.add_argument('query', help='问题描述')
    add_common_strategy_arguments(diagnose_parser)
    diagnose_parser.set_defaults(func=cmd_diagnose)

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索知识库')
    search_parser.add_argument('query', help='搜索查询')
    search_parser.add_argument('--industry', default='', help='行业类型')
    search_parser.add_argument('--stage', default='', help='业务阶段')
    search_parser.add_argument('--problem', default='', help='问题类型')
    search_parser.add_argument('--limit', type=int, default=5, help='返回结果数量')
    search_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    search_parser.set_defaults(func=cmd_search)

    # match 命令
    match_parser = subparsers.add_parser('match', help='匹配相似案例')
    match_parser.add_argument('query', help='问题描述')
    match_parser.add_argument('--industry', default='', help='行业类型')
    match_parser.add_argument('--stage', default='', help='业务阶段')
    match_parser.add_argument('--problem', default='', help='问题类型')
    match_parser.add_argument('--limit', type=int, default=5, help='返回案例数量')
    match_parser.set_defaults(func=cmd_match)

    # scenario shortcut commands
    for command_name, help_text in [
        ('cold-start', '冷启动策略外脑'),
        ('retention', '留存策略外脑'),
        ('monetization', '变现策略外脑'),
        ('referral', '裂变策略外脑'),
    ]:
        scenario_parser = subparsers.add_parser(command_name, help=help_text)
        scenario_parser.add_argument('query', help='问题描述')
        add_common_strategy_arguments(scenario_parser)
        scenario_parser.set_defaults(func=cmd_scenario)

    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证报告')
    validate_parser.add_argument('file', help='报告文件路径')
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
