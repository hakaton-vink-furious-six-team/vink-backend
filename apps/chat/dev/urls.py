from django.urls import path

from apps.chat.dev import views

# 4dev
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
