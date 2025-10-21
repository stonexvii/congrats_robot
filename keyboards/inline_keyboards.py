from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CallbackButton


def ikb_thx_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Закончить!',
        callback_data=CallbackButton(
            button='thx',
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
