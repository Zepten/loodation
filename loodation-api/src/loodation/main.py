from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from loodation.api import api_router
from loodation.core.config import settings
from loodation.core.exceptions import BusinessError, BusinessErrorResponse
from loodation.core.rate_limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    logger.debug("Lifespan for FastAPI app is ended.")
    # await db_helper.dispose() # TODO: lifespan for DB
    logger.debug("Database engine disposed.")


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
app.swagger_ui_oauth2_redirect_url = "/docs/oauth2-redirect" if settings.is_show_docs else None
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.exception_handler(BusinessError)
async def business_logic_error_handler(
    _: Request,
    exc: BusinessError,
) -> JSONResponse:
    response = BusinessErrorResponse(name=exc.code, message=exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
    )
