# Tooling by stack

Defaults for the generated `02`, `03` and `05`. The workspace's installed tools and existing conventions win; never add a framework or library without the user's agreement.

| Stack | Framework | Doubles | Typical layout | Focused run | Full run | "Did it run?" |
|---|---|---|---|---|---|---|
| Python | `pytest` (+ `pytest-asyncio`) | Hand-written fakes of `Protocol` ports; `unittest.mock` / `monkeypatch` at external edges | `tests/unit/<mirror of app>/test_<topic>.py` | `uv run pytest tests/unit/<path>::<test> -q` | `uv run pytest tests/unit -q` | `-v` or `--collect-only -q` shows the test id; check passed/skipped counts |
| TS / Node (`node --test`) | `node:test` | Plain fakes; `mock.fn()` | co-located `*.test.mjs` / `*.test.ts` | `node --test <file>` | `npm test` | Test name in TAP output; count increased |
| TS / Vitest | `vitest` | `vi.fn`, `vi.mock` at module boundaries | co-located `*.test.ts(x)` or `__tests__/` | `npx vitest run <file> -t "<name>"` | `npm test` | Name in reporter output |
| TS / Jest (NestJS) | `jest` | `jest.fn`, Nest testing module with fake providers | `*.spec.ts` next to source | `npx jest <file> -t "<name>"` | `npm test` | Name in reporter output |
| Flutter | `flutter_test` | `mocktail`; `bloc_test` for blocs/cubits | `test/<mirror of lib>/<name>_test.dart` | `flutter test <file> --plain-name "<name>"` | `flutter test` | Test name in output; `+N` count |
| Go | `testing` | Interfaces with fake structs; `httptest` | `<pkg>/<name>_test.go` | `go test ./<pkg> -run <TestName> -v` | `go test ./...` | `=== RUN <TestName>` line |

## Determinism helpers

| Need | Python | TS | Flutter / Dart | Go |
|---|---|---|---|---|
| Time | inject a clock; `freezegun` if installed | `vi.useFakeTimers()` / inject `now()` | `clock` package / inject | inject `func() time.Time` |
| Random | seed or inject | inject generator | `Random(seed)` | `rand.New(rand.NewSource(seed))` |
| Async | `pytest-asyncio`, await everything | `await` / `vi.runAllTimersAsync()` | `await tester.pump()` / `blocTest` `wait` | `t.Parallel()` only when isolated |

## Coverage

Report coverage only if the workspace already measures it (`pytest --cov`, `vitest --coverage`, `flutter test --coverage`, `go test -cover`). Do not introduce a coverage gate without the user.
