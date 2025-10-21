from aiogram.filters.callback_data import CallbackData


class CallbackButton(CallbackData, prefix='CB'):
    button: str
