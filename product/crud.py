from core.models import Order
from core.models.product import Product
from core.models.cart import Cart
from core.models.order_product_association import OrderProductAssociation
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
        product = await session.scalars(select(Product).order_by(Product.id))

        return list(product)


async def get_products_ids_by_category(category: str):
    async with db.async_session() as session:
        product = await session.scalars(select(Product).where(Product.category == category).order_by(Product.id))

        return list(product)


async def get_name_product_by_id(product_id: int):
    async with db.async_session() as session:
        product_name = await session.scalar(select(Product).where(Product.id == product_id).order_by(Product.name))

        return product_name


async def get_product_categories():
    async with db.async_session() as session:
        categories = await session.scalars(select(Product).order_by(Product.category))

        return list(categories)


async def get_price_by_id(product_id: int):
    async with db.async_session() as session:
        product_price = await session.scalar(select(Product).where(Product.id == product_id).order_by(Product.price))

        return product_price


async def get_description_by_id(product_id: int):
    async with db.async_session() as session:
        product_description = await session.scalar(select(Product).where(Product.id == product_id).order_by(Product.description))

        return product_description


async def get_product_quantity_by_id(product_id: int):
    async with db.async_session() as session:
        product_quantity = await session.scalar(select(Product).where(Product.id == product_id).order_by(Product.quantity))


async def add_product_to_cart(product_id: int, user_id: int, product_quantity: int):
    async with db.async_session() as session:
        session.add(Cart(user_id=user_id, product_id=product_id, product_quantity=product_quantity))

        await session.commit()


async def delete_product_from_cart(product_id: int):
    async with db.async_session() as session:
        product = await session.scalar(select(Cart).where(Cart.product_id == product_id))
        session.delete(product)

        await session.commit()


async def get_product_ids_cart(user_id):
    async with db.async_session() as session:
        products_ids = await session.scalars(select(Cart).where(Cart.user_id == user_id).order_by(Cart.product_id))

        return list(products_ids)


async def get_products_id_and_quantity_from_cart(user_id):
    async with db.async_session() as session:
        product_ids = await session.scalars(select(Cart).where(Cart.user_id == user_id).order_by(Cart.product_id))
        products_q = await session.scalars(select(Cart).where(Cart.user_id == user_id).order_by(Cart.product_quantity))

        list_return = []
        count = 0
        for _ in product_ids:
            list_return.append([product_ids[count], products_q[count]])
            count += 1

        return list_return


async def create_order_with_products(user_id: int, products: list[tuple[int, int]]):
    async with db.async_session() as session:
        order = Order(user_id=user_id)
        session.add(order)
        await session.flush()

        for product_id, product_quantity in products:
            order_product_assoc = OrderProductAssociation(
                order_id=order.id,
                product_id=product_id,
                count=product_quantity
            )
            session.add(order_product_assoc)

        await session.commit()
