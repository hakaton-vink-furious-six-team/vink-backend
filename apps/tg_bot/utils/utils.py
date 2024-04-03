import logging

logger = logging.getLogger(__name__)


def check_user_exists(tg_id):
    """
    Проверяет наличие пользователя с указанным tg_id в базе данных.
    Возвращает True, если пользователь существует, и False в противном случае.
    """

    try:
        from apps.user_profile.models import UserProfile

        user_exists = UserProfile.objects.filter(tg_id=tg_id).exists()
        if user_exists:
            return True
        return False
    except Exception as ex:
        logger.exception(ex)


def create_new_user(
    name=None, phone_number=None, company_name=None, tg_id=None
):
    try:
        from apps.user_profile.models import UserProfile

        UserProfile.objects.create(  # noqa
            name=name,
            phone_number=phone_number,
            company_name=company_name,
            tg_id=tg_id,
        )
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
