# Agent 测试套件

本目录包含所有 Agent 的测试用例和测试结果。

## 测试结构

```
tests/
├── agents/              # Agent 单元测试
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
├── scenarios/           # 场景集成测试
│   ├── saas-acquisition.md
│   ├── ecommerce-retention.md
│   ├── content-growth.md
│   └── viral-referral.md
├── results/             # 测试结果
│   └── expected-outputs/
└── run-tests.sh         # 测试运行脚本
```

## 运行测试

```bash
# 运行所有测试
./tests/run-tests.sh

# 运行单个 Agent 测试
./tests/run-tests.sh agents/test-lead-agent.md

# 运行场景测试
./tests/run-tests.sh scenarios/saas-acquisition.md
```

## 测试标准

每个测试用例必须包含：

1. **输入定义**：明确的输入 JSON
2. **预期输出**：期望的输出结构
3. **验证点**：关键的验证检查
4. **边界情况**：异常输入处理
