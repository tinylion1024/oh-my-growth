#!/bin/bash

# Growth Master Installation Script
# 将Agent模板安装到目标项目

set -e

TARGET_DIR="${1:-.}"
AGENTS_DIR="$TARGET_DIR/.claude/agents"

echo "🚀 Installing Growth Master Agents..."

# 创建目标目录
mkdir -p "$AGENTS_DIR/core"
mkdir -p "$AGENTS_DIR/knowledge"

# 复制Agent文件
cp agents/core/*.md "$AGENTS_DIR/core/"
cp agents/knowledge/*.md "$AGENTS_DIR/knowledge/"

echo "✅ Agents installed to: $AGENTS_DIR"
echo ""
echo "Installed agents:"
ls -la "$AGENTS_DIR/core/"
ls -la "$AGENTS_DIR/knowledge/"
echo ""
echo "🎉 Installation complete!"
