import subprocess

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.input_file import FSInputFile

from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from ai_open.settings import GPTRole
from keyboards.inline_kb import gpt_keyboard, cancel_keyboard, quiz_answer_keyboard, translate_keyboard, \
    server_comm_keyboard
from utils import Paths
from .fsm import GPTRequest, CelebrityTalk, QUIZ, Translate, Server

reply_router = Router()


@reply_router.message(GPTRequest.wait_for_request)
async def wait_for_user_request(message: Message, state: FSMContext, bot: Bot):
    msg_list = GPTMessage('gpt')
    msg_list.update(GPTRole.USER, message.text)

    await bot.delete_message(message.from_user.id, message.message_id)
    response = await chat_gpt.request(msg_list, bot)
    message_id = await state.get_value("message_id")


    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file='gpt')),
            caption=response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=gpt_keyboard(),
    )

@reply_router.message(CelebrityTalk.dialog)
async def celebrity_dialog(message: Message, state: FSMContext, bot: Bot):
    msg_list = await state.get_value("messages")
    celebrity = await state.get_value("celebrity")
    msg_list.update(GPTRole.USER, message.text)
    response = await chat_gpt.request(msg_list, bot)
    msg_list.update(GPTRole.CHAT, response)
    await state.update_data(message=msg_list)

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=FSInputFile(Paths.IMAGES.value.format(file=celebrity)),
        caption=response,
        reply_markup=cancel_keyboard('Закончить'),
    )

@reply_router.message(QUIZ.game)
async def user_answer(message: Message, state: FSMContext, bot: Bot):
    msg_list = await state.get_value("messages")
    message_id = await state.get_value("message_id")
    score = await state.get_value("score")
    msg_list.update(GPTRole.USER, message.text)
    response = await chat_gpt.request(msg_list, bot)
    msg_list.update(GPTRole.CHAT, response)
    await state.update_data(message=msg_list)

    if response=='Правильно!':
        score += 1
        await state.update_data(score=score)

    response += f'\n\nВаш счет: {score}'
    msg_list.update(GPTRole.CHAT, response)
    await state.update_data(message=msg_list)

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file='quiz')),
            caption=response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=quiz_answer_keyboard(),
    )

@reply_router.message(Translate.translate)
async def wait_for_user_text(message: Message, state: FSMContext, bot: Bot):
    lang = await state.get_value("language")
    msg_list = GPTMessage(lang)
    msg_list.update(GPTRole.USER, message.text)

    await bot.delete_message(message.from_user.id, message.message_id)
    message_id = await state.get_value("message_id")

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=lang)),
            caption=message.text,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=cancel_keyboard(),
    )

    response = await chat_gpt.request(msg_list, bot)


    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Paths.IMAGES.value.format(file=lang)),
            caption=response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=translate_keyboard(),
    )

@reply_router.message(Server.command)
async def wait_for_user_command(message: Message, state: FSMContext, bot: Bot):
    # msg_list = GPTMessage('gpt')
    # msg_list.update(GPTRole.USER, message.text)

    msg = message.text
    try:
        output = subprocess.run(msg.split(' '), capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        err_msg = e.stdout.decode()
        err = True


    # print(output.stdout)
    if err:
        out_msg = err_msg
    else:
        out_msg = output.stdout

    await bot.delete_message(message.from_user.id, message.message_id)
    # response = await chat_gpt.request(msg_list, bot)
    message_id = await state.get_value("message_id")

    await bot.edit_message_text(
        text=out_msg,
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=server_comm_keyboard(),
    )

    # await bot.edit_message_media(
    #     media=InputMediaPhoto(
    #         media=FSInputFile(Paths.IMAGES.value.format(file='gpt')),
    #         caption=response,
    #     ),
    #     chat_id=message.from_user.id,
    #     message_id=message_id,
    #     reply_markup=gpt_keyboard(),
    # )