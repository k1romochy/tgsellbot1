from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class User(Base):
    tg_id: Mapped[int]
    balance: Mapped[int | None] = mapped_column(server_default=None)
