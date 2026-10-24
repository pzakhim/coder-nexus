# Skill Standardization Checklist (User-Verified Pass Ledger)

> **Purpose:** Tracks every skill reviewed, standardized, and confirmed `PASS` with the user across `skill-factory`, `plugins/packs/flutter/`, `plugins/packs/backend/`, and `plugins/core/`.

---

## 1. Mandatory Pass Criteria (Applied to Every Skill)

1. **Unified Flags & Severities (`shared_contracts/flags_and_statuses.md`):**
   - Deterministic CLI tool gates use strictly `PASS` / `FAIL`.
   - Core rules/principles in authoring skills are mandatory compliance (no per-rule severity column).
   - Reviewer findings use the single unified scale: `BLOCKER` / `MAJOR` / `MINOR` (zero `P1` / `P2` / `P3` remnants).
   - Default developer tools installed via `coder-nexus setup tools --pack <stack>` are wired into the skill's verification gates (`rg` instead of `grep`).
2. **Cohesive `references/` Structure:**
   - `SKILL.md` is a concise routing table and rule index (< 150 lines).
   - `references/` is consolidated into 3–4 cohesive topic files (no fragmented micro-files like `02`, `02b`, `05`, `06` or obsolete `sources.md`).
   - No `assets/` folder unless the skill ships real static runtime artifacts.
3. **Profile Isolation (`profiles/{imespro,external-structured,external-standard}/`):**
   - Base `SKILL.md` and `references/` in Pack skills are 100% stack-generic (zero hardcoded `iMESPro`, `BaseScreen`, `app_ui_kit`, or `DataState` in base files).
   - Profile-specific contracts live in `profiles/<profile>/<name>.md` (with `# <Title>` and `> Topic: <Description>`) and auto-inject into `SKILL.md` at `<!-- {{profile_references}} -->` during workspace sync (`apply_workspace_profile`).
4. **100% Stack-Agnostic Generator (`src/skill_factory/library/generators/create-*-skill/`):**
   - Generator `SKILL.md`, `references/`, `checklist.md`, and `templates/` do not hardcode `BE`, `FE`, `be/`, `fe/`, or specific frameworks/tools (`FastAPI`, `React`, `Flutter`, `NestJS`, `ruff`, `eslint`, etc.).

---

## 2. Group A — Core Stack Slot Skills (`plugins/core/slots.json`)

Each row covers: **(1) Skill Factory Generator** + **(2) Flutter Pack Skill** + **(3) Backend Pack Skill**.

| # | Slot / Skill | Skill Factory Generator | Flutter Pack (`plugins/packs/flutter/skills/`) | Backend Pack (`plugins/packs/backend/skills/`) | Profile Support (`profiles/`) | Status | Confirmed Date |
|---|---|---|---|---|---|---|---|
| 1 | **`clean-code`** | `create-clean-code-skill` | `flutter/skills/clean-code` | `backend/skills/clean-code` | `imespro`, `external-structured`, `external-standard` | `[x] PASS` | 2026-10-24 |
| 2 | **`clean-architecture`** | `create-clean-architecture-skill` | `flutter/skills/clean-architecture` | `backend/skills/clean-architecture` | `imespro`, `external-structured`, `external-standard` | `[ ] IN_PROGRESS` | — |
| 3 | **`code-simplification`** | `create-code-simplification-skill` | `flutter/skills/code-simplification` | `backend/skills/code-simplification` | TBD | `[ ] PENDING` | — |
| 4 | **`secure-coding-standards`** | `create-secure-coding-standards-skill` | `flutter/skills/secure-coding-standards` | `backend/skills/secure-coding-standards` | TBD | `[ ] PENDING` | — |
| 5 | **`unit-testing`** | `create-unit-testing-skill` | `flutter/skills/unit-testing` | `backend/skills/unit-testing` | TBD | `[ ] PENDING` | — |
| 6 | **`root-cause-debugging`** | `create-root-cause-debugging-skill` | `flutter/skills/root-cause-debugging` | `backend/skills/root-cause-debugging` | TBD | `[ ] PENDING` | — |
| 7 | **`bug-hunt`** | `create-bug-hunt-skill` | `flutter/skills/bug-hunt` | `backend/skills/bug-hunt` | TBD | `[ ] PENDING` | — |
| 8 | **`code-review`** | `create-code-review-skill` | `flutter/skills/code-review` | `backend/skills/code-review` | TBD | `[ ] PENDING` | — |
| 9 | **`architecture-design`** | — | `flutter/skills/architecture-design` | `backend/skills/architecture-design` | TBD | `[ ] PENDING` | — |
| 10 | **`verification`** | — | `flutter/skills/verification` | `backend/skills/verification` | TBD | `[ ] PENDING` | — |
| 11 | **`core-package-usage`** | — | `flutter/skills/core-package-usage` | *(N/A for Backend)* | Native 3-profile router | `[ ] PENDING` | — |
| 12 | **`visual-quality`** | `create-visual-quality-skill` | `flutter/skills/visual-quality` | *(N/A for Backend)* | TBD | `[ ] PENDING` | — |
| 13 | **`ui-kit-mapping`** | — | `flutter/skills/ui-kit-mapping` | *(N/A for Backend)* | TBD | `[ ] PENDING` | — |

---

## 3. Group B — Backend Pack Extra Skills (`plugins/packs/backend/skills/`)

| # | Skill | Skill Factory Generator | Path | Status | Confirmed Date |
|---|---|---|---|---|---|
| 14 | **`fastapi`** | — | `plugins/packs/backend/skills/fastapi` | `[ ] PENDING` | — |
| 15 | **`postgres`** | — | `plugins/packs/backend/skills/postgres` | `[ ] PENDING` | — |
| 16 | **`database-migrations`** | `create-database-migrations-skill` | `plugins/packs/backend/skills/database-migrations` | `[ ] PENDING` | — |
| 17 | **`api-contract-design`** | `create-api-contract-design-skill` | `plugins/packs/backend/skills/api-contract-design` | `[ ] PENDING` | — |
| 18 | **`realtime`** | — | `plugins/packs/backend/skills/realtime` | `[ ] PENDING` | — |

---

## 4. Group C — Remaining Skill Factory Generators (`src/skill_factory/library/generators/`)

| # | Generator | Package | Status | Confirmed Date |
|---|---|---|---|---|
| 19 | `create-incremental-implementation-skill` | `coder` | `[ ] PENDING` | — |
| 20 | `create-git-workflow-skill` | `coder` | `[ ] PENDING` | — |
| 21 | `create-security-review-skill` | `reviewer`, `security` | `[ ] PENDING` | — |
| 22 | `create-quality-planning-skill` | `tester` | `[ ] PENDING` | — |
| 23 | `create-quality-environment-skill` | `tester` | `[ ] PENDING` | — |
| 24 | `create-quality-acceptance-skill` | `tester` | `[ ] PENDING` | — |
| 25 | `create-quality-reporting-skill` | `tester` | `[ ] PENDING` | — |
| 26 | `create-domain-knowledge-skill` | `planning` | `[ ] PENDING` | — |
| 27 | `create-requirements-specification-skill` | `planning` | `[ ] PENDING` | — |
| 28 | `create-change-impact-analysis-skill` | `planning` | `[ ] PENDING` | — |
| 29 | `create-implementation-planning-skill` | `planning` | `[ ] PENDING` | — |

---

## 5. Group D — Core Handshake Skills (`plugins/core/skills/`)

| # | Core Skill | Role Touchpoint | Status | Confirmed Date |
|---|---|---|---|---|
| 30 | `work-item-contract` | Handshake & unified `BLOCKER`/`MAJOR`/`MINOR` severities | `[ ] PENDING` | — |
| 31 | `delivery-workflow` | End-to-end Gate 1 → Gate 2 → Gate 3 delivery | `[ ] PENDING` | — |
| 32 | `dev-team` | Multi-agent orchestration | `[ ] PENDING` | — |
| 33 | `requirements-elicitation` | Gate 1 (`requirements.md`) | `[ ] PENDING` | — |
| 34 | `solution-options` | Architectural option exploration | `[ ] PENDING` | — |
| 35 | `architecture-decision-records` | ADR recording | `[ ] PENDING` | — |
| 36 | `implementation-planning` | Gate 3 (`plan.md`) | `[ ] PENDING` | — |
| 37 | `incremental-implementation` | Phase-by-phase execution | `[ ] PENDING` | — |
| 38 | `gate-review` | Approval gate verification | `[ ] PENDING` | — |
| 39 | `review-workflow` | Code Reviewer workflow | `[ ] PENDING` | — |
| 40 | `review-resolution` | Fixing review findings | `[ ] PENDING` | — |
| 41 | `quality-acceptance` | Test Runner acceptance against `requirements.md` | `[ ] PENDING` | — |
| 42 | `evidence-standard` | Verification evidence rules | `[ ] PENDING` | — |
| 43 | `defect-resolution` | L1/L2/L3 bug fixing triage & flow | `[ ] PENDING` | — |
| 44 | `fix-planning` | Bug fix plan contract | `[ ] PENDING` | — |
| 45 | `debug-investigation` | Read-only root-cause investigation | `[ ] PENDING` | — |
| 46 | `feature-testing` | Scenario testing entry skill | `[ ] PENDING` | — |
| 47 | `ui-ux-design` | Designer HTML prototype & UX-001..012 flow | `[ ] PENDING` | — |
| 48 | `change-control` | Mid-implementation scope/contract change | `[ ] PENDING` | — |
| 49 | `cold-reader-check` | Fresh-eyes spec/code readability check | `[ ] PENDING` | — |
| 50 | `git-preflight` | Git branch, staging & push safety | `[ ] PENDING` | — |
| 51 | `grilling` | Requirement/design stress-testing interview | `[ ] PENDING` | — |
| 52 | `huly-setup` | Huly MCP configuration | `[ ] PENDING` | — |
| 53 | `huly-task-intake` | Reading Huly ticket + Figma frames | `[ ] PENDING` | — |
| 54 | `user-documentation` | Docs Writer workflow | `[ ] PENDING` | — |
