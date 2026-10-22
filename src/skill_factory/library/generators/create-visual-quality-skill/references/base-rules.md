# Base rules (generic, every workspace)

Generalised from a real workspace's visual-fidelity check and the Coder Nexus approved-design comparison. Each rule goes into the generated skill with the workspace's references, tokens, components and tool **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| V1 | **Compare against a named reference.** The approved design (mockups, HTML design screens, design system) at its approved revision; when none exists, the pre-change UI as a **labelled baseline**. | Without a fixed reference, "looks right" is opinion. | 01 |
| V2 | **Like for like.** Same screen, state, viewport, data, role and theme as the reference. | Different inputs produce differences that are not defects. | 01, 02 |
| V3 | **Capture with the workspace's browser tool** (the one confirmed for quality-acceptance), saved under the evidence path with predictable names. | Consistent captures can be compared across rounds. | 02 |
| V4 | **Judge by dimensions:** layout and hierarchy, spacing and alignment, typography, colors via design tokens, shared components, icons, UI states, responsiveness, copy, basic accessibility (contrast, focus, keyboard in modals). | Dimensions turn taste into checkable statements. | 03 |
| V5 | **Classify deviations.** Blocking: breaks the approved layout or a required state, wrong component or token in a visible way, unreadable/inaccessible, wrong copy that changes meaning. Minor: small spacing/alignment differences. A deviation covered by a recorded decision is accepted. | Not every pixel matters; the important ones must block. | 04 |
| V6 | **Diff tools are optional helpers.** Use pixel/screenshot diffs only where installed and stable; always state the reason for each deviation in words. | A diff percentage without a reason is not actionable. | 02, 04 |
| V7 | **Baselines change only with approval.** Updating the approved baseline/reference needs the user's (or design owner's) approval. | Silently moving the baseline hides regressions. | 01 |
| V8 | **No judging by taste.** Only deviations from the reference or the design system count; suggestions go to a separate list. | Personal preference findings erode trust in real ones. | 04 |
| V9 | **Per-screen report.** For each screen × state × viewport: reference, screenshot, deviations with severity, result. | Each verdict line is checkable. | 04 |
| V10 | **Missing reference or state is not a pass.** No reference → `BLOCKED` (or labelled baseline comparison if the plan allows); a state that could not be produced → `NOT_RUN`. | Absence of evidence is not fidelity. | 01, 04 |
| V11 | **No secrets or personal data on screen.** Test data only; redact before saving. | Screenshots travel further than logs. | 02 |
| V12 | **Read-only.** Never adjust styles or code to make a screen match; report the deviation. | A tester who fixes CSS stops being independent. | SKILL |

**Never "not adopted":** V1, V2, V10, V11, V12.
