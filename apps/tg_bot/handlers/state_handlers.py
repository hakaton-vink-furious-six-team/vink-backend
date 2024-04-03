import logging
import re

from telebot.types import Message  # noqa
from telebot import TeleBot, custom_filters  # noqa

from apps.tg_bot.message_templates.base_messages import BaseMessages
from apps.tg_bot.states.profile_states import ProfileStateGroup
from apps.tg_bot.utils.utils import create_new_user

logger = logging.getLogger(__name__)


def get_name(message: Message, bot: TeleBot):
    """
    Записываем имя.
    """
    bot.send_message(message.chat.id, BaseMessages.FILL_PHONE_NUMBER)
    bot.set_state(
        message.from_user.id,
        ProfileStateGroup.get_phone_number,
        message.chat.id,
    )
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text


def get_phone_number(message: Message, bot: TeleBot):
    """
    Записываем номер телефона.
    """
    if re.match(r"^\+\d{7,15}$", message.text):
        bot.send_message(message.chat.id, "Напишите название компании.")
        bot.set_state(
            message.from_user.id,
            ProfileStateGroup.get_company,
            message.chat.id,
        )
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["phone_number"] = message.text
    else:
        bot.send_message(message.chat.id, BaseMessages.WRONG_PHONE_NUMBER)
        bot.set_state(
            message.from_user.id,
            ProfileStateGroup.get_phone_number,
            message.chat.id,
        )


def get_company_name(message: Message, bot: TeleBot):
    """
    Записываем название компании, сохраняем нового пользователя в базу данных.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.send_message(
            message.chat.id,
            text=BaseMessages.PROFILE_SUCCESS,
            parse_mode="html",
        )
        name = data["name"]
        phone_number = data["phone_number"]
        company = message.text
        tg_user_id = message.from_user.id
        create_new_user(name, phone_number, company, tg_user_id)

    bot.delete_state(message.from_user.id, message.chat.id)
