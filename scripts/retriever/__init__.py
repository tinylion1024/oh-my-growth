"""Knowledge Retriever Module.

This package provides knowledge retrieval capabilities for cases,
weapons, theories, failure modes, and method packs.

Main components:
- types: SearchResult dataclass and constants
- context: Context helper methods
- search: Search methods for cases, weapons, theories, failures, method packs
- core: KnowledgeRetriever main class
"""

from .types import (
    BASE_DIR,
    STAGE_ALIASES,
    normalize_stage,
    SearchResult,
)
from .context import (
    normalize_text,
    tokenize,
    compute_similarity,
    expand_query,
    build_query_tokens,
    context_business_model,
    context_business_model_kind,
    context_marketplace_side_focus,
    context_preferred_categories,
    context_preferred_theories,
    problem_to_categories,
    problem_to_theories,
    problem_to_process,
    problem_to_journey,
    category_stage_fit,
    category_journey_fit,
    resource_fit,
    resource_profile_fit,
    metric_category_focus,
    metric_theory_focus,
    guardrail_penalty,
    guardrail_risk,
    case_stage_fit,
    case_journey_fit,
)
from .search import (
    search_cases,
    search_weapons,
    search_theories,
    search_failures,
    search_method_packs,
)
from .core import KnowledgeRetriever

__all__ = [
    # Constants
    "BASE_DIR",
    "STAGE_ALIASES",
    # Functions
    "normalize_stage",
    "normalize_text",
    "tokenize",
    "compute_similarity",
    "expand_query",
    "build_query_tokens",
    "context_business_model",
    "context_business_model_kind",
    "context_marketplace_side_focus",
    "context_preferred_categories",
    "context_preferred_theories",
    "problem_to_categories",
    "problem_to_theories",
    "problem_to_process",
    "problem_to_journey",
    "category_stage_fit",
    "category_journey_fit",
    "resource_fit",
    "resource_profile_fit",
    "metric_category_focus",
    "metric_theory_focus",
    "guardrail_penalty",
    "guardrail_risk",
    "case_stage_fit",
    "case_journey_fit",
    # Search functions
    "search_cases",
    "search_weapons",
    "search_theories",
    "search_failures",
    "search_method_packs",
    # Dataclasses
    "SearchResult",
    # Main class
    "KnowledgeRetriever",
]
