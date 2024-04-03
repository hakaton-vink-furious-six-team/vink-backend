import logging
import time

from telebot import types, TeleBot  # noqa
from telebot.types import Message, CallbackQuery  # noqa

from apps.tg_bot.keyboards.reply_keyboard import RateKeyboard
from apps.tg_bot.message_templates.base_messages import BaseMessages
from apps.tg_bot.states.profile_states import ProfileStateGroup
from apps.tg_bot.states.rate_states import GetRateStateGroup
from apps.tg_bot.utils.utils import check_user_exists  # , delete_user

logger = logging.getLogger(__name__)


def start_process(message: Message, bot: TeleBot):
    """Обработка команды старт."""
    # delete_user(message.from_user.id)  # 4dev TODO убрать перед деплоем
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    if not check_user_exists(message.from_user.id):
        bot.set_state(
            message.from_user.id, ProfileStateGroup.get_name, message.chat.id
        )
        bot.send_message(message.chat.id, BaseMessages.FILL_NAME)
    else:
        bot.send_message(message.chat.id, BaseMessages.IM_READY)


def command_help_handler(message: types.Message, bot: TeleBot):
    """Ответ на выбор меню help."""
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(
        chat_id=message.chat.id,
        text=BaseMessages.HELP_TEXT,
    )
    logger.debug(f"Пользователь: {message.from_user.id} вызвал /help")


def command_rate_handler(message: types.Message, bot: TeleBot):
    """Оценка работы оператора /rate."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(
        chat_id=message.from_user.id,
        text=BaseMessages.RATE_FIRST_MESSAGE,
        reply_markup=RateKeyboard.rate_keyboard(),
    )
    bot.set_state(
        user_id=user_id,
        state=GetRateStateGroup.get_rate,
        chat_id=chat_id,
    )
    logger.debug(
        f"Пользователь: {user_id} перешел в состояние оценки работы оператора."
    )


def get_rate(callback: types.CallbackQuery, bot: TeleBot):
    """Обработка оценки пользователя."""

    chat_id = callback.message.chat.id
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text=BaseMessages.RATE_THX,
    )
    time.sleep(0.5)
    bot.delete_message(chat_id=chat_id, message_id=callback.message.id)

    logger.info(
        f"Пользователь: {callback.from_user.id}"
        f" оставил оценку работе оператора."
    )
