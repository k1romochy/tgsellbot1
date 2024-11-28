from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import product.crud as product


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Товары')], [KeyboardButton(text='Профиль')], [KeyboardButton(text='Корзина')]],
                           resize_keyboard=True)


profile = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Покупки')], [KeyboardButton(text='Пополнить баланс')]], resize_keyboard=True)


