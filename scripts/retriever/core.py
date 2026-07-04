"""Knowledge Retriever core module.

This module contains the main KnowledgeRetriever class that coordinates
knowledge retrieval operations.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from .types import (
    BASE_DIR,
    normalize_stage,
    SearchResult,
)
from .search import (
    search_cases,
    search_weapons,
    search_theories,
    search_failures,
    search_method_packs,
)


class KnowledgeRetriever:
    """知识检索器"""

    def __init__(self):
        self.cases = []
        self.weapons = []
        self.theories = []
        self.failures = []
        self.method_packs = []
        self.weapon_categories: Dict[str, str] = {}
        self.weapon_details: Dict[str, Dict[str, str]] = {}
        self._load_indexes()

    def _load_indexes(self):
        """加载索引文件"""
        indexes_dir = BASE_DIR / "knowledge" / "indexes"

        # 加载案例索引
        cases_path = indexes_dir / "cases-index.json"
        if cases_path.exists():
            with open(cases_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cases = data.get('cases', [])

        # 加载玩法索引
        weapons_path = indexes_dir / "weapons-index.json"
        if weapons_path.exists():
            with open(weapons_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.weapons = data.get('weapons', [])
                self.weapon_categories = {
                    item.get("id", ""): item.get("name", "")
                    for item in data.get("categories", [])
                }

        # 加载理论索引
        theories_path = indexes_dir / "theories-index.json"
        if theories_path.exists():
            with open(theories_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.theories = data.get('theories', [])

        failures_path = indexes_dir / "failures-index.json"
        if failures_path.exists():
            with open(failures_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.failures = data.get('failures', [])

        method_packs_path = indexes_dir / "method-packs-index.json"
        if method_packs_path.exists():
            with open(method_packs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.method_packs = data.get('method_packs', [])

        self.weapon_details = self._load_weapon_details()

    def _load_weapon_details(self) -> Dict[str, Dict[str, str]]:
        """Load richer weapon metadata from the markdown source files."""
        details: Dict[str, Dict[str, str]] = {}
        for path in (BASE_DIR / "knowledge" / "weapons").glob("**/weapons/*.md"):
            content = path.read_text(encoding="utf-8")
            front_matter = self._parse_front_matter(content)
            weapon_id = str(front_matter.get("id", "")).strip()
            if not weapon_id:
                continue
            details[weapon_id] = {
                "description": front_matter.get("description", "").strip(),
                "category_label": front_matter.get("category", "").strip(),
                "file": str(path.relative_to(BASE_DIR)),
            }
        return details

    def _parse_front_matter(self, content: str) -> Dict[str, str]:
        """Parse the simple front matter used by knowledge markdown files."""
        if not content.startswith("---"):
            return {}

        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            return {}

        data: Dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        return data

    def search_cases(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[SearchResult]:
        """搜索案例"""
        return search_cases(self.cases, query, context, limit)

    def search_weapons(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[SearchResult]:
        """搜索玩法"""
        return search_weapons(
            self.weapons, self.weapon_categories, self.weapon_details,
            query, context, limit
        )

    def search_theories(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 3
    ) -> List[SearchResult]:
        """搜索理论"""
        return search_theories(self.theories, query, context, limit)

    def search_failures(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 2
    ) -> List[SearchResult]:
        """Search failure modes and anti-patterns."""
        return search_failures(self.failures, query, context, limit)

    def search_method_packs(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 3
    ) -> List[SearchResult]:
        """Search absorbed marketing-growth method packs."""
        return search_method_packs(self.method_packs, query, context, limit)

    def retrieve(
        self,
        query: str,
        context: Optional[Dict] = None,
        case_limit: int = 5,
        weapon_limit: int = 5,
        theory_limit: int = 3,
        failure_limit: int = 2,
        method_pack_limit: int = 3
    ) -> Dict:
        """综合检索"""
        return {
            'cases': [
                {
                    'id': r.id,
                    'name': r.name,
                    'score': r.score,
                    'highlights': r.highlights,
                    'metadata': r.metadata
                }
                for r in self.search_cases(query, context, case_limit)
            ],
            'weapons': [
                {
                    'id': r.id,
                    'name': r.name,
                    'score': r.score,
                    'highlights': r.highlights,
                    'metadata': r.metadata
                }
                for r in self.search_weapons(query, context, weapon_limit)
            ],
            'theories': [
                {
                    'id': r.id,
                    'name': r.name,
                    'score': r.score,
                    'highlights': r.highlights,
                    'metadata': r.metadata
                }
                for r in self.search_theories(query, context, theory_limit)
            ],
            'failures': [
                {
                    'id': r.id,
                    'name': r.name,
                    'score': r.score,
                    'highlights': r.highlights,
                    'metadata': r.metadata
                }
                for r in self.search_failures(query, context, failure_limit)
            ],
            'method_packs': [
                {
                    'id': r.id,
                    'name': r.name,
                    'score': r.score,
                    'highlights': r.highlights,
                    'metadata': r.metadata
                }
                for r in self.search_method_packs(query, context, method_pack_limit)
            ],
        }
