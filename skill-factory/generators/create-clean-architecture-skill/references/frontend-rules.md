# Frontend rules (framework-agnostic)

Knowledge used to fill the frontend branch (`fe/` in the fullstack layout, or the flat layout for an FE-only project). Express every rule with real paths and the stack's syntax. Mark a rule "not adopted" rather than forcing it.

| # | Topic | Rule | Goes into |
|---|---|---|---|
| F1 | No BE architecture in React/Vue/... | No Entity/Repository/UseCase classes per component. FE layers are: route → view → hook/composable → pure utils → transport. | 02, 05, 07 |
| F2 | Feature public barrel | Exactly one public entry per feature (`index.ts`); no nested barrels; no aggregator barrel re-exporting every feature. | 03, 05 |
| F3 | Minimal feature root + subfolder whitelist | The feature root holds only the barrel (and its style file). Subfolders come from a fixed whitelist (e.g. `views/ modals/ components/ hooks/ types/ utils/`). | 01, 03 |
| F4 | Thin routes | Route files only read params and compose feature views; a line cap; no state, effects or API calls. | 02, 04, 05 |
| F5 | Server/client boundary | For SSR frameworks: server by default, client directive at the smallest interactive leaf, server-only modules guarded, secrets never reach the client graph, explicit caching keys per scope. | 08-framework-boundaries |
| F6 | State & API ownership | One owner per state; derived values computed, not synced; mutations from events, not effects; explicit UI states (loading/empty/error/forbidden/conflict); stale responses suppressed on scope change. | 09-state-and-api-flow |
| F7 | Transport layer | One API client + contract types; documented error shape; no UI concerns (toasts, navigation) in transport. | 02, 09 |
| F8 | UI permissions | Read capabilities from one central context; never compare role strings; hiding is UX only. | 05, 09 |
| F9 | Styling architecture | Design tokens are the single source of truth; feature styles co-located and prefixed; no hard-coded colors. | 10-styling-ui |
| F10 | Shared UI | Promote to shared UI only when used by ≥ 2 features and free of business meaning; layouts receive feature UI through slots/children. | 05, 10-styling-ui |
| F11 | Dependency direction | Shared layers (`ui`, `layout`, `providers`, `lib`, global hooks) never import features; features use each other only via barrels, no cycles. | 05 |
| F12 | Type placement | API contract types in one shared place; feature-only types inside the feature; no functions in type files. | 02, 03 |
| F13 | FE gate | Enforce the rules with ESLint boundaries/`no-restricted-imports` or a grep script; list rule codes and how false positives are recorded. | 05 |
| F14 | Splitting long components | Split by UI responsibility into subcomponents; logic into hooks; pure steps into utils; never into tiny fragments. | 04 |

## Stack notes

- Next.js App Router: `app/` as shell, RSC by default, `'use client'` leaves, `server-only`.
- React + Vite (SPA): no server/client split; F5 becomes "secrets never in the bundle, env vars prefixed public only".
- Flutter/mobile: "route" = page/screen, "hook" = state holder (Bloc/Notifier), F9 = theme tokens.
- Other stacks: map each row via `stacks/<stack>.md`.
