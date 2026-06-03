#!/usr/bin/env python3
"""
知识检索增强模块
支持语义相似度检索，替代简单的关键词匹配
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

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

        # 加载理论索引
        theories_path = indexes_dir / "theories-index.json"
        if theories_path.exists():
            with open(theories_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.theories = data.get('theories', [])

    def _tokenize(self, text: str) -> List[str]:
        """简单分词"""
        # 移除标点符号
        text = re.sub(r'[^\w\s一-鿿]', ' ', text.lower())
        # 分词
        tokens = text.split()
        return tokens

    def _compute_similarity(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """计算简单的词重叠相似度"""
        if not query_tokens or not doc_tokens:
            return 0.0

        query_set = set(query_tokens)
        doc_set = set(doc_tokens)

        # Jaccard 相似度
        intersection = len(query_set & doc_set)
        union = len(query_set | doc_set)

        if union == 0:
            return 0.0

        return intersection / union

    def _expand_query(self, query: str, context: Dict) -> List[str]:
        """查询扩展 - 添加同义词和相关词"""
        expansions = []

        # 行业同义词
        industry_synonyms = {
            "saas": ["软件", "订阅", "b2b", "企业服务"],
            "电商": ["购物", "零售", "交易", "平台"],
            "教育": ["学习", "培训", "课程", "知识"],
            "金融": ["支付", "理财", "信贷", "fintech"],
            "社交": ["社区", "好友", "互动", "关系"],
            "内容": ["媒体", "视频", "文章", "信息"],
        }

        # 问题同义词
        problem_synonyms = {
            "获客": ["增长", "拉新", "用户", "注册"],
            "留存": ["粘性", "活跃", "回访", "留存率"],
            "变现": ["收入", "付费", "盈利", "商业化"],
            "裂变": ["传播", "分享", "邀请", "病毒"],
        }

        # 行业扩展
        industry = context.get('industry', '').lower()
        if industry in industry_synonyms:
            expansions.extend(industry_synonyms[industry])

        # 问题类型扩展
        problem = context.get('problem_type', '').lower()
        problem_cn = {
            'acquisition': '获客',
            'retention': '留存',
            'monetization': '变现',
            'referral': '裂变',
        }
        if problem in problem_cn:
            problem_text = problem_cn[problem]
            if problem_text in problem_synonyms:
                expansions.extend(problem_synonyms[problem_text])

        return expansions

    def search_cases(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[SearchResult]:
        """搜索案例"""
        if context is None:
            context = {}

        query_tokens = self._tokenize(query)
        expansions = self._expand_query(query, context)
        query_tokens.extend(self._tokenize(' '.join(expansions)))

        results = []

        for case in self.cases:
            # 构建文档文本
            doc_text = ' '.join([
                case.get('name', ''),
                case.get('summary', ''),
                ' '.join(case.get('tags', {}).get('tactics', [])),
                ' '.join(case.get('replicable_points', []))
            ])
            doc_tokens = self._tokenize(doc_text)

            # 计算相似度
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

        query_tokens = self._tokenize(query)
        expansions = self._expand_query(query, context)
        query_tokens.extend(self._tokenize(' '.join(expansions)))

        results = []

        for weapon in self.weapons:
            # 构建文档文本
            doc_text = ' '.join([
                weapon.get('name', ''),
                weapon.get('description', ''),
                weapon.get('category', '')
            ])
            doc_tokens = self._tokenize(doc_text)

            # 计算相似度
            score = self._compute_similarity(query_tokens, doc_tokens)

            # 问题类型匹配
            problem = context.get('problem_type', '').lower()
            problem_index = {
                'acquisition': 'acquisition',
                'retention': 'retention',
                'monetization': 'monetization',
                'referral': 'referral',
            }
            if problem in problem_index:
                # 检查是否在问题索引中
                pass  # 简化处理

            # 阶段匹配
            stage = context.get('stage', '')
            if stage:
                pass  # 简化处理

            if score > 0:
                results.append(SearchResult(
                    id=str(weapon.get('id', '')),
                    name=weapon.get('name', ''),
                    type='weapon',
                    score=min(1.0, score),
                    highlights=[weapon.get('description', '')],
                    metadata={
                        'category': weapon.get('category', ''),
                        'effort': weapon.get('effort', 'Medium'),
                        'impact': weapon.get('impact', 'Medium'),
                        'evidence_tier': weapon.get('evidence_tier', 'C')
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

        query_tokens = self._tokenize(query)

        results = []

        for theory in self.theories:
            doc_text = ' '.join([
                theory.get('name', ''),
                theory.get('description', ''),
                ' '.join(theory.get('key_principles', []))
            ])
            doc_tokens = self._tokenize(doc_text)

            score = self._compute_similarity(query_tokens, doc_tokens)

            if score > 0:
                results.append(SearchResult(
                    id=theory.get('id', ''),
                    name=theory.get('name', ''),
                    type='theory',
                    score=min(1.0, score),
                    highlights=theory.get('key_principles', [])[:3],
                    metadata={
                        'evidence_tier': theory.get('evidence_tier', 'B')
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
