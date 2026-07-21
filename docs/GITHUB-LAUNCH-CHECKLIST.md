# GitHub Launch Checklist

This checklist covers repository settings that cannot be versioned in Git and the reproducible release steps for the current package.

## One-time repository settings

Complete these in **GitHub → Settings → General**:

- Set the description to: `Evidence-backed growth decisions for AI-agent teams`.
- Add topics: `growth`, `growth-hacking`, `claude-code`, `openclaw`, `hermes`, `ai-agents`, `product-growth`, `seo`, `geo`, `aeo`.
- Upload `assets/cover.png` as the social preview image.
- Add the project homepage when a public landing page exists.
- Enable Discussions only when a maintainer has capacity to respond weekly.

## Release process

1. Run `./scripts/release-check.sh` and confirm it passes.
2. Review `RELEASE_NOTES.md` and create the GitHub release matching `VERSION`.
3. Attach the source archive and publish the release from the matching signed tag.
4. Verify that the GitHub release version, `VERSION`, `pyproject.toml`, `manifest.json`, and README badge agree.

## Real-user proof before publishing it

Do not label illustrative examples as customer results. Before adding a case study to the README, collect a user-approved, anonymized record with:

- the original growth question and relevant context;
- the generated recommendation and what was actually executed;
- the measurement window, metric definition, and outcome;
- any important limitation or failed assumption.

Store sanitized feedback in `feedback/logs/real/` and the corresponding decision record under `decisions/records/`.
