#!/usr/bin/env python3
"""
Bayesian Decision Module for Growth Master Skill

Provides Bayesian probability updating for growth decision making.
Integrates with the evidence grading system and multi-turn dialogue.

Usage:
    from bayesian_decision import BayesianDecision

    bd = BayesianDecision()
    bd.set_hypothesis("邀请裂变能带来有效增长")
    bd.set_prior(0.35, rationale="有成功案例参考")
    bd.add_evidence("Notion案例", tier="B", direction="support")
    bd.update()
    print(bd.get_posterior())  # 0.50
    print(bd.get_decision())   # "run_experiment"
"""

import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Literal
from enum import Enum
from datetime import datetime


class EvidenceTier(Enum):
    """Evidence quality tiers with update magnitudes"""
    A = 0.25  # Meta-analysis, systematic reviews, official statistics
    B = 0.15  # Peer-reviewed papers, public datasets, industry standards
    C = 0.10  # Structured expert opinions, internal data
    D = 0.05  # LLM suggestions, analogies, common sense
    E = 0.00  # Blog posts, marketing claims, unsourced claims


class EvidenceDirection(Enum):
    """Evidence direction relative to hypothesis"""
    SUPPORT = "support"
    OPPOSE = "oppose"
    NEUTRAL = "neutral"


class DecisionAction(Enum):
    """Decision actions based on posterior probability"""
    INVEST_NOW = "invest_now"          # >= 0.75
    RUN_EXPERIMENT = "run_experiment"  # 0.50 - 0.74
    COLLECT_EVIDENCE = "collect_evidence"  # 0.30 - 0.49
    STOP = "stop"                      # < 0.30


# Default action thresholds
DEFAULT_THRESHOLDS = {
    DecisionAction.INVEST_NOW: 0.75,
    DecisionAction.RUN_EXPERIMENT: 0.50,
    DecisionAction.COLLECT_EVIDENCE: 0.30,
}

# High-risk thresholds (more conservative)
HIGH_RISK_THRESHOLDS = {
    DecisionAction.INVEST_NOW: 0.85,
    DecisionAction.RUN_EXPERIMENT: 0.60,
    DecisionAction.COLLECT_EVIDENCE: 0.40,
}

# Low-risk thresholds (more aggressive)
LOW_RISK_THRESHOLDS = {
    DecisionAction.INVEST_NOW: 0.65,
    DecisionAction.RUN_EXPERIMENT: 0.40,
    DecisionAction.COLLECT_EVIDENCE: 0.25,
}


@dataclass
class Evidence:
    """Single piece of evidence"""
    source: str
    tier: str
    direction: str
    summary: str = ""
    update_applied: float = 0.0

    def get_update_magnitude(self) -> float:
        """Get base update magnitude from tier"""
        return EvidenceTier[self.tier].value


@dataclass
class IterationRound:
    """Single iteration round in multi-turn dialogue"""
    round_number: int
    prior: float
    evidence_collected: List[Evidence]
    posterior: float
    readiness_score: float
    decision: str
    remaining_gaps: List[str]
    next_questions: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Hypothesis:
    """Decision hypothesis"""
    statement: str
    success_metric: str = ""
    time_horizon: str = ""
    prior: float = 0.30
    prior_rationale: str = ""
    hygiene_check: List[str] = field(default_factory=list)


class BayesianDecision:
    """Bayesian Decision Engine for Growth Master"""

    MAX_ROUNDS = 5
    MIN_PRIOR = 0.05
    MAX_PRIOR = 0.95
    MAX_REPORTABLE_CONFIDENCE = 0.95

    def __init__(self, risk_level: str = "normal"):
        """
        Initialize Bayesian Decision Engine.

        Args:
            risk_level: "normal", "high", or "low" - affects thresholds
        """
        self.hypothesis: Optional[Hypothesis] = None
        self.evidence_list: List[Evidence] = []
        self.iteration_log: List[IterationRound] = []
        self.current_posterior: float = 0.0
        self.risk_level = risk_level

        # Select appropriate thresholds
        if risk_level == "high":
            self.thresholds = HIGH_RISK_THRESHOLDS
        elif risk_level == "low":
            self.thresholds = LOW_RISK_THRESHOLDS
        else:
            self.thresholds = DEFAULT_THRESHOLDS

    def set_hypothesis(
        self,
        statement: str,
        success_metric: str = "",
        time_horizon: str = ""
    ) -> None:
        """Set the decision hypothesis"""
        self.hypothesis = Hypothesis(
            statement=statement,
            success_metric=success_metric,
            time_horizon=time_horizon
        )

    def set_prior(
        self,
        value: float,
        rationale: str = "",
        hygiene_check: List[str] = None
    ) -> None:
        """
        Set prior probability.

        Args:
            value: Prior probability (0.05 - 0.95)
            rationale: Reason for this prior
            hygiene_check: List of prior hygiene check items
        """
        # Clamp to valid range
        value = max(self.MIN_PRIOR, min(self.MAX_PRIOR, value))

        if self.hypothesis:
            self.hypothesis.prior = value
            self.hypothesis.prior_rationale = rationale
            self.hypothesis.hygiene_check = hygiene_check or []

        self.current_posterior = value

    def calculate_prior_from_scenario(self, scenario: str) -> float:
        """
        Calculate default prior based on scenario type.

        Args:
            scenario: One of "new_mechanism", "similar_case",
                     "same_industry", "multiple_cases", "internal_data"

        Returns:
            Default prior probability
        """
        scenario_priors = {
            "new_mechanism": 0.20,      # Brand new, no cases
            "similar_case": 0.35,       # Similar case, different industry
            "same_industry": 0.50,      # Same industry case
            "multiple_cases": 0.65,     # Multiple successful cases
            "internal_data": 0.75,      # Internal experimental data
        }
        return scenario_priors.get(scenario, 0.30)

    def add_evidence(
        self,
        source: str,
        tier: str,
        direction: str,
        summary: str = ""
    ) -> Evidence:
        """
        Add a piece of evidence.

        Args:
            source: Evidence source description
            tier: Evidence tier (A/B/C/D/E)
            direction: "support", "oppose", or "neutral"
            summary: Brief summary of evidence

        Returns:
            Evidence object
        """
        evidence = Evidence(
            source=source,
            tier=tier.upper(),
            direction=direction.lower(),
            summary=summary
        )
        self.evidence_list.append(evidence)
        return evidence

    def _calculate_update(self, evidence: Evidence, current_prior: float) -> float:
        """
        Calculate update magnitude for a single piece of evidence.

        Applies conservative bounds to prevent extreme updates.
        """
        base_update = evidence.get_update_magnitude()

        if evidence.direction == EvidenceDirection.NEUTRAL.value:
            return 0.0

        # Direction multiplier
        direction_mult = 1.0 if evidence.direction == EvidenceDirection.SUPPORT.value else -1.0

        # Calculate proposed update
        proposed_update = base_update * direction_mult

        # Apply boundary protection
        if direction_mult > 0:
            # Supporting evidence: don't exceed max
            proposed_update = min(proposed_update, self.MAX_PRIOR - current_prior)
        else:
            # Opposing evidence: don't go below min
            proposed_update = max(proposed_update, self.MIN_PRIOR - current_prior)

        return proposed_update

    def _apply_diminishing_returns(self, updates: List[float]) -> List[float]:
        """
        Apply diminishing returns for multiple evidence in same direction.

        First evidence: 100%, Second: 70%, Third: 50%, Fourth+: 30%
        """
        result = []
        support_count = 0
        oppose_count = 0

        for update in updates:
            if update > 0:
                support_count += 1
                multiplier = {1: 1.0, 2: 0.7, 3: 0.5}.get(support_count, 0.3)
            elif update < 0:
                oppose_count += 1
                multiplier = {1: 1.0, 2: 0.7, 3: 0.5}.get(oppose_count, 0.3)
            else:
                multiplier = 1.0

            result.append(update * multiplier)

        return result

    def update(self) -> float:
        """
        Perform Bayesian update with all collected evidence.

        Returns:
            Updated posterior probability
        """
        if not self.hypothesis:
            raise ValueError("Hypothesis not set")

        if not self.evidence_list:
            return self.current_posterior

        # Separate updates by direction
        support_updates = []
        oppose_updates = []

        for evidence in self.evidence_list:
            update = self._calculate_update(evidence, self.current_posterior)
            evidence.update_applied = update

            if update > 0:
                support_updates.append(update)
            elif update < 0:
                oppose_updates.append(update)

        # Apply diminishing returns to each direction
        support_updates = self._apply_diminishing_returns(support_updates)
        oppose_updates = self._apply_diminishing_returns(oppose_updates)

        # Calculate net update
        net_support = sum(support_updates)
        net_oppose = sum(oppose_updates)

        # Conservative combination: support and oppose partially cancel
        if net_support > 0 and net_oppose < 0:
            # Conflict: reduce both effects
            conflict_reduction = 0.7
            net_update = (net_support + net_oppose) * conflict_reduction
        else:
            net_update = net_support + net_oppose

        # Calculate posterior
        posterior = self.hypothesis.prior + net_update

        # Clamp to valid range
        posterior = max(self.MIN_PRIOR, min(self.MAX_PRIOR, posterior))

        # Cap reportable confidence
        posterior = min(posterior, self.MAX_REPORTABLE_CONFIDENCE)

        self.current_posterior = posterior

        return posterior

    def get_posterior(self) -> float:
        """Get current posterior probability"""
        return self.current_posterior

    def get_decision(self) -> DecisionAction:
        """Get recommended decision action based on posterior"""
        posterior = self.get_posterior()

        if posterior >= self.thresholds[DecisionAction.INVEST_NOW]:
            return DecisionAction.INVEST_NOW
        elif posterior >= self.thresholds[DecisionAction.RUN_EXPERIMENT]:
            return DecisionAction.RUN_EXPERIMENT
        elif posterior >= self.thresholds[DecisionAction.COLLECT_EVIDENCE]:
            return DecisionAction.COLLECT_EVIDENCE
        else:
            return DecisionAction.STOP

    def get_decision_text(self) -> Dict[str, str]:
        """Get decision recommendation as text"""
        decision = self.get_decision()

        recommendations = {
            DecisionAction.INVEST_NOW: {
                "action": "推荐投入资源",
                "description": "高置信度，可以开始执行",
                "confidence": "高"
            },
            DecisionAction.RUN_EXPERIMENT: {
                "action": "推荐小规模实验",
                "description": "中等置信度，需要验证关键假设",
                "confidence": "中"
            },
            DecisionAction.COLLECT_EVIDENCE: {
                "action": "继续收集证据",
                "description": "低置信度，信息不足",
                "confidence": "低"
            },
            DecisionAction.STOP: {
                "action": "不推荐继续",
                "description": "极低置信度，建议转向其他机会",
                "confidence": "低"
            }
        }

        return recommendations[decision]

    def get_readiness_score(self) -> int:
        """Get decision readiness score (0-100)"""
        return int(self.get_posterior() * 100)

    def log_round(
        self,
        remaining_gaps: List[str],
        next_questions: List[str]
    ) -> IterationRound:
        """
        Log current iteration round.

        Args:
            remaining_gaps: Remaining information gaps
            next_questions: Questions for next round

        Returns:
            IterationRound object
        """
        round_num = len(self.iteration_log) + 1

        iteration = IterationRound(
            round_number=round_num,
            prior=self.hypothesis.prior if round_num == 1 else self.iteration_log[-1].posterior,
            evidence_collected=self.evidence_list.copy(),
            posterior=self.current_posterior,
            readiness_score=self.get_readiness_score(),
            decision=self.get_decision().value,
            remaining_gaps=remaining_gaps,
            next_questions=next_questions
        )

        self.iteration_log.append(iteration)
        return iteration

    def is_terminal(self) -> bool:
        """Check if decision process should terminate"""
        decision = self.get_decision()

        # Terminal if high confidence or stopped
        if decision in [DecisionAction.INVEST_NOW, DecisionAction.STOP]:
            return True

        # Terminal if max rounds reached
        if len(self.iteration_log) >= self.MAX_ROUNDS:
            return True

        return False

    def generate_sensitivity_questions(self) -> List[Dict[str, str]]:
        """Generate sensitivity analysis questions"""
        return [
            {
                "question": "什么证据会让结论反转？",
                "purpose": "识别关键假设",
                "example": f"如果测试发现关键指标不达标，结论将反转为{self._get_opposite_decision()}"
            },
            {
                "question": "先验变化多少会影响决策？",
                "purpose": "评估先验依赖度",
                "example": f"先验从{self.hypothesis.prior:.2f}变到{self._get_threshold_boundary():.2f}，会改变建议"
            },
            {
                "question": "最脆弱的假设是什么？",
                "purpose": "识别风险点",
                "example": "假设用户有足够动机，但未验证"
            },
            {
                "question": "如果最佳证据被推翻，结论会怎样？",
                "purpose": "压力测试",
                "example": self._simulate_without_best_evidence()
            }
        ]

    def _get_opposite_decision(self) -> str:
        """Get opposite decision for sensitivity analysis"""
        current = self.get_decision()
        if current == DecisionAction.INVEST_NOW:
            return "不推荐"
        elif current == DecisionAction.STOP:
            return "推荐尝试"
        else:
            return "结论不变"

    def _get_threshold_boundary(self) -> float:
        """Get the threshold boundary for current decision"""
        decision = self.get_decision()
        return self.thresholds[decision]

    def _simulate_without_best_evidence(self) -> str:
        """Simulate posterior without the best evidence"""
        if not self.evidence_list:
            return "无证据可移除"

        # Find best evidence (highest tier, supporting)
        best_evidence = None
        for e in self.evidence_list:
            if e.direction == EvidenceDirection.SUPPORT.value:
                if best_evidence is None or e.tier < best_evidence.tier:
                    best_evidence = e

        if not best_evidence:
            return "无支持证据可移除"

        # Recalculate without best evidence
        original_posterior = self.current_posterior
        self.evidence_list.remove(best_evidence)
        self.update()
        new_posterior = self.current_posterior

        # Restore
        self.evidence_list.append(best_evidence)
        self.current_posterior = original_posterior

        return f"移除后后验降至{new_posterior:.2f}，决策变为{self.get_decision().value}"

    def to_dict(self) -> Dict:
        """Export decision state as dictionary"""
        return {
            "hypothesis": {
                "statement": self.hypothesis.statement if self.hypothesis else None,
                "success_metric": self.hypothesis.success_metric if self.hypothesis else None,
                "time_horizon": self.hypothesis.time_horizon if self.hypothesis else None,
                "prior": self.hypothesis.prior if self.hypothesis else None,
                "prior_rationale": self.hypothesis.prior_rationale if self.hypothesis else None,
            },
            "evidence": [
                {
                    "source": e.source,
                    "tier": e.tier,
                    "direction": e.direction,
                    "summary": e.summary,
                    "update_applied": e.update_applied
                }
                for e in self.evidence_list
            ],
            "posterior": self.current_posterior,
            "decision": self.get_decision().value,
            "decision_text": self.get_decision_text(),
            "readiness_score": self.get_readiness_score(),
            "risk_level": self.risk_level,
            "thresholds": {k.value: v for k, v in self.thresholds.items()},
            "iteration_log": [
                {
                    "round_number": i.round_number,
                    "prior": i.prior,
                    "posterior": i.posterior,
                    "readiness_score": i.readiness_score,
                    "decision": i.decision,
                    "remaining_gaps": i.remaining_gaps,
                    "next_questions": i.next_questions,
                    "timestamp": i.timestamp
                }
                for i in self.iteration_log
            ]
        }

    def to_json(self) -> str:
        """Export decision state as JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def main():
    """Demo: Bayesian decision for SaaS邀请裂变"""

    print("=" * 60)
    print("贝叶斯决策示例：SaaS 邀请裂变")
    print("=" * 60)

    # Initialize
    bd = BayesianDecision()

    # Set hypothesis
    bd.set_hypothesis(
        statement="邀请裂变机制能为 SaaS 产品带来有效增长",
        success_metric="每月新增 1000 付费用户",
        time_horizon="3个月"
    )

    # Set prior
    bd.set_prior(
        value=0.35,
        rationale="有 Notion、Dropbox 等成功案例，但产品形态不同",
        hygiene_check=[
            "✅ 锚定到案例证据",
            "✅ 避免过度自信",
            "✅ 考虑基础概率"
        ]
    )

    print(f"\n📝 假设: {bd.hypothesis.statement}")
    print(f"📊 先验: {bd.hypothesis.prior:.2f}")

    # Add evidence
    print("\n📚 收集证据:")

    bd.add_evidence(
        source="Notion 模板社区案例",
        tier="B",
        direction="support",
        summary="Notion 通过模板分享实现病毒增长"
    )
    print(f"  + Notion 案例 (B级, 支持) → +{EvidenceTier.B.value}")

    bd.add_evidence(
        source="SaaS 行业基准报告",
        tier="B",
        direction="support",
        summary="SaaS 产品平均病毒系数 0.3-0.8"
    )
    print(f"  + SaaS 基准 (B级, 支持) → +{EvidenceTier.B.value}")

    bd.add_evidence(
        source="内部用户调研",
        tier="C",
        direction="neutral",
        summary="用户愿意邀请，但需要激励"
    )
    print(f"  + 用户调研 (C级, 中性) → 无更新")

    # Update
    posterior = bd.update()

    print(f"\n🎯 后验: {posterior:.2f}")
    print(f"📈 置信度变化: {bd.hypothesis.prior:.2f} → {posterior:.2f}")

    # Get decision
    decision = bd.get_decision()
    decision_text = bd.get_decision_text()

    print(f"\n💡 决策: {decision_text['action']}")
    print(f"   说明: {decision_text['description']}")
    print(f"   置信度: {decision_text['confidence']}")

    # Sensitivity analysis
    print("\n🔍 敏感性分析:")
    for q in bd.generate_sensitivity_questions():
        print(f"  Q: {q['question']}")
        print(f"     → {q['example']}")

    # Log round
    bd.log_round(
        remaining_gaps=["病毒系数未知", "奖励成本未测算"],
        next_questions=["目标用户的邀请意愿有多强？", "每个邀请的成本预计是多少？"]
    )

    print("\n" + "=" * 60)
    print("完整决策 JSON:")
    print("=" * 60)
    print(bd.to_json())


if __name__ == "__main__":
    main()
