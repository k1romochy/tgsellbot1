from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from core.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.product import Product
    from core.models.order_product_association import OrderProductAssociation


class Order(Base):
    __tablename__ = "order"

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )

    user_id: Mapped[int]

    products: Mapped[list['Product']] = relationship(
        "Product",
        back_populates="orders",
        secondary="order_product_association"
    )

    products_details: Mapped[list['OrderProductAssociation']] = relationship(
        "OrderProductAssociation",
        back_populates="order"
    )
