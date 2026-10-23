# Sources

External ideas adapted into this skill, rewritten in Coder Nexus vocabulary (SM1–SM13, `{{slot:clean-code}}` rules, P1/P2/P3, `D-NN`, READY_FOR_REVIEW). Nothing is copied. Stars as of 2026-10.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [addyosmani/agent-skills `skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md) | 109k | A refactor that leaves the reader holding the same number of concepts only relocated complexity | [SKILL](../SKILL.md) goal; [03](03-smell-catalog.md) "Reduce or relocate?" |
| same | 109k | Do not generalize until the third use case | SM11; [03](03-smell-catalog.md) premature extraction |
| same | 109k | Nested ternaries and "clever" tricks are readability defects | SM12; [03](03-smell-catalog.md) clever code |
| same | 109k | Separate refactoring from feature work | SM9; [01](01-when-and-scope.md) |
| [mattpocock/skills `skills/engineering/code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | Speculative Generality | SM10; [03](03-smell-catalog.md) speculative abstraction |
| same | 300k | Middle Man and Message Chains | [03](03-smell-catalog.md) needless indirection |
| same | 300k | Data Clumps | [03](03-smell-catalog.md) long parameter list |
| same | 300k | Duplicated Code | [03](03-smell-catalog.md) duplicated definitions (definitions only) |

Python conventions: [PEP 8](https://peps.python.org/pep-0008/), [ruff rules](https://docs.astral.sh/ruff/rules/) (`C901`, `PLR09xx`, `SIM`, `RET`, `F401`, `F841`, `ARG`, `ERA001`), [mypy](https://mypy.readthedocs.io/), [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [SQLAlchemy 2.0 ORM querying](https://docs.sqlalchemy.org/en/20/orm/queryguide/), [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/).

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "Could this be done in fewer lines?" as the target | addyosmani | Fewer lines often means clever code; net lines are reported, not targeted |
| Extract shared shape on the first duplication | mattpocock | Early extraction couples code that later diverges |
| Replace repeated switches with polymorphism | mattpocock | Adds class hierarchies in small tasks; a lookup dict or one `match` is simpler |
| Split a large file before adding to it | addyosmani | Placement is planned work (`{{slot:clean-architecture}}`) |
| Ask before deleting dead code | addyosmani | Dead code inside the diff is deleted (behavior identical); outside it is reported, not touched |
