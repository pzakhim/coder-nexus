# Mode: Planning — Core Gaps, Technical Trade-Offs & Test Data (`planning`, Gate 2)

Use with [`SKILL.md`](../SKILL.md), [`01 — Solution Options & Divergent Pass`](../references/01-solution-options-and-divergent-pass.md), and `{{slot:architecture-design}}`. Business behavior and UI/UX workflows are already locked at Gate 1 (`spec_writer`); this mode asks **only** what Gate 2 (`design.md`) requires.

## 1. Zero-Re-Ask Precondition (Before Queuing Any `Q-NN`)

1. Read `requirements.md`, extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png` when present), and `codebase-notes.md` (`## 0A. Source Inventory`, `## 1. Decision Log (D-NN)`, `## 2. Glossary`, `## 3. Verified Baseline Facts`).
2. **Never re-ask a locked `D-NN`**, business rule (`BR-NN`), acceptance criterion (`AC-NN`), or UI workflow/screen decision from Gate 1.
3. Run the read-only codebase intelligence scan defined in `{{slot:architecture-design}}` and record all discovered paths, classes, DI bindings, and routes in `codebase-notes.md` → `## 3`. Codebase facts are looked up, never asked (`SKILL.md` §4).

## 2. Technical Topics Owned by `planning`

Queue a `Q-NN` (`Owner: planning`) only when:

| Topic | When to Queue a `Q-NN` |
|---|---|
| **Core gap** | The active foundation (`{{slot:architecture-design}}`) lacks a component, service, or base pattern the behavior requires: build privately in the module, extend shared foundation, or ask `spec_writer` to adjust scope. |
| **Core risk / Conflict** | A Gate 1 requirement conflicts with existing module boundaries or overlapping runtime logic discovered in the codebase scan. |
| **Architecture trade-off** | 2–3 materially different layer splits, state-management shapes, caching policies, or integration patterns remain viable after the codebase scan. |
| **Component choice** | Multiple viable Kit or shared components fit the same UI need. *(When exactly one verified component fits, select it as a fact without asking.)* |
| **API contract shape** | `spec_writer` settled business inputs/outputs, but technical transport details (endpoint structure, pagination cursor vs offset, error code mapping) have multiple viable forms. |
| **Test data convention** | Confirmed once per work item (§4) so Mockoon/fixtures and unit tests share one deterministic dataset. |

Every technical `Q-NN` names the `G-NN` it serves. Technical options never alter user-visible business behavior; if a technical constraint forces a behavior or scope change, route it via the coordinator (`dev-team`) to `spec_writer` before presenting to the user.

## 3. Drafting & Comparing Technical Options (`planning` Solution Options)

Apply [`01 — Solution Options & Divergent Pass`](../references/01-solution-options-and-divergent-pass.md) when multiple viable technical designs exist:

- **Focused choices** (which of two existing Kit widgets, which error mapping): compare directly across the 5 standard fields (`What it is`, `Goals`, `Gains`, `Costs`, `Evidence`).
- **Architectural / cross-layer choices** (new module boundary, external contract, complex state/sync seam): explore 2–4 distinct design constraints in parallel (via read-only subagents or blank-page passes) before converging:
  1. *Smallest interface*: 1–3 entry points hiding internal complexity.
  2. *Optimize common caller*: make the default path trivial.
  3. *Reuse first*: extend existing codebase primitives before adding new abstractions.
  4. *Explicit test seam*: isolate external I/O behind a minimal port.

Compare candidate designs across 5 engineering criteria:

| Criterion | Question |
|---|---|
| **Depth** | How much capability does a caller/test gain per unit of interface surface? |
| **Locality** | When this feature evolves, how many files/layers must change together? |
| **Seams** | Can behavior be unit-tested without live I/O, without adding speculative single-implementation interfaces? |
| **Profile Fit** | Does it comply with `{{slot:clean-architecture}}` and the active workspace profile (`architecture_profile.mode`)? |
| **Reversibility** | How costly is it to reverse or replace this choice later? |

Keep the **2–3 strongest options**, put `(Recommended)` first, ask as one `Q-NN`, log all options in `Options Considered` (`D-NN`), and write **only** the confirmed choice into `design.md` (`## Architectural decision`). Significant long-lived decisions may later be promoted via [`architecture-decision-records`](../../architecture-decision-records/SKILL.md).

## 4. Test Data Convention (One `D-NN` per Work Item)

Agree on one deterministic row per behavior so mock fixtures and unit tests assert against the same data:

| Case | What to Confirm |
|---|---|
| **Pass / Default** | Input and dataset representing normal success |
| **Fail** | Input/trigger producing each required error state (validation `400`, auth `401`/`403`, timeout, server `500`) |
| **Empty** | Input/query returning zero records and the resulting empty state |

Rows that merely restate approved Gate 1 requirements may be confirmed together in one [batch-confirm](batch-confirm.md) question and recorded as a single `D-NN`.

## 5. Role Rules

- Never write `design.md` containing `Option A / Option B`, `TBD`, `Assumptions`, or open `Q-NN` rows (`DESIGN-007`, `DESIGN-008`, `NOTES-005`).
- Retain `codebase-notes.md` throughout the entire `vN/` lifecycle so `code_writer`, `code_reviewer`, `test_runner`, and `docs_writer` read the same `D-NN` log.
