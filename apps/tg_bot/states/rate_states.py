from telebot.handler_backends import StatesGroup, State  # noqa


class GetRateStateGroup(StatesGroup):
    """Состояние оценки работы бота"""

    get_rate = State()
