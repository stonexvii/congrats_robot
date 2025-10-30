from aiogram.utils.keyboard import InlineKeyboardBuilder

from .buttons import MainMenuButton, BackButton, ApproveButton
from .callback_data import CallbackBackButton


def ikb_approve_button(button: str):
    keyboard = InlineKeyboardBuilder()
    button_text = 'Закончить' if button == 'generate' else 'Сохранить'
    keyboard.button(**ApproveButton(button_text, button).as_kwargs())
    return keyboard.as_markup()


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        MainMenuButton('Поздравление', button='generate'),
        MainMenuButton('Напоминание', button='reminder'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(2)
    return keyboard.as_markup()


def ikb_back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**BackButton('Назад', 'to_main').as_kwargs())
    return keyboard.as_markup()
