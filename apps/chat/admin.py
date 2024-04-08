import csv

from django.http import HttpResponse
from django.utils.encoding import smart_str

from apps.chat.models import BotYgpt, ProjectSettings, Chat


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import DateField
from openpyxl import Workbook


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


def export_messages_as_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = 'attachment; filename="exported_messages.csv"'

    writer = csv.writer(response)
    writer.writerow(["Text", "Sender", "Chat", "Created At"])

    for message in queryset:
        writer.writerow(
            [
                smart_str(message.text),
                smart_str(message.get_sender_display()),
                smart_str(message.chat),
                smart_str(message.created_at),
            ]
        )

    return response


export_messages_as_excel.short_description = (
    "Export selected messages as Excel"
)


class CreatedAtFilter(admin.DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.links = (
            (_("All"), {}),
            (
                _("Today"),
                {
                    "%s__gte" % field_path: str(timezone.now().date()),
                    "%s__lt"
                    % field_path: str(
                        timezone.now().date() + timezone.timedelta(days=1)
                    ),
                },
            ),
            (
                _("Past 7 days"),
                {
                    "%s__gte"
                    % field_path: str(
                        timezone.now().date() - timezone.timedelta(days=7)
                    ),
                    "%s__lt"
                    % field_path: str(
                        timezone.now().date() + timezone.timedelta(days=1)
                    ),
                },
            ),
            (
                _("This month"),
                {
                    "%s__gte"
                    % field_path: str(timezone.now().date().replace(day=1)),
                    "%s__lt"
                    % field_path: str(
                        timezone.now().date() + timezone.timedelta(days=1)
                    ),
                },
            ),
            (
                _("Past 30 days"),
                {
                    "%s__gte"
                    % field_path: str(
                        timezone.now().date() - timezone.timedelta(days=30)
                    ),
                    "%s__lt"
                    % field_path: str(
                        timezone.now().date() + timezone.timedelta(days=1)
                    ),
                },
            ),
        )
        super().__init__(
            field, request, params, model, model_admin, field_path
        )


class RangeFilter(admin.SimpleListFilter):
    title = "created_at"
    parameter_name = "created_at"

    def lookups(self, request, model_admin):
        return (
            ("today", "За сегодня"),
            ("this_week", "За эту неделю"),
            ("this_month", "За последний месяц"),
        )

    def queryset(self, request, queryset):
        if self.value() == "today":
            return queryset.filter(created_at__date=timezone.now().date())
        elif self.value() == "this_week":
            start_of_week = timezone.now().date() - timezone.timedelta(
                days=timezone.now().date().weekday()
            )
            end_of_week = start_of_week + timezone.timedelta(days=7)
            return queryset.filter(
                created_at__date__range=[start_of_week, end_of_week]
            )
        elif self.value() == "this_month":
            start_of_month = timezone.now().date().replace(day=1)
            end_of_month = start_of_month + timezone.timedelta(days=32)
            return queryset.filter(
                created_at__date__range=[start_of_month, end_of_month]
            )


class ChatAdmin(admin.ModelAdmin):
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
    list_filter = (RangeFilter,)
    actions = ["export_to_excel"]

    def export_to_excel(self, request, queryset):
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # noqa
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="chats_export.xlsx"'

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Chats"

        # Добавляем заголовки для колонок
        headers = [
            "Дата создания чата",
            "Рейтинг чата",
            "Длительность диалога",
            "Диалог пользователя с ассистентом",
        ]
        worksheet.append(headers)

        for chat in queryset:
            start_date = chat.created_at
            end_date = (
                chat.closed_at or timezone.now()
            )  # Предполагается, что чат закрывается в момент экспорта
            duration = end_date - start_date
            rating = chat.rating
            user_dialog = "\n".join(
                [
                    f"{msg.created_at}/{msg.sender}: {msg.text}"
                    for msg in chat.messages.all()
                ]
            )

            row = [
                start_date.replace(tzinfo=None),
                rating,
                duration,
                user_dialog,
            ]
            worksheet.append(row)

        workbook.save(response)  # noqa
        return response

    export_to_excel.short_description = "Экспорт в Excel"

    def get_list_filter(self, request):
        list_filter = list(self.list_filter)
        for field_name, field in self.model._meta.fields_map.items():  # noqa
            if isinstance(field, DateField):
                list_filter.append((field_name, CreatedAtFilter))
        return list_filter


admin.site.register(Chat, ChatAdmin)
admin.site.register(BotYgpt, BotYgptAdmin)
admin.site.register(ProjectSettings, ProjectSettingsAdmin)
