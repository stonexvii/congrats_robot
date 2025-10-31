from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.tables import User
from keyboards import ikb_main_menu, ikb_welcome
from utils import FileManager
from utils.enums import Path

command_router = Router()


async def message_main_menu(message: Message, message_id: int, state: FSMContext, bot: Bot):
    await state.clear()
    msg_text = await FileManager.read(Path.START_COMMAND.value)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message_id,
        text=msg_text,
        reply_markup=ikb_main_menu(),
    )


@command_router.message(Command('start'))
async def command_start(message: Message, user: User, bot: Bot):
    if user:
        await bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING,
        )
        msg_text = await FileManager.read(Path.START_COMMAND.value)
        keyboard = ikb_main_menu()
    else:
        msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_start')
        keyboard = ikb_welcome('Принять', 'apply')
    await message.answer(
        text=msg_text,
        reply_markup=keyboard,
    )
