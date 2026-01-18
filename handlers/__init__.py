from aiogram import Router

from .command_handlers import command_router
from .server_handlers import server_router
from .start_handler import start_router
from .reply_handlers import reply_router

main_router = Router()

main_router.include_routers(
    server_router,
    reply_router,
    command_router,
    start_router,

)