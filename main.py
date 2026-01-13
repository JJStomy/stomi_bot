import asyncio

from aiogram import Bot, Dispatcher

import config

from handlers import main_router

bot = Bot(token=config.BOT_KEY)
dp = Dispatcher()

async def main():
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass