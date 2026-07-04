# GEO / LLM Discovery Use Case

Use this page when a brand wants to improve visibility in AI search, answer engines, or agent retrieval.

## Problem

The brand is not being cited or described consistently by generative search systems. Existing pages may be readable for humans but hard for models to extract as reliable facts.

## Command

```bash
growth diagnose "我们的品牌在 GEO 和 LLM 搜索里没有曝光，想提高引用率" \
  --industry saas \
  --stage 10-100 \
  --problem acquisition \
  --metric 新增高意向用户数
```

## Expected Output

- `GEO/LLM 发现系统` appears in `reference_method_packs`
- evidence chain includes an `操作系统` item
- experiment steps include entity consistency, quotable conclusions, FAQ/comparison blocks, or structured summaries
- stop signals reject fabricated citations, unverifiable claims, and inconsistent brand facts

## Practical Experiment

1. Pick 5 core pages that answer high-intent questions.
2. Add a stable entity definition, short answer block, FAQ, comparison table, and source-backed claims.
3. Track AI-search mentions, branded search, referral quality, and high-intent signups.
4. Stop if citations increase but brand facts become inconsistent or traffic quality drops.

## Related Files

- `knowledge/method-packs/geo-llm-discovery-system.md`
- `knowledge/method-packs/seo-aeo-growth-system.md`
- `llms.txt`
- `docs/COMMANDS.md`
- `docs/API.md`
