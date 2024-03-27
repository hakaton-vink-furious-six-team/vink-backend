from django.db import models


class Message(models.Model):
    text = models.TextField()
    SENDER_CHOICES = (
        ("assistant", "Ассистент"),
        ("user", "Пользователь"),
    )
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text}"
