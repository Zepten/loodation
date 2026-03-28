import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loodation.api import api_router
from loodation.config import settings
from loodation.rate_limiter import limiter

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    logger.info("Lifespan for FastAPI app is ended")
    # await db_helper.dispose() # TODO: lifespan for DB
    logger.info("Database engine disposed")


app = FastAPI(
    title="Loodation",
    description="Welcome to Loodation's API documentation! Here you will able to discover all of the ways you can interact with the Loodation API.",
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    root_path="/api/v1",
    redoc_url=None,
    lifespan=lifespan,
)
app.docs_url = "/docs" if settings.is_show_docs else None
app.openapi_url = "/openapi.json" if settings.is_show_docs else None
app.swagger_ui_oauth2_redirect_url = (
    "/docs/oauth2-redirect" if settings.is_show_docs else None
)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


def run() -> None:
    uvicorn.run(
        "loodation.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.is_auto_reload,
    )


if __name__ == "__main__":
    run()
