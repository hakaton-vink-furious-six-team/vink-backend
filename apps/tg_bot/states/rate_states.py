from telebot.handler_backends import StatesGroup, State  # noqa


class GetRateStateGroup(StatesGroup):
    get_rate = State()
