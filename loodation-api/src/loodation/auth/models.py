from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loodation.core.database import Base
from loodation.core.models import ActiveMixin, TimestampMixin, UuidPk

if TYPE_CHECKING:
    from loodation.ledger.models import Transaction


class User(Base, TimestampMixin, ActiveMixin):
    id: Mapped[UuidPk]
    username: Mapped[str] = mapped_column(Text, index=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id='{self.id!s}', username='{self.username!s}', active={self.active!s})>"
