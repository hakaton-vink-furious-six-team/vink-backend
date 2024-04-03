from django.apps import AppConfig

from apps.tg_bot.main import bot_starter


class TgBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tg_bot"

    def ready(self) -> None:
        """Подготовить бота перед запуском приложения."""
        bot_starter()
