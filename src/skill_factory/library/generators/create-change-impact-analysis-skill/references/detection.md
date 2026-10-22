# Where dependencies, consumers and tests are found

Read-only. Skip what the workspace does not have.

| Category | Typical places | Tools |
|---|---|---|
| Module structure | Package/folder layout, `import`/`require` graph, `.agents/stack.json` | `rg -n "from <module>|import .*<symbol>"`, language tools (`go list -deps`, `pydeps`, `madge`, `dart pub deps`) |
| UI | Route tables, navigation configs, shared component folders | `rg -n "<ComponentName>"`, route files |
| API consumers | API client code in front ends and mobile apps, other services in the repo, documented partners, API gateway configs | `rg -n "/<path>"` across all apps; ask about consumers outside the repo |
| Data | ORM models and repositories, raw SQL, migrations, report/export queries, views | `rg -n "<table>|<Model>"` in BE and SQL files |
| Jobs and events | Schedulers, workers, queue consumers, webhooks, event names | `rg -n "<event>|@scheduled|cron|consumer"` |
| Permissions | Guards, decorators, policies, query scope filters | `rg -n "<permission>|<role>"` |
| Tests | Test folders per module, test tags/markers, CI jobs per suite, `.feature` files | Test runner's filters (`pytest -k`, `--grep`, `flutter test <path>`) |
| Past analyses | `change-impact.md` in earlier work items | Compare with their diffs |
