#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [[ "${RELEASE_CHECK_SKIP_TESTS:-0}" != "1" ]]; then
  PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/run_tests.py
fi

PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/validate-agents.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/validate-docs.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/validate-weapons.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/validate-indexes.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/validate-release.py
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/smoke_install.py --platform all
PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/smoke_wheel.py

echo "✅ Release check passed"
