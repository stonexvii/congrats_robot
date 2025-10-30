# from aiogram import Router, Bot, F
# from aiogram.enums import ChatAction
# from aiogram.filters import Command
# from aiogram.types import CallbackQuery
#
# from utils.enums import Path
# from utils import FileManager
#
# from datetime import datetime, timedelta
# from scheduler.scheduler import schedule_birthday
# from keyboards import ikb_back_button
# from keyboards.callback_data import CallbackMainMenu
#
# reminder_router = Router()
#
#
# @reminder_router.callback_query(CallbackMainMenu.filter(F.button == 'reminder'))
# async def reminder_menu(callback: CallbackQuery, bot: Bot):
#     msg_text = await FileManager.read(Path.START_REMINDER.value)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=msg_text,
#         reply_markup=ikb_back_button(),
#     )
