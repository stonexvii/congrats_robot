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
from fsm import Generate, Reminder
from keyboards import ikb_approve_button, ikb_back_button
from keyboards.callback_data import CallbackApprove
import json

from utils import FileManager
from utils.bot import bot_thinking, get_text_from_message
from utils.enums import Path
from scheduler.scheduler import schedule_birthday
from datetime import datetime

user_router = Router()


# async def voice_to_text(message: Message, bot: Bot):
#     try:
#         voice = await bot.get_file(message.voice.file_id)
#         file_path = voice.file_path
#         voice_ogg = os.path.join(Path.VOICE.value, f'voice_{message.from_user.id}.ogg')
#         await bot.download_file(file_path, destination=voice_ogg)
#         response_text = await ai_client.transcript_voice(voice_ogg, bot)
#         os.remove(voice_ogg)
#         return response_text
#     except Exception as e:
#         await message.answer(f"⚠️ Ошибка при обработке аудио: {e}")
#         return None
#
#
# async def bot_thinking(message: Message, bot: Bot):
#     await message.answer(
#         text=choice(ANSWERS),
#     )
#     await bot.send_chat_action(
#         chat_id=message.from_user.id,
#         action=ChatAction.TYPING,
#     )


# @user_router.callback_query(CallbackApprove.filter(F.button == 'generate'))
# async def say_thx(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     data = await state.get_value('messages')
#     msg_list = GPTMessage.from_json(data)
#     msg_list.update(GPTRole.USER, 'Закончить')
#     response = await ai_client.request(msg_list, bot)
#     await bot.send_message(
#         chat_id=callback.from_user.id,
#         text=response,
#     )
#     await asyncio.sleep(3)
#     await callback.answer(
#         text='История переписки очищена!',
#         show_alert=True,
#     )
#     await state.clear()


@user_router.message(Generate.wait_for_answer)
@user_router.message(Reminder.wait_for_answer)
async def wait_for_answer(message: Message, bot: Bot, state: FSMContext):
    await bot_thinking(message, bot)
    msg_text = await get_text_from_message(message, bot)
    if msg_text:
        data = await state.get_value('messages')
        msg_list = GPTMessage.from_json(data)
        msg_list.update(GPTRole.USER, msg_text)
        response = await ai_client.request(msg_list, bot)
        keyboard = ikb_back_button()
        if response.startswith('INCORRECT'):
            response = response.split('\n', 1)[-1].strip()
        elif response.startswith('DONE'):
            response = response.split('\n', 1)[-1].strip()
            msg_list.update(GPTRole.CHAT, response)
            data = json.loads('{' + response + '}')
            response = await FileManager.read(Path.MESSAGE.value, 'reminder_text', **data)
            keyboard = ikb_approve_button('reminder')
        else:
            msg_list.update(GPTRole.CHAT, response)
            keyboard = ikb_approve_button('generate')
        await message.answer(
            text=response,
            reply_markup=keyboard,
        )
        await state.update_data(
            {
                'messages': msg_list.json(),
            }
        )

# @user_router.message(Reminder.wait_for_answer)
# async def wait_for_answer(message: Message, bot: Bot, state: FSMContext):
#     await bot_thinking(message, bot)
#     if message.voice:
#         data_text = await voice_to_text(message, bot)
#     else:
#         data_text = message.text
#     if data_text:
#         data = await state.get_value('messages')
#         msg_list = GPTMessage.from_json(data)
#         msg_list.update(GPTRole.USER, data_text)
#         response = await ai_client.request(msg_list, bot)
#         if response.startswith('None'):
#             response = response.split('\n', 1)[-1].strip()
#         else:
#             msg_list.update(GPTRole.CHAT, response)
#         await message.answer(
#             text=response,
#             reply_markup=ikb_approve_button('generate'),
#         )
#         await state.set_state(UserDialog.wait_for_answer)
#         await state.update_data(
#             {
#                 'messages': msg_list.json(),
#             }
#         )

# @user_router.message()
# async def user_message(message: Message, bot: Bot, state: FSMContext):
#     await bot_thinking(message, bot)
#     if message.voice:
#         data_text = await voice_to_text(message, bot)
#         print(data_text)
#     else:
#         data_text = message.text
#     if data_text:
#         msg_list = GPTMessage('main_prompt')
#         msg_list.update(GPTRole.USER, f'Привет! Меня зовут {message.from_user.full_name}!\n' + data_text)
#         response = await ai_client.request(msg_list, bot)
#         if response.startswith('None'):
#             response = response.split('\n', 1)[-1].strip()
#         else:
#             msg_list.update(GPTRole.CHAT, response)
#         await message.answer(
#             text=response,
#             reply_markup=ikb_thx_button(),
#         )
#         await state.set_state(UserDialog.wait_for_answer)
#         await state.update_data(
#             {
#                 'messages': msg_list.json(),
#             }
#         )

# @user_router.message()
# async def user_message(message: Message, bot: Bot, state: FSMContext):
#     await bot_thinking(message, bot)
#     if message.voice:
#         data_text = await voice_to_text(message, bot)
#     else:
#         data_text = message.text
#     if data_text:
#         msg_list = GPTMessage('reminder')
#         msg_list.update(GPTRole.USER, f'Привет! Меня зовут {message.from_user.full_name}!\n' + data_text)
#         response = await ai_client.request(msg_list, bot)
#         if response.startswith('incorrect'):
#             msg_text = response.split('\n', 1)[-1]
#         else:
#             json_data = json.loads(response)
#             msg_text = await FileManager.read(Path.MESSAGE.value, 'reminder_text', **json_data)
#             # print(json_data['reminder'])
#             reminder = datetime.strptime(json_data['reminder'], '%Y-%m-%d %H:%M')
#             # print(reminder)
#             reminder = reminder.replace(year=2025)
#             print(reminder)
#             # schedule_birthday(message.from_user.id, json_data['name'], reminder, bot)
#         await message.answer(
#             text=msg_text,
#         )

# if response.startswith('None'):
#     response = response.split('\n', 1)[-1].strip()
# else:
#     msg_list.update(GPTRole.CHAT, response)
# await message.answer(
#     text=response,
#     reply_markup=ikb_thx_button(),
# )
# await state.set_state(UserDialog.wait_for_answer)
# await state.update_data(
#     {
#         'messages': msg_list.json(),
#     }
# )
