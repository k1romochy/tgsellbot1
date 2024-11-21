from core.models.product import Product
import core.models.db_helper as db
from sqlalchemy.engine import Result
from sqlalchemy import select


async def add_product(name: str, price: int, desc: str, model: str):
    async with db.async_session() as session:
        session.add(Product(name=name, price=price, description=desc, model=model))

        await session.commit()


async def get_product_id(name, model):
    async with db.async_session() as session:
        stmt = select(Product).where(Product.name == name, Product.model == model).order_by(Product.id)
        result: Result = await session.execute(stmt)
        product = session.scalar(result)


async def delete_product(product_id):
    async with db.async_session() as session:
        stmt = select(Product).where(Product.id == product_id)
        result: Result = await session.execute(stmt)
        product = session.scalar(result)

        session.delete(product)
        await session.commit()