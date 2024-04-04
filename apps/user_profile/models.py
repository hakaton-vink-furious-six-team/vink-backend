from django.core.validators import RegexValidator
from django.db import models


class UserProfile(models.Model):
    """Модель клиента|пользователя чата."""

    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^\+\d{9,15}$",
        message="Номер телефона должен быть в формате:"
        " '+999999999'. Допускается до 15 цифр.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True)
    tg_id = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, тел: {self.phone_number}"
