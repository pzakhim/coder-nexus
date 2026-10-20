# 04 — Flutter Reuse Ladder and Component Discovery

Flutter values for the core `feature-planner` UI/UX intake (Visual Intake Gate, Visual AC and the four-case decision matrix stay in the core reference). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

## Sequential Reuse Ladder (Flutter)

Check in order:

1. The `app_ui_kit` GUIDE decision table (and app_core for `BaseScreen`, `ListViewPaging`, `LabelText`), read via this skill.
2. Shared Client widgets under the actual `lib/commons/widgets/` path.
3. Composition of verified existing components.
4. A feature-private widget under `lib/modules/<feature>/presentation/widgets/`, only after the approved design records the verified gap.

Confirm each chosen widget's constructor, defaults, callbacks and variant in the GUIDE or package source; source wins over the guide.

## No viable Kit match

Verify shared widgets, composition and the Flutter SDK. Use verified composition when possible; otherwise document the gap and plan a feature-private widget. A missing GUIDE row alone never authorizes custom code; check composition first.
