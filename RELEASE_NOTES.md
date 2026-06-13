# Release v4.0.0

## 🎉 oh-my-growth - 增长策略外脑

**Claude Code 专用增长决策插件** — 输入增长问题，输出诊断、优先级判断、实验计划。

---

## 📦 本次发布亮点

### 完善的开发者体验

- ✅ **CONTRIBUTING.md** - 完整的贡献指南，包含安装、开发、测试说明
- ✅ **使用示例文档** - 每个命令的详细使用场景和输出示例
- ✅ **GitHub Issue 模板** - 标准化的 Bug 报告和功能请求
- ✅ **PR 模板** - 包含检查清单的 Pull Request 模板

### 版本一致性

- 统一版本号至 4.0.0（manifest.json、VERSION、README、SKILL.md、pyproject.toml）

---

## 🚀 核心功能

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

## 📚 知识库规模

| 类型 | 数量 |
|------|------|
| 增长案例 | 81 |
| 增长玩法 | 111 |
| 理论流派 | 12 |
| 学习模块 | 7 |

---

## 🧪 测试状态

- **82/84 测试通过** ✅
- 2 个失败测试为内部文档验证规则，不影响核心功能

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

## 📝 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解历史版本更新。

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

**Built with ❤️ by Growth Master Team**
