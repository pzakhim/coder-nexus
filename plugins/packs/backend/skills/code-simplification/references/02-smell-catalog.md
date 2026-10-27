# 02 — Smell Catalog (Four Lenses)

Rules S4–S10. Reason: concrete examples tell the agent what avoidable complexity looks like in a Python/FastAPI service, which generic advice cannot. Every simplification names one row here or a rule of `{{slot:clean-code}}`. Examples are **illustrative** (no workspace is scanned for a pack skill); the workspace may add its own rows.

Ask in order: **needed?** → **already in the repo?** → **stdlib / FastAPI / Pydantic / SQLAlchemy?** → only then write the minimum.

Pass the diff through the four lenses in order. A host that supports subagents may run the lenses in parallel; the findings and the rules are the same.

## 1. Reuse (S5, S7)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `reuse` | New helper, dependency or query that the repository already has | A second `get_current_tenant()` next to the one in `app/api/deps.py` | Call the existing one; delete the copy | Do not bend the existing one with flags for a single caller |
| `delete` | Duplicated definitions: the same Pydantic model, ORM column set, enum, constant or SQL in two places | `STATUS_PAID = "paid"` in `orders` and `payments` | One definition in its owning module; every user imports it | Look-alikes for different concepts (create vs response schema) stay separate |
| `inline` | Premature extraction: a shared helper for two call sites now growing flags or per-caller branches | `def build_query(..., for_admin: bool = False)` | Inline back into each caller; extract on the third real repetition | Logic only; definitions are never duplicated |
| `native` | Manual validation before building a model | `if len(name) > 100: raise ...` | Pydantic types and `Field(min_length=..., max_length=..., ge=...)` | A rule that needs other data (a DB lookup) belongs in the service |
| `native` | Hand-built SQL strings or manual row-to-dict mapping where SQLAlchemy 2.x does it | `text(f"SELECT ... {id}")`; `dict(zip(cols, row))` | `select()` with bound parameters; `scalars()` / ORM objects; `response_model` for serialization | A measured hot path may need `text()` with bound parameters |

### Already shipped (stdlib)

| Hand-rolled | Use instead |
|---|---|
| `try: ... finally: client.close()` | `with` / `async with`; `contextlib.contextmanager` / `asynccontextmanager` |
| `if k not in d: d[k] = []` | `collections.defaultdict(list)`; `itertools.groupby` on sorted input |
| `base + "/" + name` | `pathlib.Path(base) / name` |
| Hand-written `__init__`, `__eq__`, `__repr__` | `@dataclass(frozen=True, slots=True)` (unless custom equality is a real domain rule) |
| `STATUS_PAID = "paid"` string constants | `enum.StrEnum` or `typing.Literal` |
| `dict[str, Any]` read by key across functions | `@dataclass(frozen=True, slots=True)` or a Pydantic model (unless it is a true id → value mapping) |

## 2. Simplification (S6, S8)

| Tag | Smell | Example (illustrative) | Technique | Keep it when |
|---|---|---|---|---|
| `yagni` | `Protocol`/ABC with one implementation and no test fake, factory with one product, settings field nobody sets | `class Notifier(Protocol)` + only `EmailNotifier`, no fake in `tests/` | Use the concrete class; inline the single user | `{{slot:clean-architecture}}` makes it a port, or a `D-NN` requires it |
| `yagni` | Generic repository `BaseRepository[T]` used by one or two entities plus per-entity overrides | `get/list/create/update/delete` for every model | Concrete methods named for the queries use cases need (`list_open_for_tenant`) | Three or more entities share the exact same query shapes today |
| `yagni` | Inheritance for reuse: base class to share two helpers; subclasses override to switch behavior off | `class BaseService: def _log(...)` | Composition: call a function or inject a collaborator | A framework requires the base (`DeclarativeBase`, `BaseModel`, `BaseSettings`) |
| `inline` | Needless indirection: pass-through layer, middle man | `OrderService.get(id)` that only returns `self.repo.get(id)` | Call the target directly; delete the hop | The hop adds validation, authorization, mapping, caching or error translation |
| `inline` | Needless class: only `__init__` + one method, or only `@staticmethod`s | `class PriceUtils: @staticmethod def net(...)` | Module-level function (`_` prefix if one module uses it) | The class holds dependencies FastAPI wires per request |
| `inline` | `**kwargs` pass-through layer | `def create(self, **kwargs): return self.repo.create(**kwargs)` | Explicit keyword parameters or one model parameter | Never in new code: mypy cannot check it |
| `inline` | Flag argument switching two jobs | `save(order, notify=True)` used as two behaviors | Two functions named for each job | The flag is real user data |
| `delete` | Getters/setters or `@property` that only returns `self._x` | `def get_name(self): return self._name` | Plain attribute, frozen dataclass or Pydantic field | It validates, computes or protects an invariant |
| `shrink` | Derivable state stored and kept in sync by hand | `order.item_count` updated next to `order.items` | Compute it where it is read | A measured hot path caches it |
| `shrink` | Long parameter list; the same values always travel together | `def create(tenant_id, user_id, name, email, phone, ...)` | One Pydantic model or frozen dataclass; drop derivable parameters | The values are unrelated |
| `flatten` | Deep nesting, arrow code (beyond the `{{slot:clean-code}}` C6 limit) | `if user: if user.is_active: if order: ...` | Guard clauses, early `return`/`raise`; one well-named function per branch | — (error paths keep order, types and messages) |
| `shrink` | Clever code: nested comprehensions, `reduce` chains, `lambda` towers, metaclasses, `getattr` dispatch | `[x for g in groups for x in g if x if f(x)]` | Plain loop or one level of comprehension; a dict or one `match` for dispatch | — |

Dead code (unused function, parameter, branch, import, settings field, commented-out code) is `{{slot:clean-code}}` C2 (ruff `F401`, `F841`, `ARG`, `ERA001` where enabled); check dynamic use first.

## 3. Efficiency (S9)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `batch` | N+1 queries: one query per row inside a loop | `for o in orders: await repo.get_customer(o.customer_id)` | One `select(...).where(Customer.id.in_(ids))`, or `selectinload` on the relationship | Result order and missing-row behavior stay the same |
| `dedupe` | The same query, settings read or parse repeated in one request path | `get_settings()` and `repo.get(id)` called twice in one handler | Load once and pass the value | Data that must be re-read after a write stays re-read |
| `concurrent` | Independent outbound calls awaited one after another | `a = await client.get(u1); b = await client.get(u2)` | `asyncio.gather` (or a `TaskGroup`) | Not over one shared `AsyncSession`; error and cancellation behavior stay the same (§4 traps) |
| `defer` | Heavy or blocking work at import time or in a hot request path | Loading a model file or opening a client at module import; sync `requests` in an `async def` | Create it in the FastAPI lifespan or on first use; use the async client | Startup checks that must fail fast stay in the lifespan |
| `narrow` | Long-lived callback, background task or cache entry that captures a large scope | A closure over the whole request/session stored in a module-level registry | Pass only the ids/values it needs | Never keep request or tenant data in module state (`{{slot:clean-code}}` C15) |

Any change here on a hot path needs a measurement first ([01](01-scope-and-safety.md) §7).

## 4. Altitude (S10)

| Tag | Smell | Example (illustrative) | Technique | Watch out |
|---|---|---|---|---|
| `generalize` | Special case for one endpoint layered onto shared code | `if request.url.path == "/orders/export": ...` inside a shared dependency or middleware | Move the special case to that endpoint, or change the shared mechanism so it is not needed | A change to shared code outside the diff → Concerns |
| `root` | Symptom patched where it surfaces | `or 0`, a broad `except` with a default, a re-sort in the router, while the wrong value comes from a query in the same diff | Fix the query or mapping that produces it; delete the patch | Never swallow errors to hide a symptom (`{{slot:clean-code}}` C4) |
| `merge` | A new path added next to the old one for the same job | `create_order_v2()` beside `create_order()` with both still called | Keep one; move callers in the same step | Callers outside the diff → Concerns |

## Rule of three

Extract shared logic on the third repetition; two may stay. Definitions (Pydantic models, ORM models, enums, constants, SQL) are never duplicated (`{{slot:clean-code}}` C1). Reason: early extraction couples code that later diverges; duplicated definitions drift.

## Leave these alone

- Ports and abstractions `{{slot:clean-architecture}}` or a `D-NN` requires.
- A FastAPI dependency function that builds a service from its dependencies: it is the wiring point, not a pass-through.
- Separate Pydantic models for create input, update input and response: different contracts (mass assignment, `{{slot:secure-coding-standards}}`).
- Explicit `select()` statements repeated in two repository methods with different filters (rule of three).
- Long but linear code with one job: Alembic migrations, mapping tables, prompt text, generated code.
- Defensive checks at trust boundaries: input validation, authorization, tenant/data scope.
- Explicit `if` / `match` branches: do not replace simple branching with class polymorphism hierarchies; a lookup dict or a single `match` is the simpler form.

## Reduce or relocate?

Before keeping a change, count the concepts a reader must hold (names, branches, modes, layers) before and after. Same count means the complexity only moved: revert it. Prefer the change that makes a whole branch, mode or layer disappear.

## Candidate line

`<lens>/<tag> at <path:line>: <what to cut> -> <replacement>`

## 5. Before / After Reference Examples

### Example A — `simplification/flatten` + `shrink` (Arrow code & derivable state → Guard clauses & computed property)

```python
# ❌ BEFORE (Smell: 3-level nested arrow code + manually synced `item_count` state)
def apply_discount(order: Order, actor: Actor) -> Decimal:
    if order.status == OrderStatus.DRAFT:
        if order.tenant_id == actor.tenant_id:
            if len(order.items) > 0:
                order.item_count = len(order.items)
                return sum((i.subtotal for i in order.items), Decimal("0")) * Decimal("0.9")
            return Decimal("0")
        raise ForbiddenError("Cross-tenant access denied")
    raise ConflictError("Only draft orders accept discounts")

# ✅ AFTER (Simplified: Flat guard clauses; `item_count` derived via @property on Order)
def apply_discount(order: Order, actor: Actor) -> Decimal:
    if order.status != OrderStatus.DRAFT:
        raise ConflictError("Only draft orders accept discounts")
    if order.tenant_id != actor.tenant_id:
        raise ForbiddenError("Cross-tenant access denied")
    if not order.items:
        return Decimal("0")
    return sum((i.subtotal for i in order.items), Decimal("0")) * Decimal("0.9")
```

### Example B — `efficiency/batch` (N+1 loop queries → Single batched query)

```python
# ❌ BEFORE (Smell: N+1 query inside loop over orders)
summaries: list[OrderSummary] = []
for order in orders:
    customer = await customer_repo.get_by_id(tenant_id, order.customer_id)
    summaries.append(OrderSummary(id=order.id, customer_name=customer.name))

# ✅ AFTER (Simplified: 1 batched `IN` query preserving order and behavior)
customer_ids = {o.customer_id for o in orders}
customers_by_id = await customer_repo.get_many_by_ids(tenant_id, customer_ids)
summaries = [
    OrderSummary(id=o.id, customer_name=customers_by_id[o.customer_id].name)
    for o in orders
]
```
