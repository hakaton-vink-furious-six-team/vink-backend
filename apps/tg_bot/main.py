import time
import logging

from apps.tg_bot.handlers.command_handlers import start_process
from apps.tg_bot.handlers.state_handlers import (
    get_company_name,
    get_name,
    get_phone_number,
)
from apps.tg_bot.states.profile_states import ProfileStateGroup

from config.settings import THREAD_QTY
from environs import Env
from telebot import TeleBot, StateMemoryStorage, custom_filters  # noqa
from telebot.types import Message  # noqa


from telebot.handler_backends import StatesGroup, State  # noqa

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

state_storage = StateMemoryStorage()

token = env("BOT_TOKEN")
bot = TeleBot(
    token=token,
    parse_mode="HTML",
    num_threads=THREAD_QTY,
    state_storage=state_storage,
)


def register_handlers() -> None:
    """Регистрация хэндлеров."""
    bot.register_message_handler(
        start_process, commands=["start"], pass_bot=True
    )
    bot.register_message_handler(
        get_name,
        state=ProfileStateGroup.get_name,  # noqa
        pass_bot=True,
        func=None,  # noqa
    )
    bot.register_message_handler(
        get_phone_number,
        state=ProfileStateGroup.get_phone_number,  # noqa
        pass_bot=True,
        func=None,  # noqa
    )
    bot.register_message_handler(
        get_company_name,
        state=ProfileStateGroup.get_company,
        pass_bot=True,
        func=None,  # noqa
    )


def bot_starter():
    logger.info("Запуск телеграмм бота.")
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    register_handlers()
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
        url=env("WEBHOOK_URL"),  # dev - ngrok http http://127.0.0.1:8000
        drop_pending_updates=True,
        allowed_updates=["*"],
    )
    logger.info("Бот запущен.>")
