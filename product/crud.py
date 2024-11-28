from core.models.product import Product
from core.models.cart import Cart
import core.models.db_helper as db
from sqlalchemy.engine import Result
from sqlalchemy import select


async def add_product(name: str, price: int, desc: str, category: str):
    async with db.async_session() as session:
        session.add(Product(name=name, price=price, description=desc, category=category))

        await session.commit()


async def get_product_id(name, category):
    async with db.async_session() as session:
        stmt = select(Product).where(Product.name == name, Product.category == category).order_by(Product.id)
        result: Result = await session.execute(stmt)
        product = session.scalar(result)


async def delete_product(product_id):
    async with db.async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == product_id))

        session.delete(product)
        await session.commit()


async def get_products_ids():
    async with db.async_session() as session:
        product = await session.scalars(select(Product.id).order_by(Product.id))

        return list(product)


async def get_products_ids_by_category(category: str):
    async with db.async_session() as session:
        product = await session.scalars(select(Product.id).where(Product.category == category).order_by(Product.id))

        return list(product)


async def get_name_product_by_id(id: int):
    async with db.async_session() as session:
        product_name = await session.scalar(select(Product.name).where(Product.id == id).order_by(Product.name))

        return product_name


async def get_product_categories():
    async with db.async_session() as session:
        categories = await session.scalars(select(Product.category).order_by(Product.category))

        return list(categories)


async def get_price_by_id(id: int):
    async with db.async_session() as session:
        product_price = await session.scalar(select(Product.price).where(Product.id == id).order_by(Product.price))

        return product_price


async def get_description_by_id(id: int):
    async with db.async_session() as session:
        product_description = await session.scalar(select(Product.description).where(Product.id == id).order_by(Product.description))

        return product_description


async def add_product_to_cart(product_id: int, user_id: int):
    async with db.async_session() as session:
        session.add(Cart(user_id=user_id, product_id=product_id))

        await session.commit()


async def get_product_ids_cart(user_id):
    async with db.async_session() as session:
        products_ids = await session.scalars(select(Cart.product_id).where(Cart.user_id == user_id).order_by(Cart.product_id))

        return list(products_ids)
