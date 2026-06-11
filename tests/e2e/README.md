# E2E Testing

端到端测试用于验证 Growth Master Skill 的输出质量。

## 目录结构

```
tests/e2e/
├── README.md                    # 本文件
├── test-scenarios.md            # 测试场景定义
├── E2E-TEST-SUMMARY.md          # 测试汇总
├── E2E-SCORE-OPTIMIZATION.md    # 优化计划
├── E2E-OPTIMIZATION-RESULT.md   # 优化结果
├── e2e-test-report.md           # 测试报告
├── e2e-test-summary.json        # 测试汇总数据
├── reports/                     # 测试报告
│   ├── e2e-test-scenario-01.md
│   ├── e2e-test-scenario-02.md
│   └── ...
└── verification/                # 验证结果
    ├── verification-01.json
    ├── verification-02.json
    └── ...
```

## 运行测试

```bash
# 从项目根目录运行
cd /path/to/growth-master-skill
python scripts/e2e_test_runner.py
```

## 测试场景

| # | 场景 | 核心问题 | 推荐命令 |
|---|------|----------|----------|
| 1 | SaaS冷启动 | 如何获取首批1000种子用户？ | diagnose |
| 2 | 电商复购 | 如何将复购率从15%提升到30%？ | diagnose + design |
| 3 | 教育完课率 | 如何通过游戏化提升完课率？ | design + match |
| 4 | 内容社区活跃 | 如何激活5万用户中的沉睡用户？ | assess + diagnose |
| 5 | 金融新功能推广 | 如何提升新功能渗透率？ | assess |
| 6 | 社交病毒传播 | 如何设计裂变降低CAC？ | fast-scan + match |
| 7 | B2B线索转化 | 如何优化线索到成单路径？ | diagnose |
| 8 | 订阅付费转化 | 如何提升付费转化率？ | diagnose + design |
| 9 | 本地生活商家冷启动 | 如何快速拓展1000家商家？ | diagnose + match |
| 10 | 游戏长期留存 | 如何解决7日留存暴跌问题？ | diagnose |

## 验证报告

```bash
# 验证单个报告
python scripts/verify_report.py -i tests/e2e/reports/e2e-test-scenario-01.md -o tests/e2e/verification/verification-01.json

# 验证所有报告
for i in 01 02 03 04 05 06 07 08 09 10; do
  python scripts/verify_report.py \
    -i "tests/e2e/reports/e2e-test-scenario-$i.md" \
    -o "tests/e2e/verification/verification-$i.json"
done
```

## 测试指标

- **Output Contract 合规性**: 10个必需章节
- **事实标记数量**: observed/estimated/assumed
- **评分**: 0-100 分，目标 85+

## 最新结果

| 指标 | 结果 |
|------|------|
| 平均分数 | 97.0/100 |
| 通过率 | 10/10 (100%) |
| 事实标记 | 44+ per report |

详见 [E2E-OPTIMIZATION-RESULT.md](./E2E-OPTIMIZATION-RESULT.md)
