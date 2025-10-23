from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message

from ai_gpt.enums import Path
from utils import FileManager

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_text')
    await message.answer(
        text=msg_text,
    )
