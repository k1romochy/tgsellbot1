from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

import product.crud as product

router = Router()


@router.message(Command('create_product'))
async def create_product(message: Message):
    if message.from_user.id == 5470849504:
        secondary_message = str(message).split()
        start_index = next((i for i, item in enumerate(secondary_message) if item.startswith("text='/create_product")),
                           None)

        result = []
        if start_index is not None:
            for item in secondary_message[start_index + 1:]:
                if "=" in item:
                    break
                result.append(item)

        await product.add_product(category=str(result[0]), name=str(result[1]), price=int(result[2]),
                                  desc=str(result[3]), quantity=int(result[4][:-1]))
        await message.answer('Вы успешно добавили товар!')
    else:
        await message.answer('Вы не обладаете правами для использования этой команды')


@router.message(F.data.startswith('delete_'))
async def delete_product(callback: CallbackQuery):
    result = str(callback).split('delete_')
    result.pop(0)
    await product.delete_product(int(result[0]))


@router.message(F.text == 'Товары')
async def show_categories(message: Message):
    product_categories = await product.get_product_categories()

    builder = InlineKeyboardBuilder()
    for category in product_categories:
        builder.button(text=f"{category}", callback_data=f"category_{category}")

    builder.adjust(3)
    keyboard = builder.as_markup()

    await message.answer("Выберите категорию:", reply_markup=keyboard)


@router.callback_query(F.data.startswith('category_'))
async def show_products(callback: CallbackQuery):
    category = callback.data.split("category_")[1]

    product_ids = await product.get_products_ids_by_category(category)

    count = 1
    builder = InlineKeyboardBuilder()
    for product_id in product_ids:
        builder.button(text=f"Продукт {count}", callback_data=f"product_{product_id}")
        count += 1

    builder.adjust(3)
    keyboard = builder.as_markup()

    await callback.message.answer(f"Товары в категории {category}:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith('product_'))
async def show_product(callback: CallbackQuery):
    product_id = callback.data.split('product_')[1]

    product_name = await product.get_name_product_by_id(int(product_id))
    product_price = await product.get_price_by_id(int(product_id))
    product_description = await product.get_description_by_id(int(product_id))
    product_quantity = await product.get_product_quantity_by_id(int(product_id))

    builder = InlineKeyboardBuilder()
    builder.button(text='В корзину', callback_data=f'addcart_{product_id}')
    if callback.from_user.id == 5470849504:
        builder.button(text='Удалить', callback_data=f'delete_{product_id}')

    keyboard = builder.as_markup()

    await callback.message.answer(f'{product_name} Цена: {product_price} \n{product_description} \n Осталось: {product_quantity}',
                                  reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith('addcart_'))
async def get_quantity_to_cart(callback: CallbackQuery):
    product_id = callback.data.split('addcart_')[1]
    max_product_quantity = await product.get_product_quantity_by_id(int(product_id))

    builder = InlineKeyboardBuilder()
    for quan in range(max_product_quantity):
        while quan < 11:
            builder.button(text=f'{quan}', callback_data=f'addcartq_{product_id}_{quan}')

    builder.adjust(5)
    keyboard = builder.as_markup()

    await callback.message.answer('Какое колличество товара вы хотите добавить в корзину?', keyboard=keyboard)

    await callback.answer()


@router.callback_query(F.data.startswith('addcartq_'))
async def add_to_cart(callback: CallbackQuery):
    product_id = callback.data.split('addcart_')[1]
    user_id = callback.from_user.id
    product_quantity = callback.data.split('_')[2]

    await product.add_product_to_cart(product_id=int(product_id), user_id=user_id, product_quantity=int(product_quantity))

    await callback.message.answer('Вы успешно добавили товар в корзину')

    await callback.answer()


@router.callback_query(F.text('Корзина'))
async def show_cart(message: Message):
    user_id = message.from_user.id
    product_ids = await product.get_product_ids_cart(user_id=user_id)

    builder = InlineKeyboardBuilder()
    for product_id in product_ids:
        product_name = await product.get_name_product_by_id(product_id)
        builder.button(text=product_name, callback_data=f'cart_{product_id}')
    builder.button(text='Купить продукты', callback_data=f'buyproduct{product_ids}')
    builder.adjust(2)
    keyboard = builder.as_markup()

    await message.answer('Выберите продукт', reply_markup=keyboard)


@router.callback_query(F.data.startswith('cart_'))
async def show_product(callback: CallbackQuery):
    product_id = callback.data.split('product_')[1]

    product_name = await product.get_name_product_by_id(int(product_id))
    product_price = await product.get_price_by_id(int(product_id))
    product_description = await product.get_description_by_id(int(product_id))
    product_quantity = await product.get_product_quantity_by_id(int(product_id))

    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data=f'back_to_cart')
    if callback.from_user.id == 5470849504:
        builder.button(text='Удалить', callback_data=f'deletefromcart_{product_id}')

    keyboard = builder.as_markup()

    await callback.message.answer(f'{product_name} Цена: {product_price} \n{product_description} \n Осталось: {product_quantity}',
                                  reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith('deletefromcart_'))
async def delete_product_from_cart(callback: CallbackQuery):
    product_id = callback.data.split('product_')[1]

    await product.delete_product_from_cart(product_id=int(product_id))

    await callback.message.answer('Вы успешно удалили товар с корзины')
    await callback.answer()


@router.callback_query(F.data('back_to_cart'))
async def back_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    product_ids = await product.get_product_ids_cart(user_id=user_id)

    builder = InlineKeyboardBuilder()
    for product_id in product_ids:
        product_name = await product.get_name_product_by_id(product_id)
        builder.button(text=product_name, callback_data=f'cart_{product_id}')
    builder.button(text='Купить продукты', callback_data=f'buyproducts_{product_ids}') # тут надо pay юзнуть

    builder.adjust(2)
    keyboard = builder.as_markup()

    await callback.message.answer('Выберите продукт', reply_markup=keyboard)
    await callback.answer()


# @router.callback_query(F.data.startswith('buyproducts_')) тут pay надо ловить
# async def buy_product()



@router.message(Command('testing'))
async def testing_func(message: Message):
    products = await product.get_products_ids()
    await message.answer(text=f'{products}')


# реализовать покупку, убавление колл-ва товаров в корзине
