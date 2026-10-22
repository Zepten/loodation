from typing import Annotated

from fastapi import Depends

from loodation.core.database import DbSessionDep
from loodation.core.paginator.deps import PaginatorServiceDep, create_paginator_dependency
from loodation.core.paginator.schemas import PaginatorParams
from loodation.ledger.enums import TransactionSortFields
from loodation.ledger.service import LedgerService


def get_ledger_service(session: DbSessionDep, paginator: PaginatorServiceDep) -> LedgerService:
    return LedgerService(session, paginator)


LedgerServiceDep = Annotated[LedgerService, Depends(get_ledger_service)]

TransactionPaginatorParamsDep = Annotated[
    PaginatorParams[TransactionSortFields],
    Depends(
        create_paginator_dependency(
            TransactionSortFields, default_sorting_field=TransactionSortFields.ID
        )
    ),
]
