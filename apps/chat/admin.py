from django.contrib import admin

from apps.chat.models import BotYgpt, ProjectSettings, Chat


class BotYgptAdmin(admin.ModelAdmin):
    list_display = (
        "bot_name",
        "temperature",
        "answer_len",
        "promt",
        "uri",
        "catalog_id",
        "model_base",
        "api_key",
    )
    search_fields = (
        "bot_name",
        "model_base",
    )
    list_display_links = ("bot_name",)
    list_editable = "temperature", "answer_len", "promt"


class ProjectSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "active_bot",
        "project",
    )
    list_editable = ("active_bot",)
    list_display_links = ("project",)


admin.site.register(BotYgpt, BotYgptAdmin)
admin.site.register(ProjectSettings, ProjectSettingsAdmin)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """Админ панель для"""

    list_display = (
        "id",
        "is_open",
        "user",
        "rating",
        "created_at",
        "closed_at",
    )
    list_display_links = ("id",)
    list_editable = ("is_open",)
    search_fields = ("user__name",)
    search_help_text = "Поиск по имени пользователя."
