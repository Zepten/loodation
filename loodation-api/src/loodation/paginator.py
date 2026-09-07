import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Callable, Generic, Sequence, TypeAlias, TypeVar, cast

from fastapi import Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import Select, asc, desc, func, select

from loodation.config import settings
from loodation.database import DbSessionDep

logger = logging.getLogger(__name__)

T = TypeVar("T")
SortFieldsT = TypeVar("SortFieldsT", bound=StrEnum)


# ==================================================================================================
# SCHEMAS
# ==================================================================================================


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


# ==================================================================================================
# SERVICE
# ==================================================================================================


class PaginatorService:
    def __init__(self, session: DbSessionDep) -> None:
        self.session = session

    async def paginate(
        self,
        model: type[T],
        stmt: Select[tuple[T]],
        params: PaginatorParams[SortFieldsT],
    ) -> PaginatedResult[T]:
        try:
            column = getattr(model, params.sort_by.value)
        except AttributeError as exc:
            raise RuntimeError(
                f'Invalid sort field "{params.sort_by.value}" for ORM model "{model.__name__}".'
            ) from exc
        order_by_stmt = (
            desc(column) if params.sort_order is SortOrder.DESC else asc(column)
        )
        result = await self.session.scalars(
            stmt.order_by(order_by_stmt).offset(params.offset).limit(params.limit)
        )
        total_count = (
            await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
            or 0
        )
        return PaginatedResult[T](total_count=total_count, items=result.all())


# ==================================================================================================
# DEPENDENCIES
# ==================================================================================================


SortFieldType: TypeAlias = type[SortFieldsT]


def create_paginator_dependency(
    sorting_field: SortFieldType, default_sorting_field: SortFieldsT | None = None
) -> Callable[..., PaginatorParams[SortFieldsT]]:
    if default_sorting_field is None:
        default_sorting_field = next(iter(cast(type[SortFieldsT], sorting_field)))

    def get_paginator_params(
        limit: Annotated[
            int, Query(ge=1, le=settings.paginator.max_limit)
        ] = settings.paginator.default_limit,
        offset: Annotated[int, Query(ge=0)] = 0,
        sort_by: Annotated[sorting_field, Query()] = default_sorting_field,
        sort_order: Annotated[SortOrder, Query()] = SortOrder.DESC,
    ) -> PaginatorParams[SortFieldsT]:
        return PaginatorParams(
            limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order
        )

    return get_paginator_params


def get_paginator_service(session: DbSessionDep) -> PaginatorService:
    return PaginatorService(session)


PaginatorServiceDep = Annotated[PaginatorService, Depends(get_paginator_service)]
