import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from core.models.db_helper import async_main
from user.handler import router
from product.handler import router as router2


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router2)
    await async_main()
    await dp.start_polling((bot))

if __name__ == '__main__':
    asyncio.run(main())


