from telebot.types import InlineKeyboardButton  # noqa


class ProfileKeyboard:
    button = InlineKeyboardButton(
        text="❌ Отменить.",
        callback_data="cancel",
    )


def cancel_button():
    button = InlineKeyboardButton(
        text="❌ Отменить.",
        callback_data="cancel",
    )
    return button
