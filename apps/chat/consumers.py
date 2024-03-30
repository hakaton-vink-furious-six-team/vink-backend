import asyncio
import json
import logging
from pprint import pprint

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.message.models import Message
from apps.user_profile.models import UserProfile

stop_words = [
    "пока",
    "до свидания",
]

logger = logging.getLogger(__name__)


# class ChatConsumer(WebsocketConsumer):
class ChatConsumer(AsyncWebsocketConsumer):
    """Реализация функциональности чата."""

    @database_sync_to_async
    def _save_user_to_db(self, name, phone_number, company_name):
        user = UserProfile.objects.create(  # noqa
            name=name, phone_number=phone_number, company_name=company_name
        )
        user = UserProfile.objects.create(  # noqa
            name=name, phone_number=phone_number, company_name=company_name
        )
        return user

    # async def _save_user_to_db(self, name, phone_number, company_name):
    #     user = await UserProfile.objects.acreate(  # noqa
    #         name=name, phone_number=phone_number, company_name=company_name
    #     )
    #     user = UserProfile.objects.create(
    #         name=name, phone_number=phone_number, company_name=company_name
    #     )
    #     return user

    @database_sync_to_async
    def _save_message_to_db(self, text, sender, chat):
        message = Message.objects.create(  # noqa
            text=text, sender=sender, chat=chat
        )
        return message

    async def connect(self):
        """Вызывается при установлении сокет соединения."""
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        logger.info(f"Установлено ws соединение: {room_name}")
        pprint(self.scope)
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "message": "Здравствуйте, меня зовут Вика.\n"
                    "Я оператор в компании Vink, буду рада ответить"  # noqa
                    " на Ваши вопросы."
                }
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        pprint(text_data_json)
        message = text_data_json["message"]
        # 4prod

        # 4dev
        await self.send(
            text_data=json.dumps({"message": f"Пользователь: {message}"})
        )
        await asyncio.sleep(2)
        await self.send(
            text_data=json.dumps({"message": "Оператор: а вот и ответ"})
        )

    async def disconnect(self, close_code):
        # pprint(f"{self.scope}")
        logger.info("WebSocket закрыт.")
