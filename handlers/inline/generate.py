# from aiogram import Router, Bot, F
# from aiogram.enums import ChatAction
# from aiogram.filters import Command
# from aiogram.types import CallbackQuery, Message
# from aiogram.fsm.context import FSMContext
#
# from utils.enums import Path
# from utils import FileManager
# from ai_gpt import GPTMessage, ai_client
# from ai_gpt.enums import GPTRole
# from datetime import datetime, timedelta
# from scheduler.scheduler import schedule_birthday
# from keyboards import ikb_back_button
# from keyboards.callback_data import CallbackMainMenu
# from utils.bot import voice_to_text, bot_thinking, get_text_from_message
# from fsm.states import Generate, Reminder
#
# generate_router = Router()
#
#
# @generate_router.callback_query(CallbackMainMenu.filter())
# async def menu_choice(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
#     msg_text = await FileManager.read(Path.MESSAGE.value, f'start_{callback_data.button}')
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=msg_text,
#         reply_markup=ikb_back_button(),
#     )
#     state_name = Generate
#     if callback_data.button == 'reminder':
#         state_name = Reminder
#     await state.set_state(state_name.wait_for_answer)
#     msg_list = GPTMessage(callback_data.button)
#     await state.update_data(
#         {
#             'messages': msg_list.json(),
#         }
#     )
#
#
# async def user_message(message: Message, function: str, bot: Bot, state: FSMContext):
#     await bot_thinking(message, bot)
#     msg_text = await get_text_from_message(message, bot)
#     if msg_text:
#         msg_list = GPTMessage(function)
#         msg_list.update(GPTRole.USER, f'Привет! Меня зовут {message.from_user.full_name}!\n' + msg_text)
#         response = await ai_client.request(msg_list, bot)
#         if response.startswith('incorrect'):
#             response = response.split('\n', 1)[-1].strip()
#         else:
#             msg_list.update(GPTRole.CHAT, response)
#         await message.answer(
#             text=response,
#             reply_markup=ikb_thx_button(),
#         )
#         await state.update_data(
#             {
#                 'messages': msg_list.json(),
#             }
#         )
