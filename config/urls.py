from django.contrib import admin
from django.urls import path, include

from apps.chat.gpt_utilities import ask_run


urlpatterns = [
    path("admin/", admin.site.urls),
    path("tg_bot/", include("apps.tg_bot.urls")),
    path("api/v1/", include("apps.user_profile.api_v1.urls")),
    path('api/', include("apps.admin_user.urls")),
    path("gpt/", ask_run)  # для проверки обращения к GPT (удалить на проде)
]
