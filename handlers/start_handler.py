from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from keyboards.inline_kb import main_keyboard
from utils import FileManager
from utils import Paths

start_router = Router()


@start_router.message(Command('start'))
async def on_start(message: Message, command: CommandObject):
    await message.answer_photo(
        photo=FSInputFile(Paths.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_file(Paths.MESSAGES, command.command),
        reply_markup = main_keyboard(),
    )

