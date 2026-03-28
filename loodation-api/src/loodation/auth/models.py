from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from loodation.database import Base
from loodation.models import TimestampMixin, UuidPkMixin


class User(Base, UuidPkMixin, TimestampMixin):
    username: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!s}), username={self.username!r}>"
