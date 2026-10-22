from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")
SortFieldsT = TypeVar("SortFieldsT", bound=StrEnum)


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class PaginatorParams(BaseModel, Generic[SortFieldsT]):
    limit: int = Field(ge=1)
    offset: int = Field(0, ge=0)
    sort_by: SortFieldsT
    sort_order: SortOrder = Field(SortOrder.DESC)


class PaginatedResponse(BaseModel, Generic[T]):
    total_count: int
    items: Sequence[T]


@dataclass
class PaginatedResult(Generic[T]):
    total_count: int
    items: Sequence[T]
