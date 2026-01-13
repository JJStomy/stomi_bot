from aiogram import Router

from .command_handlers import command_router
from .start_handler import start_router
from .reply_handlers import reply_router

main_router = Router()

main_router.include_routers(
    reply_router,
    command_router,
    start_router,

)