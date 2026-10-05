from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.exceptions.error import AppException, ErrorResponse


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        req_id = get_request_id(request)
        error_resp = ErrorResponse(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            request_id=req_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_resp.model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        req_id = get_request_id(request)
        code_map = {
            401: "UNAUTHENTICATED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            400: "BAD_REQUEST",
        }
        code = code_map.get(exc.status_code, "HTTP_ERROR")
        error_resp = ErrorResponse(
            code=code,
            message=str(exc.detail) if exc.detail else "HTTP Exception",
            details=None,
            request_id=req_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_resp.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        req_id = get_request_id(request)
        error_resp = ErrorResponse(
            code="VALIDATION_ERROR",
            message="Dữ liệu yêu cầu không hợp lệ",
            details=exc.errors(),
            request_id=req_id,
        )
        return JSONResponse(
            status_code=422,
            content=error_resp.model_dump(),
        )
