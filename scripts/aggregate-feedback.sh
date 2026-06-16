#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
exec python3 -B scripts/aggregate_feedback.py "$@"
