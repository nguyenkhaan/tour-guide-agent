from typing import Any
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Mã lỗi ứng dụng")
    message: str = Field(..., description="Mô tả lỗi dễ hiểu cho người dùng")
    details: Any | None = Field(default=None, description="Chi tiết lỗi hoặc validation context")
    request_id: str = Field(..., description="Mã định danh duy nhất theo dõi request")


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
        message: str = "Xác thực không thành công",
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
        message: str = "Bạn không có quyền thực hiện thao tác này",
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
        message: str = "Không tìm thấy tài nguyên yêu cầu",
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
        message: str = "Yêu cầu không hợp lệ",
        details: Any | None = None,
    ):
        super().__init__(
            status_code=400,
            code="BAD_REQUEST",
            message=message,
            details=details,
        )