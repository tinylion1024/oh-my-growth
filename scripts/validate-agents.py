#!/usr/bin/env python3
"""
Validate Agent definitions
"""

import os
import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = ['name', 'description', 'model']

def validate_agent(file_path):
    """Validate a single agent file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Check front matter
    if not content.startswith('---'):
        return False, "Missing YAML front matter"

    # Parse front matter
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid front matter format"

        front_matter = yaml.safe_load(parts[1])
    except Exception as e:
        return False, f"YAML parse error: {e}"

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in front_matter:
            return False, f"Missing required field: {field}"

    # Check content structure
    if '# ' not in parts[2]:
        return False, "Missing main heading"

    return True, "Valid"

def main():
    agents_dir = Path('agents')
    errors = []

    for agent_file in agents_dir.glob('**/*.md'):
        valid, msg = validate_agent(agent_file)
        if not valid:
            errors.append(f"{agent_file}: {msg}")
        else:
            print(f"✅ {agent_file}")

    if errors:
        print("\n❌ Validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n✅ All agents validated successfully")

if __name__ == "__main__":
    main()
