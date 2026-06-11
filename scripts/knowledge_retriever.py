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
        self.failures = []
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
        business_model_kind = self._context_business_model_kind(context)
        if business_model_kind in {"marketplace", "local-services"}:
            expansions.extend(["供给", "需求", "撮合", "流动性"])
            side_focus = self._context_marketplace_side_focus(query, context)
            if side_focus == "supply":
                expansions.extend(["商家", "司机", "房东", "入驻"])
            elif side_focus == "demand":
                expansions.extend(["买家", "乘客", "房客", "拉新"])
        if business_model_kind == "local-services":
            expansions.extend(["单城", "区域密度", "履约", "到店", "上门", "同城"])

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

    def _context_business_model(self, context: Dict) -> str:
        profile = context.get("company_profile", {})
        if isinstance(profile, dict):
            return self._normalize_text(str(profile.get("business_model", "")))
        return ""

    def _context_business_model_kind(self, context: Dict) -> str:
        industry = self._normalize_text(context.get("industry", ""))
        business_model = self._context_business_model(context)
        if industry == "local-services" or any(
            token in business_model
            for token in ["local services", "本地生活", "到店", "上门", "同城", "配送", "外卖", "出行"]
        ):
            return "local-services"
        if any(token in business_model for token in ["b2b", "sales led", "sales-led", "销售驱动"]):
            return "b2b-sales-led"
        if industry == "marketplace" or any(token in business_model for token in ["marketplace", "双边", "平台"]):
            return "marketplace"
        if industry == "ai" or any(token in business_model for token in ["ai", "agent", "copilot"]):
            return "ai"
        return "general"

    def _context_marketplace_side_focus(self, query: str, context: Dict) -> str:
        text = self._normalize_text(
            " ".join(
                [
                    query,
                    str(context.get("goal", "")),
                    str(context.get("metric", "")),
                    str(context.get("constraints", "")),
                ]
            )
        )
        explicit_demand_markers = ["先补需求侧", "先做需求侧", "需求侧优先", "先拉需求", "先做需求"]
        explicit_supply_markers = ["先补供给侧", "先做供给侧", "供给侧优先", "先拉供给", "先做供给"]
        if any(marker in text for marker in explicit_demand_markers):
            return "demand"
        if any(marker in text for marker in explicit_supply_markers):
            return "supply"

        supply_hits = sum(
            1 for token in ["供给", "商家", "司机", "房东", "创作者", "seller", "supply", "inventory", "入驻"]
            if token in text
        )
        demand_hits = sum(
            1 for token in ["需求", "买家", "乘客", "房客", "游客", "buyer", "demand", "rider", "guest"]
            if token in text
        )
        if demand_hits > supply_hits:
            return "demand"
        if supply_hits > demand_hits:
            return "supply"
        return "liquidity"

    def _context_preferred_categories(self, context: Dict, problem: str) -> Set[str]:
        categories = set(self._problem_to_categories(problem))
        business_model_kind = self._context_business_model_kind(context)

        if business_model_kind == "b2b-sales-led":
            categories.add("b2b-sales")
        if business_model_kind == "marketplace":
            categories.update({"community", "viral-referral"})
        if business_model_kind == "local-services":
            categories.update({"cold-start", "community"})
        if business_model_kind == "ai":
            categories.update({"content-growth", "plg"})

        return categories

    def _context_preferred_theories(self, context: Dict, problem: str) -> Set[str]:
        theories = set(self._problem_to_theories(problem))
        business_model_kind = self._context_business_model_kind(context)

        if business_model_kind == "b2b-sales-led":
            theories.update({"business-models", "plg"})
        if business_model_kind in {"marketplace", "local-services"}:
            theories.update({"network-effects", "flywheel"})
        if business_model_kind == "ai":
            theories.update({"content-growth", "plg"})

        return theories

    def _problem_to_categories(self, problem: str) -> Set[str]:
        mapping = {
            "acquisition": {"cold-start", "content-growth", "paid-ads", "plg", "b2b-sales"},
            "activation": {"plg", "community", "retention"},
            "retention": {"retention", "community", "gamification"},
            "monetization": {"monetization", "plg", "b2b-sales"},
            "referral": {"viral-referral", "community", "plg"},
        }
        return mapping.get(problem, set())

    def _problem_to_theories(self, problem: str) -> Set[str]:
        mapping = {
            "acquisition": {"growth-hacking", "content-growth", "plg", "network-effects"},
            "activation": {"growth-hacking", "plg", "gamification"},
            "retention": {"gamification", "flywheel", "community-growth"},
            "monetization": {"business-models", "plg"},
            "referral": {"viral-growth", "network-effects", "plg"},
        }
        return mapping.get(problem, set())

    def _problem_to_process(self, problem: str) -> str:
        mapping = {
            "acquisition": "用户获取",
            "activation": "用户深耕",
            "retention": "用户深耕",
            "monetization": "用户深耕",
            "referral": "用户获取",
        }
        return mapping.get(problem, "增长经营")

    def _problem_to_journey(self, problem: str) -> str:
        mapping = {
            "acquisition": "认知/到达",
            "activation": "注册/激活",
            "retention": "留存",
            "monetization": "付费",
            "referral": "分享",
        }
        return mapping.get(problem, "用户旅程待明确")

    def _category_stage_fit(self, category: str, stage: str) -> float:
        stage_fit = {
            "0-1": {"cold-start": 1.0, "content-growth": 0.7, "plg": 0.6, "viral-referral": 0.6, "paid-ads": 0.1, "b2b-sales": 0.5},
            "1-10": {"plg": 1.0, "retention": 0.9, "community": 0.8, "viral-referral": 0.8, "content-growth": 0.7, "b2b-sales": 1.0},
            "10-100": {"paid-ads": 1.0, "brand": 0.9, "b2b-sales": 0.9, "monetization": 0.8, "retention": 0.7},
        }
        return stage_fit.get(stage, {}).get(category, 0.4)

    def _category_journey_fit(self, category: str, journey_stage: str) -> float:
        journey_fit = {
            "认知/到达": {"cold-start": 1.0, "content-growth": 0.9, "paid-ads": 0.8, "brand": 0.7, "b2b-sales": 0.95},
            "注册/激活": {"plg": 1.0, "community": 0.6, "retention": 0.6},
            "留存": {"retention": 1.0, "community": 0.8, "plg": 0.7},
            "付费": {"monetization": 1.0, "plg": 0.7, "b2b-sales": 0.8},
            "分享": {"viral-referral": 1.0, "community": 0.7, "plg": 0.6},
        }
        return journey_fit.get(journey_stage, {}).get(category, 0.3)

    def _resource_fit(self, effort: str, context: Dict) -> float:
        budget_text = self._normalize_text(context.get("budget", ""))
        team_text = self._normalize_text(context.get("team", ""))
        effort_fit = {"Low": 1.0, "Medium": 0.7, "High": 0.3}.get(effort, 0.6)

        constrained_budget = any(token in budget_text for token in ["小", "有限", "10万", "5万", "无预算", "低预算"])
        constrained_team = any(token in team_text for token in ["1", "2", "单人", "兼职", "最小"])

        if constrained_budget and effort == "High":
            effort_fit -= 0.3
        if constrained_team and effort == "High":
            effort_fit -= 0.3
        if constrained_team and effort == "Medium":
            effort_fit -= 0.1

        return max(0.1, effort_fit)

    def _guardrail_risk(self, category: str, problem: str) -> str:
        risk_map = {
            "viral-referral": "可能带来低质量用户和激励滥用",
            "paid-ads": "可能放大未验证转化链路并拉高 CAC",
            "plg": "可能在核心价值未成立时形成空转 onboarding",
            "retention": "可能用假活跃掩盖主价值问题",
            "monetization": "可能短期收入提升但伤害长期留存",
        }
        if category in risk_map:
            return risk_map[category]
        if problem == "acquisition":
            return "需要警惕低质量流量替代真实增长"
        return "需要结合约束线验证副作用"

    def _case_stage_fit(self, case: Dict, stage: str) -> float:
        case_stages = set(case.get("stage_fit", []) or case.get("tags", {}).get("stage", []))
        if not stage:
            return 0.4
        if stage in case_stages:
            return 1.0
        return 0.3

    def _case_journey_fit(self, case: Dict, journey_stage: str, problem: str) -> float:
        if not journey_stage:
            return 0.4
        indexed_journey = case.get("journey_stage", "")
        if indexed_journey == journey_stage:
            return 1.0
        tactics = " ".join(case.get("tags", {}).get("tactics", []))
        summary = f"{case.get('summary', '')} {tactics}"
        summary_text = self._normalize_text(summary)
        journey_keywords = {
            "认知/到达": ["获客", "拉新", "内容", "投放", "入口", "曝光"],
            "注册/激活": ["激活", "引导", "onboarding", "首次价值", "转化"],
            "留存": ["留存", "复访", "召回", "习惯", "活跃"],
            "付费": ["付费", "定价", "变现", "订阅", "升级"],
            "分享": ["分享", "邀请", "裂变", "推荐", "传播"],
        }
        hits = sum(1 for keyword in journey_keywords.get(journey_stage, []) if keyword in summary_text)
        if hits:
            return min(1.0, 0.5 + hits * 0.15)
        return 0.8 if self._problem_to_journey(problem) == journey_stage else 0.3

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
        problem = context.get('problem_type', '').lower()
        journey_stage = context.get("journey_stage", "") or self._problem_to_journey(problem)
        growth_process = context.get("growth_process", "") or self._problem_to_process(problem)
        marketplace_side_focus = self._context_marketplace_side_focus(query, context)
        business_model_kind = self._context_business_model_kind(context)

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
            case_problems = case.get('tags', {}).get('problem', [])
            if problem in case_problems:
                score += 0.2

            if case.get("growth_process") == growth_process:
                score += 0.08

            # 阶段匹配加分
            stage = context.get('stage', '')
            case_stages = case.get('stage_fit', []) or case.get('tags', {}).get('stage', [])
            if stage in case_stages:
                score += 0.1

            stage_fit = self._case_stage_fit(case, stage)
            score += stage_fit * 0.1

            journey_fit = self._case_journey_fit(case, journey_stage, problem)
            score += journey_fit * 0.08

            company_type = case.get("company_type", "")
            marketplace_side = case.get("marketplace_side", "")
            if business_model_kind == "local-services":
                if company_type == "local-services":
                    score += 0.2
                elif company_type == "marketplace":
                    score += 0.08
            elif industry == "marketplace" or company_type == "marketplace":
                if company_type == "marketplace":
                    score += 0.14
                elif company_type == "local-services":
                    score += 0.12
            if business_model_kind in {"marketplace", "local-services"}:
                if marketplace_side == marketplace_side_focus:
                    score += 0.12
                elif marketplace_side == "liquidity":
                    score += 0.08
                elif marketplace_side_focus in {"supply", "demand"} and marketplace_side in {"supply", "demand"}:
                    score -= 0.06

            if score > 0:
                results.append(SearchResult(
                    id=case.get('id', ''),
                    name=case.get('name', ''),
                    type='case',
                    score=round(min(1.5, score), 4),
                    highlights=case.get('replicable_points', [])[:3],
                    metadata={
                        'region': case.get('region', ''),
                        'evidence_tier': case.get('evidence_tier', 'C'),
                        'confidence': case.get('confidence', 0.75),
                        'growth_process': case.get('growth_process', growth_process),
                        'journey_stage': case.get('journey_stage', journey_stage),
                        'stage_fit': round(stage_fit, 2),
                        'journey_fit': round(journey_fit, 2),
                        'company_type': company_type,
                        'marketplace_side': marketplace_side,
                        'resource_profile': case.get('resource_profile', ''),
                        'failure_refs': case.get('failure_refs', []),
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
        problem = context.get('problem_type', '').lower()
        stage = context.get("stage", "")
        journey_stage = context.get("journey_stage", "") or self._problem_to_journey(problem)
        growth_process = context.get("growth_process", "") or self._problem_to_process(problem)
        business_model_kind = self._context_business_model_kind(context)

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

            if category_id in self._context_preferred_categories(context, problem):
                score += 0.35

            if context.get("industry", "").lower() == "saas" and category_id == "plg":
                score += 0.12
            business_model = self._context_business_model(context)
            if business_model_kind == "b2b-sales-led" and category_id == "b2b-sales":
                score += 0.22
            if business_model_kind == "marketplace" and category_id in {"community", "viral-referral"}:
                score += 0.14
            if business_model_kind == "local-services" and category_id in {"cold-start", "community"}:
                score += 0.16
            if business_model_kind == "ai" and category_id in {"content-growth", "plg"}:
                score += 0.12

            indexed_stage_fit = weapon.get("stage_fit", [])
            stage_fit = 1.0 if stage and stage in indexed_stage_fit else self._category_stage_fit(category_id, stage)
            score += stage_fit * 0.18

            indexed_journey = weapon.get("journey_stage", "")
            journey_fit = 1.0 if indexed_journey == journey_stage else self._category_journey_fit(category_id, journey_stage)
            score += journey_fit * 0.16

            resource_fit = self._resource_fit(weapon.get('effort', 'Medium'), context)
            score += resource_fit * 0.1

            if weapon.get("growth_process") == growth_process:
                score += 0.08

            marketplace_side = weapon.get("marketplace_side", "")
            if business_model_kind == "local-services":
                if marketplace_side in {"supply", "liquidity"}:
                    score += 0.12
                elif marketplace_side == "demand" and stage == "0-1":
                    score -= 0.08
            if business_model_kind in {"marketplace", "local-services"} and marketplace_side:
                side_focus = self._context_marketplace_side_focus(query, context)
                if marketplace_side == side_focus:
                    score += 0.16
                elif marketplace_side == "liquidity":
                    score += 0.08
                elif side_focus in {"supply", "demand"} and marketplace_side in {"supply", "demand"}:
                    score -= 0.05

            if score > 0:
                results.append(SearchResult(
                    id=weapon_id,
                    name=weapon.get('name', ''),
                    type='weapon',
                    score=round(score, 4),
                    highlights=[description or category_name or category_id],
                    metadata={
                        'category': category_id,
                        'category_name': category_name,
                        'effort': weapon.get('effort', 'Medium'),
                        'impact': weapon.get('impact', 'Medium'),
                        'evidence_tier': weapon.get('evidence_tier', 'C'),
                        'file': weapon_detail.get("file", ""),
                        'growth_process': weapon.get('growth_process', growth_process),
                        'journey_stage': weapon.get('journey_stage', journey_stage),
                        'stage_fit': round(stage_fit, 2),
                        'resource_fit': round(resource_fit, 2),
                        'journey_fit': round(journey_fit, 2),
                        'marketplace_side': marketplace_side,
                        'guardrail_risk': weapon.get('guardrail_risk', self._guardrail_risk(category_id, problem)),
                        'resource_profile': weapon.get('resource_profile', ''),
                        'failure_refs': weapon.get('failure_refs', []),
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
        problem = context.get("problem_type", "").lower()
        growth_process = context.get("growth_process", "") or self._problem_to_process(problem)
        journey_stage = context.get("journey_stage", "") or self._problem_to_journey(problem)
        stage = context.get("stage", "")
        marketplace_side_focus = self._context_marketplace_side_focus(query, context)
        business_model_kind = self._context_business_model_kind(context)

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
            if theory.get("id", "") in self._context_preferred_theories(context, problem):
                score += 0.25
            if theory.get("growth_process") == growth_process:
                score += 0.08

            business_model = self._context_business_model(context)
            if business_model_kind == "b2b-sales-led" and theory.get("id", "") in {"business-models", "plg"}:
                score += 0.15
            if business_model_kind in {"marketplace", "local-services"} and theory.get("id", "") in {"network-effects", "flywheel"}:
                score += 0.18
            if business_model_kind == "ai" and theory.get("id", "") in {"content-growth", "plg"}:
                score += 0.12

            indexed_journey = theory.get("journey_stage", "")
            journey_fit = 1.0 if indexed_journey == journey_stage else 0.35
            score += journey_fit * 0.08

            indexed_stage_fit = theory.get("stage_fit", [])
            stage_fit = 1.0 if stage and stage in indexed_stage_fit else 0.4
            score += stage_fit * 0.06

            if business_model_kind == "local-services":
                if theory.get("id", "") in {"network-effects", "flywheel"}:
                    score += 0.06
                if theory.get("company_type", "") == "local-services":
                    score += 0.12
            elif context.get("industry", "").lower() == "marketplace" or "marketplace" in business_model:
                if theory.get("company_type", "") == "marketplace":
                    score += 0.12
            if business_model_kind in {"marketplace", "local-services"}:
                if theory.get("marketplace_side", "") == marketplace_side_focus:
                    score += 0.1
                elif theory.get("marketplace_side", "") == "liquidity":
                    score += 0.06
                elif marketplace_side_focus in {"supply", "demand"} and theory.get("marketplace_side", "") in {"supply", "demand"}:
                    score -= 0.04

            if score > 0:
                results.append(SearchResult(
                    id=theory.get('id', ''),
                    name=theory.get('name', ''),
                    type='theory',
                    score=round(min(1.5, score), 4),
                    highlights=theory.get('core_principles', [])[:3],
                    metadata={
                        'evidence_tier': theory.get('evidence_tier', 'B'),
                        'file': theory.get('file', ''),
                        'growth_process': theory.get('growth_process', growth_process),
                        'journey_stage': theory.get('journey_stage', journey_stage),
                        'stage_fit': round(stage_fit, 2),
                        'journey_fit': round(journey_fit, 2),
                        'company_type': theory.get('company_type', ''),
                        'marketplace_side': theory.get('marketplace_side', ''),
                        'resource_profile': theory.get('resource_profile', ''),
                        'failure_refs': theory.get('failure_refs', []),
                    }
                ))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def search_failures(
        self,
        query: str,
        context: Optional[Dict] = None,
        limit: int = 2
    ) -> List[SearchResult]:
        """Search failure modes and anti-patterns."""
        if context is None:
            context = {}

        query_tokens = self._build_query_tokens(query, context)
        problem = context.get("problem_type", "").lower()
        growth_process = context.get("growth_process", "") or self._problem_to_process(problem)
        journey_stage = context.get("journey_stage", "") or self._problem_to_journey(problem)

        results = []
        for failure in self.failures:
            doc_text = " ".join([
                failure.get("id", ""),
                failure.get("name", ""),
                failure.get("summary", ""),
                " ".join(failure.get("warning_signals", [])),
                " ".join(failure.get("suggestions", [])),
            ])
            doc_tokens = self._tokenize(doc_text)

            score = self._compute_similarity(query_tokens, doc_tokens)
            if problem in failure.get("problem_types", []):
                score += 0.28
            if failure.get("growth_process") == growth_process:
                score += 0.08

            indexed_journey = failure.get("journey_stage", "")
            journey_fit = 1.0 if indexed_journey == journey_stage else 0.35
            score += journey_fit * 0.08

            if score > 0:
                results.append(SearchResult(
                    id=failure.get("id", ""),
                    name=failure.get("name", ""),
                    type="failure",
                    score=min(1.0, score),
                    highlights=failure.get("warning_signals", [])[:2] or [failure.get("summary", "")],
                    metadata={
                        "file": failure.get("file", ""),
                        "growth_process": failure.get("growth_process", growth_process),
                        "journey_stage": failure.get("journey_stage", journey_stage),
                        "problem_types": failure.get("problem_types", []),
                        "summary": failure.get("summary", ""),
                        "suggestions": failure.get("suggestions", [])[:2],
                        "journey_fit": round(journey_fit, 2),
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
        theory_limit: int = 3,
        failure_limit: int = 2
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
