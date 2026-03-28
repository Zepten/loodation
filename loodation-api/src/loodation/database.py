from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from loodation.config import settings


def create_db_engine() -> AsyncEngine:
    return create_async_engine(
        url=str(settings.db.url),
        echo=settings.db.echo,
        # pool_size=settings.db.pool_size,
        # max_overflow=settings.db.max_overflow,
        # pool_pre_ping=settings.db.pool_pre_ping,
    )


def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db_session_factory = get_session_factory(create_db_engine())
