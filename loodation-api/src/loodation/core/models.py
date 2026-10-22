from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from loguru import logger
from sqlalchemy import UUID as SqlaUUID
from sqlalchemy import DateTime, TextClause, event, inspect, text
from sqlalchemy.orm import Mapped, Session, mapped_column


def get_uuid_sql() -> TextClause:
    return text("gen_random_uuid()")


def get_utc_now_sql() -> TextClause:
    return text("TIMEZONE('utc', now())")


IntPk = Annotated[
    int,
    mapped_column(primary_key=True),
]
"""Integer primary key."""

UuidPk = Annotated[
    UUID,
    mapped_column(
        SqlaUUID(as_uuid=True),
        primary_key=True,
        server_default=get_uuid_sql(),
    ),
]
"""UUID primary key."""

StrPk = Annotated[
    str,
    mapped_column(primary_key=True),
]
"""String primary key."""

Active = Annotated[bool, mapped_column()]


class CreatedAtMixin:
    """
    Mixin for logging datetime for create with timezone.

    Attributes:
        created_at: Date and time of creation
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=get_utc_now_sql(),
        nullable=False,
    )


class UpdatedAtMixin:
    """
    Mixin for logging datetime for update with timezone.

    Attributes:
        updated_at: Date and time of update
    """

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=get_utc_now_sql(),
        server_onupdate=get_utc_now_sql(),
        # onupdate=func.now(),  # TODO: use trigger instead of onupdate
    )


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    """
    Mixin for datetime logging with timezone.

    Attributes:
        created_at: Date and time of creation
        updated_at: Date and time of update
    """


class ActiveMixin:
    active: Mapped[bool] = mapped_column(default=True, server_default="true")
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


@event.listens_for(Session, "before_flush")
def active_mixin_before_flush(session: Session, flush_context, instances) -> None:
    now = datetime.now(tz=UTC)

    for instance in session.dirty:
        if not isinstance(instance, ActiveMixin):
            continue

        history = inspect(instance).attrs.active.history  # TODO: FIXME

        if not history.has_changes():
            continue

        if instance.active:
            instance.deleted_at = None
            logger.info(f"Restored (reactivated) user {instance}.")
        else:
            instance.deleted_at = now
            logger.info(f"Deleted (deactivated) user {instance}.")
