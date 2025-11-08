from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import BaseAPIException


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(
        request: Request, exc: BaseAPIException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.detail}
        )
