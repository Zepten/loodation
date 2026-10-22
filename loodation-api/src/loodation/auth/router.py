from uuid import UUID

from fastapi import APIRouter, status

from loodation.auth.deps import UserPaginatorParamsDep, UserServiceDep
from loodation.auth.schemas import UserCreate, UserResponse, UserResponsePaginated

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: UUID, user_service: UserServiceDep) -> UserResponse:
    user = await user_service.get_user_by_id(user_id)
    return UserResponse.model_validate(user)


@router.get("/users", response_model=UserResponsePaginated)
async def get_users(
    user_service: UserServiceDep, paginator: UserPaginatorParamsDep, username: str | None = None
) -> UserResponsePaginated:
    if username and username.strip():
        result = await user_service.search_by_username(username, paginator)
    else:
        result = await user_service.get_users(paginator)
    return UserResponsePaginated(
        total_count=result.total_count,
        items=tuple(UserResponse.model_validate(user) for user in result.items),
    )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, user_service: UserServiceDep) -> UserResponse:
    user = await user_service.create_user(**user_create.model_dump())
    return UserResponse.model_validate(user)


@router.delete("/users", response_model=UserResponse)
async def delete_user(user_id: UUID, user_service: UserServiceDep) -> UserResponse:
    user = await user_service.set_active(user_id, False)
    return UserResponse.model_validate(user)


@router.patch("/users", response_model=UserResponse)
async def restore_user(user_id: UUID, user_service: UserServiceDep) -> UserResponse:
    user = await user_service.set_active(user_id, True)
    return UserResponse.model_validate(user)
