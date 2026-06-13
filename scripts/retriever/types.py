"""Knowledge retriever types and data structures.

This module contains dataclass definitions and constants for knowledge retrieval.
"""

from dataclasses import dataclass
from typing import Dict, List

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

# 阶段名称映射：CLI 输入 -> 索引内部格式
STAGE_ALIASES = {
    "10+": "10-100",
    "10-100": "10-100",
    "0-1": "0-1",
    "1-10": "1-10",
}


def normalize_stage(stage: str) -> str:
    """Normalize stage input to internal format."""
    return STAGE_ALIASES.get(stage, stage)


@dataclass
class SearchResult:
    """检索结果"""
    id: str
    name: str
    type: str  # case, weapon, theory
    score: float
    highlights: List[str]
    metadata: Dict
