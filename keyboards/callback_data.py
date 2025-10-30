from aiogram.filters.callback_data import CallbackData


class CallbackMainMenu(CallbackData, prefix='CMM'):
    button: str


class CallbackApprove(CallbackData, prefix='CA'):
    button: str


class CallbackBackButton(CallbackData, prefix='CB'):
    button: str
