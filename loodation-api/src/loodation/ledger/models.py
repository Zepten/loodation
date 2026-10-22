from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loodation.core.database import Base
from loodation.core.models import StrPk, TimestampMixin, UuidPk

if TYPE_CHECKING:
    from loodation.auth.models import User


class TransactionStatus(Base):
    __tablename__ = "transaction_statuses"

    code: Mapped[StrPk]
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="status")

    def __repr__(self) -> str:
        return f"<TransactionStatus(code='{self.code!s}'')>"


class TransactionType(Base):
    __tablename__ = "transaction_types"

    code: Mapped[StrPk]
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="type")

    def __repr__(self) -> str:
        return f"<TransactionType(code='{self.code!s}'')>"


class Transaction(Base, TimestampMixin):
    __table_args__ = (CheckConstraint("amount_cents != 0", name="amount_cents_not_zero"),)

    id: Mapped[UuidPk]
    reference_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        index=True,
        nullable=True,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(back_populates="transactions")
    amount_cents: Mapped[int] = mapped_column(BigInteger)
    idempotency_key: Mapped[UUID] = mapped_column(
        PostgresUUID,
        unique=True,
        nullable=False,
    )

    type_code: Mapped[str] = mapped_column(
        ForeignKey("transaction_types.code"),
        server_default="pending",
        index=True,
    )
    type: Mapped[TransactionType] = relationship(TransactionType, back_populates="transactions")

    status_code: Mapped[str] = mapped_column(ForeignKey("transaction_statuses.code"), index=True)
    status: Mapped[TransactionStatus] = relationship(
        TransactionStatus, back_populates="transactions"
    )

    def __repr__(self) -> str:
        return f"<Transaction(id='{self.id!s}', amount='{self.amount_cents!s}, type='{self.type_code!s}')>"
