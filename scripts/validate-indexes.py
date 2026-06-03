#!/usr/bin/env python3
"""
Validate knowledge indexes
"""

import json
import sys
from pathlib import Path

def validate_index(file_path, required_fields):
    """Validate a single index file"""
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return False, f"JSON parse error: {e}"

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, "Valid"

def main():
    indexes_dir = Path('knowledge/indexes')
    errors = []

    # Validate cases index
    cases_index = indexes_dir / 'cases-index.json'
    if cases_index.exists():
        valid, msg = validate_index(cases_index, ['metadata', 'cases'])
        if valid:
            print(f"✅ {cases_index}")
        else:
            errors.append(f"{cases_index}: {msg}")
    else:
        errors.append(f"Missing: {cases_index}")

    # Validate weapons index
    weapons_index = indexes_dir / 'weapons-index.json'
    if weapons_index.exists():
        valid, msg = validate_index(weapons_index, ['metadata', 'categories', 'weapons'])
        if valid:
            print(f"✅ {weapons_index}")
        else:
            errors.append(f"{weapons_index}: {msg}")
    else:
        errors.append(f"Missing: {weapons_index}")

    # Validate theories index
    theories_index = indexes_dir / 'theories-index.json'
    if theories_index.exists():
        valid, msg = validate_index(theories_index, ['metadata', 'theories'])
        if valid:
            print(f"✅ {theories_index}")
        else:
            errors.append(f"{theories_index}: {msg}")
    else:
        errors.append(f"Missing: {theories_index}")

    if errors:
        print("\n❌ Validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n✅ All indexes validated successfully")

if __name__ == "__main__":
    main()
