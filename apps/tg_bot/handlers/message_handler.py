import logging

from telebot import types, TeleBot  # noqa
from telebot.types import Message  # noqa

from apps.chat.gpt_utilities import sync_gpt_answer
from apps.tg_bot.message_templates.base_messages import BaseMessages
from apps.tg_bot.states.profile_states import ProfileStateGroup
from apps.tg_bot.utils.utils import (
    check_user_exists,
    get_user,
    get_or_create_chat,
    create_message,
)

logger = logging.getLogger(__name__)


def bot_message_handler(message: Message, bot: TeleBot):
    """Обработка стандартных текстовых сообщений."""
    # Если пользователь уже есть в бд
    if check_user_exists(message.from_user.id):
        message_list = [
            {"role": "user", "text": message.text},
        ]
        user = get_user(message.from_user.id)
        chat, created = get_or_create_chat(user)
        create_message(chat, "user", message.text)
        logger.info("Ответ пользователя записан в бд")
        try:
            bot_answer = sync_gpt_answer(message_list)
            bot.send_message(message.chat.id, bot_answer)
            create_message(chat, "assistant", bot_answer)
            logger.info("Ответ бота записан в бд")
        except Exception as ex:
            logger.exception(ex)

    # Если новый пользователь
    else:
        bot.set_state(
            message.from_user.id,
            ProfileStateGroup.get_name,
            message.chat.id,
        )
        bot.send_message(message.chat.id, BaseMessages.FILL_NAME)
        logger.info("Новый пользователь отправлен на регистрацию.")


def not_valid_message_handler(message: types.Message, bot: TeleBot):
    """Хендлер не текстовых сообщений"""

    bot.send_message(
        chat_id=message.chat.id,
        text=BaseMessages.NOT_VALID_MESSAGE,
    )
    logger.info("Пользователь отправил не текстовое сообщение")
