import telebot


class InlineKeyboard(telebot.types.InlineKeyboardMarkup):  #
    def __init__(self, text: list[str | list[str]], width: int = 2) -> None:
        super().__init__()
        self.text: list[str | list[str]] = text
        if width == 2:
            self.row_width = len(text)
        else:
            self.row_width = width
        self.make_keyboard()

    def make_keyboard(self) -> None:
        for text in self.text:
            self.add(telebot.types.InlineKeyboardButton(text[0], callback_data=text[1]))


class Keyboard(telebot.types.ReplyKeyboardMarkup):
    def __init__(self, text: list[str], resize: bool = True) -> None:
        super().__init__()
        self.resize_keyboard = resize
        self.text: list[str] = text
        self.make_keyboard()

    def make_keyboard(self) -> None:
        for text in self.text:
            if isinstance(text, list):
                self.row(*[telebot.types.KeyboardButton(text_[0]) for text_ in text])
            else:
                self.add(telebot.types.KeyboardButton(text))
