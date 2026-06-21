# 测试套件

本目录包含脚本级自动化测试、场景资料和测试结果。

## 测试结构

```
tests/
├── agents/              # Agent 测试说明（Markdown 规范样例）
│   ├── test-lead-agent.md
│   ├── test-growth-agent.md
│   ├── test-monetization-agent.md
│   ├── test-roi-agent.md
│   ├── test-execution-agent.md
│   ├── test-skeptic-agent.md
│   ├── test-narrative-agent.md
│   ├── test-case-agent.md
│   ├── test-weapon-agent.md
│   └── test-theory-agent.md
├── e2e/                 # 场景资料与历史报告
├── scenarios/           # 业务场景素材
├── results/             # 自动生成的测试报告
├── test_bayesian_decision.py
├── test_cli_integration.py
├── test_knowledge_retriever.py
├── test_validation_scripts.py
└── run-tests.sh         # 测试入口（含校验脚本）
```

## 运行测试

```bash
# 运行所有测试
./tests/run-tests.sh

# 运行索引同步
python3 scripts/update-indexes.py

# 单独运行 CLI 测试
python3 scripts/run_tests.py

# 如需导出 Markdown 测试报告
python3 scripts/run_tests.py --report tests/results/test-report.md
```

## 测试标准

当前自动化覆盖：

- CLI 核心流程：`assess`、`diagnose`、场景快捷入口、`match`、`validate`
- 模式入口：`fast-scan`、`brd`、`learn`
- 分层输出：`executive` / `report` / `json` / `weekly` / `experiment-card` / `decision-memo` / `qbr`
- 结构化上下文：`--context-json`、`--profile-file`、`--history-file` 会进入策略判断
- 检索质量：案例、玩法、理论召回
- 策略质量：阶段匹配、主业务过程、失败模式、Game Theory / Kelly 触发
- Golden scenarios：基于 `tests/fixtures/strategy-golden-scenarios.json` 的高风险误判场景回归
- 验证脚本：`validate-agents.py`、`validate-docs.py`、`update-indexes.py`、`validate-indexes.py`
- 贝叶斯决策模块：阈值、证据更新、导出、边界保护
- 插件产品化：三平台安装烟雾、平台触发契约、反馈/决策样本池、输出质量 fixture

当前全量结果：`96/96` 自动化检查通过。
