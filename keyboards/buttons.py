from .callback_data import CallbackMainMenu, CallbackBackButton, CallbackApprove


class MainMenuButton:
    def __init__(self, text: str, button: str | None = None, url: str | None = None):
        self.text = text
        if button:
            self.callback_data = CallbackMainMenu(
                button=button,
            )
        if url:
            self.url = url

    def as_kwargs(self):
        return self.__dict__


class ApproveButton:
    def __init__(self, text: str, button: str | None = None):
        self.text = text
        if button:
            self.callback_data = CallbackApprove(
                button=button,
            )

    def as_kwargs(self):
        return self.__dict__


class BackButton:
    def __init__(self, text: str, button: str | None = None):
        self.text = text
        if button:
            self.callback_data = CallbackBackButton(
                button=button,
            )

    def as_kwargs(self):
        return self.__dict__
