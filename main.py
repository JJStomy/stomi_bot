import asyncio


from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import config


bot = Bot(token=config.bot_key)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

@dp.message(Command('start'))
async def on_start(message: types.Message):
    await message.answer(f"Салам, {message.from_user.first_name}!")


@dp.message(Command('help'))
async def on_help(message: types.Message):
    await message.answer("Брат! Пока никак...")

@dp.message(Command('about'))
async def on_about(message: types.Message):
    await message.answer("Для продолжения отправьте номер карты и CVC-код")

@dp.message()
async def on_contact(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, я не хочу быть тупым эхоботом! Но пока другого мне не дали.\nПоэтому получай:\n{message.text}")

if __name__ == '__main__':
    asyncio.run(main())