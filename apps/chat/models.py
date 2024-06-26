from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.user_profile.models import UserProfile


class Chat(models.Model):
    """Модель чата."""

    RATING_CHOICES = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chats"
    )
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        default=3,
        help_text="Оценка работы оператора от 0 до 5",
    )

    def __str__(self):
        return f"Chat {self.id}"

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def clean(self):
        if (
            self.is_open == "open"
            and Chat.objects.filter(status="open").exists()  # noqa
        ):
            raise ValidationError(
                "Может существовать только один чат со статусом 'open'."
            )

    # @sync_to_async
    def close_chat(self):
        if self.is_open:
            self.is_open = False
            self.closed_at = timezone.now()
            self.save()


class BotYgpt(models.Model):  # noqa
    bot_name = models.CharField(
        verbose_name="Имя ассистента",
        max_length=32,
        unique=True,
        null=False,
        blank=False,
    )
    api_key = models.CharField(
        verbose_name="API Ключ GPT-модели",
        max_length=64,
        unique=False,
        null=False,
        blank=False,
    )
    catalog_id = models.CharField(
        verbose_name="Идентификатор каталога",
        max_length=64,
        null=False,
        blank=False,
    )
    uri = models.CharField(
        verbose_name="URL-префикс адреса модели",
        max_length=16,
        default="gpt://",
        null=False,
        blank=False,
    )
    model_base = models.CharField(
        verbose_name="адрес используемой модели",
        max_length=32,
        default="/yandexgpt-lite/latest",  # noqa
        null=True,
        blank=True,
    )
    temperature = models.FloatField(
        verbose_name="Коэффициент креативности",
        help_text="Число от 0 до 1. Низкие значения дают более простые ответы",
        default=0.5,
        null=False,
        blank=False,
    )
    answer_len = models.IntegerField(
        verbose_name="Допустимая длинна ответа",
        help_text="Количество символов (от 0 до 2000)",
        default=500,
        null=False,
        blank=False,
    )
    promt = models.CharField(  # noqa
        verbose_name="Инструкция к работе",
        max_length=2024,
        default="Ты онлайн консультант в чате поддержки пользователей.",
    )
    url_api = models.CharField(
        verbose_name="адрес запроса к API YandexGPT",
        default="https://llm.api.cloud.yandex.net/"
        "foundationModels/v1/completion",
        max_length=128,
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return self.bot_name


class ProjectSettings(models.Model):
    project = models.CharField(
        default="setup",
        verbose_name="настройки",
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )
    active_bot = models.ForeignKey(
        BotYgpt,
        verbose_name="дежурный бот",
        related_name="settings",
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        return self.active_bot.bot_name  # noqa
