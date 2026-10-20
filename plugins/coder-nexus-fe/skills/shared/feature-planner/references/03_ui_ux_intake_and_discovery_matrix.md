# 03 — UI/UX Intake and Sequential Component Discovery

Apply the approved profile through [core-usage](../../../flutter/core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

## Visual Intake Gate

For UI-affecting work, inspect the supplied Figma frame, screenshot, PDF or local design asset directly before choosing components or writing the plan. A text description alone does not replace an available visual. If no visual source exists, record `VISUAL_INPUT_MISSING`, draft a minimal layout specification, and request user confirmation at Gate 2. Never invent a generic screen as a fallback.

## Visual deconstruction and Visual AC

Record the actual design source and observable details: layout hierarchy, spacing and alignment, typography, color and surface tokens, radius/elevation, icons, and required initial/loading/populated/empty/error/interactive states. Cite measured values only when supported by the source or verified Client design system. Map each Visual AC to the relevant UI phase and runtime target.

A UI can pass analyzer and tests yet still be `FAILED` when it materially differs from the approved Designer visual or Visual AC. Verify touch targets (normally at least **48x48 dp** on Android and **44x44 pt** on iOS) and text contrast (normally at least **4.5:1** for regular text) against the project's accessibility requirements. Preserve entered input on recoverable failures when the approved behavior requires it.

## Sequential Reuse Ladder

Check in order:

1. The `app_ui_kit` GUIDE decision table (and app_core for `BaseScreen`, `ListViewPaging`, `LabelText`), read via `{{slot:core-usage}}`.
2. Shared Client widgets under the actual `lib/commons/widgets/` path.
3. Composition of verified existing components.
4. A feature-private widget under `lib/modules/<feature>/presentation/widgets/`, only after the approved design records the verified gap.

Do not recreate a kit component. Confirm each chosen widget's constructor, defaults, callbacks and variant in the GUIDE or package source; source wins over the guide. Missing or mismatched source keeps the dependent phase `BLOCKED`.

## Component Discovery Matrix

Record this matrix in `design.md` and link relevant rows from UI phases:

| UI element / AC | Choice | Component and variant | Verified Client import | Source file, symbol and revision | Tokens and accessibility | Gap or decision |
|---|---|---|---|---|---|---|
| Actual element from the approved design | `REUSED` / `COMPOSITION` / `CUSTOM` / `BLOCKED` | Verified candidate or N/A | Verified path or BLOCKED | Actual source evidence | Verified values | Actual decision reference |

The row above is a schema, not task data. Fill it only from real design, core GUIDE and Client evidence.

## Four-case decision matrix

1. **One viable verified Kit match:** Select it automatically, even if styling differs from the visual; Kit styling wins. Record the difference and revise conflicting Visual AC during Gate 2.
2. **One match with a visual difference:** Apply case 1 when role and behavior fit; do not create a replacement or restyle the Kit.
3. **Several viable matches:** Ask one structured question with 2–3 options and a recommendation.
4. **No viable Kit match:** Verify shared widgets, composition and the Flutter SDK. Use verified composition when possible; otherwise document the gap and plan a feature-private widget. A missing GUIDE row alone never authorizes custom code; check composition first.

Call `get_ux_error_patterns` for relevant validation, timeout, auth or empty/error behavior. Do not copy a pattern into an unrelated feature or invent tokens, props, callbacks or UI states.
