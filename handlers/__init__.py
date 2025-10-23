from aiogram import Router

from middleware import Membership
from .admin import admin_router
from .command import command_router
from .user import user_router

main_router = Router()
main_router.message.middleware(Membership())

main_router.include_routers(
    admin_router,
    command_router,
    user_router,
)
