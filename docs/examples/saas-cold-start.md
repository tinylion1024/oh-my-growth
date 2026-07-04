# Example: SaaS Cold Start

## Input

```bash
growth diagnose "SaaS 产品如何获取首批 1000 个用户" \
  --industry saas \
  --stage 0-1 \
  --problem acquisition
```

## What The Output Should Answer

- whether the team is still validating PMF or ready to scale acquisition
- which first channel deserves the first two-week experiment
- which cases and plays are similar enough to reuse
- what not to do before the first acquisition loop is proven

## Good Follow-Up Context

```json
{
  "metric": "新增高意向注册",
  "team": "创始人 + 1 个工程",
  "budget": "2 万以内",
  "constraints": "不能依赖大额付费投放",
  "history": "发过 5 篇内容，没有稳定注册"
}
```

## Success Signal

The first experiment produces a measurable source of high-intent users and a repeatable outreach or content loop.
