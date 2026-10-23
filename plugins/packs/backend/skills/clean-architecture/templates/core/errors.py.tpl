# app/core/errors.py - framework-free errors raised by services and repositories.
#
# Rules:
# - No FastAPI import: app/api/error_handlers.py maps each class to its status code
#   and to the error body agreed in the API contract (api-contract-design).
# - `code` is a stable, machine-readable string the frontend client may branch on;
#   it never contains user data, ids of other tenants or secrets.
# - Add a class only when a new status code or handling is needed; otherwise reuse one.


class AppError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class PermissionDeniedError(AppError):
    pass
