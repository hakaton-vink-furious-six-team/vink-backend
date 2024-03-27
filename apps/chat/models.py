from django.db import models

from apps.user_profile.models import UserProfile
from apps.message.models import Message


class Chat(models.Model):
    """Модель чата."""

    STATUS_CHOICES = (
        ("open", "Открыт"),
        ("closed", "Закрыт"),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chats"
    )
    messages = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="chat_messages"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="open"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"
