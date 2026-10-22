from uuid import UUID

from fastapi import status

from loodation.core.exceptions import BusinessError


class UserNotFoundError(BusinessError):
    name = "user_not_found"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, user_id: UUID) -> None:
        super().__init__(message="User not found.", extra={"user_id": user_id})
