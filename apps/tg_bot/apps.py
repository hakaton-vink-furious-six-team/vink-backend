from django.apps import AppConfig

from apps.tg_bot.main import bot_starter


def startup():
    bot_starter()


class TgBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tg_bot"

    def ready(self) -> None:
        """Устанавливаем очередность запуска бота после Джанго."""
        import os

        if os.environ.get("RUN_MAIN"):
            startup()
