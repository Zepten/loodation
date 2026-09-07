from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from loodation.config import settings
from loodation.utils import camel_to_snake

db_engine = create_async_engine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    # pool_size=settings.db.pool_size,
    # max_overflow=settings.db.max_overflow,
    # pool_pre_ping=settings.db.pool_pre_ping,
)


db_session_factory = async_sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with db_session_factory() as session:
        async with session.begin():
            yield session


DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_to_snake(cls.__name__)}s"

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
