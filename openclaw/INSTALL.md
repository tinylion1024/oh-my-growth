# OpenClaw 安装指南

## 安装 oh-my-growth 到 OpenClaw

### 方式一：克隆安装

```bash
# 1. 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 2. 复制到 OpenClaw skills 目录
cp -R oh-my-growth/openclaw ~/.openclaw/skills/oh-my-growth

# 3. 复制知识库
cp -R oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.openclaw/skills/oh-my-growth/

# 4. 安装 Python 依赖
cd ~/.openclaw/skills/oh-my-growth
pip install -r requirements.txt
```

### 方式二：符号链接（推荐开发时使用）

```bash
# 克隆仓库
git clone https://github.com/tinylion1024/oh-my-growth.git

# 创建符号链接
ln -s $(pwd)/oh-my-growth/openclaw ~/.openclaw/skills/oh-my-growth
ln -s $(pwd)/oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/knowledge
ln -s $(pwd)/oh-my-growth/references ~/.openclaw/skills/oh-my-growth/references
ln -s $(pwd)/oh-my-growth/scripts ~/.openclaw/skills/oh-my-growth/scripts
```

---

## 验证安装

在 OpenClaw 中运行：

```
/oh-my-growth diagnose test installation
```

如果输出诊断结果，说明安装成功！

---

## 使用示例

### 核心命令

```bash
# 策略诊断
/oh-my-growth diagnose 如何获得前 1000 个用户

# 机会评估
/oh-my-growth assess 我们准备做裂变，先评估可行性

# 策略设计
/oh-my-growth design SaaS 产品如何设计变现策略

# 案例匹配
/oh-my-growth match 游戏化留存案例

# 学习路径
/oh-my-growth learn 如何系统学习裂变增长
```

### 场景快捷入口

```bash
# 冷启动
/oh-my-growth cold-start 如何获得 AI 写作 SaaS 的前 100 个付费用户

# 留存
/oh-my-growth retention 如何提升电商 APP 的 30 天留存率

# 变现
/oh-my-growth monetization 如何为内容社区设计变现策略

# 裂变
/oh-my-growth referral 我们的教育 APP 适合做裂变吗
```

---

## 目录结构

安装后的目录结构：

```
~/.openclaw/skills/oh-my-growth/
├── SKILL.md              # OpenClaw 技能定义
├── knowledge/            # 知识库
│   ├── cases/           # 81 个案例
│   ├── weapons/         # 111 种玩法
│   ├── schools/         # 12 个流派
│   └── indexes/         # JSON 索引
├── references/           # 框架文档
├── scripts/              # Python 计算脚本
└── requirements.txt      # Python 依赖
```

---

## 依赖要求

- Python 3.8+
- OpenClaw

---

## 故障排除

### 问题：命令不识别

检查 SKILL.md 是否在正确位置：
```bash
ls ~/.openclaw/skills/oh-my-growth/SKILL.md
```

### 问题：Python 脚本执行失败

检查 Python 依赖是否安装：
```bash
pip install -r ~/.openclaw/skills/oh-my-growth/requirements.txt
```

### 问题：知识库检索失败

检查 knowledge 目录是否存在：
```bash
ls ~/.openclaw/skills/oh-my-growth/knowledge/
```

---

## 同时支持 Claude Code 和 OpenClaw

如果您同时使用 Claude Code 和 OpenClaw：

```bash
# Claude Code 安装
cp -R oh-my-growth ~/.claude/skills/oh-my-growth

# OpenClaw 安装
cp -R oh-my-growth/openclaw ~/.openclaw/skills/oh-my-growth
cp -R oh-my-growth/knowledge ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/references ~/.openclaw/skills/oh-my-growth/
cp -R oh-my-growth/scripts ~/.openclaw/skills/oh-my-growth/
```

两个平台可以共享同一份知识库和脚本。
