import logging

from telebot import types, TeleBot  # noqa
from telebot.types import Message, CallbackQuery  # noqa

from apps.tg_bot.message_templates.base_messages import BaseMessages
from apps.tg_bot.states.profile_states import ProfileStateGroup

logger = logging.getLogger(__name__)


def start_process(message: Message, bot: TeleBot):
    """Обработка команды старт."""

    if message.from_user.id not in []:
        bot.set_state(
            message.from_user.id, ProfileStateGroup.get_name, message.chat.id
        )
        bot.send_message(message.chat.id, BaseMessages.FILL_NAME)
    else:
        bot.send_message(message.chat.id, BaseMessages.IM_READY)
