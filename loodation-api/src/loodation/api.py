from fastapi import APIRouter

from loodation.auth.router import router as auth_router
from loodation.ledger.router import router as ledger_router

api_router = APIRouter()


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    """Basic healthcheck"""
    return {"status": "ok"}


api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(ledger_router, prefix="/ledger")
