from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Товары')], [KeyboardButton(text='Профиль')], [KeyboardButton(text='Покупки')]],
                           resize_keyboard=True)