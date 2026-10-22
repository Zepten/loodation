from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from loodation.core.paginator.schemas import PaginatedResponse


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=120, description="Username")


class UserResponse(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    active: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None


UserResponsePaginated: TypeAlias = PaginatedResponse[UserResponse]
