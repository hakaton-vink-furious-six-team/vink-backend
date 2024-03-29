from django.db import models
from django.utils import timezone

from apps.user_profile.models import UserProfile


class Chat(models.Model):
    """Модель чата."""

    STATUS_CHOICES = (
        ("open", "Открыт"),
        ("closed", "Закрыт"),
    )
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
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="open"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        default=3,
        help_text="Оцените помощь нашего сотрудника по шкале от 0 до 5,"
        " где 0 - очень плохо, 5 - великолепно.",
    )

    def __str__(self):
        return f"Chat {self.id}"

    def close_chat(self, rating=None):
        if self.status == "open":
            self.status = "closed"
            self.closed_at = timezone.now()
            self.rating = rating
            self.save()
