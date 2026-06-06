#!/usr/bin/env python3
"""
Validate Agent definitions
"""

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ['name', 'description', 'model']


def parse_front_matter(content):
    """Parse the small YAML subset used by agent markdown files."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, "Invalid front matter format"

    parsed = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            return None, f"Invalid front matter line: {line}"
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed, None

def validate_agent(file_path):
    """Validate a single agent file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check front matter
    if not content.startswith('---'):
        return False, "Missing YAML front matter"

    # Parse front matter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, "Invalid front matter format"

    front_matter, error = parse_front_matter(content)
    if error:
        return False, error

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
