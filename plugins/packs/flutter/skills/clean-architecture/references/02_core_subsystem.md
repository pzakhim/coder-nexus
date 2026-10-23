# 02 — Core Subsystems, Network and Data Contracts

Apply the approved profile through [core-package-usage](../../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

> **Sources:** Clean Architecture and Data Layer guidelines.
> **Scope:** Verified Client core infrastructure and contracts.

## Network stack

The architecture uses an `ApiClient` / `ApiService` over the configured HTTP client (Dio or HttpClient), with authentication and performance instrumentation in core. Read the actual Client stack before naming constructor parameters or changing transport. Do not add a second HTTP stack without an approved design.

## DataSource and endpoints

API-backed module DataSources extend the Client's base data source and receive API services through DI. Use verified endpoint constants from the Client's configuration or route tables; do not hardcode endpoint strings. Missing API contracts remain `BLOCKED`.

## DataState and errors

Repository contracts use the Client's `Future<DataState<T>>` where applicable. Apply `tryCatch` for synchronous mapping and `tryCatchAsync` when the callback awaits another operation. Preserve actual `ErrorEntity` information and report missing required fields explicitly. Never replace a failure with fabricated empty data, an invented response or a success fallback.
