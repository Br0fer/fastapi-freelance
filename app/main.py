from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import app.core.models_registry

from app.core.config import settings
from app.core.exceptions import AppError
from app.modules.auth.router import router as auth_router

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(auth_router)

@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
