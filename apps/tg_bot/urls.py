from django.urls import path

from apps.tg_bot.views import bot_view

urlpatterns = [
    path("", bot_view),
]
