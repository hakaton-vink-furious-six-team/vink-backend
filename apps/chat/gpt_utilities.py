from aiohttp import ClientSession
from django.http import HttpResponse
from .models import ProjectSettings
import requests


SORRY_TEXT = (
    'В настоящий момент все операторы заняты, обратитесь пожалуйста позднее.'
)
YGPT_API_KEY = "AQVN3w8RT5FZ9zjc1clPFoV6hhJTAo76pg4FyIUv"
CATALOG_ID = "b1gqr96555efj5p78okn"
PRO = "/yandexgpt/latest"
LITE = "/yandexgpt-lite/latest"
MODEL_URI = "gpt://" + CATALOG_ID + LITE
URL_COMPL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


async def get_gpt_answer(message):
    async with ClientSession() as session:
        setup = ProjectSettings.objects.select_related('active_bot')
        bot = await setup.aget(project='setup')
        bot = bot.active_bot
        prompt = {
            "modelUri": bot.uri + bot.catalog_id + bot.model_base,
            "completionOptions": {
                "stream": False,
                "temperature": bot.temperature,
                "maxTokens": bot.answer_len
            },
            "messages": [{"role": "system", "text": bot.promt}]
        }
        auth = {"Content-Type": "application/json",
                "Authorization": "Api-Key " + bot.api_key}
        prompt['messages'].append(
            {
                "role": "system",
                "text": (f"Тебя зовут {bot.bot_name}. "
                         "Отвечай как в чате, коротко.")
            }
        )
        prompt['messages'].extend(message)

        async with session.post(
            url=bot.url_api, headers=auth, json=prompt
        ) as response:
            json_res = await response.json()
            return json_res.get(
                'result')['alternatives'][0]['message']['text']


async def ask_run(args):
    # Данные которые нужно получать от фронта
    USERNAME = 'Василий Иванович'
    PHONE_NUMBER = '+79990014422'
    DEFAULT_MESSAGE = "У вас картриджи для Epson цветные есть?"

    # << Написать сохранение в БД входящих данных>>

    # Если в базе сообщений не было, то старт общения делать таким
    begin_conversation = [
        {"role": "user",
         "text": f"Здравствуйте, это {USERNAME}. Мой телефон {PHONE_NUMBER}."}
    ]

    # конструкция для отладки HTTP-запросами
    question = args.GET.get('ask')
    if question is None:
        question = DEFAULT_MESSAGE

    user_request = {
        "role": "user",
        "text": question
    }
    begin_conversation.append(user_request)
    answer = await get_gpt_answer(begin_conversation)
    return HttpResponse(answer)  # для отладки
    # а на проде тут надо возвращать веб-сокетам


def sync_gpt_answer(messages):
    prompt = {
        "modelUri": MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": 500
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты онлайн консультант в чате поддержки пользователей."
            },
        ]
    }
    prompt["messages"].extend(messages)
    auth = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key " + YGPT_API_KEY
    }
    response = requests.post(URL_COMPL, headers=auth, json=prompt)
    js_res = response.json()
    result = js_res.get('result')
    if result:
        answer = result['alternatives'][0]['message']['text']
    else:
        answer = SORRY_TEXT
    return answer
