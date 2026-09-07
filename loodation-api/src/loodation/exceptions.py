from fastapi import status
from pydantic import BaseModel


class BusinessError(Exception):
    """
    Base exception for errors caused by business logic violations.

    Business logic errors are expected application errors that can be safely converted into an HTTP
    response with a corresponding status code and machine-readable error code.

    Attributes:
        name: Machine-readable code identifying the specific business error. Should be overridden.
        status_code: HTTP status code to return when handling the error. Should be overridden.
        message: Human-readable description of the business error.
    """

    message: str
    name: str = "business_error"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class BusinessErrorResponse(BaseModel):
    """API response schema for business logic errors."""

    name: str
    message: str
