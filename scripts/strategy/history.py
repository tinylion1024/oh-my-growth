"""History-related methods for strategy brain.

This module contains methods that handle historical experiment data,
failure condition analysis, and protection control generation.
"""

from typing import Any, Dict, List, Optional, Tuple

from .constants import STAGE_LABELS
from .utils import normalize_text


class StrategyHistory:
    """Handles historical experiment analysis and failure condition processing."""

    def __init__(self, brain: Any):
        """Initialize with reference to the strategy brain.

        Args:
            brain: StrategyBrain instance to access its properties and methods.
        """
        self.brain = brain

    def _get_experiment_log(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract experiment log from context."""
        payload = context.get("experiment_log", {})
        if isinstance(payload, dict):
            experiments = payload.get("experiments", [])
            if isinstance(experiments, list):
                return [item for item in experiments if isinstance(item, dict)]
        return []

    def _failure_condition_tags(self, text: str) -> List[str]:
        """Extract failure condition tags from text."""
        normalized = normalize_text(text)
        mapping = {
            "low_quality_users": ["低质量用户", "低质量流量", "羊毛", "薅羊毛", "意向低"],
            "activation_drop": ["激活低", "激活偏低", "首次价值", "转化偏低", "转化低", "试用激活"],
            "retention_damage": ["留存低", "留存偏低", "伤害留存", "假留存", "假活跃", "回访低"],
            "cac_loss": ["cac", "获客成本", "成本高", "投放失控", "预算失控"],
            "subsidy_abuse": ["高补贴", "补贴", "高激励", "激励滥用"],
            "diffuse_execution": ["无法归因", "同时做太多", "太分散", "多机制同时"],
            "lead_quality": ["线索质量", "高意向线索", "成交低", "成单低", "demo"],
        }
        tags = [tag for tag, keywords in mapping.items() if any(keyword in normalized for keyword in keywords)]
        return tags

    def _failure_tag_labels(self) -> Dict[str, str]:
        """Get readable labels for failure tags."""
        return {
            "low_quality_users": "低质量用户/流量",
            "activation_drop": "激活不成立",
            "retention_damage": "留存受损或假留存",
            "cac_loss": "CAC/预算失控",
            "subsidy_abuse": "高补贴或激励滥用",
            "diffuse_execution": "动作过多导致无法归因",
            "lead_quality": "线索质量不足",
        }

    def _option_failure_condition_tags(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
    ) -> List[str]:
        """Extract failure condition tags for a specific option."""
        source = " ".join(
            [
                category,
                weapon_name,
                str(metadata.get("guardrail_risk", "")),
                str(metadata.get("resource_profile", "")),
            ]
        )
        tags = set(self._failure_condition_tags(source))
        category_defaults = {
            "viral-referral": {"low_quality_users", "subsidy_abuse"},
            "paid-ads": {"cac_loss", "low_quality_users"},
            "plg": {"activation_drop"},
            "retention": {"retention_damage", "diffuse_execution"},
            "monetization": {"retention_damage"},
            "b2b-sales": {"lead_quality"},
        }
        tags.update(category_defaults.get(category, set()))
        return list(tags)

    def _history_score_adjustment(
        self, category: str, weapon_name: str, context: Dict[str, Any]
    ) -> Tuple[float, str]:
        """Calculate score adjustment based on historical experiments."""
        adjustments = 0.0
        notes: List[str] = []
        normalized_name = weapon_name.lower()
        for item in self._get_experiment_log(context):
            exp_category = str(item.get("category", "")).strip()
            exp_name = str(item.get("name", "")).strip().lower()
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            lesson = str(item.get("lesson", "")).strip()
            same_track = (
                exp_category == category
                or (exp_name and exp_name in normalized_name)
                or (normalized_name and normalized_name in exp_name)
            )
            if not same_track:
                continue
            if outcome in {"failed", "stop", "stopped", "negative"}:
                adjustments -= 1.0
                notes.append(f"历史上同方向做过但未跑通：{lesson or exp_name or exp_category}")
            elif outcome in {"success", "succeeded", "positive", "validated"}:
                adjustments += 0.45
                notes.append(f"历史上同方向已有正向信号：{lesson or exp_name or exp_category}")
        return adjustments, "；".join(notes[:2])

    def _history_repeat_risk_prompts(self, context: Dict[str, Any]) -> List[str]:
        """Generate prompts for avoiding historical failure conditions."""
        prompts: List[str] = []
        readable = self._failure_tag_labels()
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [
                    str(item.get("name", "")),
                    str(item.get("lesson", "")),
                    str(item.get("avoid_repeat", "")),
                ]
            )
            tags = self._failure_condition_tags(failure_text)
            if not tags:
                continue
            prompts.append("这次准备如何避免历史失败条件：" + "、".join(readable[tag] for tag in tags[:3]))
        return prompts[:2]

    def _history_protection_controls(
        self,
        context: Dict[str, Any],
        top_option: Optional[Any],
    ) -> List[Dict[str, str]]:
        """Generate protection controls based on historical failures."""
        controls: List[Dict[str, str]] = []
        readable = self._failure_tag_labels()
        control_map = {
            "low_quality_users": {
                "control": "只统计高意向样本，拆开流量量与高意向转化率，不用总新增替代真实质量。",
                "guardrail": "高意向转化率 / 激活率不能继续下滑",
                "stop": "新增上涨但高意向转化或激活继续恶化时立即停",
            },
            "activation_drop": {
                "control": "把首次价值达成率设成首个过程指标，先验证核心动作，不同时改多处 onboarding。",
                "guardrail": "首次价值达成率不能低于当前基线",
                "stop": "曝光或注册上涨但首次价值达成率不升反降时立即停",
            },
            "retention_damage": {
                "control": "主实验之外单独监控 7 日 / 30 日留存，禁止用短期刺激替代真实回访。",
                "guardrail": "7 日 / 30 日留存不能恶化",
                "stop": "短期指标改善但留存或复访连续恶化时立即停",
            },
            "cac_loss": {
                "control": "预算拆成小批次，先验证单渠道单位经济性，再决定是否加仓。",
                "guardrail": "CAC 不能超出当前可接受区间",
                "stop": "样本量尚小但 CAC 已明显失控时立即停",
            },
            "subsidy_abuse": {
                "control": "把补贴和激励限定在小样本白名单，不让补贴直接决定传播动机。",
                "guardrail": "补贴成本和作弊率不能失控",
                "stop": "需要持续加大补贴才能维持指标时立即停",
            },
            "diffuse_execution": {
                "control": "一次只改一个主机制，实验期间锁定其他变量，保证可归因。",
                "guardrail": "实验窗口内不允许并行改多个主机制",
                "stop": "一旦并行改动过多导致无法归因，本轮实验作废",
            },
            "lead_quality": {
                "control": "把线索数和高意向线索/成单率分开看，先验证 ICP 与线索质量。",
                "guardrail": "高意向线索率和 demo-to-close 不能继续下滑",
                "stop": "线索数上涨但成交效率继续恶化时立即停",
            },
        }

        option_tags = (
            set(
                self._option_failure_condition_tags(
                    top_option.category,
                    top_option.name,
                    {
                        "guardrail_risk": top_option.guardrail_risk,
                        "resource_profile": top_option.resource_profile,
                    },
                )
            )
            if top_option
            else set()
        )
        problem_relevant_tags = {
            "acquisition": {"low_quality_users", "cac_loss", "lead_quality", "activation_drop"},
            "activation": {"activation_drop", "diffuse_execution"},
            "retention": {"retention_damage", "diffuse_execution"},
            "monetization": {"retention_damage", "cac_loss"},
            "referral": {"low_quality_users", "subsidy_abuse", "activation_drop"},
        }.get(str(context.get("problem_type", "")), set())
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [str(item.get("name", "")), str(item.get("lesson", "")), str(item.get("avoid_repeat", ""))]
            )
            failure_tags = self._failure_condition_tags(failure_text)
            tags = [tag for tag in failure_tags if not option_tags or tag in option_tags]
            if not tags:
                tags = [tag for tag in failure_tags if tag in problem_relevant_tags]
            for tag in tags[:2]:
                if tag not in control_map:
                    continue
                controls.append(
                    {
                        "risk": readable[tag],
                        "control": control_map[tag]["control"],
                        "guardrail": control_map[tag]["guardrail"],
                        "stop": control_map[tag]["stop"],
                    }
                )

        deduped: List[Dict[str, str]] = []
        seen = set()
        for item in controls:
            key = item["risk"]
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        return deduped[:3]

    def _history_failure_condition_adjustment(
        self,
        category: str,
        weapon_name: str,
        metadata: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[float, str]:
        """Calculate penalty for options that repeat historical failure conditions."""
        option_tags = set(self._option_failure_condition_tags(category, weapon_name, metadata))
        if not option_tags:
            return 0.0, ""

        penalty = 0.0
        notes: List[str] = []
        for item in self._get_experiment_log(context):
            outcome = str(item.get("outcome", item.get("status", ""))).lower()
            if outcome not in {"failed", "stop", "stopped", "negative"}:
                continue
            failure_text = " ".join(
                [
                    str(item.get("name", "")),
                    str(item.get("lesson", "")),
                    str(item.get("avoid_repeat", "")),
                ]
            )
            failure_tags = set(self._failure_condition_tags(failure_text))
            overlap = option_tags & failure_tags
            if not overlap:
                continue
            penalty += 0.35
            readable = self._failure_tag_labels()
            notes.append("历史失败条件重复：" + "、".join(readable[tag] for tag in sorted(overlap)))
        return min(0.9, penalty), "；".join(notes[:2])
