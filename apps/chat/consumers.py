import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.gpt_utilities import get_gpt_answer
from apps.chat.models import Chat
from apps.message.models import Message
from apps.user_profile.models import UserProfile


logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Реализация функциональности чата."""

    message_list = {}

    async def connect(self):
        """Вызывается при установлении сокет соединения."""

        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.message_list[room_name] = []
        logger.info(f"Установлено ws соединение: {room_name}")
        user = await UserProfile.objects.aget(id=room_name)  # noqa
        await Chat.objects.aget_or_create(user=user, is_open=True)  # noqa
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"Здравствуйте {user.name}, меня зовут Вика.\n"
                    "Я оператор в компании Vink, буду рада ответить"  # noqa
                    " на Ваши вопросы."
                }
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Обработка входящих сообщений. Входящие сообщения и ответы к ним
          записываются в message_list для поддержания контекста диалога.
          Дополнительно все реплики сохраняются в базу данных.
        """

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_dict = {"role": "user", "text": message}
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.message_list[room_name].append(message_dict)

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
            gpt_answer = await get_gpt_answer(self.message_list[room_name])
            message_dict = {"role": "assistant", "text": gpt_answer}
            self.message_list[room_name].append(message_dict)
            await Message.objects.acreate(  # noqa
                sender="assistant", text=gpt_answer, chat=chat
            )
            await self.send(text_data=json.dumps({"message": gpt_answer}))
            logger.info(gpt_answer)
        except Exception as ex:
            logger.exception(ex)

    async def disconnect(self, close_code):
        """Закрытие сокет соединения."""

        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        chat = await Chat.objects.aget(user=room_name, is_open=True)  # noqa
        await sync_to_async(chat.close_chat)()  # noqa
        logger.info(f"WebSocket '/{room_name}' закрыт. результаты чата:"
                    f" {self.message_list.pop(room_name)}")
