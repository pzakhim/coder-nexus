# 01 — Straight-Line Architectural Decision (Backed by `codebase-notes.md`)

Apply the approved profile through [core-package-usage](../../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for Section 1 of `design.md`: **Architectural Decision**.

## Purpose
Before writing `design.md`, the Tech Lead (`planning`) scans the codebase and resolves any **Core Risk / Core Gap**, overlapping logic with `requirements.md`, or architectural trade-off by queueing `Q-NN` in `codebase-notes.md` and asking the user **1 question at a time** via `ask_question` (presenting a clear `(Recommended)` choice first).

All options considered and rejected are recorded in `## 1. Decision Log (D-NN)` inside `codebase-notes.md`. Once locked in with the user, `design.md` is written in **one straight locked-in line** citing `D-NN` — never containing `### Option A` / `### Option B` headings or unresolved questions.

## Format
```markdown
## Architectural decision

- **Confirmed architecture (`D-NN`)**: Concise description of the locked-in architecture (e.g. Single Flow Cubit with sealed state machine under `lib/modules/<feature>/`) and why it fits this module.
- **Decision log reference**: All evaluated trade-offs and rejected alternatives are recorded in `codebase-notes.md` (`## 1. Decision Log (D-NN)`).
```

## Checklist
- [ ] All Core risks, Core gaps, or logic conflicts with `requirements.md` were queued as `Q-NN` in `codebase-notes.md`, confirmed by the user 1-by-1 via `ask_question`, and closed into `D-NN` *before* finalizing `design.md`.
- [ ] `design.md` reads as a single, decisive forward blueprint without `Option A / Option B`, `Open Questions`, or `TBD`.
