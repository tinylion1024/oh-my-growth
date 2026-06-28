#!/bin/bash
#
# oh-my-growth 交互式 Onboarding 脚本
# 引导新用户完成首次成功时刻（5分钟体验）
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 清屏
clear

echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}   🚀 欢迎使用 oh-my-growth${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""
echo -e "${GREEN}让我们在 5 分钟内完成你的第一次增长诊断！${NC}"
echo ""
sleep 1

# 问题 1：产品阶段
echo -e "${YELLOW}Q1: 你的产品处于哪个阶段？${NC}"
echo ""
echo "  [1] 0-1 冷启动期（产品刚上线或即将上线）"
echo "  [2] 1-10 增长期（有一定的用户基础）"
echo "  [3] 10-100 规模化期（用户量快速增长）"
echo ""
read -p "请选择 [1-3]: " stage_choice

case $stage_choice in
    1)
        stage="cold-start"
        stage_name="冷启动期"
        ;;
    2)
        stage="growth"
        stage_name="增长期"
        ;;
    3)
        stage="scale"
        stage_name="规模化期"
        ;;
    *)
        stage="cold-start"
        stage_name="冷启动期"
        ;;
esac

echo ""
echo -e "${GREEN}✓ 已识别阶段: ${stage_name}${NC}"
sleep 1

# 问题 2：核心问题
echo ""
echo -e "${YELLOW}Q2: 你当前最关心的问题是什么？${NC}"
echo ""
echo "  [1] 获取用户（如何获得更多新用户）"
echo "  [2] 提升留存（如何让用户持续使用）"
echo "  [3] 提高变现（如何增加收入）"
echo "  [4] 降低流失（如何减少用户流失）"
echo ""
read -p "请选择 [1-4]: " problem_choice

case $problem_choice in
    1)
        problem="acquisition"
        problem_name="获取用户"
        ;;
    2)
        problem="retention"
        problem_name="提升留存"
        ;;
    3)
        problem="monetization"
        problem_name="提高变现"
        ;;
    4)
        problem="churn"
        problem_name="降低流失"
        ;;
    *)
        problem="acquisition"
        problem_name="获取用户"
        ;;
esac

echo ""
echo -e "${GREEN}✓ 已识别核心问题: ${problem_name}${NC}"
sleep 1

# 问题 3：行业（可选）
echo ""
echo -e "${YELLOW}Q3: 你的产品属于哪个行业？（可选，按回车跳过）${NC}"
echo ""
echo "  [1] SaaS / B2B"
echo "  [2] 电商 / 零售"
echo "  [3] 内容 / 社区"
echo "  [4] 教育 / 培训"
echo "  [5] 金融 / 支付"
echo "  [6] 其他"
echo ""
read -p "请选择 [1-6 或回车]: " industry_choice

case $industry_choice in
    1)
        industry="saas"
        industry_name="SaaS"
        ;;
    2)
        industry="ecommerce"
        industry_name="电商"
        ;;
    3)
        industry="content"
        industry_name="内容"
        ;;
    4)
        industry="education"
        industry_name="教育"
        ;;
    5)
        industry="fintech"
        industry_name="金融"
        ;;
    6)
        industry="other"
        industry_name="其他"
        ;;
    *)
        industry="saas"
        industry_name="通用"
        ;;
esac

echo ""
echo -e "${GREEN}✓ 已识别行业: ${industry_name}${NC}"
sleep 1

# 生成诊断问题
echo ""
echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}   🔍 正在为你生成个性化诊断...${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# 根据阶段和问题推荐命令
if [ "$stage" = "cold-start" ] && [ "$problem" = "acquisition" ]; then
    recommended_cmd="cold-start"
    example_question="如何获取首批1000用户"
elif [ "$stage" = "growth" ] && [ "$problem" = "retention" ]; then
    recommended_cmd="retention"
    example_question="如何提升30日留存率"
elif [ "$problem" = "monetization" ]; then
    recommended_cmd="monetization"
    example_question="如何设计产品定价策略"
elif [ "$problem" = "churn" ]; then
    recommended_cmd="retention"
    example_question="如何降低用户流失率"
else
    recommended_cmd="diagnose"
    example_question="增长策略建议"
fi

# 显示推荐
echo -e "${GREEN}📊 基于你的情况，我们推荐：${NC}"
echo ""
echo -e "  阶段: ${YELLOW}${stage_name}${NC}"
echo -e "  问题: ${YELLOW}${problem_name}${NC}"
echo -e "  行业: ${YELLOW}${industry_name}${NC}"
echo ""

echo -e "${GREEN}🎯 推荐命令：${NC}"
echo ""
echo -e "  ${CYAN}/omg-${recommended_cmd} ${example_question}${NC}"
echo ""

# 执行首次诊断
echo -e "${YELLOW}是否现在就尝试这个命令？${NC}"
echo ""
read -p "立即体验？[Y/n]: " try_now

if [[ "$try_now" =~ ^[Yy]$ ]] || [[ -z "$try_now" ]]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}   🎉 开始你的第一次增长诊断！${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${CYAN}请在 Claude Code 中输入以下命令：${NC}"
    echo ""
    echo -e "  ${YELLOW}/omg-${recommended_cmd} ${example_question}${NC}"
    echo ""
    echo -e "${GREEN}提示：你可以在命令后添加更多细节，例如：${NC}"
    echo -e "  ${YELLOW}/omg-${recommended_cmd} 我是做${industry_name}的，${example_question}，目前有XX用户${NC}"
    echo ""
fi

# 显示下一步建议
echo ""
echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}   📝 下一步建议${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""
echo -e "${GREEN}完成首次诊断后，你可以：${NC}"
echo ""
echo "  1. 📚 查看相似案例"
echo -e "     ${YELLOW}/omg-match ${example_question}${NC}"
echo ""
echo "  2. 🎯 深度评估可行性"
echo -e "     ${YELLOW}/omg-assess 应该先做什么实验${NC}"
echo ""
echo "  3. 📖 系统学习增长方法"
echo -e "     ${YELLOW}/omg-learn ${problem_name}策略${NC}"
echo ""

# 保存用户画像
CONFIG_DIR="$HOME/.oh-my-growth"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/user-profile.json" << EOF
{
  "created_at": "$(date -Iseconds)",
  "stage": "${stage}",
  "problem": "${problem}",
  "industry": "${industry}",
  "recommended_command": "omg-${recommended_cmd}",
  "first_diagnosis_completed": false
}
EOF

echo -e "${GREEN}✓ 用户画像已保存至: ${CONFIG_DIR}/user-profile.json${NC}"
echo ""

# 完成提示
echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}   ✨ 准备就绪！${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""
echo -e "${GREEN}你已准备好开始使用 oh-my-growth！${NC}"
echo ""
echo -e "📚 查看完整文档: ${YELLOW}https://github.com/tinylion1024/oh-my-growth${NC}"
echo -e "💬 加入社区: ${YELLOW}Discord（即将上线）${NC}"
echo -e "🐦 关注我们: ${YELLOW}@ohmygrowth on Twitter${NC}"
echo ""
echo -e "${GREEN}祝你的产品增长顺利！🚀${NC}"
echo ""
