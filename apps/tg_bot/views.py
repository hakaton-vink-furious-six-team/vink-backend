from rest_framework.decorators import api_view
from rest_framework.response import Response
from telebot import types  # noqa

from apps.tg_bot.main import bot


@api_view(["POST"])
def bot_view(request) -> Response:
    """Эндпоинт для вебхука."""

    update = types.Update.de_json(request.data)
    bot.process_new_updates([update])
    return Response(status=200)
