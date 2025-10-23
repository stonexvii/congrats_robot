import asyncio
import os
from random import choice

from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ai_gpt import ai_client
from ai_gpt.enums import GPTRole, Path
from ai_gpt.gpt_client import GPTMessage
from data import ANSWERS
from fsm.states import UserDialog
from keyboards import ikb_thx_button
from keyboards.callback_data import CallbackButton

user_router = Router()


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


async def bot_thinking(message: Message, bot: Bot):
    await message.answer(
        text=choice(ANSWERS),
    )
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )


@user_router.callback_query(CallbackButton.filter())
async def say_thx(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_value('messages')
    msg_list = GPTMessage.from_json(data)
    msg_list.update(GPTRole.USER, 'Закончить')
    response = await ai_client.request(msg_list, bot)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=response,
    )
    await asyncio.sleep(3)
    await callback.answer(
        text='История переписки очищена!',
        show_alert=True,
    )
    await state.clear()


@user_router.message(UserDialog.wait_for_answer)
async def wait_for_answer(message: Message, bot: Bot, state: FSMContext):
    await bot_thinking(message, bot)
    if message.voice:
        data_text = await voice_to_text(message, bot)
    else:
        data_text = message.text
    if data_text:
        data = await state.get_value('messages')
        msg_list = GPTMessage.from_json(data)
        msg_list.update(GPTRole.USER, data_text)
        response = await ai_client.request(msg_list, bot)
        if response.startswith('None'):
            response = response.split('\n', 1)[-1].strip()
        else:
            msg_list.update(GPTRole.CHAT, response)
        await message.answer(
            text=response,
            reply_markup=ikb_thx_button(),
        )
        await state.set_state(UserDialog.wait_for_answer)
        await state.update_data(
            {
                'messages': msg_list.json(),
            }
        )


@user_router.message()
async def user_message(message: Message, bot: Bot, state: FSMContext):
    await bot_thinking(message, bot)
    if message.voice:
        data_text = await voice_to_text(message, bot)
    else:
        data_text = message.text
    if data_text:
        msg_list = GPTMessage('main_prompt')
        msg_list.update(GPTRole.USER, f'Привет! Меня зовут {message.from_user.full_name}!\n' + data_text)
        response = await ai_client.request(msg_list, bot)
        if response.startswith('None'):
            response = response.split('\n', 1)[-1].strip()
        else:
            msg_list.update(GPTRole.CHAT, response)
        await message.answer(
            text=response,
            reply_markup=ikb_thx_button(),
        )
        await state.set_state(UserDialog.wait_for_answer)
        await state.update_data(
            {
                'messages': msg_list.json(),
            }
        )
