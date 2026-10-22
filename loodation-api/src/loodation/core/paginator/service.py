from enum import StrEnum
from typing import TypeVar

from sqlalchemy import Select, asc, desc, func, select

from loodation.core.database import DbSessionDep
from loodation.core.paginator.schemas import PaginatedResult, PaginatorParams, SortOrder

T = TypeVar("T")
SortFieldsT = TypeVar("SortFieldsT", bound=StrEnum)


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
        order_by_stmt = desc(column) if params.sort_order is SortOrder.DESC else asc(column)
        result = await self.session.scalars(
            stmt.order_by(order_by_stmt).offset(params.offset).limit(params.limit)
        )
        total_count = (
            await self.session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        )
        return PaginatedResult[T](total_count=total_count, items=result.all())
