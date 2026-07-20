#!/bin/bash
# Install oh-my-growth for Claude Code, OpenClaw, or Hermes Agent.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

PLATFORM="claude"
if [ "${1:-}" = "--platform" ]; then
    PLATFORM="${2:-}"
elif [ "$#" -ne 0 ]; then
    echo "Usage: $0 [--platform claude|openclaw|hermes]" >&2
    exit 2
fi

case "$PLATFORM" in
    claude)
        SKILLS_ROOT="$HOME/.claude/skills"
        PLATFORM_SKILL="SKILL.md"
        ;;
    openclaw)
        SKILLS_ROOT="$HOME/.openclaw/skills"
        PLATFORM_SKILL="openclaw/SKILL.md"
        ;;
    hermes)
        SKILLS_ROOT="$HOME/.hermes/skills"
        PLATFORM_SKILL="hermes/SKILL.md"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM. Choose claude, openclaw, or hermes." >&2
        exit 2
        ;;
esac

SKILL_DIR="$SKILLS_ROOT/oh-my-growth"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"
SUBCOMMANDS=(diagnose assess design brd match learn search validate fast-scan cold-start retention monetization referral)

echo -e "${GREEN}Installing oh-my-growth for ${PLATFORM}...${NC}"

if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}Replacing existing installation at $SKILL_DIR${NC}"
    rm -rf "$SKILL_DIR"
fi
mkdir -p "$SKILL_DIR"
cp -R "$SOURCE_DIR"/* "$SKILL_DIR/"

# OpenClaw and Hermes consume an adapter-specific SKILL.md at their package root.
if [ "$PLATFORM" != "claude" ]; then
    cp "$SOURCE_DIR/$PLATFORM_SKILL" "$SKILL_DIR/SKILL.md"
fi

for required in SKILL.md knowledge scripts; do
    if [ ! -e "$SKILL_DIR/$required" ]; then
        echo -e "${RED}Installation failed: missing $required${NC}" >&2
        exit 1
    fi
done

if [ "$PLATFORM" = "claude" ]; then
    OMG_ALIAS="$SKILLS_ROOT/omg"
    if [ -L "$OMG_ALIAS" ] || [ -d "$OMG_ALIAS" ]; then
        rm -rf "$OMG_ALIAS"
    fi
    ln -s "$SKILL_DIR" "$OMG_ALIAS"

    for cmd in "${SUBCOMMANDS[@]}"; do
        shortcut_dir="$SKILLS_ROOT/omg-$cmd"
        shortcut_source="$SKILL_DIR/skills/omg-$cmd.md"
        if [ -L "$shortcut_dir" ] || [ -d "$shortcut_dir" ]; then
            rm -rf "$shortcut_dir"
        fi
        mkdir -p "$shortcut_dir"
        cp "$shortcut_source" "$shortcut_dir/SKILL.md"
        for resource in knowledge scripts agents references; do
            ln -s "../oh-my-growth/$resource" "$shortcut_dir/$resource"
        done
        ln -s "../oh-my-growth/manifest.json" "$shortcut_dir/manifest.json"
    done
fi

echo -e "${GREEN}✓ Installed at $SKILL_DIR${NC}"
echo -e "${GREEN}✓ Try: /omg-diagnose test installation${NC}"
