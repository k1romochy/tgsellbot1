from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import user.crud as user
from markups.main import main
from app.context import bot

router = Router()


@router.message(CommandStart())
async def get_user_id_first_mess(message: Message):
    await user.create_user(tg_id=message.from_user.id)
    await message.answer(text='Добро пожаловать!', reply_markup=main)
    if message.from_user.id == 5470849504:
        await message.answer(
            'Вы авторизовались как администратор \nВведите /create_product чтобы добавить товар'
        )


@router.message(Command('sendmess'))
async def send_message_to_user(message: Message):
    if message.from_user.id == 5470849504:
        args = message.text.split(' ', 2)
        if len(args) < 3:
            await message.answer('Используйте формат: /sendmess user_id текст')
            return
        user_id = int(args[1])
        text = args[2]
        await bot.send_message(chat_id=user_id, text=text)
    else:
        await message.answer('Вы не обладаете такими правами')
