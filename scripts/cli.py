#!/usr/bin/env python3
"""
Growth Master CLI
命令行接口，支持独立使用
"""

import argparse
import json
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_retriever import KnowledgeRetriever
from assess_clarity import assess_clarity


def cmd_assess(args):
    """评估增长机会"""
    print("=" * 60)
    print("Growth Master - 评估模式")
    print("=" * 60)

    # 解析上下文
    context = {}
    if args.industry:
        context['industry'] = args.industry
    if args.stage:
        context['stage'] = args.stage
    if args.problem:
        context['problem_type'] = args.problem

    # 评估清晰度
    clarity_result = assess_clarity(context)
    clarity_score = clarity_result.total_score if hasattr(clarity_result, 'total_score') else 0
    print(f"\n清晰度评分: {clarity_score}/100")

    if clarity_score < 55:
        print("状态: 信息不足，建议补充更多信息")
        print("\n建议补充:")
        print("  - 明确的目标和成功标准")
        print("  - 当前阶段和用户规模")
        print("  - 关键约束条件")
        return

    # 知识检索
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(args.query, context)

    print("\n--- 相关案例 ---")
    for case in results['cases'][:3]:
        print(f"  • {case['name']} (证据等级: {case['metadata']['evidence_tier']})")
        if case['highlights']:
            print(f"    关键点: {case['highlights'][0][:50]}...")

    print("\n--- 推荐玩法 ---")
    for weapon in results['weapons'][:3]:
        print(f"  • {weapon['name']} (难度: {weapon['metadata']['effort']}, 影响: {weapon['metadata']['impact']})")

    if results['theories']:
        print("\n--- 相关理论 ---")
        for theory in results['theories'][:2]:
            print(f"  • {theory['name']}")

    print("\n" + "=" * 60)
    print("建议: 基于以上分析，建议进一步设计详细方案")
    print("=" * 60)


def cmd_design(args):
    """设计增长策略"""
    print("=" * 60)
    print("Growth Master - 设计模式")
    print("=" * 60)

    context = {
        'industry': args.industry,
        'stage': args.stage,
        'problem_type': args.problem
    }

    # 知识检索
    retriever = KnowledgeRetriever()
    results = retriever.retrieve(args.query, context)

    print(f"\n问题: {args.query}")
    print(f"上下文: 行业={args.industry}, 阶段={args.stage}, 问题类型={args.problem}")

    print("\n=== 策略设计 ===\n")

    # 推荐玩法组合
    print("【推荐玩法组合】")
    if results['weapons']:
        for i, weapon in enumerate(results['weapons'][:3], 1):
            print(f"  {i}. {weapon['name']}")
            print(f"     难度: {weapon['metadata']['effort']} | 影响: {weapon['metadata']['impact']}")
            print(f"     描述: {weapon['highlights'][0] if weapon['highlights'] else 'N/A'}")
    else:
        print("  未找到匹配玩法，建议提供更多上下文")

    # 案例参考
    print("\n【案例参考】")
    if results['cases']:
        for case in results['cases'][:2]:
            print(f"  • {case['name']}")
            print(f"    证据等级: {case['metadata']['evidence_tier']}")
            if case['highlights']:
                print(f"    可复制点: {case['highlights'][0][:40]}...")

    # 实施建议
    print("\n【实施建议】")
    print("  1. 优先选择低难度高影响的玩法")
    print("  2. 设计小规模实验验证效果")
    print("  3. 设置明确的成功指标和监控")

    print("\n" + "=" * 60)


def cmd_search(args):
    """搜索知识库"""
    retriever = KnowledgeRetriever()

    context = {
        'industry': args.industry,
        'problem_type': args.problem,
        'stage': args.stage
    }

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


def cmd_validate(args):
    """验证报告"""
    from verify_report import verify_report

    result = verify_report(args.file)
    print(f"\n报告: {args.file}")
    print(f"评分: {result.score}/100")
    print(f"状态: {'✅ 通过' if result.valid else '❌ 未通过'}")

    if result.issues:
        print(f"\n问题 ({len(result.issues)} 个):")
        for issue in result.issues[:5]:
            print(f"  [{issue['severity']}] {issue['section']}: {issue['message']}")


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

  # 搜索知识库
  growth search "裂变机制" --limit 10

  # 验证报告
  growth validate report.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # assess 命令
    assess_parser = subparsers.add_parser('assess', help='评估增长机会')
    assess_parser.add_argument('query', help='问题描述')
    assess_parser.add_argument('--industry', help='行业类型')
    assess_parser.add_argument('--stage', help='业务阶段 (0-1, 1-10, 10-100)')
    assess_parser.add_argument('--problem', help='问题类型 (acquisition, retention, monetization, referral)')
    assess_parser.set_defaults(func=cmd_assess)

    # design 命令
    design_parser = subparsers.add_parser('design', help='设计增长策略')
    design_parser.add_argument('query', help='问题描述')
    design_parser.add_argument('--industry', default='', help='行业类型')
    design_parser.add_argument('--stage', default='', help='业务阶段')
    design_parser.add_argument('--problem', default='', help='问题类型')
    design_parser.set_defaults(func=cmd_design)

    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索知识库')
    search_parser.add_argument('query', help='搜索查询')
    search_parser.add_argument('--industry', default='', help='行业类型')
    search_parser.add_argument('--stage', default='', help='业务阶段')
    search_parser.add_argument('--problem', default='', help='问题类型')
    search_parser.add_argument('--limit', type=int, default=5, help='返回结果数量')
    search_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    search_parser.set_defaults(func=cmd_search)

    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证报告')
    validate_parser.add_argument('file', help='报告文件路径')
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
