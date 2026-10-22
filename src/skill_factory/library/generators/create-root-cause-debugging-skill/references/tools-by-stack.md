# Tools by stack

Defaults for `05-tools-and-commands.md`. Prefer the workspace's scripts and tools; interactive debuggers that need a human (pdb, DevTools stepping) are not usable by an agent — use focused reruns, verbose output and temporary logging instead.

| Stack | Reproduce one | Rerun failed only | Verbose / stop at first | Notes |
|---|---|---|---|---|
| Python (pytest) | `uv run pytest <file>::<test> -q` | `uv run pytest --lf -q` | `-x -vv -s --tb=long` | `-p no:randomly` if a random-order plugin is installed; `--count` only if `pytest-repeat` exists |
| TS (node --test) | `node --test --test-name-pattern "<name>" <file>` | — | `--test-reporter=spec` | |
| TS (Vitest) | `npx vitest run <file> -t "<name>"` | `npx vitest run --changed` | `--reporter=verbose` | |
| TS (Jest) | `npx jest <file> -t "<name>"` | `npx jest --onlyFailures` | `--verbose --runInBand` | `--runInBand` exposes shared-state flakiness |
| Next.js build | `npm run build` | — | read the first error block | Server/client boundary errors name the importing file |
| Flutter | `flutter test <file> --plain-name "<name>"` | — | `-r expanded` | `flutter analyze <file>` for type errors |
| Go | `go test ./<pkg> -run '^<Test>$' -v` | — | `-count=1 -race` | `-count=1` defeats the test cache |

## Regressions

```bash
git bisect start <bad> <good>
git bisect run <command that exits non-zero on the failure>
git bisect reset
```

Only on a clean working tree; never in someone else's checkout.

## Code intelligence

If the workspace configures a code-intelligence tool (e.g. GitNexus: `query` for the error text, `context` for callers/callees, `impact` before editing a symbol, `detect_changes` before committing), its mandatory rules apply and go into `05`.
