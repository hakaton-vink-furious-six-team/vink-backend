from django.contrib import admin

from apps.message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админ панель для"""

    list_display = (
        "id",
        "created_at",
        "chat",
        "sender",
        "text",
    )
    list_display_links = ("id",)
    search_fields = ("created_at",)
    search_help_text = "Поиск по дате создания"
