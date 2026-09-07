import logging
from enum import StrEnum
from functools import cached_property

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Environment(StrEnum):
    DEV = "dev"
    PROD = "prod"


class LoggingLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LoggingSettings(BaseModel):
    level: LoggingLevel = LoggingLevel.ERROR

    @computed_field
    @cached_property
    def format(self) -> str:
        match self.level:
            case LoggingLevel.DEBUG:
                return "%(asctime)s [%(levelname)s] %(message)s [%(name)s.%(funcName)s:%(lineno)d]"
            case _:  # TODO: make formats for other format levels
                return "%(asctime)s [%(levelname)s] %(message)s [%(name)s.%(funcName)s:%(lineno)d]"


class DbSettings(BaseModel):
    username: str = "db_username"
    password: SecretStr = SecretStr("db_password")
    host: str = "db_host"
    port: int = 5432
    name: str = "db_name"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field
    @cached_property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        )


class RedisSettings(BaseModel):
    host: str = "redis_host"
    port: int = Field(default=6380, ge=0, le=65535)
    username: str = "redis_user"
    password: SecretStr = SecretStr("redis_password")
    db: int = Field(default=0, ge=0, le=15)

    @computed_field
    @cached_property
    def url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=str(self.db),
        )


class PaginatorSettings(BaseModel):
    max_limit: int = Field(default=100, ge=1)
    default_limit: int = Field(default=20, ge=1)

    @model_validator(mode="after")
    def validate_limits(self) -> "PaginatorSettings":
        if self.default_limit > self.max_limit:
            raise ValueError("default_limit cannot be greater than max_limit")

        return self


class TelegramMiniappSettings(BaseModel):
    host: str = "miniapp"
    port: int = 8001


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    environment: Environment = Environment.DEV
    logging: LoggingSettings = LoggingSettings()
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()
    paginator: PaginatorSettings = PaginatorSettings()
    telegram_miniapp: TelegramMiniappSettings = TelegramMiniappSettings()

    @computed_field
    @cached_property
    def is_debug(self) -> bool:
        return self.environment is Environment.DEV

    @computed_field
    @cached_property
    def is_show_docs(self) -> bool:
        return self.environment is Environment.DEV

    @computed_field
    @cached_property
    def cors_origins(self) -> tuple[str, ...]:
        return tuple(
            str(HttpUrl(origin_url))
            for origin_url in {
                f"http://{self.telegram_miniapp.host}:{self.telegram_miniapp.port}",
                f"https://{self.telegram_miniapp.host}:{self.telegram_miniapp.port}",
            }
        )


def configure_logging() -> None:
    logging.basicConfig(
        level=settings.logging.level.upper(), format=settings.logging.format
    )


settings = Settings()
configure_logging()

if settings.environment is Environment.DEV:
    logger.info("Running in development environment")
    logger.debug(f"Application settings: {settings}")
