from sqlalchemy.orm import Mapped

from core.models.base import Base


class User(Base):
    tg_id: Mapped[int]
