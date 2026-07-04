# Example: Retention Drop

## Input

```bash
growth diagnose "产品更新后 DAU 下降 20%，应该先修什么" \
  --industry consumer \
  --stage 1-10 \
  --problem retention \
  --view report
```

## What The Output Should Answer

- whether the problem is activation, habit, value perception, or product confusion
- what to fix before buying more traffic
- which guardrail prevents fake retention
- what two-week experiment can prove the retention hypothesis

## Good Follow-Up Context

```json
{
  "metric": "D7 留存",
  "history": "更新后新用户首次关键动作完成率下降",
  "constraints": "不能回滚全部功能",
  "stakeholder": "产品负责人和增长负责人共同决策"
}
```

## Success Signal

D7 retention and key activation completion improve together, without relying on short-term incentives.
