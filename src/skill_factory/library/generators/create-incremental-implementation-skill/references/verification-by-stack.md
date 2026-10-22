# Verification commands by stack

Starting points for `06-verification.md`. Always prefer the workspace's real scripts (`Makefile`, `package.json` scripts, CI steps, existing gates found in P2) over these defaults, and confirm them at the gate.

| Stack | Task-level check (I6) | Phase suite (I7) | Visual (I8) |
|---|---|---|---|
| Python / FastAPI | `uv run ruff check <files>`; `uv run pytest <test file> -q` | `uv run pytest -q` (+ architecture tests if present) | — |
| Python / Django | `python -m pytest <test file>` | `python -m pytest`; `python manage.py check` | — |
| TS / NestJS | `npx eslint <files>`; `npx jest <test file>` | `npm test`; `npm run build` | — |
| TS / Next.js | `npx eslint <files>`; `node --test <file>` or `npx vitest run <file>` | `npm test`; `npm run build` (+ boundary script if present) | Run the dev server and check the approved routes/states in a browser |
| TS / React + Vite | `npx eslint <files>`; `npx vitest run <file>` | `npm test`; `npm run build` | Dev server + approved states |
| Flutter | `flutter analyze <files>`; `flutter test <test file>` | `flutter analyze`; `flutter test` | Run on the approved device/simulator; capture the approved states |
| Go | `go vet ./<pkg>`; `go test ./<pkg> -run <Test>` | `go test ./...`; `go build ./...` | — |

## Evidence line format

```
<command> @ <revision> on <target> → PASS | FAIL | NOT_RUN | BLOCKED | UNVERIFIED (<short reason>)
```

## Rules

- A command that was not run is `NOT_RUN`, never omitted.
- A command that cannot run (missing service, missing credentials) is `BLOCKED` with the reason.
- Visual checks name the target (route/screen, state, device/browser) and the revision.
