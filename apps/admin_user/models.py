from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    pass
    # email = models.EmailField(unique=True)
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    #
    # class Meta:
    #     verbose_name = "Пользователь"
    #     verbose_name_plural = "Пользователи"
    #
    # def __str__(self):
    #     return self.email
