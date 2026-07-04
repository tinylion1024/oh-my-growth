# API Documentation

oh-my-growth is primarily a skill and CLI project, but the Python modules expose stable local integration points for agents, scripts, and tests.

## Public Surfaces

| Surface | Module | Use |
|---|---|---|
| CLI router | `scripts/cli.py` | Parse commands and render views |
| Strategy engine | `scripts/strategy_brain.py` | Turn a query and context into diagnosis and plan |
| Retriever | `scripts/retriever/core.py` | Retrieve cases, plays, theories, failures, and method packs |
| Search scoring | `scripts/retriever/search.py` | Score individual knowledge objects |
| Index validation | `scripts/validate-indexes.py` | Validate generated JSON indexes |

## Strategy API

```python
from strategy_brain import StrategyBrain

brain = StrategyBrain()
analysis = brain.analyze(
    "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率",
    {
        "industry": "saas",
        "stage": "10-100",
        "problem_type": "acquisition",
        "metric": "新增高意向用户数",
    },
    mode="diagnose",
)

print(analysis["decision_line"])
print(analysis["experiment"]["steps"])
```

When importing from outside `scripts/`, add the scripts directory to `PYTHONPATH` or use the installed `growth` CLI.

## CLI JSON Contract

```bash
growth diagnose "自然注册没有增长" \
  --industry saas \
  --stage 1-10 \
  --problem acquisition \
  --view json
```

Important top-level fields:

| Field | Type | Meaning |
|---|---|---|
| `query` | string | Original user problem |
| `context_summary` | string | Normalized context display |
| `stage_diagnosis` | object | Current stage and stage focus |
| `growth_process` | object | Main growth process |
| `north_star` | object | Primary metric and guardrail |
| `journey_focus` | object | Journey bottleneck |
| `priorities` | array | Ranked growth options |
| `do_now` | array | Immediate actions |
| `avoid_now` | array | Actions to delay or stop |
| `experiment` | object | Hypothesis, steps, success signals, stop signals |
| `reference_cases` | array | Matched growth cases |
| `reference_theories` | array | Matched theories |
| `reference_failures` | array | Failure modes |
| `reference_method_packs` | array | Operating-system method packs |
| `confidence_label` | string | Bayesian confidence label |
| `confidence_score` | number | Posterior confidence score |

## Retrieval API

```python
from knowledge_retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()
results = retriever.retrieve(
    "SEO 和 AEO 获客",
    {"industry": "saas", "problem_type": "acquisition", "stage": "1-10"},
    case_limit=3,
    weapon_limit=5,
    theory_limit=2,
    failure_limit=2,
    method_pack_limit=3,
)
```

Retrieval result shape:

```json
{
  "cases": [],
  "weapons": [],
  "theories": [],
  "failures": [],
  "method_packs": []
}
```

Each item uses:

| Field | Meaning |
|---|---|
| `id` | Stable object id |
| `name` | Human-readable name |
| `score` | Search/relevance score |
| `highlights` | Short matched decision rules or reusable points |
| `metadata` | Source-specific structured fields |

## Method Pack Semantics

Method packs are the operating-framework layer. They do not replace cases or plays; they shape how the recommendation is organized.

For SEO/GEO/CRO/paid/GTM/lifecycle/referral queries, method packs can:

- add scoring bonus to aligned growth options
- appear in the evidence chain as `操作系统`
- add experiment steps from `experiment_shapes`
- add stop signals from `guardrails`

## Stability Notes

- CLI command names are release-gated by `scripts/validate-release.py`.
- Knowledge counts are checked against `knowledge/indexes/*.json` metadata.
- JSON field names above should be treated as the stable integration surface for local agent use.
- Internal score weights may change as long as the output contract remains compatible.
