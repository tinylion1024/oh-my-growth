#!/bin/bash
#
# oh-my-growth 安装脚本
# 将增长策略外脑安装为 Claude Code skill
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 目标目录
SKILL_DIR="$HOME/.claude/skills/oh-my-growth"
OMG_ALIAS="$HOME/.claude/skills/omg"
SKILLS_ROOT="$HOME/.claude/skills"

# 子命令列表
SUBCOMMANDS=(
  "diagnose"
  "assess"
  "design"
  "brd"
  "match"
  "learn"
  "search"
  "validate"
  "fast-scan"
  "cold-start"
  "retention"
  "monetization"
  "referral"
)

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   oh-my-growth - 增长策略外脑 安装程序${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 检查是否已安装
if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}检测到已存在 oh-my-growth，将进行更新...${NC}"
    rm -rf "$SKILL_DIR"
fi

# 清理旧别名（如果存在）
if [ -L "$OMG_ALIAS" ] || [ -d "$OMG_ALIAS" ]; then
    echo -e "${YELLOW}清理旧别名...${NC}"
    rm -rf "$OMG_ALIAS"
fi

# 清理旧的子命令 skill
for cmd in "${SUBCOMMANDS[@]}"; do
    skill_path="$SKILLS_ROOT/omg-${cmd}"
    if [ -L "$skill_path" ] || [ -d "$skill_path" ]; then
        rm -rf "$skill_path"
    fi
done

# 创建目标目录
mkdir -p "$SKILL_DIR"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"

# 复制文件
echo -e "${GREEN}正在安装 oh-my-growth...${NC}"
cp -r "$SOURCE_DIR"/* "$SKILL_DIR/"

# 验证安装
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo -e "${GREEN}✓ SKILL.md 已安装${NC}"
else
    echo -e "${RED}✗ 安装失败：SKILL.md 未找到${NC}"
    exit 1
fi

if [ -d "$SKILL_DIR/knowledge" ]; then
    echo -e "${GREEN}✓ 知识库已安装${NC}"
else
    echo -e "${RED}✗ 安装失败：知识库未找到${NC}"
    exit 1
fi

if [ -d "$SKILL_DIR/scripts" ]; then
    echo -e "${GREEN}✓ 决策引擎已安装${NC}"
else
    echo -e "${RED}✗ 安装失败：决策引擎未找到${NC}"
    exit 1
fi

# 创建 /omg 别名
echo -e "${GREEN}正在创建 /omg 别名...${NC}"
ln -s "$SKILL_DIR" "$OMG_ALIAS"
echo -e "${GREEN}✓ /omg 别名已创建${NC}"

# 创建子命令 skill 目录
echo -e "${GREEN}正在创建快捷命令...${NC}"
for cmd in "${SUBCOMMANDS[@]}"; do
    skill_path="$SKILLS_ROOT/omg-${cmd}"
    skill_file="$SKILL_DIR/skills/omg-${cmd}.md"

    mkdir -p "$skill_path"

    if [ -f "$skill_file" ]; then
        cp "$skill_file" "$skill_path/SKILL.md"
    else
        # 动态创建 SKILL.md
        cat > "$skill_path/SKILL.md" << EOF
---
name: omg-${cmd}
description: oh-my-growth ${cmd} 快捷命令
metadata:
  author: Growth Master Team
  version: 1.0.1
  category: growth-strategy
  parent: oh-my-growth
---

# omg-${cmd}

\`/omg-${cmd}\` 快捷命令。

## 用法

\`\`\`
/omg-${cmd} <问题描述>
\`\`\`

## 示例

\`\`\`
/omg-${cmd} 我的产品日活下降20%，该怎么办？
\`\`\`

完整文档请查看 [oh-my-growth](../oh-my-growth/SKILL.md)
EOF
    fi

    # 创建符号链接指向主目录资源
    cd "$skill_path"
    ln -sf ../oh-my-growth/knowledge knowledge
    ln -sf ../oh-my-growth/scripts scripts
    ln -sf ../oh-my-growth/agents agents
    ln -sf ../oh-my-growth/references references
    ln -sf ../oh-my-growth/manifest.json manifest.json
done

echo -e "${GREEN}✓ 快捷命令已创建${NC}"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   安装完成！${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "安装位置: ${YELLOW}$SKILL_DIR${NC}"
echo ""
echo -e "${GREEN}可用命令:${NC}"
echo -e "  ${YELLOW}/omg-diagnose${NC}    策略诊断"
echo -e "  ${YELLOW}/omg-assess${NC}      机会评估"
echo -e "  ${YELLOW}/omg-design${NC}      策略设计"
echo -e "  ${YELLOW}/omg-brd${NC}         决策文档"
echo -e "  ${YELLOW}/omg-match${NC}       案例匹配"
echo -e "  ${YELLOW}/omg-learn${NC}       学习路径"
echo -e "  ${YELLOW}/omg-search${NC}      知识搜索"
echo -e "  ${YELLOW}/omg-validate${NC}    文档验证"
echo -e "  ${YELLOW}/omg-fast-scan${NC}   快速扫描"
echo -e "  ${YELLOW}/omg-cold-start${NC}  冷启动策略"
echo -e "  ${YELLOW}/omg-retention${NC}   留存策略"
echo -e "  ${YELLOW}/omg-monetization${NC} 变现策略"
echo -e "  ${YELLOW}/omg-referral${NC}    裂变策略"
echo ""
echo -e "${GREEN}功能特性:${NC}"
echo -e "  • 81个增长案例（中国/海外/垂直行业）"
echo -e "  • 111种增长玩法（冷启动/裂变/内容/留存...）"
echo -e "  • 12大增长理论流派"
echo -e "  • 贝叶斯决策引擎"
echo -e "  • 博弈论竞争分析"
echo -e "  • Kelly资源分配"
echo ""
