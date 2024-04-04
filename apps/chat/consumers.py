import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.gpt_utilities import get_gpt_answer
from apps.chat.models import Chat
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

    message_list = []

    async def connect(self):
        """Вызывается при установлении сокет соединения."""

        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(type(room_name))
        logger.info(f"Установлено ws соединение: {room_name}")
        user = await UserProfile.objects.aget(id=room_name)  # noqa
        await Chat.objects.aget_or_create(user=user, is_open=True)  # noqa
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "message": "Здравствуйте , меня зовут Вика.\n"
                    "Я оператор в компании Vink, буду рада ответить"  # noqa
                    " на Ваши вопросы."
                }
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Обработка входящих сообщений."""

        # Получаем сообщение, записываем его в словарь, добавляем этот
        # в список словарей для дообучения модели.
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_dict = {"role": "user", "text": message}
        self.message_list.append(message_dict)
        await self.send(
            text_data=json.dumps({"message": f"Пользователь: {message}"})
        )  # для отладки

        # Получаем id пользователя - название комнаты,
        # создаем новый объект сообщения.
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        chat = await Chat.objects.aget(user=room_name, is_open=True)  # noqa
        await Message.objects.acreate(
            sender="user", text=message, chat=chat
        )  # noqa
        logger.info(f"Сообщение от пользователя: {message}")

        # Отправляем запрос ygpt, полученный ответ отдаем пользователю.
        try:
            gpt_answer = await get_gpt_answer(self.message_list)
            logger.info(gpt_answer)
            await self.send(text_data=json.dumps({"message": gpt_answer}))
            await Message.objects.acreate(
                sender="assistant", text=gpt_answer, chat=chat
            )  # noqa
            logger.info(gpt_answer)
        except Exception as ex:
            logger.exception(ex)

    async def disconnect(self, close_code):
        """Закрытие сокет соединения."""

        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        logger.info(f"Установлено ws соединение: {room_name}")
        chat = await Chat.objects.aget(user=room_name, is_open=True)  # noqa
        chat.close_chat()
        logger.info(f"WebSocket закрыт. результаты чата {self.message_list}")
