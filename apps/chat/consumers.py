import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer

stop_words = [
    "пока",
    "до свидания",
]


# class ChatConsumer(WebsocketConsumer):
class ChatConsumer(AsyncWebsocketConsumer):
    # groups = ["lobby"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {
                    "message": "Здравствуйте, меня зовут Вика.\n"
                    "Я оператор в компании Vink, буду рада ответить"
                    " на Ваши вопросы."
                }
            )
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # 4prod

        # 4dev
        await self.send(
            text_data=json.dumps({"message": f"Пользователь: {message}"})
        )
        await asyncio.sleep(10)
        await self.send(
            text_data=json.dumps({"message": "Оператор: а вот и ответ"})
        )

    async def disconnect(self, close_code):
        print("Закрытие соединения")  # TODO Добавить логгирование
