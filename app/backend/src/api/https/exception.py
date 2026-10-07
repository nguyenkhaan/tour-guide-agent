from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.exceptions.error import ErrorResponse


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def app_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        req_id = get_request_id(request)

        try: 
            default_code = HTTPStatus(exc.status_code).name
        except ValueError: 
            default_code = "HTTP_ERROR"
        
        if isinstance(exc.detail, dict):
            code = exc.detail.get("code", default_code)
            message = exc.detail.get("message", "HTTP Exception")
            details = exc.detail.get("details", None)
        else:
            code = default_code
            message = exc.detail if exc.detail else "HTTP Exception"
            details = None
        error_resp = ErrorResponse(
            code=code,
            message=message,
            details=details,
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
            message="Invalid request data",
            details=exc.errors(),
            request_id=req_id,
        )
        return JSONResponse(
            status_code=422,
            content=error_resp.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        req_id = get_request_id(request)
        error_resp = ErrorResponse(
            code="INTERNAL_SERVER_ERROR",
            message= "Internal Server Error",
            details=None,
            request_id=req_id,
        )
        return JSONResponse(
            status_code=500,
            content=error_resp.model_dump(),
        )
