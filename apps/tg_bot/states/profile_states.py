from telebot.handler_backends import StatesGroup, State  # noqa


class ProfileStateGroup(StatesGroup):
    """Состояния для создания нового пользователя"""

    get_name = State()
    get_phone_number = State()
    get_company = State()
