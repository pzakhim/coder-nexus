# Self-check by stack

Starting points for `05-self-check.md`. Prefer the workspace's real configs, scripts and gates; list a tool only if it is installed or the user agrees to add it (never install it yourself).

| Stack | Format | Lint / analyze | Types | Rule-specific grep (review the hits, do not auto-fix) |
|---|---|---|---|---|
| Python | `ruff format` / `black` | `ruff check` | `pyright` / `mypy` | `grep -rnE "print\(|breakpoint\(|except Exception|# type: ignore" <changed files>` |
| TS / React / Next.js | `prettier --check` | `eslint` | `tsc --noEmit` | `grep -nE "console\.log|debugger|: any\b|as any|catch\s*(\([^)]*\))?\s*\{\s*\}" <changed files>` |
| TS / NestJS | `prettier --check` | `eslint` | `tsc --noEmit` | same as TS |
| Dart / Flutter | `dart format --set-exit-if-changed` | `flutter analyze` | (analyzer) | `grep -nE "print\(|debugPrint\(|// ignore:" <changed files>` |
| Go | `gofmt -l` | `go vet`, `golangci-lint run` | (compiler) | `grep -nE "fmt\.Println|panic\(" <changed files>` |

## Map rules to checks

| Rule | Check |
|---|---|
| C2 dead code | Linter unused-import/variable rules; `ruff` F401/F841, `eslint no-unused-vars`, Dart `unused_*` |
| C3 debug code | Grep column above; existing AST tests if any |
| C4 swallowed errors | Grep for broad catches; existing AST tests if any |
| C6 size | `wc -l <changed files>`; linters with max-lines / complexity rules if configured |
| C9 types | Type checker in strict mode |
| C14 | All of the above on the changed files, then the task's tests |

## Rules

- Run on **changed files** for the task check; on the whole branch only when the workspace's gate does.
- A grep hit is a prompt to look, not proof of a violation; a false positive is recorded with its reason.
