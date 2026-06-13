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
OMG_DIR="$HOME/.claude/skills/omg"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   oh-my-growth - 增长策略外脑 安装程序${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# 检查是否已安装
if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}检测到已存在 oh-my-growth，将进行更新...${NC}"
    rm -rf "$SKILL_DIR"
fi

if [ -d "$OMG_DIR" ]; then
    echo -e "${YELLOW}检测到已存在 omg 别名，将进行更新...${NC}"
    rm -rf "$OMG_DIR"
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

# 创建 omg 别名
echo -e "${GREEN}正在创建 /omg 别名...${NC}"
mkdir -p "$OMG_DIR"

# 复制 omg SKILL.md
if [ -f "$SOURCE_DIR/omg/SKILL.md" ]; then
    cp "$SOURCE_DIR/omg/SKILL.md" "$OMG_DIR/SKILL.md"
else
    # 如果项目中没有 omg/SKILL.md，则动态创建
    cat > "$OMG_DIR/SKILL.md" << 'OMGSKILL'
---
name: omg
description: 增长策略外脑 - Claude Code 专用增长决策插件。整合81个案例、111种玩法、12大流派，输出诊断、优先级判断、建议做/不做与实验计划。
metadata:
  author: Growth Master Team
  maturity: production
  version: 4.0.0
  license: MIT
  category: business-strategy
  alias_for: oh-my-growth
---

# omg - oh-my-growth 别名

这是 `/oh-my-growth` 的缩写别名，提供相同的功能。

## 快速开始

```
/omg diagnose 我的产品日活下降20%，该怎么办？
/omg assess 我们准备做裂变，先评估可行性
/omg design SaaS产品如何设计变现策略？
/omg match 游戏化留存案例
```

## 可用命令

| 命令 | 用途 |
|------|------|
| `/omg diagnose` | 诊断+优先级+实验建议 |
| `/omg assess` | 评估可行性 |
| `/omg design` | 策略设计 |
| `/omg match` | 案例匹配 |
| `/omg learn` | 学习路径 |
| `/omg cold-start` | 冷启动场景 |
| `/omg retention` | 留存策略 |
| `/omg monetization` | 变现策略 |
| `/omg referral` | 裂变策略 |

完整文档请查看 [oh-my-growth SKILL.md](../oh-my-growth/SKILL.md)
OMGSKILL
fi

# 创建符号链接指向主目录的资源
cd "$OMG_DIR"
ln -sf ../oh-my-growth/knowledge knowledge
ln -sf ../oh-my-growth/scripts scripts
ln -sf ../oh-my-growth/agents agents
ln -sf ../oh-my-growth/references references
ln -sf ../oh-my-growth/templates templates
ln -sf ../oh-my-growth/manifest.json manifest.json

echo -e "${GREEN}✓ /omg 别名已创建${NC}"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   安装完成！${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "安装位置: ${YELLOW}$SKILL_DIR${NC}"
echo -e "别名位置: ${YELLOW}$OMG_DIR${NC}"
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
