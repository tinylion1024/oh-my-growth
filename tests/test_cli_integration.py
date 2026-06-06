#!/usr/bin/env python3

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "scripts/cli.py", *args],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_assess_example_is_actionable():
    result = run_cli(
        "assess",
        "SaaS产品如何获取首批1000用户",
        "--industry",
        "saas",
        "--stage",
        "0-1",
        "--problem",
        "acquisition",
    )

    assert result.returncode == 0, result.stderr
    assert "清晰度评分:" in result.stdout
    assert "状态: 信息不足" not in result.stdout
    assert "【一句话判断】" in result.stdout
    assert "【优先级排序】" in result.stdout
    assert "【两周实验】" in result.stdout


def test_diagnose_outputs_strategy_brain_sections():
    result = run_cli(
        "diagnose",
        "如何提升月活跃用户留存率",
        "--industry",
        "content",
        "--problem",
        "retention",
    )

    assert result.returncode == 0, result.stderr
    assert "增长策略外脑" in result.stdout
    assert "【核心矛盾】" in result.stdout
    assert "【建议先别做】" in result.stdout
    assert "【两周实验】" in result.stdout


def test_diagnose_executive_view_is_compact():
    result = run_cli(
        "diagnose",
        "SaaS产品如何获取首批1000用户",
        "--industry",
        "saas",
        "--stage",
        "0-1",
        "--problem",
        "acquisition",
        "--view",
        "executive",
    )

    assert result.returncode == 0, result.stderr
    assert "董事会/负责人摘要" in result.stdout
    assert "这周拍板" in result.stdout
    assert "优先级" in result.stdout


def test_diagnose_report_view_can_be_validated():
    report = run_cli(
        "diagnose",
        "我们要不要做邀请裂变",
        "--industry",
        "saas",
        "--stage",
        "1-10",
        "--problem",
        "referral",
        "--view",
        "report",
    )

    assert report.returncode == 0, report.stderr
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        suffix=".md",
        dir=ROOT_DIR / "tests",
        delete=False,
    ) as handle:
        handle.write(report.stdout)
        report_path = Path(handle.name)

    validated = run_cli("validate", str(report_path))
    report_path.unlink(missing_ok=True)

    assert validated.returncode == 0, validated.stdout
    assert "✅ 通过" in validated.stdout


def test_match_command_returns_case_matches():
    result = run_cli("match", "教育产品如何做裂变", "--problem", "referral", "--limit", "3")

    assert result.returncode == 0, result.stderr
    assert "案例匹配模式" in result.stdout
    assert "匹配案例" in result.stdout
    assert "Dropbox" in result.stdout or "裂变" in result.stdout


def test_cold_start_shortcut_sets_external_brain_context():
    result = run_cli("cold-start", "AI写作SaaS如何拿到前100个种子用户", "--industry", "saas")

    assert result.returncode == 0, result.stderr
    assert "冷启动外脑" in result.stdout
    assert "阶段=冷启动" in result.stdout
    assert "问题=获客" in result.stdout


def test_structured_context_is_reflected_in_json_view():
    result = run_cli(
        "retention",
        "如何提升月活跃用户留存率",
        "--industry",
        "content",
        "--context-json",
        '{"goal":"提升30日留存","metric":"30日留存率","budget":"10万元","team":"产品1+工程2+运营1","history":"做过Push召回但效果一般"}',
        "--view",
        "json",
    )

    assert result.returncode == 0, result.stderr
    assert '"goal": "提升30日留存"' in result.stdout
    assert '"metric": "30日留存率"' in result.stdout or '"30日留存率 (observed)"' in result.stdout
    assert '"resources": "产品1+工程2+运营1"' in result.stdout


def test_validate_reads_file_content():
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        suffix=".md",
        dir=ROOT_DIR / "tests",
        delete=False,
    ) as handle:
        handle.write(
            "\n".join(
                [
                    "## 先看结论",
                    "目标：提升留存 理由：案例支撑 置信度：中 行动：先做实验",
                    "## 先把现状说清楚",
                    "目标：提升留存 阶段：增长期 约束：预算有限 资源：3人团队",
                    "## 现状够不够清楚",
                    "评分：75 诊断：可以开始",
                    "## 判断过程",
                    "方案：A/B测试 对比：邮件和Push 评分：70",
                    "## 推荐方案",
                    "方案：连续使用激励 理由：高频触达 路径：两周试点",
                    "## 时间、精力、资源应该怎么重新分配",
                    "主攻：留存 次要：获客 监控：7日留存",
                    "## 接下来怎么做",
                    "行动：上线实验 负责人：增长经理 期限：两周",
                    "## 做完以后可能怎样",
                    "概率：60% 假设：激励有效 证据：历史案例 (observed)",
                    "## 什么时候回头看",
                    "时间：两周后 信号：留存提升 证据：实验数据 (estimated)",
                    "## 注意事项",
                    "警告：避免过度激励 不确定：长期效果 (assumed)",
                ]
            )
        )
        report_path = Path(handle.name)

    result = run_cli("validate", str(report_path))
    report_path.unlink(missing_ok=True)

    assert result.returncode == 0, result.stdout
    assert "✅ 通过" in result.stdout
