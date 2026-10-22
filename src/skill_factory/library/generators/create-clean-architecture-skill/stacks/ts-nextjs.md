# Preset: TypeScript / Next.js (App Router)

> A starting point, not a final answer. Always tailor to the project and confirm with the user.

## Detect

`package.json` containing `next`. App Router if `app/` or `src/app/` exists; Pages Router if `pages/`. Check `zod`, `@tanstack/react-query`, `zustand`, `prisma`/`drizzle-orm`, `next-auth`.

## Framework-enforced conventions

`app/` file-based routing: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `route.ts`; route groups `(group)`; private folders `_name`. Server vs client components (`"use client"`), server actions (`"use server"`). `public/` for static files.

## Concept mapping

| Concept | In this stack |
|---|---|
| Presentation | `app/` routes (thin) + feature `components/` |
| Use case | Server-side function in `features/<f>/server/` called by server components/actions |
| Domain entity | TS types + pure functions in `features/<f>/domain/` (`full` only) |
| Repository / data access | `features/<f>/server/*.repository.ts` (DB) or `api/` (remote API client) |
| Input validation | `zod` schemas in `features/<f>/schemas/` |
| Client state / side effects | Hooks in `features/<f>/hooks/`, store in `stores/` |
| DI / composition root | Module-level clients in `lib/` (db, auth, http) |
| Config | `config/env.ts` validated with zod |

## Standard tree (feature-first)

```
src/
  app/                              # routing shell only — thin, calls into features
    (dashboard)/orders/page.tsx
    (dashboard)/orders/[id]/page.tsx
    api/webhooks/route.ts
    layout.tsx
  features/
    orders/
      components/                   # UI owned by this feature
      hooks/                        # client-side state & effects
      actions/                      # server actions ("use server")
      server/                       # server-only: queries, use cases, repositories
      schemas/                      # zod
      types.ts
      index.ts                      # public API
  components/ui/                    # design system, no business logic
  lib/                              # db client, auth config, http client
  config/
  stores/                           # global client state (only if needed)
```

## Lite / full variations

- **lite:** `app/` + `components/` + `lib/`, no `features/`.
- **full:** add `features/<f>/domain/` for pure rules; `server/` split into `use-cases/` and `repositories/` behind interfaces.

## Naming

| Kind | Pattern |
|---|---|
| Component file | `PascalCase.tsx` or `kebab-case.tsx` — pick one project-wide |
| Hook | `use-order-filters.ts` exporting `useOrderFilters` |
| Other files | `kebab-case.ts` |

## Enforcing import rules

`eslint-plugin-boundaries`, or the built-in `no-restricted-imports` for the essentials:
```js
'no-restricted-imports': ['error', { patterns: [
  { group: ['@/features/*/*'], message: 'Import from the feature public API (@/features/<name>).' },
]}]
```
Mark server-only modules with `import 'server-only'` so they cannot leak into client bundles.

## Stack-specific pitfalls

- Fat `page.tsx` files with data fetching, logic, and UI mixed.
- Importing server-only code (DB client) into client components.
- `"use client"` at the top of large trees, losing server rendering.
- A global `components/` folder holding feature-specific UI.

## Reference sources

Candidates to verify: Next.js official "Project structure" docs, `alan2207/bulletproof-react` (feature-based React structure).
