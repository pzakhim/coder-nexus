# 03 — Smell catalog

Rules SM3, SM4, SM5, SM10, SM11 and SM12. Reason: concrete examples tell the agent what avoidable complexity looks like in a Python/FastAPI service, which generic advice cannot. Every simplification names one row here or a rule of `{{slot:clean-code}}`. Examples are **illustrative** (no workspace is scanned for a pack skill); the workspace may add its own rows.

Ask in order: **needed?** → **already in the repo?** → **stdlib / FastAPI / Pydantic / SQLAlchemy?** → only then write the minimum.

## General rows

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `flatten` | Deep nesting, arrow code; happy path at the deepest level (beyond the `{{slot:clean-code}}` nesting limit) | `if user: if user.is_active: if order: ...` | Guard clauses, early `return`/`raise`; one well-named function per branch | Error paths keep their order, exception types and messages |
| `shrink` | Clever code: nested comprehensions, `reduce` chains, `lambda` towers, metaclasses, `getattr` dispatch, recursion where a loop is plainer, nested conditional expressions | `[x for g in groups for x in g if x if f(x)]` | Plain loop or one level of comprehension | Plain is not longer for its own sake |
| `yagni` | Speculative abstraction: `Protocol`/ABC with one implementation and no test fake, factory with one product, settings field nobody sets, parameter always passed the same value | `class Notifier(Protocol)` + only `EmailNotifier`, no fake in `tests/` | Use the concrete class; inline the single user | Ports required by `{{slot:clean-architecture}}` or a `D-NN` stay |
| `inline` | Premature extraction: a shared helper or base class for two call sites now growing flags or per-caller branches | `def build_query(..., for_admin: bool = False)` | Inline back into each caller; extract on the third real repetition | Logic only; definitions are never duplicated (next row) |
| `delete` | Duplicated definitions: the same Pydantic model, ORM column set, enum, constant or SQL in two places | `STATUS_PAID = "paid"` in `orders` and `payments` | One definition in its owning module; every user imports it | Look-alikes for different concepts (create vs response schema) stay separate |
| `shrink` | Long parameter list (beyond the `{{slot:clean-code}}` limit); the same values always travel together | `def create(tenant_id, user_id, name, email, phone, ...)` | One Pydantic model or frozen dataclass for values that belong together; drop derivable parameters | Do not invent a type for unrelated values |
| `inline` | Flag argument switching two jobs | `save(order, notify=True)` used as two behaviors | Two functions named for each job | A flag that is real user data is not a flag argument |
| `inline` | Needless indirection: pass-through layer, middle man, module exporting one trivial thing | `OrderService.get(id)` that only returns `self.repo.get(id)` | Call the target directly; delete the hop | Keep hops that add validation, authorization, mapping, caching or error translation |
| `delete` | Dead code: unused function, parameter, branch, import, settings field, file; commented-out code | `# old_total = compute_v1(order)` | Delete it and the arguments callers no longer need (ruff `F401`, `F841`, `ARG`, `ERA001` where enabled) | Check dynamic use (routes, task names, `getattr`, settings keys) first |

## Python / backend rows

| Tag | Smell | Example (illustrative) | Technique | Keep it when |
|---|---|---|---|---|
| `inline` | Needless class: only `__init__` + one method, or only `@staticmethod`s | `class PriceUtils: @staticmethod def net(...)` | Module-level function (`_` prefix if one module uses it) | The class holds injected dependencies FastAPI wires per request |
| `delete` | Getters/setters or `@property` that only returns `self._x` | `def get_name(self): return self._name` | Plain attribute, frozen dataclass or Pydantic field | It validates, computes or protects an invariant |
| `yagni` | Inheritance for reuse: base class to share two helpers; subclasses override to switch behavior off | `class BaseService: def _log(...)` | Composition: call a function or inject a collaborator | A framework requires the base (`DeclarativeBase`, `BaseModel`, `BaseSettings`) |
| `yagni` | Single-implementation repository `Protocol` | `OrderRepository(Protocol)` + one `SqlAlchemyOrderRepository`, no fake | Use the concrete repository directly | `{{slot:clean-architecture}}` makes it a port, or a unit test uses a fake through it |
| `yagni` | Generic repository `BaseRepository[T]` used by one or two entities plus per-entity overrides | `get/list/create/update/delete` for every model | Concrete methods named for the queries use cases need (`list_open_for_tenant`) | Three or more entities share the exact same query shapes today |
| `inline` | `**kwargs` pass-through layer | `def create(self, **kwargs): return self.repo.create(**kwargs)` | Explicit keyword parameters or one model parameter | Never in new code: mypy cannot check it |
| `stdlib` | Dict as record: `dict[str, Any]` built and read by key across functions | `order["total"]` in four functions | `@dataclass(frozen=True, slots=True)` or a Pydantic model | It is a true mapping (id → value) |
| `stdlib` | Manual resource handling | `try: ... finally: client.close()` | `with` / `async with`; `contextlib.contextmanager` / `asynccontextmanager` | — |
| `stdlib` | Hand-rolled grouping | `if k not in d: d[k] = []` | `collections.defaultdict(list)`; `itertools.groupby` on sorted input | — |
| `stdlib` | String paths | `base + "/" + name` | `pathlib.Path(base) / name` | — |
| `stdlib` | Boilerplate dunders | Hand-written `__init__`, `__eq__`, `__repr__` | `@dataclass(frozen=True, slots=True)` | Custom equality is a real domain rule |
| `stdlib` | Hand-written enum strings | `STATUS_PAID = "paid"` constants | `enum.StrEnum` or `typing.Literal` | — |
| `stdlib` | Ad-hoc caching dict at module level | `_cache: dict = {}` | `functools.cache` / `lru_cache` on a pure function, or the cache the architecture names | The value depends on request or tenant: never cache it in a module |
| `native` | Manual validation before building a model | `if len(name) > 100: raise ...` | Pydantic types and `Field(min_length=..., max_length=..., ge=...)` | The rule needs other data (a DB lookup) and belongs in the service |
| `native` | Sync wrapper around async in request code | `asyncio.run(...)` or a thread to call async code | Make the caller `async` and `await` | — |
| `native` | Hand-built SQL strings or manual row-to-dict mapping where SQLAlchemy 2.x does it | `text(f"SELECT ... {id}")`; `dict(zip(cols, row))` | `select()` with bound parameters; `scalars()` / ORM objects; `response_model` for serialization | A measured hot path needs `text()` with bound parameters |

## Rule of three

Extract shared logic on the third repetition; two may stay. Definitions (Pydantic models, ORM models, enums, constants, SQL) are never duplicated (`{{slot:clean-code}}`). Reason: early extraction couples code that later diverges; duplicated definitions drift.

## Leave these alone

- Ports and abstractions `{{slot:clean-architecture}}` or a `D-NN` requires.
- A FastAPI dependency function that builds a service from its dependencies: it is the wiring point, not a pass-through.
- Separate Pydantic models for create input, update input and response: different contracts (mass assignment, `{{slot:secure-coding-standards}}`).
- Explicit `select()` statements repeated in two repository methods with different filters (rule of three).
- Long but linear code with one job: Alembic migrations, mapping tables, prompt text, generated code.
- Defensive checks at trust boundaries: input validation, authorization, tenant/data scope.

## Reduce or relocate?

Before keeping a change, count the concepts a reader must hold (names, branches, modes, layers) before and after. Same count means the complexity only moved: revert it. Prefer the change that makes a whole branch, mode or layer disappear.

## Candidate line

`<smell> at <path:line>: <what to cut> -> <replacement>`
