import logging

from telebot import types, TeleBot  # noqa
from telebot.types import Message  # noqa

from apps.tg_bot.message_templates.base_messages import BaseMessages
from apps.tg_bot.states.profile_states import ProfileStateGroup

logger = logging.getLogger(__name__)


def bot_message_handler(message: Message, bot: TeleBot):
    user_id = message.from_user.id
    try:
        from apps.user_profile.models import UserProfile

        user = UserProfile.objects.filter(tg_id=user_id)
        if user:
            bot.send_message(
                message.chat.id, "Да, абсолютно верно, есть еще вопросы"
            )
        else:
            bot.set_state(
                message.from_user.id,
                ProfileStateGroup.get_name,
                message.chat.id,
            )
            bot.send_message(message.chat.id, BaseMessages.FILL_NAME)

    except Exception as e:
        logger.exception(e)
