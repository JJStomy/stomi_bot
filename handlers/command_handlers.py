import os, shutil

from aiogram import Router, Bot, F
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from ai_open.settings import GPTRole
from keyboards.callbacks import CallbackMainMenu, CallbackTalkMenu, CallbackQuizMenu, CallbackLangMenu, \
    CallbackServerMenu
from keyboards.inline_kb import main_keyboard, random_keyboard, cancel_keyboard, talk_keyboard, quiz_keyboard, \
    lang_keyboard
from keyboards.server_keyboards import server_comm_keyboard
from utils import FileManager
from utils import Paths
from .fsm import GPTRequest, CelebrityTalk, QUIZ, Translate, Server

command_router = Router()

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'random'))
async def on_random(callback: CallbackQuery, callback_data: CallbackMainMenu, bot: Bot):
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
    await bot.send_chat_action(callback.from_user.id, ChatAction.TYPING)
    response = await chat_gpt.request(GPTMessage('random'), bot)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=random_keyboard(),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'start'))
async def on_main(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(callback.from_user.id),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'gpt'))
async def on_gpt(callback: CallbackQuery, callback_data: CallbackMainMenu, state : FSMContext, bot: Bot):
    await state.set_state(GPTRequest.wait_for_request)
    await state.update_data(message_id=callback.message.message_id)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=cancel_keyboard(),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'talk'))
async def on_talk(callback: CallbackQuery, callback_data: CallbackMainMenu, state : FSMContext, bot: Bot):
    await state.clear()
    await state.set_state(GPTRequest.wait_for_request)
    await state.update_data(message_id=callback.message.message_id)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=talk_keyboard(),
    )

@command_router.callback_query(CallbackTalkMenu.filter(F.button == 'talk'))
async def on_celebrity(callback: CallbackQuery, callback_data: CallbackTalkMenu, state : FSMContext, bot: Bot):
    await state.set_state(CelebrityTalk.dialog)

    message_list = GPTMessage(callback_data.celebrity)
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages=message_list, celebrity=callback_data.celebrity)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.celebrity)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=cancel_keyboard('Закончить'),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'quiz'))
async def on_quiz(callback: CallbackQuery, callback_data: CallbackMainMenu, state : FSMContext, bot: Bot):
    await state.set_state(QUIZ.game)
    message_list = await state.get_value('messages')
    if not message_list:
        await state.update_data(score=0, messages=None, message_id=callback.message.message_id)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=quiz_keyboard(),
    )

@command_router.callback_query(CallbackQuizMenu.filter(F.button == 'quiz'))
async def on_quiz(callback: CallbackQuery, callback_data: CallbackQuizMenu, state : FSMContext, bot: Bot):
    message_list = await state.get_value('messages')
    if not message_list:
        message_list = GPTMessage('quiz')
    message_list.update(GPTRole.USER, callback_data.subject)
    response = await chat_gpt.request(message_list, bot)
    await state.update_data(messages=message_list)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=cancel_keyboard(),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'translate'))
async def on_translate(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=lang_keyboard(),
    )

@command_router.callback_query(CallbackLangMenu.filter(F.button == 'translate'))
async def on_lang(callback: CallbackQuery, callback_data: CallbackLangMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await state.set_state(Translate.translate)
    await state.update_data(message_id=callback.message.message_id)
    await state.update_data(language=callback_data.language)


    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.language)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.language),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=cancel_keyboard(),
    )

@command_router.callback_query(CallbackLangMenu.filter(F.button == 'training'))
async def on_training(callback: CallbackQuery, callback_data: CallbackLangMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await state.set_state(Translate.translate)
    await state.update_data(message_id=callback.message.message_id)
    await state.update_data(language=callback_data.language)


    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=callback_data.language)),
            caption=FileManager.read_file(Paths.MESSAGES, callback_data.language),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=cancel_keyboard(),
    )

@command_router.callback_query(CallbackMainMenu.filter(F.button == 'server'))
async def on_server(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
    total, used, free = shutil.disk_usage("/")

    msg = f'Operation system: {os.name}\nDisc usage:\nTotal: {total / (1024**3):.2f} GB\nUsed: {used / (1024**3):.2f} GB\nFree: {free / (1024**3):.2f} GB'

    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.message.chat.id, msg, reply_markup=server_comm_keyboard())

