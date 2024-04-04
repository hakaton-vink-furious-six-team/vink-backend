import logging

logger = logging.getLogger(__name__)


def check_user_exists(tg_id):
    """
    Проверяет наличие пользователя с указанным tg_id в базе данных.
    Возвращает True, если пользователь существует, и False в противном случае.
    """

    try:
        from apps.user_profile.models import UserProfile

        user_exists = UserProfile.objects.filter(tg_id=tg_id).exists()  # noqa
        if user_exists:
            return True
        return False
    except Exception as ex:
        logger.exception(ex)


def get_user(tg_id):
    """
    Возвращает объект пользователя из базы по tg.id
    """

    try:
        from apps.user_profile.models import UserProfile

        user = UserProfile.objects.get(tg_id=tg_id)
        return user
    except Exception as ex:
        logger.exception(ex)


def create_new_user(
    name=None, phone_number=None, company_name=None, tg_id=None
):
    try:
        from apps.user_profile.models import UserProfile

        if UserProfile.objects.filter(
            name=name,
            phone_number=phone_number,
        ).exists():
            user = UserProfile.objects.get(
                name=name, phone_number=phone_number
            )
            user.company_name = (company_name,)
            user.tg_id = tg_id
            user.save()
            logger.info(f"Создан  новый пользователь: {user.name}")
    except Exception as ex:
        logger.exception(ex)


def get_or_create_chat(user):
    """Получение объекта открытого чата или создание нового."""
    try:
        from apps.chat.models import Chat

        chat = Chat.objects.get_or_create(user=user, is_open=True)  # noqa
        return chat
    except Exception as ex:
        logger.exception(ex)


def get_chat(user):
    """Получение объекта открытого чата."""
    try:
        from apps.chat.models import Chat

        chat, created = Chat.objects.get_or_create(
            user=user, is_open=True
        )  # noqa
        return chat
    except Exception as ex:
        logger.exception(ex)


def create_message(chat, sender, message):
    try:
        from apps.message.models import Message

        logger.info(chat)
        message = Message.objects.create(  # noqa
            chat=chat, sender=sender, text=message
        )
        return message
    except Exception as ex:
        logger.exception(ex)


# 4dev
def delete_user(tg_id):
    """
    Удаляет пользователя с указанным tg_id из базы данных.
    """
    try:
        from apps.user_profile.models import UserProfile

        user = UserProfile.objects.get(tg_id=tg_id)  # noqa
        user.delete()
        logger.info("Пользователь удален из базы данных")
    except Exception as ex:
        logger.exception(ex)
