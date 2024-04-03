from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tg_bot/", include("apps.tg_bot.urls")),
    path("api/v1/", include("apps.user_profile.api_v1.urls")),
    path("chat/", include("apps.chat.dev.urls")),  # 4dev
]
