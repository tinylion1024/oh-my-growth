#!/usr/bin/env python3
"""
Validate knowledge indexes
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def validate_index(file_path, required_fields, items_key, required_item_fields):
    """Validate a single index file with basic structural checks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {e}"

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    items = data.get(items_key, [])
    if not isinstance(items, list):
        return False, f"Field '{items_key}' must be a list"

    metadata = data.get("metadata", {})
    total_field = f"total_{items_key.replace('-', '_')}"
    if total_field in metadata and metadata[total_field] != len(items):
        return False, f"Metadata count mismatch: {total_field}={metadata[total_field]}, actual={len(items)}"

    for item in items:
        for field in required_item_fields:
            if field not in item:
                return False, f"Item missing required field '{field}': {item}"
        file_ref = item.get("file")
        if file_ref and not (ROOT_DIR / "knowledge" / file_ref).exists():
            return False, f"Referenced file does not exist: knowledge/{file_ref}"
        if "failure_refs" in item:
            if not isinstance(item["failure_refs"], list):
                return False, f"failure_refs must be a list: {item}"
            for failure_ref in item["failure_refs"]:
                if not (ROOT_DIR / failure_ref).exists():
                    return False, f"Referenced failure doc does not exist: {failure_ref}"
        if "stage_fit" in item and not isinstance(item["stage_fit"], list):
            return False, f"stage_fit must be a list: {item}"
        if "growth_process" in item and not isinstance(item["growth_process"], str):
            return False, f"growth_process must be a string: {item}"
        if "journey_stage" in item and not isinstance(item["journey_stage"], str):
            return False, f"journey_stage must be a string: {item}"
        if "marketplace_side" in item and not isinstance(item["marketplace_side"], str):
            return False, f"marketplace_side must be a string: {item}"
        if "problem_types" in item and not isinstance(item["problem_types"], list):
            return False, f"problem_types must be a list: {item}"

    return True, "Valid"

def main():
    indexes_dir = Path('knowledge/indexes')
    errors = []

    # Validate cases index
    cases_index = indexes_dir / 'cases-index.json'
    if cases_index.exists():
        valid, msg = validate_index(
            cases_index,
            ['metadata', 'cases'],
            'cases',
            ['id', 'name', 'file', 'summary', 'tags', 'growth_process', 'journey_stage', 'stage_fit', 'company_type', 'marketplace_side', 'resource_profile', 'failure_refs']
        )
        if valid:
            print(f"✅ {cases_index}")
        else:
            errors.append(f"{cases_index}: {msg}")
    else:
        errors.append(f"Missing: {cases_index}")

    # Validate weapons index
    weapons_index = indexes_dir / 'weapons-index.json'
    if weapons_index.exists():
        valid, msg = validate_index(
            weapons_index,
            ['metadata', 'categories', 'weapons'],
            'weapons',
            ['id', 'name', 'category', 'effort', 'impact', 'evidence_tier', 'growth_process', 'journey_stage', 'stage_fit', 'marketplace_side', 'resource_profile', 'guardrail_risk', 'failure_refs']
        )
        if valid:
            print(f"✅ {weapons_index}")
        else:
            errors.append(f"{weapons_index}: {msg}")
    else:
        errors.append(f"Missing: {weapons_index}")

    # Validate theories index
    theories_index = indexes_dir / 'theories-index.json'
    if theories_index.exists():
        valid, msg = validate_index(
            theories_index,
            ['metadata', 'theories'],
            'theories',
            ['id', 'name', 'file', 'core_question', 'core_principles', 'growth_process', 'journey_stage', 'stage_fit', 'company_type', 'marketplace_side', 'resource_profile', 'failure_refs']
        )
        if valid:
            print(f"✅ {theories_index}")
        else:
            errors.append(f"{theories_index}: {msg}")
    else:
        errors.append(f"Missing: {theories_index}")

    # Validate failures index
    failures_index = indexes_dir / 'failures-index.json'
    if failures_index.exists():
        valid, msg = validate_index(
            failures_index,
            ['metadata', 'failures'],
            'failures',
            ['id', 'name', 'file', 'growth_process', 'journey_stage', 'problem_types', 'summary']
        )
        if valid:
            print(f"✅ {failures_index}")
        else:
            errors.append(f"{failures_index}: {msg}")
    else:
        errors.append(f"Missing: {failures_index}")

    if errors:
        print("\n❌ Validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n✅ All indexes validated successfully")

if __name__ == "__main__":
    main()
