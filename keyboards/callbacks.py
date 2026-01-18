from aiogram.filters.callback_data import CallbackData

class CallbackMainMenu(CallbackData, prefix='MAIN'):
    button: str
    id: int = 0

class CallbackTalkMenu(CallbackData, prefix='TALK'):
    button: str
    celebrity: str

class CallbackQuizMenu(CallbackData, prefix='QUIZ'):
    button: str
    subject: str

class CallbackLangMenu(CallbackData, prefix='LANG'):
    button: str
    language: str

class CallbackServerMenu(CallbackData, prefix='SERV'):
    button: str
    command_type: str