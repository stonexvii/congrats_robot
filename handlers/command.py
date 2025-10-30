from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.enums import Path
from utils import FileManager

from datetime import datetime, timedelta
from scheduler.scheduler import schedule_birthday
from keyboards import ikb_main_menu

command_router = Router()


async def message_main_menu(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    msg_text = await FileManager.read(Path.START_COMMAND.value)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
        text=msg_text,
        reply_markup=ikb_main_menu(),
    )


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    msg_text = await FileManager.read(Path.START_COMMAND.value)
    await message.answer(
        text=msg_text,
        reply_markup=ikb_main_menu(),
    )


@command_router.message(Command('test'))
async def add_birthday(message: Message, bot: Bot):
    # для простоты — ввод: "Иван 2025-11-02"
    # try:
    # name, date_str = msg.text.split()
    date = datetime.now() + timedelta(minutes=1)
    schedule_birthday(message.from_user.id, 'STONE', date, bot)
    await message.answer(f"Напоминание о дне рождения STONE установлено ✅")
    # except Exception:
    #     await message.answer("Формат: Имя YYYY-MM-DD")
