# Mode: Design — Gate 2 Pre-Gate Verification (`planning` in `dev-team`)

Reviews `design.md` against the Gate 1 approved `requirements.md`, `codebase-notes.md`, and (when present) extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`). Pass 1 (`validate_proposal_spec` on `design.md` = `PASS`, including `DESIGN-007` and `DESIGN-008`) must be clean before starting Pass 2. Findings use `GR-D-NN`.

---

## Pass 2 — Design Checklist (`D1`–`D5`)

### D1. Input Reconciliation (`BR-NN`, `AC-NN`, `W-NN`, `D-NN`)
Build one traceability row per Gate 1 input item and name the `design.md` section and element that serves it:

| Input ID | Served By (`design.md` Section & Element) | Status (`served` / `not served`) |
|---|---|---|
| `BR-03` | `## State Management & Data Flow`: submit validation guard | `served` |
| `AC-05` | — | `not served` (`BLOCKER`) |

- Any unserved `AC-NN`, `BR-NN`, `W-NN`, or technical-binding `D-NN` is a **`BLOCKER`**.
- **Reverse direction (Gold-plating)**: Any design element that serves no Gate 1 input is **`MAJOR`** unless `codebase-notes.md` records a verified architectural necessity.
- **Scope creep**: Any behavior, business rule, or permission introduced in `design.md` that does not exist in `requirements.md` is **`BLOCKER`** — route back to `spec_writer` as a `Q-NN`.

### D2. Deferred Decisions Integrity
- Any choice intentionally deferred (`### Deferred decisions`) must state what is deferred, why it is safe to wait, and when it will be revisited.
- An unacknowledged open architectural choice is **`MAJOR`**.
- A deferred item where two components, phases, or layers could choose incompatibly during build is **`BLOCKER`** — it cannot be deferred and must be settled as a `D-NN` now.

### D3. Risks & Mitigations
Every risk listed in `design.md` must name a concrete mitigation, a check that detects it, or a `BLOCKED` owner. A risk without mitigation is **`MAJOR`** (**`BLOCKER`** when it touches data loss, security, permissions, or an `AC-NN`).

### D4. Divergence Points Bound by `D-NN`
Verify that every boundary where two tasks or layers could diverge — shared entity/field names, state shape, error mapping, API payload/status codes, route arguments, shared components, storage keys — has a clear rule in `design.md` citing a `D-NN` (**`BLOCKER`** if missing or vague like *"follow standard conventions"*).

### D5. Verified Codebase & Profile Fit
- Every existing file path, class, package, or API named in `design.md` must appear in `codebase-notes.md` → `## 3. Verified Baseline Facts` or be explicitly marked `NEW` (**`BLOCKER`** if an unverified existing symbol is assumed).
- Deviations from the active architecture profile (`{{slot:architecture-design}}` / `{{slot:clean-architecture}}`) without a justifying `D-NN` are **`MAJOR`**.

---

## D6. Pass 3 — Cold-Reader Subagent Check (Reader Plays `code_writer`)

After Pass 1 (`PASS`) and Pass 2 (`0 BLOCKER`, `0 MAJOR`), spawn one fresh read-only subagent with this exact prompt:

```text
You are the Code Writer of this team. You have been handed the technical
architecture design (design.md) of a work item and must next implement it
phase by phase. You cannot talk to the author, and you have no chat history.

Read the document under review:
- {{vN_path}}/design.md

Already approved Gate 1 context (do not question unless design.md contradicts it):
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md

You may open files these documents cite by path, read-only, only to verify that
a cited path, class, or component exists. Do not use the codebase to fill gaps
left by design.md. Do not write or modify any file.

Report only the questions you would still need answered before you could build
this without guessing: places where you would have to invent a contract, class
signature, state transition, UI component mapping, error mapping, or test dataset,
and a wrong guess would matter.
For each question provide:
1. The question
2. Where it comes from (design.md section, D-NN, AC-NN, S-NN / C-NN)
3. Why the answer changes what you build
4. What you would guess if forced
Rank by importance, at most 10.

Skip local implementation details explicitly left to Code Writer and wording nits.
If nothing important is left, reply: nothing important left
```

Sort every returned question per [`SKILL.md` §5](../SKILL.md#5-pass-3--fresh-cold-reader-subagent-check) (`Answered already`, `Minor — Agent's call`, or `User's call — OPEN Q-NN`).
