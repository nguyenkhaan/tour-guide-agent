from typing import Any
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Application error code")
    message: str = Field(..., description="Human-readable error message")
    details: Any | None = Field(default=None, description="Error details or validation context")
    request_id: str = Field(..., description="Unique request identifier")