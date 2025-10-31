from aiogram.utils.keyboard import InlineKeyboardBuilder

from .buttons import KeyboardButton
from .callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove


def ikb_welcome(text: str, button: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**KeyboardButton(text, CallbackMainMenu, button=button).as_kwargs())
    return keyboard.as_markup()


def ikb_approve_button(button: str):
    keyboard = InlineKeyboardBuilder()
    button_text = 'Закончить' if button == 'generate' else 'Сохранить'
    keyboard.button(**KeyboardButton(button_text, CallbackApprove, button=button).as_kwargs())
    return keyboard.as_markup()


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Поздравление', CallbackMainMenu, button='generate'),
        KeyboardButton('Напоминание', CallbackMainMenu, button='reminder'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(2)
    return keyboard.as_markup()


def ikb_remind_menu(task_id: int):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Поздравление', CallbackMainMenu, button='generate', id=task_id),
        KeyboardButton('Назад', CallbackBackButton, button='to_main'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(2)
    return keyboard.as_markup()


def ikb_back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**KeyboardButton('Назад', CallbackBackButton, button='to_main').as_kwargs())
    return keyboard.as_markup()
