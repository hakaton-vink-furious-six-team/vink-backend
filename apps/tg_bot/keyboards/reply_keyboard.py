from telebot.callback_data import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup  # noqa


class RateKeyboard:
    """Клавиатура для оценки работы оператора."""

    rate_callback = CallbackData("value", prefix="rate")

    @classmethod
    def cancel_button(cls):
        """Кнопка отмены"""

        button = InlineKeyboardButton(
            text="❌ Отменить.",
            callback_data="cancel",
        )
        return button

    @classmethod
    def rate_keyboard(cls):
        """Клавиатура для оценки рейтинга"""

        rate_dict = [
            ("0️⃣", 0),
            ("1️⃣", 1),
            ("2️⃣", 2),
            ("3️⃣", 3),
            ("4️⃣", 4),
            ("5️⃣", 5),
        ]
        markup = InlineKeyboardMarkup()
        markup.row(
            *[
                InlineKeyboardButton(
                    text=rate[0],
                    callback_data=cls.rate_callback.new(value=rate[1]),
                )
                for rate in rate_dict
            ]
        )
        return markup
