from typing import Any
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Application error code")
    message: str = Field(..., description="Human-readable error message")
    details: Any | None = Field(default=None, description="Error details or validation context")
    request_id: str = Field(..., description="Unique request identifier")


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class UnauthenticatedException(AppException):
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Any | None = None,
    ):
        super().__init__(
            status_code=401,
            code="UNAUTHENTICATED",
            message=message,
            details=details,
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
        details: Any | None = None,
    ):
        super().__init__(
            status_code=403,
            code="FORBIDDEN",
            message=message,
            details=details,
        )


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "The requested resource was not found",
        details: Any | None = None,
    ):
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=message,
            details=details,
        )


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Invalid request",
        details: Any | None = None,
    ):
        super().__init__(
            status_code=400,
            code="BAD_REQUEST",
            message=message,
            details=details,
        )
