from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.requests import Request


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(_: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": {"code": "validation_error", "message": str(exc)}},
        )

