from aiogram import Router, Bot, F
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from ai_gpt import GPTMessage
from utils.enums import Path
from utils import FileManager
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from scheduler.scheduler import schedule_event
from keyboards import ikb_main_menu, ikb_back_button
from keyboards.callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove
from fsm import Generate, Reminder

callback_router = Router()


async def callback_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    msg_text = await FileManager.read(Path.START_COMMAND.value)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text,
        reply_markup=ikb_main_menu(),
    )


@callback_router.callback_query(CallbackMainMenu.filter())
async def menu_choice(callback: CallbackQuery, callback_data: CallbackMainMenu, state: FSMContext, bot: Bot):
    msg_text = await FileManager.read(Path.MESSAGE.value, f'start_{callback_data.button}')
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text,
        reply_markup=ikb_back_button(),
    )
    state_name = Generate
    if callback_data.button == 'reminder':
        state_name = Reminder
    await state.set_state(state_name.wait_for_answer)
    msg_list = GPTMessage(callback_data.button)
    await state.update_data(
        {
            'messages': msg_list.json(),
        }
    )


@callback_router.callback_query(CallbackBackButton.filter(F.button == 'to_main'))
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback_main_menu(callback, state, bot)


@callback_router.callback_query(CallbackApprove.filter())
async def approve_callback(callback: CallbackQuery, callback_data: CallbackApprove, state: FSMContext, bot: Bot):
    await callback.answer(
        text=callback_data.button,
        show_alert=True,
    )
    await callback_main_menu(callback, state, bot)
