# Hermes Agent 安装指南

## 安装 oh-my-growth 到 Hermes Agent

### 方式一：通过 Skills Hub 安装（推荐）

```bash
# 搜索技能
hermes skills search growth

# 安装技能
hermes skills install oh-my-growth
```

### 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 2. 复制到 Hermes skills 目录
mkdir -p ~/.hermes/skills/oh-my-growth
cp -R oh-my-growth/hermes/SKILL.md ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/knowledge ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.hermes/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.hermes/skills/oh-my-growth/

# 3. 安装 Python 依赖
pip install -r oh-my-growth/requirements.txt
```

### 方式三：符号链接（推荐开发时使用）

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 创建符号链接
mkdir -p ~/.hermes/skills/oh-my-growth
ln -s $(pwd)/oh-my-growth/hermes/SKILL.md ~/.hermes/skills/oh-my-growth/SKILL.md
ln -s $(pwd)/oh-my-growth/knowledge ~/.hermes/skills/oh-my-growth/knowledge
ln -s $(pwd)/oh-my-growth/references ~/.hermes/skills/oh-my-growth/references
ln -s $(pwd)/oh-my-growth/scripts ~/.hermes/skills/oh-my-growth/scripts
```

---

## 验证安装

在 Hermes Agent 中运行：

```
hermes skills list
```

应该看到 `oh-my-growth` 在列表中。

然后测试：

```
/omg-diagnose test installation
```

如果输出诊断结果，说明安装成功！

---

## 使用示例

### 核心命令

```bash
# 策略诊断
/omg-diagnose 如何获得前 1000 个用户

# 机会评估
/omg-assess 我们准备做裂变，先评估可行性

# 策略设计
/omg-design SaaS 产品如何设计变现策略

# 案例匹配
/omg-match 游戏化留存案例

# 学习路径
/omg-learn 如何系统学习裂变增长
```

### 场景快捷入口

```bash
# 冷启动
/omg-cold-start 如何获得 AI 写作 SaaS 的前 100 个付费用户

# 留存
/omg-retention 如何提升电商 APP 的 30 天留存率

# 变现
/omg-monetization 如何为内容社区设计变现策略

# 裂变
/omg-referral 我们的教育 APP 适合做裂变吗
```

---

## 目录结构

安装后的目录结构：

```
~/.hermes/skills/oh-my-growth/
├── SKILL.md              # Hermes 技能定义
├── knowledge/            # 知识库
│   ├── cases/           # 81 个案例
│   ├── weapons/         # 111 种玩法
│   ├── schools/         # 12 个流派
│   └── indexes/         # JSON 索引
├── references/           # 框架文档
└── scripts/              # Python 计算脚本
```

---

## 技能配置

### 启用/禁用技能

```bash
# 禁用技能
hermes skills disable oh-my-growth

# 启用技能
hermes skills enable oh-my-growth
```

### 按平台配置

编辑 `~/.hermes/config.yaml`:

```yaml
skills:
  disabled: []
  platform_disabled:
    telegram: [oh-my-growth]  # 在 Telegram 平台禁用
    cli: []                    # 在 CLI 平台启用
```

---

## 依赖要求

- Python 3.8+
- Hermes Agent

---

## 故障排除

### 问题：技能不显示

检查 SKILL.md 是否在正确位置：
```bash
ls ~/.hermes/skills/oh-my-growth/SKILL.md
```

### 问题：Python 脚本执行失败

检查 Python 依赖是否安装：
```bash
pip install -r ~/.hermes/skills/oh-my-growth/scripts/../requirements.txt
```

### 问题：知识库检索失败

检查 knowledge 目录是否存在：
```bash
ls ~/.hermes/skills/oh-my-growth/knowledge/
```

---

## 同时支持多个平台

oh-my-growth 支持以下平台：

| 平台 | 安装目录 | 状态 |
|------|----------|------|
| Claude Code | `~/.claude/skills/oh-my-growth/` | ✅ |
| OpenClaw | `~/.openclaw/skills/oh-my-growth/` | ✅ |
| Hermes Agent | `~/.hermes/skills/oh-my-growth/` | ✅ |

可以共享同一份知识库和脚本：

```bash
# 共享知识库
ln -s /path/to/oh-my-growth/knowledge ~/.claude/skills/oh-my-growth/
ln -s /path/to/oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/
ln -s /path/to/oh-my-growth/knowledge ~/.hermes/skills/oh-my-growth/
```
