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

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   安装完成！${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "安装位置: ${YELLOW}$SKILL_DIR${NC}"
echo -e "别名位置: ${YELLOW}$OMG_ALIAS -> $SKILL_DIR${NC}"
echo ""
echo -e "${GREEN}快速开始:${NC}"
echo -e "  在 Claude Code 中输入:"
echo ""
echo -e "  ${YELLOW}/oh-my-growth diagnose 我的产品日活下降，该怎么办？${NC}"
echo -e "  ${YELLOW}/omg diagnose 我的产品日活下降，该怎么办？${NC}"
echo ""
echo -e "  ${YELLOW}/oh-my-growth assess 我们准备做裂变，先评估可行性${NC}"
echo -e "  ${YELLOW}/omg assess 我们准备做裂变，先评估可行性${NC}"
echo ""
echo -e "${GREEN}功能特性:${NC}"
echo -e "  • 81个增长案例（中国/海外/垂直行业）"
echo -e "  • 111种增长玩法（冷启动/裂变/内容/留存...）"
echo -e "  • 12大增长理论流派"
echo -e "  • 贝叶斯决策引擎"
echo -e "  • 博弈论竞争分析"
echo -e "  • Kelly资源分配"
echo ""
