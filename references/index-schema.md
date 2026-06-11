# Index Schema

当前知识索引不只是为了展示数量，也服务于检索、排序、失败模式提示和策略判断。

## Cases Index

每个 case 至少包含：

- `id`
- `name`
- `file`
- `summary`
- `tags`
- `growth_process`
- `journey_stage`
- `stage_fit`
- `company_type`
- `marketplace_side`
- `resource_profile`
- `failure_refs`

字段说明：

- `growth_process`：当前案例更偏 `用户获取` / `用户深耕`
- `journey_stage`：案例主要命中的用户旅程断点
- `stage_fit`：案例适配的阶段列表，例如 `["0-1", "1-10"]`
- `company_type`：`saas` / `marketplace` / `local-services` / `ecommerce` / `ai` / `general`
- `marketplace_side`：当案例属于双边平台时，标记为 `supply` / `demand` / `liquidity`，否则为空字符串
- `resource_profile`：实施该类案例通常需要的资源特征
- `failure_refs`：相关失败模式文档路径

## Weapons Index

每个 weapon 至少包含：

- `id`
- `name`
- `category`
- `effort`
- `impact`
- `evidence_tier`
- `growth_process`
- `journey_stage`
- `stage_fit`
- `marketplace_side`
- `resource_profile`
- `guardrail_risk`
- `failure_refs`

字段说明：

- `stage_fit`：该玩法更适配的阶段列表
- `marketplace_side`：当玩法可用于双边平台时，标记其更偏 `supply` / `demand` / `liquidity`，否则为空字符串
- `resource_profile`：该玩法通常要求的资源条件
- `guardrail_risk`：该玩法最需要盯住的约束线风险
- `failure_refs`：相关反模式/失效条件文档路径

## Theories Index

每个 theory 至少包含：

- `id`
- `name`
- `file`
- `core_question`
- `core_principles`
- `growth_process`
- `journey_stage`
- `stage_fit`
- `company_type`
- `marketplace_side`
- `resource_profile`
- `failure_refs`

字段说明：

- `growth_process`：该理论更适合解释 `用户获取` / `用户深耕` / `增长经营` 哪类问题
- `journey_stage`：该理论主要帮助判断哪个旅程节点
- `stage_fit`：该理论更适配的阶段列表
- `company_type`：该理论天然更适配的公司类型
- `marketplace_side`：当理论主要解释双边平台问题时，标记其更偏 `supply` / `demand` / `liquidity`
- `resource_profile`：落地该理论通常需要的资源结构
- `failure_refs`：使用该理论时最需要同时查看的失效条件

## Failures Index

每个 failure 至少包含：

- `id`
- `name`
- `file`
- `growth_process`
- `journey_stage`
- `problem_types`
- `summary`

字段说明：

- `problem_types`：该失败模式主要约束哪些问题类型
- `summary`：最短可消费的风险提醒
- `warning_signals`：高频预警信号
- `suggestions`：优先动作建议

## Validation

当前以下脚本会约束 schema：

- `scripts/update-indexes.py`
- `scripts/validate-indexes.py`
- `scripts/validate-docs.py`

修改索引结构后，应至少重新运行：

```bash
python3 scripts/update-indexes.py
python3 scripts/validate-indexes.py
python3 scripts/run_tests.py
```
