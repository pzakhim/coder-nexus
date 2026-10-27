# Changelog — create-incremental-implementation-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`).

## 1.1.0 — 2026-10-24

- Consolidated generated `references/` from 7 files (flat `01–07`, branched `shared/01–05`, `be/06–07`, `fe/06–07`) into 3: `01-preconditions-and-preflight.md`, `02-task-loop-and-checks.md` (loop, triage, commands, order of work, resuming) and `03-phase-end-and-handoff.md` (phase suite, bug-hunt, simplicity pass, evidence, hand-off). Dropped the branched layout and `{{branch_suffix}}`.
- Added rules I15 (pre-flight Consumes / Produces table plus global constraints and review focus), I16 (triage against the expected result: match / code wrong / plan wrong) and I17 (resume from ticks and git history); I16 joins the never-"not adopted" set. I1–I14 keep their IDs.
- Made the generator stack-agnostic: replaced `references/plan-formats.md` and `references/verification-by-stack.md` with `references/discovery-and-checks.md`; the per-stack order-of-work table became one inner-to-outer rule.
- Step 1 no longer reads the Coder Nexus core skill as base input; the generator relies on its own `references/base-rules.md`.

**Affects:** `SKILL.md`, `references/01-preconditions-and-preflight.md`, `references/02-task-loop-and-checks.md`, `references/03-phase-end-and-handoff.md`.
**Migration:** merge `01` into `01-preconditions-and-preflight.md` and add the pre-flight section; merge `02` + `06` + `07` into `02-task-loop-and-checks.md` and add the triage table and resuming; merge `03` + `04` + `05` into `03-phase-end-and-handoff.md`; add rows I15–I17 to the `SKILL.md` rule table (keep workspace IDs, P5).

## 1.0.0 — 2026-10-22

First version.

- Base rules I1–I14 extracted from Coder Nexus `plugins/core/skills/incremental-implementation` (generic parts only).
- Plan-format detection (work-items dossier, versioned feature docs, issue/PR checklists, plain plan file).
- Verification commands per stack; layer order of work per branch.
- Layouts: flat `references/01–07`; branched `references/shared/01–05`, `be/06–07`, `fe/06–07`.
- Output path: `<workspace>/.agents/skills/incremental-implementation/`.
- Step 0: never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name. Distributed with `skill-factory get`.
- Output table gains Kind + Why columns. **Mandatory:** `SKILL.md`, task loop (02), phase completion (03), verification (06), and rules I1, I4, I5, I10, I11, I14. Other files are suggested shapes and may merge (e.g. 04 + 05 into 03 for a light plan format).
- Base rules I1–I14 gain a Why column; generated rules carry their reason (`core/authoring-guide.md`).
- Every template starts with a `<!-- GEN: Why … -->` note.
- New Step 7 **Trial run** with topic tasks (implement a real task, mapped component that does not fit, a check that cannot run) — `core/trial-run.md`.
- New Step 8 **Description**; Step 9 records provenance and reports deviations.
- Generator description rewritten to trigger on more phrasings (incl. Vietnamese).
- Added: phase completion (03) links root-cause-debugging for failing checks; root-cause-debugging added to the sibling skills in Step 4.
- Changed: sibling skill name `unit-test` → `unit-testing` in the Step 4 gate list; generated sibling links should point to `.agents/skills/unit-testing/`.

**Affects:** all generated files.
**Migration:** existing, unregistered `incremental-implementation` skills in a workspace → run the generator there to **adopt** (keeps workspace rules and custom blocks, records provenance).
