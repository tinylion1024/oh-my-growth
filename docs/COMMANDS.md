# Command Reference

oh-my-growth exposes the same strategy surface in two forms:

- Skill commands: `/omg-diagnose ...`, `/omg-design ...`
- Standalone CLI: `growth diagnose ...`, `growth design ...`

Use skill commands inside Claude Code, OpenClaw, or Hermes. Use `growth` when the project is installed as a local Python CLI.

## Which Command To Use

| Need | Skill command | CLI command | Output |
|---|---|---|---|
| Decide whether an idea is worth analysis | `/omg-assess` | `growth assess` | clarity score, go/no-go, missing facts |
| Diagnose an unclear growth problem | `/omg-diagnose` | `growth diagnose` | stage, priority, evidence, experiment |
| Turn a direction into a plan | `/omg-design` | `growth design` | strategy design and action path |
| Quickly screen a direction | `/omg-fast-scan` | `growth fast-scan` | lightweight feasibility read |
| Draft a decision document | `/omg-brd` | `growth brd` | BRD-style decision draft |
| Find similar cases | `/omg-match` | `growth match` | matched cases and rationale |
| Build a learning path | `/omg-learn` | `growth learn` | guides, cases, theories |
| Search the knowledge base | `/omg-search` | `growth search` | cases, plays, theories, method packs |
| Validate a report | `/omg-validate` | `growth validate` | output quality checks |

## Common Options

| Option | Meaning | Example |
|---|---|---|
| `--industry` | Industry or business type | `--industry saas` |
| `--stage` | Growth stage | `--stage 0-1`, `--stage 1-10`, `--stage 10-100` |
| `--problem` | Problem type | `--problem acquisition`, `--problem retention` |
| `--journey` | Journey bottleneck | `--journey 认知/到达` |
| `--goal` | Business goal | `--goal 提升自然注册` |
| `--metric` | Primary metric | `--metric 新增高意向用户数` |
| `--budget` | Budget constraint | `--budget 5万以内` |
| `--team` | Team constraint | `--team 1个增长+1个工程` |
| `--constraints` | Hard constraints | `--constraints 不做付费投放` |
| `--history` | Past attempts | `--history SEO文章无转化` |
| `--context-json` | Structured context inline | `--context-json '{"metric":"D7留存"}'` |
| `--profile-file` | Company profile JSON | `--profile-file company.json` |
| `--history-file` | Experiment log JSON | `--history-file experiments.json` |
| `--view` | Output format | `--view executive`, `--view json` |

## Output Views

| View | Best for |
|---|---|
| `operator` | Default detailed operator console |
| `executive` | Short leadership summary |
| `report` | Full decision report |
| `json` | Agent/API integration |
| `weekly` | Weekly planning |
| `experiment-card` | Single experiment ticket |
| `share` | Public-safe experiment snapshot for a post or team update |
| `decision-memo` | Decision record |
| `qbr` | Quarterly business review |

## Copy-Paste Examples

### GEO / LLM Discovery

```bash
growth diagnose "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率" \
  --industry saas \
  --stage 10-100 \
  --problem acquisition \
  --metric 新增高意向用户数
```

Expected signals:

- Recommended method pack includes `GEO/LLM 发现系统`
- Experiment steps include entity consistency, quotable facts, FAQ/comparison blocks, or structured summaries
- Stop signals warn against fabricated sources and inconsistent brand facts

### SEO / AEO Acquisition

```bash
growth design "我们的网站自然搜索流量少，需要做 SEO 和 AEO 获客" \
  --industry saas \
  --stage 1-10 \
  --problem acquisition \
  --view decision-memo
```

Expected signals:

- Recommended method pack includes `SEO/AEO 获客系统`
- Plan ties content work to conversion, not traffic alone
- Measurement includes search visibility and high-intent signup quality

### Cold Start

```bash
growth diagnose "SaaS 产品如何获取首批 1000 个用户" \
  --industry saas \
  --stage 0-1 \
  --problem acquisition
```

### Shareable Experiment Snapshot

```bash
growth diagnose "Should we test a referral loop?" \
  --industry saas \
  --stage 1-10 \
  --problem referral \
  --view share
```

`share` omits company-profile and experiment-history fields, so it can be pasted into a public post or a team update after a quick review.

### Retention Drop

```bash
growth diagnose "产品更新后 DAU 下降 20%，应该先修什么" \
  --industry consumer \
  --stage 1-10 \
  --problem retention \
  --view report
```

## Structured Context Example

```bash
growth diagnose "自然注册没有增长" \
  --context-json '{"industry":"saas","stage":"1-10","problem_type":"acquisition","metric":"新增高意向注册","constraints":"不能增加付费投放"}' \
  --view json
```

## Validation

Run these checks before publishing command-surface changes:

```bash
python3 scripts/validate-docs.py
python3 scripts/validate-indexes.py
python3 scripts/validate-release.py
```
