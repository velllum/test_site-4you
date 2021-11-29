from typing import Optional, List

from pydantic import BaseModel


class ValidationError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: Optional[str]
    validation_error: Optional[List[ValidationError]]
    debug: Optional[str]
