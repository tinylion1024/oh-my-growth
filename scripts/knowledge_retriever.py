#!/usr/bin/env python3
"""Knowledge retrieval helpers for cases, weapons, and theories."""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

BASE_DIR = Path(__file__).parent.parent


@dataclass
class SearchResult:
    """检索结果"""
    id: str
    name: str
    type: str  # case, weapon, theory
    score: float
    highlights: List[str]
    metadata: Dict


class KnowledgeRetriever:
    """知识检索器"""

    def __init__(self):
        self.cases = []
        self.weapons = []
        self.theories = []
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

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower().replace("_", " ").replace("-", " ")).strip()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize English terms and Chinese phrases/bigrams for retrieval."""
        normalized = self._normalize_text(text)
        normalized = re.sub(r"[^0-9a-z\u4e00-\u9fff\s]", " ", normalized)

        tokens: List[str] = []
        tokens.extend(re.findall(r"[a-z0-9]+", normalized))

        for chunk in re.findall(r"[\u4e00-\u9fff]+", normalized):
            tokens.append(chunk)
            if len(chunk) == 1:
                continue
            for size in (2, 3):
                if len(chunk) < size:
                    continue
                for index in range(len(chunk) - size + 1):
                    tokens.append(chunk[index:index + size])

        # Preserve token order for substring scoring while removing duplicates.
        return list(dict.fromkeys(token for token in tokens if token))

    def _compute_similarity(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """Combine token overlap and substring matching for mixed CN/EN text."""
        if not query_tokens or not doc_tokens:
            return 0.0

        query_set = set(query_tokens)
        doc_set = set(doc_tokens)

        intersection = len(query_set & doc_set)
        union = len(query_set | doc_set)
        token_score = intersection / union if union else 0.0

        doc_text = " ".join(doc_tokens)
        substring_hits = 0
        for token in query_tokens:
            if len(token) < 2:
                continue
            if token in doc_text:
                substring_hits += 1

        substring_score = min(0.45, substring_hits * 0.08)
        return token_score + substring_score

    def _expand_query(self, query: str, context: Dict) -> List[str]:
        """Expand queries using lightweight domain synonyms."""
        expansions: List[str] = []

        industry_synonyms = {
            "saas": ["软件", "订阅", "b2b", "企业服务"],
            "ecommerce": ["电商", "购物", "零售", "交易", "平台"],
            "education": ["教育", "学习", "培训", "课程", "知识"],
            "fintech": ["金融", "支付", "理财", "信贷"],
            "social": ["社交", "社区", "好友", "互动", "关系"],
            "content": ["内容", "媒体", "视频", "文章", "信息"],
            "marketplace": ["平台", "双边市场", "供给", "商家"],
        }

        problem_synonyms = {
            "acquisition": ["获客", "增长", "拉新", "用户", "注册", "冷启动"],
            "retention": ["留存", "粘性", "活跃", "回访", "留存率", "复购"],
            "monetization": ["变现", "收入", "付费", "盈利", "商业化", "定价"],
            "referral": ["裂变", "传播", "分享", "邀请", "病毒", "推荐"],
            "activation": ["激活", "首购", "转化", "体验价值"],
        }

        category_keywords = {
            "cold-start": ["冷启动", "种子用户", "早期用户", "首批用户"],
            "viral-referral": ["裂变", "邀请", "推荐", "病毒", "分享"],
            "content-growth": ["内容", "seo", "教程", "newsletter", "案例研究"],
            "community": ["社区", "用户社群", "超级用户", "共创"],
            "plg": ["产品驱动增长", "plg", "freemium", "onboarding", "模板"],
            "retention": ["留存", "活跃", "召回", "复购", "习惯"],
            "monetization": ["变现", "付费", "定价", "upsell", "订阅"],
            "paid-ads": ["广告", "投放", "获客成本", "cac", "推广"],
            "brand": ["品牌", "pr", "创始人ip", "视觉"],
            "b2b-sales": ["销售", "线索", "demo", "客户成功", "外联"],
        }

        theory_keywords = {
            "growth-hacking": ["增长黑客", "实验", "aarrr", "ice"],
            "plg": ["产品驱动增长", "plg", "自传播", "自助体验"],
            "network-effects": ["网络效应", "双边市场", "临界质量"],
            "content-growth": ["内容增长", "内容营销", "seo", "入站"],
            "community-growth": ["社区增长", "超级用户", "共创"],
            "brand-growth": ["品牌增长", "品牌资产", "价值观"],
            "viral-growth": ["病毒增长", "裂变", "推荐", "分享"],
            "performance-marketing": ["效果营销", "投放", "广告"],
            "gamification": ["游戏化", "积分", "成就", "排行榜"],
            "flywheel": ["飞轮", "复利增长", "长期增长"],
            "business-models": ["商业模式", "变现", "付费", "定价"],
        }

        industry = context.get("industry", "").lower()
        problem = context.get("problem_type", "").lower()

        expansions.extend(industry_synonyms.get(industry, []))
        expansions.extend(problem_synonyms.get(problem, []))

        query_text = self._normalize_text(query)
        for category_id, keywords in category_keywords.items():
            if any(keyword in query_text for keyword in keywords):
                expansions.extend(keywords)
                expansions.append(category_id)

        for theory_id, keywords in theory_keywords.items():
            if any(keyword in query_text for keyword in keywords):
                expansions.extend(keywords)
                expansions.append(theory_id)

        return list(dict.fromkeys(expansions))

    def _build_query_tokens(self, query: str, context: Dict) -> List[str]:
        query_tokens = self._tokenize(query)
        expansions = self._expand_query(query, context)
        query_tokens.extend(self._tokenize(" ".join(expansions)))
        return list(dict.fromkeys(query_tokens))

    def _problem_to_categories(self, problem: str) -> Set[str]:
        mapping = {
            "acquisition": {"cold-start", "content-growth", "paid-ads", "plg"},
            "activation": {"plg", "community", "retention"},
            "retention": {"retention", "community", "gamification"},
            "monetization": {"monetization", "plg", "b2b-sales"},
            "referral": {"viral-referral", "community", "plg"},
        }
        return mapping.get(problem, set())

    def _problem_to_theories(self, problem: str) -> Set[str]:
        mapping = {
            "acquisition": {"growth-hacking", "content-growth", "plg"},
            "activation": {"growth-hacking", "plg", "gamification"},
            "retention": {"gamification", "flywheel", "community-growth"},
            "monetization": {"business-models", "plg"},
            "referral": {"viral-growth", "network-effects", "plg"},
        }
        return mapping.get(problem, set())

    def search_cases(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[SearchResult]:
        """搜索案例"""
        if context is None:
            context = {}

        query_tokens = self._build_query_tokens(query, context)

        results = []

        for case in self.cases:
            doc_text = ' '.join([
                case.get('name', ''),
                case.get('summary', ''),
                case.get('region', ''),
                ' '.join(case.get('tags', {}).get('tactics', [])),
                ' '.join(case.get('tags', {}).get('industry', [])),
                ' '.join(case.get('tags', {}).get('problem', [])),
                ' '.join(case.get('replicable_points', []))
            ])
            doc_tokens = self._tokenize(doc_text)

            score = self._compute_similarity(query_tokens, doc_tokens)

            # 行业匹配加分
            industry = context.get('industry', '').lower()
            case_industries = case.get('tags', {}).get('industry', [])
            if industry in case_industries:
                score += 0.3

            # 问题类型匹配加分
            problem = context.get('problem_type', '').lower()
            case_problems = case.get('tags', {}).get('problem', [])
            if problem in case_problems:
                score += 0.2

            # 阶段匹配加分
            stage = context.get('stage', '')
            case_stages = case.get('tags', {}).get('stage', [])
            if stage in case_stages:
                score += 0.1

            if score > 0:
                results.append(SearchResult(
                    id=case.get('id', ''),
                    name=case.get('name', ''),
                    type='case',
                    score=min(1.0, score),
                    highlights=case.get('replicable_points', [])[:3],
                    metadata={
                        'region': case.get('region', ''),
                        'evidence_tier': case.get('evidence_tier', 'C'),
                        'confidence': case.get('confidence', 0.75)
                    }
                ))

        # 排序并返回
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def search_weapons(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[SearchResult]:
        """搜索玩法"""
        if context is None:
            context = {}

        query_tokens = self._build_query_tokens(query, context)

        results = []

        for weapon in self.weapons:
            weapon_id = str(weapon.get("id", ""))
            weapon_detail = self.weapon_details.get(weapon_id, {})
            category_id = weapon.get("category", "")
            category_name = self.weapon_categories.get(category_id, "")
            description = weapon.get("description") or weapon_detail.get("description", "")

            doc_text = ' '.join([
                weapon.get('name', ''),
                description,
                category_id,
                category_name,
                weapon_detail.get("category_label", ""),
            ])
            doc_tokens = self._tokenize(doc_text)

            score = self._compute_similarity(query_tokens, doc_tokens)

            problem = context.get('problem_type', '').lower()
            if category_id in self._problem_to_categories(problem):
                score += 0.35

            if context.get("industry", "").lower() == "saas" and category_id == "plg":
                score += 0.12

            if context.get("stage", "") == "0-1" and category_id == "cold-start":
                score += 0.12

            if score > 0:
                results.append(SearchResult(
                    id=weapon_id,
                    name=weapon.get('name', ''),
                    type='weapon',
                    score=min(1.0, score),
                    highlights=[description or category_name or category_id],
                    metadata={
                        'category': category_id,
                        'category_name': category_name,
                        'effort': weapon.get('effort', 'Medium'),
                        'impact': weapon.get('impact', 'Medium'),
                        'evidence_tier': weapon.get('evidence_tier', 'C'),
                        'file': weapon_detail.get("file", "")
                    }
                ))

        # 排序并返回
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def search_theories(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 3
    ) -> List[SearchResult]:
        """搜索理论"""
        if context is None:
            context = {}

        query_tokens = self._build_query_tokens(query, context)

        results = []

        for theory in self.theories:
            doc_text = ' '.join([
                theory.get('id', ''),
                theory.get('name', ''),
                theory.get('core_question', ''),
                ' '.join(theory.get('core_principles', [])),
                ' '.join(theory.get('applicable_scenarios', [])),
                ' '.join(theory.get('key_tactics', [])),
            ])
            doc_tokens = self._tokenize(doc_text)

            score = self._compute_similarity(query_tokens, doc_tokens)
            if theory.get("id", "") in self._problem_to_theories(context.get("problem_type", "").lower()):
                score += 0.25

            if score > 0:
                results.append(SearchResult(
                    id=theory.get('id', ''),
                    name=theory.get('name', ''),
                    type='theory',
                    score=min(1.0, score),
                    highlights=theory.get('core_principles', [])[:3],
                    metadata={
                        'evidence_tier': theory.get('evidence_tier', 'B'),
                        'file': theory.get('file', '')
                    }
                ))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def retrieve(
        self,
        query: str,
        context: Optional[Dict] = None,
        case_limit: int = 5,
        weapon_limit: int = 5,
        theory_limit: int = 3
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
            ]
        }


def main():
    """测试检索功能"""
    retriever = KnowledgeRetriever()

    # 测试用例
    test_queries = [
        {
            'query': 'SaaS产品如何获取首批用户',
            'context': {'industry': 'saas', 'problem_type': 'acquisition', 'stage': '0-1'}
        },
        {
            'query': '如何提升用户留存率',
            'context': {'industry': 'education', 'problem_type': 'retention', 'stage': '1-10'}
        },
        {
            'query': '设计裂变机制',
            'context': {'problem_type': 'referral'}
        }
    ]

    for test in test_queries:
        print(f"\n查询: {test['query']}")
        print(f"上下文: {test.get('context', {})}")
        print("-" * 50)

        results = retriever.retrieve(test['query'], test.get('context'))

        print(f"\n案例 ({len(results['cases'])} 个):")
        for case in results['cases']:
            print(f"  - {case['name']} (分数: {case['score']:.2f}, 证据等级: {case['metadata']['evidence_tier']})")

        print(f"\n玩法 ({len(results['weapons'])} 个):")
        for weapon in results['weapons']:
            print(f"  - {weapon['name']} (分数: {weapon['score']:.2f}, 难度: {weapon['metadata']['effort']}, 影响: {weapon['metadata']['impact']})")

        print(f"\n理论 ({len(results['theories'])} 个):")
        for theory in results['theories']:
            print(f"  - {theory['name']} (分数: {theory['score']:.2f})")


if __name__ == "__main__":
    main()
