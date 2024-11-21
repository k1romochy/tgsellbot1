from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

import product.crud as product
import aiosqlite
from markups.admin import main_admin
from markups.main import main

router = Router()


@router.message(Command('create_product'))
async def create_product(message: Message):
    if message.from_user.id == 5470849504:
        secondary_message = str(message).split()
        start_index = next((i for i, item in enumerate(secondary_message) if item.startswith("text='/create_product")), None)

        result = []
        if start_index is not None:
            for item in secondary_message[start_index + 1:]:
                if "=" in item:
                    break
                result.append(item)


        await product.add_product(name=str(result[0]), model=str(result[1]), price=int(result[2]), desc=str(result[3][:-1]))
        await message.answer('Вы успешно добавили товар!')
    else:
        await message.answer('Вы не обладаете правами для использования этой команды')


@router.message(F.text == 'Товары')
async def get_product(message: Message):
    pass


@router.message(Command('delete_product'))
async def delete_product(message: Message): # 123 надо сделать через клаву, чтобы админ нажимал "удалить товар"