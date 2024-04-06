from django.db import models

from apps.chat.models import Chat


class Message(models.Model):
    """Модель сообщения."""

    text = models.TextField()
    SENDER_CHOICES = (
        ("assistant", "assistant"),
        ("user", "user"),
    )
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text}"
