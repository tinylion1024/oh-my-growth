# Contributing to oh-my-growth

感谢您考虑为 oh-my-growth 做贡献！🎉

## 📋 目录

- [快速开始](#-快速开始)
- [开发环境设置](#-开发环境设置)
- [项目结构](#-项目结构)
- [如何贡献](#-如何贡献)
- [开发指南](#-开发指南)
- [提交规范](#-提交规范)

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Git
- Claude Code（用于测试插件）

### 安装步骤

```bash
# 1. Fork 并克隆仓库
git clone https://github.com/YOUR_USERNAME/oh-my-growth.git
cd oh-my-growth

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 运行测试验证环境
python3 scripts/run_tests.py
```

---

## 🛠️ 开发环境设置

### 安装到 Claude Code

在开发时，将插件安装到本地 Claude Code：

```bash
# 创建符号链接（推荐）
ln -s $(pwd) ~/.claude/skills/oh-my-growth

# 或直接复制
cp -R . ~/.claude/skills/oh-my-growth
```

### 验证安装

在 Claude Code 中运行：

```
/omg-diagnose test installation
```

如果输出诊断结果，说明安装成功！

---

## 📁 项目结构

```
oh-my-growth/
├── SKILL.md              # 插件入口（Claude Code 加载此文件）
├── manifest.json         # 插件元数据
├── agents/               # Agent 定义
│   ├── core/            # 核心决策 Agent（7个）
│   └── knowledge/       # 知识检索 Agent（4个）
├── knowledge/           # 知识库
│   ├── cases/          # 81个增长案例
│   ├── weapons/        # 111种增长玩法
│   ├── schools/        # 12大流派理论
│   └── indexes/        # JSON 索引
├── scripts/             # Python 计算脚本
│   ├── bayesian.py     # 贝叶斯决策
│   ├── kelly.py        # Kelly 资源分配
│   ├── cli.py          # CLI 入口
│   └── run_tests.py    # 测试运行器
├── skills/              # 子技能定义（13个）
├── references/          # 框架文档
├── templates/           # 输出模板
└── tests/               # 测试套件
```

---

## 🤝 如何贡献

### 报告 Bug

1. 搜索 [existing issues](https://github.com/tinylion1024/oh-my-growth/issues) 确认未重复
2. 使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.yml) 创建 Issue
3. 提供清晰的复现步骤和预期行为

### 提交新功能

1. 先开 Issue 讨论功能想法
2. 使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.yml) 描述功能
3. 等待维护者反馈后再开始实现

### 提交代码

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 进行更改并添加测试
4. 运行测试：`python3 scripts/run_tests.py`
5. 提交更改：`git commit -m "feat: add your feature"`
6. 推送分支：`git push origin feature/your-feature`
7. 创建 Pull Request

### 添加新案例

在 `knowledge/cases/` 目录下创建新的 Markdown 文件：

```markdown
---
id: case-xxx
title: 案例标题
industry: [saas|consumer|marketplace]
stage: [0-1|1-10|10-100]
problem: [acquisition|retention|monetization|referral]
evidence: [A|B|C|D|E]
tags: [tag1, tag2, tag3]
---

## 背景
描述公司和产品背景...

## 问题
遇到的具体增长问题...

## 解决方案
实施的策略和方法...

## 结果
量化结果和关键学习...

## 关键启示
其他产品可借鉴的要点...
```

### 添加新玩法

在 `knowledge/weapons/` 目录下创建新的 Markdown 文件：

```markdown
---
id: weapon-xxx
name: 玩法名称
category: [acquisition|retention|monetization|referral]
difficulty: [low|medium|high]
prerequisites: [前置条件]
---

## 概述
一句话描述玩法...

## 适用场景
- 场景1
- 场景2

## 执行步骤
1. 步骤1
2. 步骤2

## 关键指标
- 指标1: 说明
- 指标2: 说明

## 常见坑点
- 坑点1: 如何避免
- 坑点2: 如何避免

## 案例参考
- [案例A](../cases/case-xxx.md)
```

---

## 📏 开发指南

### 代码风格

- 遵循 [PEP 8](https://pep8.org/)
- 使用 Black 格式化：`black scripts/`
- 使用 Ruff 检查：`ruff check scripts/`

### 测试要求

- 所有新功能必须添加测试
- 运行测试套件：`python3 scripts/run_tests.py`
- 确保所有 84+ 测试通过

### 文档规范

- Markdown 文件使用 UTF-8 编码
- 保持中英文文档同步更新
- 使用清晰的标题层级

### Agent 定义规范

Agent 定义文件使用 YAML frontmatter + Markdown 格式：

```markdown
---
name: agent-name
role: Agent 角色描述
triggers:
  - trigger1
  - trigger2
outputs:
  - output1
  - output2
---

# Agent Name

## Responsibility
详细描述 Agent 的职责...

## Inputs
需要的输入...

## Outputs
输出的内容...

## Decision Rules
决策规则...
```

---

## 📝 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>: <description>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: add Kelly sizing for experiments` |
| `fix` | Bug 修复 | `fix: correct Bayesian prior calculation` |
| `docs` | 文档更新 | `docs: add usage examples for diagnose` |
| `test` | 测试相关 | `test: add unit tests for kelly.py` |
| `refactor` | 代码重构 | `refactor: extract formatting from strategy` |
| `perf` | 性能优化 | `perf: optimize knowledge index lookup` |
| `chore` | 杂项 | `chore: update dependencies` |

### 示例

```bash
# 新增案例
git commit -m "feat(cases): add Notion PLG case study"

# 修复 Bug
git commit -m "fix(bayesian): correct posterior calculation for edge cases"

# 更新文档
git commit -m "docs: clarify Kelly criterion usage in README"
```

---

## 🧪 运行测试

```bash
# 运行所有测试
python3 scripts/run_tests.py

# 运行特定测试
python3 -m pytest tests/test_cli_integration.py -v

# 验证 Agent 定义
python3 scripts/validate-agents.py

# 验证知识库索引
python3 scripts/validate-indexes.py
```

---

## 📚 相关文档

- [README.md](./README.md) - 项目概述和快速开始
- [SKILL.md](./SKILL.md) - 插件完整定义
- [使用示例](./docs/USAGE_EXAMPLES.md) - 每个命令的详细使用场景
- [开发指南](./docs/developer-guide.md) - 更详细的开发文档

---

## ❓ 有问题？

- 📖 查看 [文档](./docs/)
- 🐛 提交 [Issue](https://github.com/tinylion1024/oh-my-growth/issues)
- 💬 在 [Discussions](https://github.com/tinylion1024/oh-my-growth/discussions) 讨论

---

感谢您的贡献！🙏
