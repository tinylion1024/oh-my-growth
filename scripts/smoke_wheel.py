#!/usr/bin/env python3
"""Smoke test the installed wheel from outside the source tree."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence


ROOT_DIR = Path(__file__).resolve().parent.parent


def run(command: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def require_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode == 0:
        return
    print(f"❌ {label} failed")
    print(result.stdout)
    print(result.stderr)
    raise SystemExit(result.returncode)


def require_contains(output: str, expected: str, label: str) -> None:
    if expected in output:
        return
    print(f"❌ {label} missing `{expected}`")
    print(output)
    raise SystemExit(1)


def venv_bin(venv_dir: Path, executable: str) -> Path:
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" and not executable.endswith(".exe") else ""
    return venv_dir / bin_dir / f"{executable}{suffix}"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="omg-wheel-smoke-") as tmp:
        work_dir = Path(tmp)
        venv_dir = work_dir / "venv"

        result = run([sys.executable, "-m", "venv", str(venv_dir)], cwd=work_dir)
        require_success(result, "create venv")

        python_bin = venv_bin(venv_dir, "python")
        growth_bin = venv_bin(venv_dir, "growth")

        result = run([str(python_bin), "-m", "pip", "install", str(ROOT_DIR), "--no-deps"], cwd=work_dir)
        require_success(result, "pip install")

        import_check = """
import scripts.cli
import scripts.retriever
import scripts.strategy
from scripts.knowledge_retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()
results = retriever.retrieve('GEO LLM 搜索曝光 引用率', {'industry': 'saas', 'problem_type': 'acquisition'})
assert results['method_packs'], 'method packs were not loaded from package data'
assert results['cases'], 'cases were not loaded from package data'
print('imports and knowledge data ok')
"""
        result = run([str(python_bin), "-c", import_check], cwd=work_dir)
        require_success(result, "package import and knowledge load")

        result = run(
            [
                str(growth_bin),
                "diagnose",
                "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率",
                "--industry",
                "saas",
                "--stage",
                "10-100",
                "--problem",
                "acquisition",
            ],
            cwd=work_dir,
        )
        require_success(result, "growth diagnose")
        require_contains(result.stdout, "GEO/LLM 发现系统", "growth diagnose")
        require_contains(result.stdout, "推荐增长操作系统", "growth diagnose")
        require_contains(result.stdout, "参考案例", "growth diagnose")

    print("✅ Wheel smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
