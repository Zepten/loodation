from typing import Annotated

from fastapi import Depends

from loodation.auth.enums import UserSortFields
from loodation.auth.service import UserService
from loodation.core.database import DbSessionDep
from loodation.core.paginator.deps import PaginatorServiceDep, create_paginator_dependency
from loodation.core.paginator.schemas import PaginatorParams


def get_user_service(session: DbSessionDep, paginator: PaginatorServiceDep) -> UserService:
    return UserService(session, paginator)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

UserPaginatorParamsDep = Annotated[
    PaginatorParams[UserSortFields],
    Depends(create_paginator_dependency(UserSortFields, default_sorting_field=UserSortFields.ID)),
]
