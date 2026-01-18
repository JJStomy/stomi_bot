from keyboards.callbacks import CallbackServerMenu, CallbackMainMenu
from keyboards.inline_kb import Button, get_keyboard
import os
from utils import Paths, FileManager


def server_comm_keyboard():
    buttons = []

    scripts = [file for file in os.listdir(Paths.SERVER.value)]

    for script in scripts:
        text = FileManager.read_file(Paths.SERVER, script).split('\n', 1)[1].lstrip('# ')
        buttons.append(
            Button(text, CallbackServerMenu(button='server', command_type=script)),
        )

    buttons.append(Button('Выполнить', CallbackServerMenu(button='server', command_type='exec')))
    buttons.append(Button('Назад', CallbackMainMenu(button='start')))



    keyboard = get_keyboard(buttons)
    keyboard.adjust(1)


    return keyboard.as_markup()