import asyncio
import os
from random import choice

from aiogram import Router, Bot, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ai_gpt import ai_client
from ai_gpt.enums import GPTRole
from utils.enums import Path
from ai_gpt.gpt_client import GPTMessage
from data import ANSWERS
from fsm.states import UserDialog
from keyboards import ikb_approve_button
from keyboards.callback_data import CallbackApprove
import json

from utils import FileManager
from utils.enums import Path
from scheduler.scheduler import schedule_event
from datetime import datetime


async def bot_thinking(message: Message, bot: Bot):
    await message.answer(
        text=choice(ANSWERS),
    )
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )


async def voice_to_text(message: Message, bot: Bot):
    try:
        voice = await bot.get_file(message.voice.file_id)
        file_path = voice.file_path
        voice_ogg = os.path.join(Path.VOICE.value, f'voice_{message.from_user.id}.ogg')
        await bot.download_file(file_path, destination=voice_ogg)
        response_text = await ai_client.transcript_voice(voice_ogg, bot)
        os.remove(voice_ogg)
        return response_text
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при обработке аудио: {e}")
        return None


async def get_text_from_message(message: Message, bot: Bot):
    if message.voice:
        data_text = await voice_to_text(message, bot)
    else:
        data_text = message.text
    return data_text
