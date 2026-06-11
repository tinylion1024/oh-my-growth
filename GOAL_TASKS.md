# Goal 任务拆分：增长策略外脑升级

> 原始提示词无法收敛的原因：8个项目级改造混在一起，验收标准模糊，优先级依赖被忽略。
>
> 本文档将其拆分为独立、可执行、有明确验收标准的 Goal 任务。

---

## 优先级与依赖关系

```
阶段 1：产品契约对齐
    ↓
阶段 2：检索排序增强
    ↓
阶段 3：证据驱动判断
    ↓
阶段 4：策略质量评测
    ↓
阶段 5：上下文记忆
    ↓
阶段 6：输出产品化
    ↓
阶段 7：框架资产接入
    ↓
阶段 8：知识系统可维护性
```

---

## 任务 1：产品契约对齐（P0）

### 目标
让 README、SKILL.md、CLI 三方能力描述一致

### 范围
- 只改文档和 CLI 帮助文本
- 不动核心逻辑

### 验收标准（必须全部满足）
- [ ] README 中提到的每个模式（Fast Scan、Decision BRD、Learning Path）在 CLI 中都有对应命令
- [ ] `python scripts/cli.py --help` 输出的命令列表与 README 描述一致
- [ ] SKILL.md 的"七个核心入口"表格与 CLI 命令一一对应
- [ ] 无文档承诺但未实现的命令

### 执行步骤
```bash
# 1. 提取 README 中提到的所有模式
grep -E "(Fast Scan|Decision BRD|Learning Path|Strategy Brain|Case Match)" README.md

# 2. 检查 CLI 是否都有实现
python scripts/cli.py --help

# 3. 对每个未实现的模式：
#    - 要么在 CLI 中添加命令
#    - 要么在 README 中删除该描述

# 4. 同步 SKILL.md
# 确保与 README 和 CLI 保持一致
```

### 完成定义
运行以下命令无差异：
```bash
# 提取 README 模式名
grep -oE "(diagnose|assess|design|fast-scan|brd|match|learn|search|validate)" README.md | sort -u

# 提取 CLI 命令
python scripts/cli.py --help 2>&1 | grep -oP "(?<=\{).*(?=\})" | tr ',' '\n' | tr -d ' ' | sort -u

# 两者应该完全一致
```

---

## 任务 2：阶段感知检索（P0）

### 目标
让检索结果根据 `--stage` 参数返回不同的建议

### 范围
- 只改 `knowledge_retriever.py` 的排序函数
- 增加阶段权重因子

### 验收标准
- [ ] 相同问题，不同 `--stage` 参数，Top3 推荐有差异
- [ ] 0-1 阶段优先返回冷启动相关案例
- [ ] 1-10 阶段优先返回规模化相关案例
- [ ] 10+ 阶段优先返回精细化运营相关案例

### 执行步骤
```bash
# 1. 测试当前行为
python scripts/cli.py diagnose "如何获取用户" --stage 0-1 --problem acquisition
python scripts/cli.py diagnose "如何获取用户" --stage 1-10 --problem acquisition
python scripts/cli.py diagnose "如何获取用户" --stage 10+ --problem acquisition

# 2. 修改 knowledge_retriever.py
# 在排序函数中增加 stage_fit 权重

# 3. 验证差异
python scripts/cli.py diagnose "如何获取用户" --stage 0-1 --problem acquisition --view json | jq '.top_recommendations[0]'
python scripts/cli.py diagnose "如何获取用户" --stage 1-10 --problem acquisition --view json | jq '.top_recommendations[0]'
# 两个输出应该不同
```

### 完成定义
```bash
# 运行 Golden 测试
python -m pytest tests/test_strategy_golden.py::test_stage_awareness -v
# 应该通过
```

---

## 任务 3：增加证据链字段（P0）

### 目标
策略输出中显式展示判断依据

### 范围
- 只改 `strategy_brain.py` 的输出格式
- 增加 `evidence_chain` 字段

### 验收标准
- [ ] `diagnose` 命令输出包含 `evidence_chain` 数组
- [ ] 每个建议至少有 1 条 evidence
- [ ] evidence 包含：source（来源）、type（类型：case/weapon/theory）、confidence（置信度）

### 输出示例
```json
{
  "recommendation": "Beta邀请制",
  "evidence_chain": [
    {
      "source": "Dropbox案例",
      "type": "case",
      "confidence": "B",
      "summary": "通过邀请制实现快速增长"
    },
    {
      "source": "PLG理论",
      "type": "theory",
      "confidence": "B",
      "summary": "产品驱动增长适用于SaaS冷启动"
    }
  ]
}
```

### 执行步骤
```bash
# 1. 运行命令查看当前输出
python scripts/cli.py diagnose "SaaS产品如何获取首批用户" --view json

# 2. 修改 strategy_brain.py
# 在输出构建函数中增加 evidence_chain 字段

# 3. 验证
python scripts/cli.py diagnose "SaaS产品如何获取首批用户" --view json | jq '.evidence_chain'
# 应该返回数组，非空
```

### 完成定义
```bash
# 运行测试
python -m pytest tests/test_strategy_quality.py::test_evidence_chain_present -v
# 应该通过
```

---

## 任务 4：策略质量评测（P0）

### 目标
验证判断质量，不只是格式完整

### 范围
- 新增测试文件 `tests/test_strategy_quality.py`
- 测试判断逻辑，不是测试命令能跑通

### 验收标准
- [ ] 测试：Top1 推荐符合阶段约束
- [ ] 测试：不推荐违背约束线的建议
- [ ] 测试：高成本动作在低预算时被降权
- [ ] 测试：错阶段动作被识别

### 测试用例
```python
# tests/test_strategy_quality.py

def test_top1_matches_stage():
    """Top1 推荐应该符合阶段"""
    result = run_diagnose("如何获取用户", stage="0-1", problem="acquisition")
    top1 = result["top_recommendations"][0]
    assert top1["stage_fit"] in ["0-1", "all"]

def test_no_constraint_violation():
    """不推荐违背约束线的建议"""
    result = run_diagnose("如何获取用户", stage="0-1", budget="1万")
    for rec in result["top_recommendations"]:
        assert "预算不足" not in rec.get("warnings", [])

def test_high_cost_demoted_in_low_budget():
    """高成本动作在低预算时被降权"""
    result_low = run_diagnose("如何获客", budget="1万")
    result_high = run_diagnose("如何获客", budget="100万")

    # 低预算时，付费广告应该排名更低
    # 高预算时，付费广告可以排更高
    # 具体逻辑根据实际业务规则实现

def test_wrong_stage_identified():
    """错阶段动作被识别"""
    result = run_diagnose("如何做大规模裂变", stage="0-1")
    # 0-1 阶段不应该推荐大规模裂变
    assert not any(
        "大规模" in rec.get("name", "")
        for rec in result["top_recommendations"][:3]
    )
```

### 完成定义
```bash
python -m pytest tests/test_strategy_quality.py -v
# 所有测试通过
```

---

## 任务 5：项目记忆注入（P1）

### 目标
支持 company profile / experiment log / history file

### 范围
- CLI 已支持 `--profile-file` 和 `--history-file`
- 需要验证这些数据真正进入判断链路

### 验收标准
- [ ] 提供 profile 时，输出中引用公司画像信息
- [ ] 提供 history 时，输出中引用历史实验
- [ ] 历史失败实验进入 `avoid_now` 列表

### 执行步骤
```bash
# 1. 创建测试用 profile
cat > /tmp/test-profile.json << 'EOF'
{
  "company_name": "测试公司",
  "industry": "saas",
  "stage": "0-1",
  "team_size": 5,
  "budget": "10万"
}
EOF

# 2. 创建测试用 history
cat > /tmp/test-history.json << 'EOF'
{
  "experiments": [
    {
      "name": "付费广告",
      "outcome": "失败",
      "lesson": "预算不足，ROI太低"
    }
  ]
}
EOF

# 3. 运行诊断
python scripts/cli.py diagnose "如何获客" \
  --profile-file /tmp/test-profile.json \
  --history-file /tmp/test-history.json \
  --view json

# 4. 检查输出
# - 应该引用公司画像
# - "付费广告"应该在 avoid_now 或被降权
```

### 完成定义
```bash
python -m pytest tests/test_cli_integration.py::test_profile_history_integration -v
# 应该通过
```

---

## 任务 6：输出视图产品化（P1）

### 目标
增加更贴近实际工作的视图

### 范围
- 新增视图：`weekly`、`experiment-card`、`decision-memo`、`qbr`
- CLI 已支持这些视图，需要验证输出质量

### 验收标准
- [ ] `weekly` 视图：输出周会摘要格式，包含负责人、本周不做什么
- [ ] `experiment-card` 视图：输出实验卡格式，包含假设、步骤、成功/停止信号
- [ ] `decision-memo` 视图：输出决策备忘录格式
- [ ] `qbr` 视图：输出季度经营摘要，包含 Kelly 预算建议

### 执行步骤
```bash
# 测试每个视图
python scripts/cli.py diagnose "如何获客" --view weekly
python scripts/cli.py diagnose "如何获客" --view experiment-card
python scripts/cli.py diagnose "如何获客" --view decision-memo
python scripts/cli.py diagnose "如何获客" --budget "50万" --view qbr

# 检查输出是否符合预期格式
```

### 完成定义
```bash
# 每个视图都有对应的格式验证测试
python -m pytest tests/test_cli_integration.py -k "weekly or experiment_card or decision_memo or qbr" -v
```

---

## 任务 7：框架资产接入验证（P1）

### 目标
验证 Kelly、Game Theory 是否真正进入主链路

### 范围
- 不新增功能
- 验证现有功能是否真正被使用

### 验收标准
- [ ] 提供预算时，输出包含 Kelly 建议字段
- [ ] 竞争/平台场景下，输出包含 Game Theory 分析
- [ ] 以上信息在 `diagnose` 和 `qbr` 视图中可见

### 执行步骤
```bash
# 1. 测试 Kelly
python scripts/cli.py diagnose "如何获客" --budget "50万" --view json | jq '.kelly_result'
# 应该有输出

# 2. 测试 Game Theory
python scripts/cli.py diagnose "如何应对竞争对手降价" \
  --context-json '{"competitors":["竞品A"],"market_structure":"oligopoly"}' \
  --view json | jq '.gametheory_result'
# 应该有输出
```

### 完成定义
```bash
python -m pytest tests/test_kelly_integration.py tests/test_gametheory_integration.py -v
# 测试通过
```

---

## 任务 8：知识系统可维护性（P2）

### 目标
增加文档结构校验、链接校验、schema 校验

### 范围
- 新增或强化校验脚本
- 不影响主流程

### 验收标准
- [ ] `scripts/validate-docs.py` 能检测 Markdown 格式问题
- [ ] `scripts/validate-indexes.py` 能检测索引 schema 问题
- [ ] 索引包含 `growth_process`、`journey_stage`、`stage_fit` 字段
- [ ] 有独立的 `failures-index.json`

### 执行步骤
```bash
# 1. 运行现有校验
python scripts/validate-docs.py
python scripts/validate-indexes.py

# 2. 检查索引字段
cat knowledge/indexes/cases-index.json | jq '.[0] | keys'
# 应该包含 growth_process, journey_stage, stage_fit

# 3. 检查失败模式索引
ls knowledge/indexes/failures-index.json
# 应该存在
```

### 完成定义
```bash
python scripts/run_tests.py
# 82/82 checks passed
```

---

## 执行顺序建议

### 第一批（建议顺序执行）
1. 任务 1：产品契约对齐
2. 任务 2：阶段感知检索
3. 任务 3：增加证据链字段
4. 任务 4：策略质量评测

### 第二批（可并行执行）
5. 任务 5：项目记忆注入
6. 任务 6：输出视图产品化
7. 任务 7：框架资产接入验证

### 第三批（低优先级）
8. 任务 8：知识系统可维护性

---

## 使用方式

### 方式一：逐个执行
```bash
# 每次只执行一个任务
# 用 goal 模式执行任务 1
# 完成后再执行任务 2
```

### 方式二：批量执行
```bash
# 用 ralph 或 ultrawork 模式
# 一次性执行多个任务
# 但每个任务仍独立验收
```

### 方式三：手动执行
```bash
# 按照本文档的执行步骤
# 手动完成每个任务
```

---

## 注意事项

1. **不要跳任务**：任务 2-4 依赖任务 1 完成产品契约对齐
2. **独立验收**：每个任务必须满足所有验收标准才算完成
3. **增量改动**：尽量低侵入，不破坏现有功能
4. **验证一致**：每完成一个任务，运行 `python scripts/run_tests.py` 确保无回归
