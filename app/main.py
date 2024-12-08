from aiogram import Dispatcher
from dotenv import load_dotenv
import os
import asyncio

from core.models.db_helper import async_main
from user.handler import router as user_router
from product.handler import router as product_router
from context import bot


async def main():
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(product_router)
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
