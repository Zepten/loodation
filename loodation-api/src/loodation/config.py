import logging
from enum import StrEnum
from functools import cached_property

from pydantic import (
    BaseModel,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    SecretStr,
    computed_field,
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
        if self.level is LoggingLevel.DEBUG:
            return "%(asctime)s [%(levelname)s] %(message)s [%(name)s.%(funcName)s:%(lineno)d]"
        else:
            return "%(asctime)s [%(levelname)s] %(message)s [%(name)s.%(funcName)s:%(lineno)d]"  # TODO


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
    port: int = 6380
    username: str = "redis_user"
    password: SecretStr = SecretStr("redis_password")
    db: int = 0

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


class ApiSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


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
    api: ApiSettings = ApiSettings()
    telegram_miniapp: TelegramMiniappSettings = TelegramMiniappSettings()

    @computed_field
    @cached_property
    def is_auto_reload(self) -> bool:
        return settings.environment is Environment.DEV

    @computed_field
    @cached_property
    def is_show_docs(self) -> bool:
        return settings.environment is Environment.DEV

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
logger.debug(f"Application settings: {settings}")
