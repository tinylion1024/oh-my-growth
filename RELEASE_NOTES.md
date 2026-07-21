# Release v1.0.2

## oh-my-growth 发布收口更新

v1.0.2 聚焦公开分发与社区增长，不新增策略框架。

### 修复内容

- 统一使用 `/omg-*` 命令格式。
- 恢复 README 案例与玩法自动索引。
- 统一 VERSION、Python 包、主 Skill、平台适配和快捷命令版本。
- 修复文档结构与命令契约校验。
- 新增 `scripts/release-check.sh` 发布门禁。
- 全量自动化检查恢复为 **98/98**。
- 新增三平台安装烟雾测试、反馈/决策样本池和输出质量 fixture 门禁。
- 将 PyPI 发行包名对齐为 `oh-my-growth`，并配置 GitHub Release 驱动的 Trusted Publishing 工作流。

### 核心命令

| 功能 | 命令 |
|------|------|
| 策略诊断 | `/omg-diagnose` |
| 机会评估 | `/omg-assess` |
| 策略设计 | `/omg-design` |
| 快速扫描 | `/omg-fast-scan` |
| 决策文档 | `/omg-brd` |
| 案例匹配 | `/omg-match` |
| 学习路径 | `/omg-learn` |
| 知识搜索 | `/omg-search` |
| 文档校验 | `/omg-validate` |

场景入口：`/omg-cold-start`、`/omg-retention`、`/omg-monetization`、`/omg-referral`。

### 发布验证

```bash
./scripts/release-check.sh
```

通过条件包括全量测试、Agent/文档/知识索引校验，以及版本和命令契约一致性检查。
