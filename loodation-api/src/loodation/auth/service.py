from uuid import UUID

from loguru import logger
from sqlalchemy import select

from loodation.auth.enums import UserSortFields
from loodation.auth.exceptions import UserNotFoundError
from loodation.auth.models import User
from loodation.core.paginator.schemas import PaginatedResult, PaginatorParams
from loodation.core.service import BaseService


class UserService(BaseService):
    async def get_user_by_id(self, user_id: UUID) -> User:
        if user := await self.session.get(User, user_id):
            return user
        raise UserNotFoundError(user_id)

    async def is_user_active(self, user_id: UUID) -> bool:
        if user := await self.session.get(User, user_id):
            return bool(user.active)
        raise UserNotFoundError(user_id)

    async def ensure_user_exists(self, user_id: UUID) -> None:
        if not await self.session.get(User, user_id):
            raise UserNotFoundError(user_id)

    async def get_users(self, paginator: PaginatorParams[UserSortFields]) -> PaginatedResult[User]:
        stmt = select(User)
        return await self.paginator.paginate(User, stmt, paginator)

    async def search_by_username(
        self, username: str, paginator: PaginatorParams[UserSortFields]
    ) -> PaginatedResult[User]:
        stmt = select(User).where(User.username.ilike(f"%{username}%"))
        return await self.paginator.paginate(User, stmt, paginator)

    async def create_user(self, username: str) -> User:
        user = User(username=username)

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        logger.info(f"Created user {user}.")
        return user

    async def set_active(self, user_id: UUID, active: bool) -> User:
        user = await self.get_user_by_id(user_id)
        user.active = active

        await self.session.flush()
        await self.session.refresh(user)

        return user
