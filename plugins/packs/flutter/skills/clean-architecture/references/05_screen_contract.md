# Screen contract for Flutter Client work

Apply the approved profile through [core-package-usage](../../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> Source: Screen contract and architectural guidelines. Always inspect the active workspace definitions of `BaseScreen`, `BaseScreenState`, tracking state, and responsive mixin. A commented-out or missing class is evidence of an unavailable API, not a usable import or proof of runtime behavior.

## Decide what is a screen

Before naming files or choosing a widget superclass, inspect the approved flow, Client router, existing destinations and their ownership. A screen is an independently navigable full UI destination at screen level; it need not be complex or hold local state. Put feature screens in `lib/modules/<feature>/presentation/screens/`, name files `*_screen.dart`, and name widget classes `*Screen`. A dialog, bottom sheet or child widget is not a screen merely because it uses `StatefulWidget`; put it with the feature's widgets or the Client's verified shared UI. If a full-screen modal's ownership is unclear, resolve it in design from the real route and neighboring UI.

Every new or modified screen in the approved task uses the Client's active `BaseScreen` and `BaseScreenState` contract, including its screen metadata hook (such as `getScreen()`) and required layout hook. This applies even when an ordinary `StatelessWidget` could render the content. A standard implementation provides `BaseScreenState<Screen> createState()` and `ScreenModel getScreen()`; the template leaves these overrides to be filled from the resolved Client API. Cubit state classes never replace either screen base class. Use the existing screen registry and route declaration; do not create an `AppScreen` entry or import from an example without verifying the Client API. Route annotations, Cubit providers and DI follow the Client's real router and ownership model.

## Verify the base before implementation

Read the Client's `pubspec.yaml`, lockfile and resolved package source, then inspect the active definitions of `BaseScreen`, `BaseScreenState`, `ScreenModel` and their inherited tracking and responsive behavior. Compare at least one working screen and its router/DI registration. A commented class, historical Git version, guide entry or screenshot alone is not an available API. If the resolved Client has no usable base screen or required metadata/layout hook, report `BLOCKED` with the missing source and return to the affected design decision. Do not invent a stub, remove tracking or silently fall back to `StatefulWidget`.

For an existing feature, rename or migrate only screens in the approved change scope. Update imports, route references, registry references and tests together. Leave unrelated historical Client files in place.

## Review and evidence

Spec Writer records intended destinations in requirements. Planning records the selected profile, verified screen source, registry/route and checks in design. Code Writer implements against that source. Reviewer checks naming, inheritance, metadata, lifecycle, routing and side effects on the same revision. Test Runner runs analyzer and targeted behavior checks; tracking and responsive portrait/landscape claims require actual Client evidence on the relevant target. Hub lexical checks can detect obvious declarations and paths; they cannot prove package resolution, that tracking fires, or that orientation layouts render correctly. Mark those checks `UNVERIFIED`, `BLOCKED` or `NOT_RUN` until independently checked.
