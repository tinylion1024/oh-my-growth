# Release v1.0.0

## 🎉 oh-my-growth - 增长策略外脑

**Claude Code 专用增长决策插件** — 输入增长问题，输出诊断、优先级判断、实验计划。

---

## 🚀 首次发布

这是 oh-my-growth 的首次正式发布！

### 核心功能

| 功能 | 命令 | 描述 |
|------|------|------|
| 策略诊断 | `/omg diagnose` | 诊断增长问题，输出优先级和实验建议 |
| 机会评估 | `/omg assess` | 评估是否值得深入分析 |
| 策略设计 | `/omg design` | 可落地的策略执行路径 |
| 快速扫描 | `/omg fast-scan` | 快速判断想法是否靠谱 |
| 决策文档 | `/omg brd` | 完整决策文档，用于申请预算 |
| 案例匹配 | `/omg match` | 找到可借鉴的成功案例 |
| 学习路径 | `/omg learn` | 系统学习某个增长领域 |

**场景快捷入口**：`/omg cold-start` | `/omg retention` | `/omg monetization` | `/omg referral`

---

## 📚 知识库

| 类型 | 数量 |
|------|------|
| 增长案例 | 81 |
| 增长玩法 | 111 |
| 理论流派 | 12 |
| 学习模块 | 7 |

---

## 🧠 决策框架

- **贝叶斯决策引擎** - 概率推理，量化置信度
- **Kelly 资源分配** - 最优投资比例计算
- **博弈论分析** - 竞争态势判断
- **证据分级系统** - A/B/C/D/E 五级证据评级

---

## 🧪 测试状态

- **82/84 测试通过** ✅

---

## 📖 文档

- [README.md](./README.md) - 项目概述和快速开始
- [使用示例](./docs/USAGE_EXAMPLES.md) - 每个命令的详细使用场景
- [CONTRIBUTING.md](./CONTRIBUTING.md) - 贡献指南
- [SKILL.md](./SKILL.md) - 插件完整定义

---

## 📥 安装

### 方式一：一键安装（推荐）

```bash
cd oh-my-growth
./scripts/install.sh
```

### 方式二：手动安装

```bash
git clone https://github.com/tinylion1024/oh-my-growth.git
cp -R oh-my-growth ~/.claude/skills/oh-my-growth
```

### 验证安装

在 Claude Code 中运行：

```
/omg diagnose test installation
```

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解如何：

- 报告 Bug
- 提交新功能建议
- 添加案例和玩法
- 贡献代码

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

**Built with ❤️ by Growth Master Team**
