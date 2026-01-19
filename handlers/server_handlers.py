import shutil, os, subprocess

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers import command_router
from handlers.fsm import Server
from keyboards.callbacks import CallbackMainMenu, CallbackServerMenu
from keyboards.inline_kb import cancel_keyboard
from keyboards.server_keyboards import server_comm_keyboard
from utils import Paths

server_router = Router()

@server_router.callback_query(CallbackMainMenu.filter(F.button == 'server'))
async def on_server(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
    total, used, free = shutil.disk_usage("/")

    msg = f'Operation system: {os.name}\nDisc usage:\nTotal: {total / (1024**3):.2f} GB\nUsed: {used / (1024**3):.2f} GB\nFree: {free / (1024**3):.2f} GB'

    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.message.chat.id, msg, reply_markup=server_comm_keyboard())

@server_router.callback_query(CallbackServerMenu.filter(F.button == 'server'))
async def on_exec(callback: CallbackQuery, callback_data: CallbackServerMenu, state: FSMContext, bot: Bot):
    await state.clear()

    await state.set_state(Server.command)
    await state.update_data(message_id=callback.message.message_id)

    if callback_data.command_type == 'exec':
        await bot.edit_message_text(
            text='Введите команду:',
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=cancel_keyboard()
        )
    else:
        err = False
        try:
            output = subprocess.run(os.path.join(Paths.SERVER.value, callback_data.command_type), capture_output=True, text=True)
        except Exception as e:
            err_msg = e
            err = True

        if err:
            out_msg = str(err_msg)
        else:
            out_msg = output.stdout

        message_id = await state.get_value("message_id")

        await bot.edit_message_text(
            text=out_msg,
            chat_id=callback.from_user.id,
            message_id=message_id,
            reply_markup=server_comm_keyboard(),
        )

@server_router.message(Server.command)
async def wait_for_user_command(message: Message, state: FSMContext, bot: Bot):
    err = False

    msg = message.text
    try:
        output = subprocess.run(msg.split(' '), capture_output=True, text=True)
    except Exception as e:
        err_msg = e
        err = True

    if err:
        out_msg = err_msg
    else:
        out_msg = output.stdout

    await bot.delete_message(message.from_user.id, message.message_id)
    message_id = await state.get_value("message_id")

    await bot.edit_message_text(
        text=out_msg,
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=server_comm_keyboard(),
    )
