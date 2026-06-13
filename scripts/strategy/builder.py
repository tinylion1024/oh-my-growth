#!/usr/bin/env python3
"""Strategy builder module - coordinator for all _build_* methods.

This module provides the StrategyBuilder class which delegates to specialized
sub-modules for different aspects of strategy analysis.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from strategy.diagnosis import DiagnosisBuilder
from strategy.evidence import EvidenceBuilder
from strategy.experiment import ExperimentBuilder
from strategy.planning import PlanningBuilder

if TYPE_CHECKING:
    from strategy_brain import StrategyOption


class StrategyBuilder:
    """Builder class for constructing strategy analysis components.

    This class coordinates all the _build_* methods by delegating to specialized
    sub-builders for different aspects of strategy analysis.

    Sub-builders:
        - DiagnosisBuilder: Stage, growth process, journey focus diagnosis
        - EvidenceBuilder: Evidence chains, confidence, decision lines
        - ExperimentBuilder: Experiment design, actions, missing info
        - PlanningBuilder: Kelly allocation, game theory, projections
    """

    def __init__(self, brain: Any) -> None:
        """Initialize the builder with a reference to the StrategyBrain instance.

        Args:
            brain: The StrategyBrain instance to access its methods and attributes.
        """
        self.brain = brain
        # Initialize sub-builders
        self._diagnosis = DiagnosisBuilder(brain)
        self._evidence = EvidenceBuilder(brain)
        self._experiment = ExperimentBuilder(brain)
        self._planning = PlanningBuilder(brain)

    # =========================================================================
    # Diagnosis methods - delegate to DiagnosisBuilder
    # =========================================================================

    def _build_stage_diagnosis(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build stage diagnosis with focus and reason."""
        return self._diagnosis._build_stage_diagnosis(context)

    def _build_growth_process(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build growth process analysis."""
        return self._diagnosis._build_growth_process(context)

    def _build_north_star(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build north star metric with guardrails."""
        return self._diagnosis._build_north_star(context)

    def _build_journey_focus(self, context: Dict[str, str]) -> Dict[str, str]:
        """Build journey stage focus."""
        return self._diagnosis._build_journey_focus(context)

    def _build_context_summary(self, context: Dict[str, str]) -> str:
        """Build context summary for display."""
        return self._diagnosis._build_context_summary(context)

    def _build_retrieval_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for retrieval operations."""
        return self._diagnosis._build_retrieval_context(context)

    def _build_memory_summary(self, context: Dict[str, Any]) -> List[str]:
        """Build memory summary from company profile and experiment log."""
        return self._diagnosis._build_memory_summary(context)

    def _build_measurement_notes(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        north_star: Dict[str, str],
        growth_process: Dict[str, str],
    ) -> List[str]:
        """Build measurement notes for experiment setup."""
        return self._diagnosis._build_measurement_notes(context, top_option, north_star, growth_process)

    def _build_business_model_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build business model-specific diagnosis."""
        return self._diagnosis._build_business_model_diagnosis(query, context, top_option, results)

    def _build_marketplace_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build marketplace-specific diagnosis."""
        return self._diagnosis._build_marketplace_diagnosis(query, context, top_option, results)

    def _build_local_services_diagnosis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Optional[Dict[str, str]]:
        """Build local services-specific diagnosis."""
        return self._diagnosis._build_local_services_diagnosis(query, context, top_option, results)

    # =========================================================================
    # Evidence methods - delegate to EvidenceBuilder
    # =========================================================================

    def _build_evidence_chain(
        self,
        results: Dict,
        top_option: Optional["StrategyOption"],
        context: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Build evidence chain from cases, theories, and failures."""
        return self._evidence._build_evidence_chain(results, top_option, context)

    def _build_confidence(
        self,
        query: str,
        context: Dict[str, str],
        results: Dict,
        top_option: Optional["StrategyOption"],
    ) -> Tuple[Dict[str, str], str, float]:
        """Build Bayesian confidence assessment."""
        return self._evidence._build_confidence(query, context, results, top_option)

    def _build_decision_line(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        decision_text: Dict[str, str],
        confidence_label: str,
    ) -> str:
        """Build the main decision line statement."""
        return self._evidence._build_decision_line(query, context, top_option, decision_text, confidence_label)

    def _build_core_tension(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        evidence_chain: List[Dict[str, str]],
        results: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build core tension analysis."""
        return self._evidence._build_core_tension(query, context, top_option, evidence_chain, results)

    def _build_why_now(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict,
        evidence_chain: List[Dict[str, str]],
    ) -> List[str]:
        """Build reasons why this strategy should be executed now."""
        return self._evidence._build_why_now(context, top_option, results, evidence_chain)

    # =========================================================================
    # Experiment methods - delegate to ExperimentBuilder
    # =========================================================================

    def _build_experiment(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, Union[List[str], str]]:
        """Build experiment design."""
        return self._experiment._build_experiment(query, context, top_option, results, protection_controls)

    def _build_do_now(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build immediate action items."""
        return self._experiment._build_do_now(top_option, context)

    def _build_avoid_now(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build items to avoid."""
        return self._experiment._build_avoid_now(top_option, context)

    def _build_missing_info(self, context: Dict[str, str]) -> List[str]:
        """Identify missing information in context."""
        return self._experiment._build_missing_info(context)

    def _build_actions(
        self,
        query: str,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Build action items with owners, deadlines, and acceptance criteria."""
        return self._experiment._build_actions(query, context, top_option, results)

    # =========================================================================
    # Planning methods - delegate to PlanningBuilder
    # =========================================================================

    def _build_kelly_context(self, context: Dict[str, Any], top_option: Optional["StrategyOption"]) -> Dict[str, Any]:
        """Build context for Kelly criterion sizing."""
        return self._planning._build_kelly_context(context, top_option)

    def _build_kelly_allocation(
        self,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        posterior: float,
    ) -> Optional[Dict[str, Any]]:
        """Build Kelly criterion based allocation recommendation."""
        return self._planning._build_kelly_allocation(context, top_option, posterior)

    def _build_game_theory_analysis(
        self,
        query: str,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
    ) -> Optional[Dict[str, Any]]:
        """Build game theory competitive analysis."""
        return self._planning._build_game_theory_analysis(query, context, top_option)

    def _build_failure_modes(
        self,
        context: Dict[str, Any],
        top_option: Optional["StrategyOption"],
        results: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, str]]:
        """Build failure modes analysis."""
        return self._planning._build_failure_modes(context, top_option, results)

    def _build_resource_allocation(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        """Build resource allocation recommendations."""
        return self._planning._build_resource_allocation(context, top_option, results)

    def _build_review_trigger(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
        protection_controls: List[Dict[str, str]],
    ) -> Dict[str, str]:
        """Build review trigger conditions."""
        return self._planning._build_review_trigger(context, top_option, results, protection_controls)

    def _build_caveats(self, top_option: Optional["StrategyOption"], context: Dict[str, str]) -> List[str]:
        """Build caveats and warnings."""
        return self._planning._build_caveats(top_option, context)

    def _build_current_state(
        self,
        context: Dict[str, str],
        results: Dict[str, Any],
    ) -> Dict[str, Union[List[str], str]]:
        """Build current state summary."""
        return self._planning._build_current_state(context, results)

    def _build_projection(
        self,
        context: Dict[str, str],
        top_option: Optional["StrategyOption"],
        results: Dict[str, Any],
    ) -> Dict[str, str]:
        """Build outcome projection."""
        return self._planning._build_projection(context, top_option, results)

    def _build_decision_process(self, options: List["StrategyOption"]) -> Dict[str, List[Dict]]:
        """Build decision process table."""
        return self._planning._build_decision_process(options)
