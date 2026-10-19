class AppError(Exception):
    status_code = 400
    detail = "Application error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = 404
    detail = "Not found"


class ForbiddenError(AppError):
    status_code = 403
    detail = "Forbidden"


class ConflictError(AppError):
    status_code = 409
    detail = "Conflict"


class InsufficientFundsError(AppError):
    status_code = 402
    detail = "Insufficient funds"


class InvalidStateError(AppError):
    status_code = 409
    detail = "Invalid state transition"
