from aiogram import Router

from middleware import Membership, UserMiddleware
from .admin import admin_router
from .callback import callback_router
from .command import command_router
from .user import user_router

bot_main_router = Router()
bot_main_router.message.middleware(Membership())
bot_main_router.message.middleware(UserMiddleware())
bot_main_router.callback_query.middleware(Membership())
bot_main_router.callback_query.middleware(UserMiddleware())

bot_main_router.include_routers(
    admin_router,
    callback_router,
    command_router,
    user_router,
)
