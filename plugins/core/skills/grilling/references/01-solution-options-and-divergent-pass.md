# 01 — Solution Options & Divergent Pass (`Q-NN` Trade-Offs → `D-NN`)

Your first idea is rarely the only good one, and the user cannot reject an approach they never saw. Whenever a `Q-NN` row has **more than one materially different, viable way** to meet the confirmed `G-NN` goals, use this guide to construct 2–3 real options, present them as a single `ask_question` call with `(Recommended)` first, and record the rejected options in the `Options Considered` column of `## 1. Decision Log (D-NN)`.

## 1. When to Build 2–3 Options (vs. Fact vs. Simple Inference)

| Case | Condition | Action |
|---|---|---|
| **Verified Fact** | One way is forced by an existing contract, foundation class, codebase convention, or locked `D-NN`. | Do **not** ask. Record the fact and its `file:line` / source in `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes`. |
| **Single-Way Inference** | Only one way makes sense, but the user did not state it explicitly. | Queue a normal confirmation `Q-NN` (or include in [batch-confirm](../modes/batch-confirm.md) if low-risk). |
| **Multi-Way Trade-Off** | **2–3 materially different ways** meet the confirmed `G-NN` goals, differing in what the actor sees/does, scope, build cost, risk, reversibility, or where future change lands. | Build 2–3 real options (§2–§3), ask as one `Q-NN` with `(Recommended)` first, and log all options in `Options Considered` (§4). |
| **Out of Scope** | The topic serves no confirmed `G-NN`. | Do **not** ask. Record under **Non-goals** (`work-item-contract` goal lock). |

*(Different variable names, wording, or file layouts for the same underlying idea are **not** materially different options.)*

---

## 2. Optional Divergent Pass (6 Lenses in Working Notes)

Use this pass only when the first options you see are minor variants of a single idea, or when the user asks for alternatives. Skip it when 2–3 genuinely distinct options are already clear.

Write 4–6 one-line candidates in your working notes using the lenses that fit:

| Lens | Question to Ask Yourself | Typical Candidate Produced |
|---|---|---|
| **Inversion** | What if we did the opposite of the obvious approach? | Pull instead of push; warn instead of hard-block; system auto-selects instead of manual user input |
| **Remove a constraint** | Which assumed constraint is not a confirmed `D-NN` or verified fact? What if it were removed? | Reveals a much cheaper path, or exposes an unconfirmed constraint that should be asked as a `Q-NN` |
| **10x simpler** | What is the smallest version that still satisfies every confirmed `G-NN`? | Fewer screens, reuse of an existing flow or component, zero new API contract |
| **Audience shift** | What if the primary actor were a different role (admin, first-time user, support, background job)? | Different entry point, defaults, or permission scope |
| **Reuse** | What does the codebase or Kit already do that nearly fits? | Extend an existing module/widget instead of building a new one |
| **Combination** | Can two partial ideas merge cleanly into one stronger option? | A hybrid option combining the best traits of two candidates |

**Converge before asking**:
1. Drop any candidate that misses a confirmed `G-NN`, contradicts a locked `D-NN`, crosses your role's ownership boundary (see `modes/{spec,planning}.md`), or is a strawman.
2. Keep the **2–3 strongest candidates** that differ most in what the decision owner cares about. Never dump the raw 4–6 divergent list onto the user.

---

## 3. Describing & Presenting the 2–3 Options

Ground every option in the read sources, `## 1. Decision Log (D-NN)`, and verified codebase facts (`## 3`). Evaluate each option across the same 5 fields:

| Field | Content |
|---|---|
| **What it is** | 1–2 sentences in the role's vocabulary (business/UX terms for `spec_writer`; architecture/contract terms for `planning`) |
| **Goals (`G-NN`)** | Which confirmed `G-NN` it fulfills fully or partially |
| **Gains** | What it makes easy, fast, or low-risk |
| **Costs / Trade-offs** | What it makes harder, slower, riskier, or harder to reverse |
| **Evidence** | The source, `D-NN`, or `file:line` supporting the claims |

- **Recommend one (`(Recommended)` first)**: Place the recommended option first in `ask_question` and state in one line why it wins (tied to a `G-NN` or codebase evidence).
- **Only one sensible way after converging?** State in one line why alternatives do not fit and ask it as a standard confirmation `Q-NN`.

---

## 4. Recording in `Decision Log (D-NN)` & Straight-Line Documents

1. When the user makes a clear pick (`grilling` §3):
   - Mark `Q-NN` → `CLOSED -> D-NN`.
   - In `codebase-notes.md` → `## 1. Decision Log (D-NN)`:
     - **`Options Considered`**: List **every** option presented (recommended first), each with its core trade-off and, for rejected options, why it was not chosen.
     - **`User Confirmed Decision`**: Record only the chosen option, ending with `(user choice)` or `(default accepted)`.
2. Write the chosen option into the gate document in **one straight locked-in line** citing `D-NN`:
   - `requirements.md`: `BR-NN`, `## Workflows` (`W-NN`), scope items, and `AC-NN`
   - `design.md`: `## Architectural decision` and layer/contract sections
3. **Never bend**:
   - Never leave `Option A / Option B`, comparison tables, `TBD`, or `Assumptions` inside `requirements.md` or `design.md` (`REQ-003`, `NOTES-005`).
   - Never cross role ownership: `spec_writer` options carry no technical implementation choices; `planning` options never alter user-visible business behavior.
