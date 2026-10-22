from enum import StrEnum
from typing import Annotated, Callable, TypeAlias, TypeVar, cast

from fastapi import Depends, Query

from loodation.core.config import settings
from loodation.core.database import DbSessionDep
from loodation.core.paginator.schemas import PaginatorParams, SortOrder
from loodation.core.paginator.service import PaginatorService

T = TypeVar("T")
SortFieldsT = TypeVar("SortFieldsT", bound=StrEnum)

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
        sort_by: Annotated[sorting_field, Query()] = default_sorting_field,  # type: ignore
        sort_order: Annotated[SortOrder, Query()] = SortOrder.DESC,
    ) -> PaginatorParams[SortFieldsT]:
        return PaginatorParams(limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)

    return get_paginator_params


def get_paginator_service(session: DbSessionDep) -> PaginatorService:
    return PaginatorService(session)


PaginatorServiceDep = Annotated[PaginatorService, Depends(get_paginator_service)]
