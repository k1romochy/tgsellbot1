from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from core.models.order import Order
from core.models.product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='index_unique_order_product'),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    count: Mapped[int] = mapped_column(default=1)
    # unit_price: Mapped[int] = mapped_column(default=1)

    order: Mapped['Order'] = relationship(back_populates='products_details')
    product: Mapped['Product'] = relationship(back_populates='user_details')
