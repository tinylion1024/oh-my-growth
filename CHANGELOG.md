# Changelog

All notable changes to Growth Master will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-05-31

### Added

#### Complete Yao Open Skills Integration (100% Coverage)

All 12 skills from yao-open-skills are now integrated:

##### Core Decision Frameworks

**Game Theory Framework** (`references/gametheory-framework.md`)
- Prisoner's Dilemma, Cournot Competition
- Signaling Game, Commitment Game
- Two-Sided Market, Bargaining Game
- Nash Equilibrium analysis
- Commitment credibility check
- Historical behavior calibration

**Kelly Allocation Framework** (`references/kelly-allocation.md`)
- Kelly formula: f* = (bp - q) / b
- Fractional Kelly (1/2, 1/4)
- Multiple opportunity allocation
- Correlation adjustment
- Minimum action package
- Add/stop conditions

**Business Model Framework** (`references/business-model.md`)
- Business Model Canvas
- Revenue model analysis
- Porter's Five Forces
- Competitor analysis
- AI-era upgrade paths

##### Extended Frameworks

**Tutorial Production** (`references/tutorial-production.md`)
- Module design
- Visual enhancement
- Multi-format export (MD/HTML/DOCX/PDF)

**Learning Builder** (`references/learning-builder.md`)
- Learner profile
- Authority-first resources
- Personalized curriculum

**Web Security Audit** (`references/websecurity-audit.md`)
- OWASP Top 10
- Static/Dynamic analysis
- Security reporting

**WeRead Report** (`references/weread-report.md`)
- Reading analytics
- Visualization
- Report generation

**Copyright Management** (`references/copyright-management.md`)
- Copyright header management
- License compliance

**Skills Sync** (`references/skills-sync.md`)
- Open source evaluation
- Catalog management

**Security Test Skills** (`references/security-test-skills.md`)
- Code review
- Dependency check
- Tech selection security

### Changed

#### SKILL.md
- Added Game Theory Framework section
- Added Kelly Allocation Framework section
- Added Extended Frameworks section
- Updated Reference Map with all new frameworks

#### README.md
- Updated version to 3.0.0
- Added Game Theory and Kelly sections
- Added Complete Framework System table
- Added yao-skills 100% integrated badge

### Integration Summary

| Skill | Status | Integration Location |
|-------|--------|---------------------|
| yao-crux-skill | ✅ Complete | references/, agents/ |
| yao-bayesian-skill | ✅ Complete | references/bayesian-decision.md |
| yao-gametheory-skill | ✅ Complete | references/gametheory-framework.md |
| yao-kelly-skill | ✅ Complete | references/kelly-allocation.md |
| yao-business-skill | ✅ Complete | references/business-model.md |
| yao-tutorial-skill | ✅ Complete | references/tutorial-production.md |
| learning-builder | ✅ Complete | references/learning-builder.md |
| yao-websecurity-skill | ✅ Complete | references/websecurity-audit.md |
| yao-weread-skill | ✅ Complete | references/weread-report.md |
| yao-copyright-skill | ✅ Complete | references/copyright-management.md |
| yao-open-skills-sync | ✅ Complete | references/skills-sync.md |
| security-test-hskills | ✅ Complete | references/security-test-skills.md |

**Total Coverage: 100% (12/12)**

## [2.1.0] - 2026-05-31

### Added

#### Bayesian Decision Engine (贝叶斯决策引擎)
- Created `references/bayesian-decision.md` with complete Bayesian framework
- Created `scripts/bayesian_decision.py` with BayesianDecision class
- Support for prior probability setting with hygiene check
- Evidence-based posterior probability updating (A/B/C/D/E tiers)
- Action threshold comparison (invest_now/experiment/collect_evidence/stop)
- Multi-round iteration with diminishing returns
- Sensitivity analysis generation
- High-risk threshold adjustment
- Created `tests/test_bayesian_decision.py` with 10 test cases

#### Integration
- Updated Lead Agent to integrate Bayesian decision workflow
- Updated SKILL.md with Bayesian Decision configuration section
- Added Bayesian output sections to report contract

### Technical Details

#### Bayesian Update Formula
```
posterior = prior + Σ(evidence_update × diminishing_factor)

where:
- evidence_update = tier_magnitude × direction
- diminishing_factor = [1.0, 0.7, 0.5, 0.3] for repeated same-direction evidence
```

#### Action Thresholds
| Threshold | Posterior Range | Action |
|-----------|-----------------|--------|
| invest_now | ≥ 75% | Direct investment |
| run_experiment | 50-75% | Small-scale experiment |
| collect_evidence | 30-50% | Continue gathering evidence |
| stop | < 30% | Stop considering |

#### Evidence Tier Updates
| Tier | Update Magnitude | Definition |
|------|-----------------|------------|
| A | ±25% | Meta-analysis, systematic reviews |
| B | ±15% | Peer-reviewed papers, industry reports |
| C | ±10% | Expert opinions, internal data |
| D | ±5% | LLM suggestions, analogies |
| E | 0% | Blog posts, marketing claims |

## [1.1.0] - 2024-01-15

### Added

#### Evidence Quality System (证据分级系统)
- Added `evidence_tier` field to all knowledge indexes (cases, weapons, theories)
- Added `evidence_tier_definition` in metadata with A/B/C/D/E grading scale
- Added `evidence_sources` field documenting the source of each piece of knowledge
- Added `confidence` field (0-1) indicating reliability of each entry

#### Current-State Clarity Gate (现状清晰度门控)
- Created `references/current-state-clarity.md` with 7-dimension scoring system
- Dimensions: goal_success (20%), facts_evidence (20%), stage (12%), scarce_resources (12%), hard_constraints (12%), stakeholders (8%), repeated_patterns (8%)
- Three clarity levels: insufficient (0-54), workable (55-74), clear (75-100)
- Hard requirements: goal_success and facts_evidence must score ≥50

#### Safety Boundaries (安全边界)
- Created `references/safety-boundaries.md` with 4 risk domains
- Domains: financial, legal, regulatory, operational
- Each domain has trigger keywords, response rules, and confidence caps
- Automatic warning generation for high-risk scenarios

#### Output Contract (输出契约)
- Created `references/report-contract.md` with 10 required sections
- User-friendly title mappings (e.g., "主要矛盾" → "最关键的卡点")
- Fact marking rules: (observed), (estimated), (assumed)
- Validation checklist for completeness and safety

#### Question Bank (追问问题库)
- Created `references/question-bank.md` with structured questions
- Questions organized by mode: Fast Scan (3), Strategy Design (5), Decision BRD (7)
- Upstream diagnosis questions for root cause analysis
- Follow-up strategy for multi-turn dialogue

#### Scripts (脚本)
- Created `scripts/assess_clarity.py` for clarity assessment
- Created `scripts/verify_report.py` for report contract validation
- Both scripts support JSON and Markdown output formats

### Changed

#### SKILL.md
- Added decision_gates section with clarity gate and safety protocol
- Added output_contract section referencing report-contract.md
- Added Reference Map section

#### Core Agents
- **lead-agent.md**: Added multi-turn dialogue mode, clarity gate integration, Reference Map
- **guide-agent.md**: Added question_bank reference, follow_up_strategy, clarity gate integration
- **growth-agent.md**: Added three_question_gate, first_principles_gate, Reference Map
- **skeptic-agent.md**: Added safety_check with domain triggers, response rules, Reference Map
- **narrative-agent.md**: Added output_contract compliance, validation_checklist, Reference Map

#### Knowledge Indexes
- **cases-index.json**: Updated to v1.1.0, added evidence_tier (mostly B), evidence_sources, confidence
- **weapons-index.json**: Updated to v1.1.0, added evidence_tier to categories and individual weapons
- **theories-index.json**: Updated to v1.1.0, added evidence_tier, evidence_sources, confidence

#### Documentation
- **README.md**: Updated features list, added evidence tier table, updated testing section
- **docs/user-guide.md**: Added evidence grading, clarity gate, safety boundary sections
- **docs/developer-guide.md**: Added Reference Map system, script documentation, configuration guides
- **docs/best-practices.md**: Added clarity improvement tips, evidence grading usage, safety boundary best practices

### Technical Details

#### Evidence Tier Distribution

| Tier | Cases | Weapons | Theories | Meaning |
|------|-------|---------|----------|---------|
| A | 3 | 5 | 1 | Meta-analysis, academic research |
| B | 52 | 85 | 8 | Industry practice, case studies |
| C | 18 | 18 | 3 | Expert opinion, field evidence |
| D | 4 | 3 | 0 | LLM suggestions, analogies |
| E | 0 | 0 | 0 | Blog posts, marketing claims |

#### Clarity Gate Thresholds

```
Score Calculation:
total_score = Σ(dimension_score × weight)

Levels:
- insufficient (0-54): Cannot proceed, must clarify first
- workable (55-74): Can proceed, clarify while doing
- clear (75-100): Can proceed with deep analysis

Hard Requirements:
- goal_success.score ≥ 50
- facts_evidence.score ≥ 50
```

#### Safety Boundary Response Rules

```yaml
on_detection:
  - Add warning declaration to output
  - Do not let high scores override safety boundaries
  - Cap confidence at domain's confidence_cap
  - Recommend reversible, conservative, review-oriented actions
```

## [1.0.0] - 2024-01-01

### Added

#### Phase 1 - 核心体验
- 快速启动模板 (`templates/quick-start.md`)
- Agent测试套件 (`tests/`)
- 反馈收集机制 (`feedback/`)

#### Phase 2 - 智能化
- Orchestrator Agent - 自动编排工作流
- 知识索引系统 (`knowledge/indexes/`)
  - cases-index.json
  - weapons-index.json
  - theories-index.json
- Guide Agent - 交互式引导

#### Phase 3 - 知识增强
- 案例结构化规范 (`knowledge/STRUCTURE-SPEC.md`)
- 决策追踪系统 (`decisions/`)
- 完整文档
  - 用户指南
  - 开发者指南
  - 最佳实践

#### Phase 4 - 持续迭代
- Competitor Agent - 竞品分析
- 知识图谱 (`knowledge/indexes/knowledge-graph.json`)
- 输出可视化模块
- CI/CD集成
  - 自动测试
  - 索引验证
  - 决策追踪提醒

### Agent体系

#### 核心决策Agent (7个)
- Lead Agent - 编排协调
- Growth Agent - 增长机制评估
- Monetization Agent - 变现影响评估
- ROI Agent - 投资回报计算
- Execution Agent - 执行可行性
- Skeptic Agent - 风险识别
- Narrative Agent - 文档撰写

#### 知识驱动Agent (4个)
- Case Agent - 案例匹配
- Weapon Agent - 玩法推荐
- Theory Agent - 理论支撑
- Competitor Agent - 竞品分析

#### 辅助Agent (2个)
- Orchestrator Agent - 自动编排
- Guide Agent - 交互引导

### 知识库

- 77个增长案例
- 111种增长玩法
- 12大理论流派
- 结构化索引

### 工作流模式

- Fast Scan - 快速评估
- Decision BRD - 决策文档
- Strategy Design - 策略设计
- Case Match - 案例匹配
- Learning Path - 学习路径

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| 1.1.0 | 2024-01-15 | Evidence grading, Clarity gate, Safety boundaries, Output contract |
| 1.0.0 | 2024-01-01 | Initial release |


## 📝 版本历史

| 版本 | 发布日期 | 主要更新 |
|------|----------|----------|
| 4.0.0 | 2025-06-13 | 完善开发者体验，统一版本号 |


