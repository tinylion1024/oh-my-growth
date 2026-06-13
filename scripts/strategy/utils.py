"""Utility functions for strategy modules.

This module contains shared utility functions used across multiple strategy modules.
"""

from typing import Any


def normalize_text(text: Any) -> str:
    """Normalize text for comparison.

    Args:
        text: Input text to normalize (any type will be converted to string)

    Returns:
        Normalized lowercase string with underscores and hyphens replaced by spaces
    """
    return " ".join(str(text).lower().replace("_", " ").replace("-", " ").split())
