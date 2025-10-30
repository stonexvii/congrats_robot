from aiogram import Router

from middleware import Membership
from .generate import generate_router
from .reminder import reminder_router
from handlers.callback import callback_router

inline_router = Router()
inline_router.message.middleware(Membership())

inline_router.include_routers(
    callback_router,
    # generate_router,
    # reminder_router,
)
