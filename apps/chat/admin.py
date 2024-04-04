from django.contrib import admin

from .models import BotYgpt, ProjectSettings


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
