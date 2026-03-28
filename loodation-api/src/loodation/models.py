from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column


class UuidPkMixin:
    """
    Mixin for identifier
        Fields:
            - `id`: `Mapped[UUID]`
    """

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )


class TimestampMixin:
    """
    Mixin for datetime logging with timezone
        Fields:
            - `created_at`: `Mapped[datetime]`
            - `updated_at`: `Mapped[datetime]`
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=func.now(),  # TODO: use trigger instead of onupdate
        nullable=False,
    )
