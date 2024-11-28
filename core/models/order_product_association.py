from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.order import Order
    from core.models.product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='index_unique_order_product'),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), primary_key=True)
    count: Mapped[int] = mapped_column(default=1)

    order: Mapped['Order'] = relationship(
        "Order",
        back_populates="products_details"
    )
    product: Mapped['Product'] = relationship(
        "Product",
        back_populates="orders_details"
    )
