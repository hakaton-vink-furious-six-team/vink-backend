from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.user_profile.api_v1.urls")),
    path("chat/", include("apps.chat.dev.urls")),  # 4dev
]
