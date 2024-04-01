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
