# Changelog

All notable changes to oh-my-growth are documented here. The project follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Semantic Versioning.

## [1.0.1] - 2026-06-16

### Fixed

- Restored generated case/play navigation markers in `README.md`.
- Updated documentation validation for the `/omg-*` command contract.
- Unified release metadata across the package, platform adapters, installer, and command skills.
- Removed stale command examples and unsupported `audit`/`feedback` command references.
- Added release metadata validation and a single `scripts/release-check.sh` gate.

### Changed

- Standardized public commands such as `/omg-diagnose`, `/omg-assess`, and `/omg-design`.
- Documented all standalone CLI output views.
- Updated the automated test baseline to 96 checks, including install smoke tests for Claude Code, Hermes Agent, and OpenClaw.

## [1.0.0] - 2026-06-13

### Added

- Initial public release of the growth decision skill.
- 13 command and scenario entry points.
- 81 growth cases, 111 growth plays, 12 theory schools, and 7 learning modules.
- Bayesian decision, Kelly allocation, game theory, evidence grading, safety boundaries, and report validation.
- Claude Code support with standalone Python CLI.

### Changed

- Added OpenClaw and Hermes Agent adapters on 2026-06-14.
