# Stack notes

Typical `stdlib` / `native` replacements and stack-specific smells for the generated catalog. Use only what the workspace's language version and installed libraries support.

## Python

| Hand-rolled | Use |
|---|---|
| Manual dict-of-lists grouping | `collections.defaultdict(list)`, `itertools.groupby` (sorted input) |
| String path joining | `pathlib.Path` |
| Manual `__init__`/`__eq__` boilerplate | `dataclasses.dataclass(frozen=True, slots=True)` |
| Hand-written enum strings | `enum.StrEnum` / `typing.Literal` |
| try/finally resource handling | `contextlib.contextmanager`, `with` |
| Caching dict | `functools.cache` / `lru_cache` |

Smells: service classes with only static methods; `Protocol` with one implementation and no fake in tests; nested comprehensions; `**kwargs` passthrough layers.

## TypeScript / React / Next.js

| Hand-rolled | Use |
|---|---|
| Manual query-string building | `URLSearchParams` |
| Deep clone helpers | `structuredClone` |
| Date/number formatting helpers | `Intl.DateTimeFormat`, `Intl.NumberFormat` |
| Loops building arrays/maps | `map`/`filter`/`Object.fromEntries` (one level) |
| `useEffect` + `useState` mirroring props/derived values | Compute during render |
| `useMemo`/`useCallback` everywhere | Remove where not measured |
| Wrapper component forwarding all props | Use the inner component |

Smells: hooks returning a large bag of state; prop drilling through components that do not use the props; barrel files re-exporting one module.

## Flutter / Dart

Collection-if/for instead of manual list building; `copyWith` from data classes instead of hand-written; extension methods instead of util classes with static members; no Bloc for state a `StatefulWidget` or a simple notifier holds.

## Go

`slices`/`maps` packages (Go 1.21+) instead of hand loops; `errors.Is/As` instead of string matching; small interfaces defined at the consumer, not one big interface with one implementation.
