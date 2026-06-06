#!/bin/bash

# Growth Master Test Runner

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================="
echo "  Growth Master Test Runner"
echo "========================================="
echo ""

echo "--- Validation Checks ---"
python3 "$ROOT_DIR/scripts/enrich-weapons.py"
python3 "$ROOT_DIR/scripts/validate-agents.py"
python3 "$ROOT_DIR/scripts/update-indexes.py"
python3 "$ROOT_DIR/scripts/validate-weapons.py"
python3 "$ROOT_DIR/scripts/validate-indexes.py"

echo ""
echo "--- Python Test Suite ---"
python3 "$ROOT_DIR/scripts/run_tests.py"
