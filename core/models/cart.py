from sqlalchemy.orm import Mapped

from core.models.base import Base


class Cart(Base):
    product_id: Mapped[int]
    user_id: Mapped[int]

    product_quantity: Mapped[int]