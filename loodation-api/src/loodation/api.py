from fastapi import APIRouter
from sqlalchemy import select, text

from loodation.auth.models import User
from loodation.auth.router import router as auth_router
from loodation.config import settings
from loodation.database import db_session_factory
from loodation.ledger.router import router as ledger_router

api_router = APIRouter()


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    """Basic healthcheck"""
    return {"status": "ok"}


# TODO FIXME remove this ASAP (for testing purposes)
@api_router.get("/config")
def get_config():
    return settings


# TODO FIXME remove this ASAP (for testing purposes)
@api_router.get("/db")
async def get_db_version():
    async with db_session_factory() as session:
        result = await session.execute(text("SELECT VERSION()"))
        await session.commit()
    return str(result.first())


# TODO FIXME remove this ASAP (for testing purposes)
@api_router.post("/users")
async def create_user(username: str):
    async with db_session_factory() as session:
        user = User(username=username)
        session.add(user)
        await session.commit()
    return f"User {user} created"


# TODO FIXME remove this ASAP (for testing purposes)
@api_router.get("/users")
async def get_users():
    async with db_session_factory() as session:
        result = await session.scalars(select(User))
        await session.commit()
    return str(result.all())


# TODO FIXME remove this ASAP (for testing purposes)
@api_router.get("/users/search/{query}")
async def find_user_by_username(query: str):
    async with db_session_factory() as session:
        result = await session.scalars(select(User).where(User.username.ilike(query)))
        await session.commit()
    return str(result.all())


api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(ledger_router, prefix="/ledger")
