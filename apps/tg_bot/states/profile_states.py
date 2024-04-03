from telebot.handler_backends import StatesGroup, State  # noqa


class ProfileStateGroup(StatesGroup):
    get_name = State()
    get_phone_number = State()
    get_company = State()
