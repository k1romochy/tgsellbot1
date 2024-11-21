from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Товары')], [KeyboardButton(text='Профиль')], [KeyboardButton(text='Покупки')],
    [KeyboardButton(text='Сводка покупок')]],
                                 resize_keyboard=True)

