from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from .base import Base

from .product import Product
from .order_product_association import OrderProductAssociation


class Order(Base):
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now
    )
    products: Mapped[list[Product]] = relationship(back_populates='orders',
                                                   secondary='order_product_association',)
    products_details: Mapped[list['OrderProductAssociation']] = relationship(
        back_populates='order'
    )

