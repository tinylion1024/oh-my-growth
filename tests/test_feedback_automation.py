#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


def run_script(script: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=cwd or ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_aggregate_feedback_generates_summary_reports():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        feedback_dir = tmp_path / "feedback"
        logs_dir = feedback_dir / "logs"
        analysis_dir = feedback_dir / "analysis"
        logs_dir.mkdir(parents=True)

        entries = [
            {
                "feedback_id": "fb-001",
                "timestamp": "2024-01-15T10:30:00Z",
                "session_id": "s-1",
                "input_summary": {"mode": "Fast Scan", "problem_type": "acquisition"},
                "rating": {"stars": 5, "usefulness": "非常有帮助"},
                "qualitative": {
                    "most_helpful": "案例很准",
                    "missing_info": "希望补充执行步骤",
                    "will_act": True,
                    "suggestions": "增加 ROI 计算模板",
                },
                "case_feedback": {"relevant": True, "want_more": False},
                "output_metadata": {"agents_used": ["Lead", "ROI"], "confidence": "High", "output_length": 1200},
            },
            {
                "feedback_id": "fb-002",
                "timestamp": "2024-01-16T10:30:00Z",
                "session_id": "s-2",
                "input_summary": {"mode": "Decision BRD", "problem_type": "monetization"},
                "rating": {"stars": 3, "usefulness": "一般"},
                "qualitative": {
                    "most_helpful": "判断逻辑清晰",
                    "missing_info": "太长了",
                    "will_act": False,
                    "suggestions": "缩短输出并突出结论",
                },
                "case_feedback": {"relevant": True, "want_more": True},
                "output_metadata": {"agents_used": ["Lead", "Growth", "ROI"], "confidence": "Medium", "output_length": 2200},
            },
            {
                "feedback_id": "fb-003",
                "timestamp": "2024-01-17T10:30:00Z",
                "session_id": "s-3",
                "input_summary": {"mode": "Weekly", "problem_type": "retention"},
                "rating": {"stars": 4, "usefulness": "有帮助"},
                "qualitative": {
                    "most_helpful": "本周不做什么很清楚",
                    "missing_info": "需要更多留存指标",
                    "will_act": True,
                    "suggestions": "补充留存指标与复盘信号",
                },
                "case_feedback": {"relevant": True, "want_more": False},
                "output_metadata": {"agents_used": ["Lead", "Skeptic"], "confidence": "Medium", "output_length": 1600},
            },
        ]

        for idx, entry in enumerate(entries, start=1):
            (logs_dir / f"{idx:02d}.json").write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")

        result = run_script(
            "scripts/aggregate_feedback.py",
            "--feedback-dir",
            str(feedback_dir),
            "--output-dir",
            str(analysis_dir),
            "--week",
            "2024-W03",
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert "feedback aggregated" in result.stdout.lower()

        weekly_report = analysis_dir / "weekly-report-2024-W03.md"
        patterns_report = analysis_dir / "patterns.md"
        assert weekly_report.exists()
        assert patterns_report.exists()

        weekly = weekly_report.read_text(encoding="utf-8")
        assert "Total feedback: 3" in weekly
        assert "Average stars: 4.0" in weekly
        assert "Fast Scan" in weekly
        assert "Decision BRD" in weekly
        assert "ROI 计算模板" in weekly or "ROI计算模板" in weekly

        patterns = patterns_report.read_text(encoding="utf-8")
        assert "增加 ROI 计算模板" in patterns
        assert "缩短输出并突出结论" in patterns


def test_decision_tracking_reports_pending_items():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        decisions_dir = tmp_path / "decisions"
        report_dir = tmp_path / "reports"
        (decisions_dir / "2024" / "01").mkdir(parents=True)
        (decisions_dir / "2024" / "04").mkdir(parents=True)

        pending_decision = decisions_dir / "2024" / "01" / "decision-20240101-001.md"
        tracked_decision = decisions_dir / "2024" / "04" / "decision-20240401-001.md"
        tracked_followup = decisions_dir / "2024" / "04" / "decision-20240401-001-tracking.md"

        pending_decision.write_text(
            "---\n"
            "decision_id: decision-20240101-001\n"
            "date: 2024-01-01\n"
            "status: completed\n"
            "tracking: pending\n"
            "---\n\n"
            "# 决策记录\n",
            encoding="utf-8",
        )
        tracked_decision.write_text(
            "---\n"
            "decision_id: decision-20240401-001\n"
            "date: 2024-04-01\n"
            "status: completed\n"
            "tracking: done\n"
            "---\n\n"
            "# 决策记录\n",
            encoding="utf-8",
        )
        tracked_followup.write_text("# 决策追踪\n", encoding="utf-8")

        result = run_script(
            "scripts/decision_tracking.py",
            "--decisions-dir",
            str(decisions_dir),
            "--output-file",
            str(report_dir / "pending-tracking.md"),
            "--today",
            "2024-04-15",
            "--threshold-days",
            "30",
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert "pending tracking: 1" in result.stdout.lower()

        report = (report_dir / "pending-tracking.md").read_text(encoding="utf-8")
        assert "decision-20240101-001" in report
        assert "decision-20240401-001" not in report
        assert "Recommended next step" in report
