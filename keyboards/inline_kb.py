import os
from collections import namedtuple

from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Paths, FileManager
from .callbacks import CallbackMainMenu, CallbackTalkMenu, CallbackQuizMenu

Button = namedtuple('Button', ['text', 'callback'])

def get_keyboard(buttons):
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.button(text=button.text, callback_data=button.callback)


    return keyboard

def main_keyboard():
    buttons = [
        Button('Рандомный факт', CallbackMainMenu(button='random')),
        Button('Спросить ChatGPT', CallbackMainMenu(button='gpt')),
        Button('Разговор со звездой', CallbackMainMenu(button='talk')),
        Button('Квиз', CallbackMainMenu(button='quiz')),
    ]

    keyboard = get_keyboard(buttons)
    keyboard.adjust(2, 2)
    return keyboard.as_markup()

def random_keyboard():
    buttons = [
        Button('Хочу еще факт!', CallbackMainMenu(button='random')),
        Button('Закончить', CallbackMainMenu(button='start')),
    ]
    return get_keyboard(buttons).as_markup()

def gpt_keyboard():
    buttons = [
        Button('Еще запрос', CallbackMainMenu(button='gpt')),
        Button('Закончить', CallbackMainMenu(button='start')),
    ]

    return get_keyboard(buttons).as_markup()

def cancel_keyboard(name='Отмена'):
    buttons = [
        Button(name, CallbackMainMenu(button='start')),
    ]

    return get_keyboard(buttons).as_markup()

def talk_keyboard():
    celebrities = [file.rsplit('.', 1)[0] for file in os.listdir(Paths.IMAGES_DIR.value) if file.startswith('talk_')]
    buttons = []
    for celebrity in celebrities:
        text = FileManager.read_file(Paths.PROMPTS, celebrity).split(',', 1)[0].split(' - ', 1)[-1]
        buttons.append(
            Button(text, CallbackTalkMenu(button='talk', celebrity=celebrity)),
        )

    buttons.append(Button('Назад', CallbackMainMenu(button='start')))
    keyboard = get_keyboard(buttons)
    keyboard.adjust(1)

    return keyboard.as_markup()

def quiz_keyboard():
    buttons = [
        Button('Программирование', CallbackQuizMenu(button='quiz', subject='quiz_prog')),
        Button('Математика', CallbackQuizMenu(button='quiz', subject='quiz_math')),
        Button('Биология>', CallbackQuizMenu(button='quiz', subject='quiz_biology')),
        Button('Назад', CallbackMainMenu(button='start'))
    ]

    keyboard = get_keyboard(buttons)

    keyboard.adjust(1)
    return keyboard.as_markup()

def quiz_answer_keyboard():
    buttons = [

        Button('Сменить тему', CallbackMainMenu(button='quiz')),
        Button('Закончить', CallbackMainMenu(button='start')),
        Button('Биология>', CallbackQuizMenu(button='quiz', subject='quiz_more')),
    ]

    return get_keyboard(buttons).as_markup()