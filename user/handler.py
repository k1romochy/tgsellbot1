from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

import user.crud as user
import aiosqlite
from markups.admin import main_admin
from markups.main import main

router = Router()


@router.message(CommandStart())
async def get_user_id_first_mess(message: Message):
    await user.create_user(tg_id=message.from_user.id)
    await message.answer(text='Добро пожаловать!', reply_markup=main)

    if message.from_user.id == 5470849504:
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)

asd