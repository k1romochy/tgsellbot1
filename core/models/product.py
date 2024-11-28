from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.order_product_association import OrderProductAssociation


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()

    orders: Mapped[list['Order']] = relationship(
        "Order",
        back_populates="products",
        secondary="order_product_association"
    )
    orders_details: Mapped[list['OrderProductAssociation']] = relationship(
        "OrderProductAssociation",
        back_populates="product"
    )
