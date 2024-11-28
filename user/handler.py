from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

import user.crud as user
import aiosqlite
from markups.main import main
import product.crud as product

router = Router()


@router.message(CommandStart())
async def get_user_id_first_mess(message: Message):
    await user.create_user(tg_id=message.from_user.id)
    await message.answer(text='Добро пожаловать!', reply_markup=main)

    if message.from_user.id == 5470849504:
        await message.answer(f'Вы авторизовались как администратор \nВведите /create_product чтобы добавить товар')


@router.message(F.text == 'Профиль')
async def get_user_profile(message: Message):
    balance = await user.get_user_balande(message.from_user.id)

    await message.reply(f'Баланс: {balance}', reply_markup=main.profile)
