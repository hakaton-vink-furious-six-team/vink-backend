from aiohttp import ClientSession
from django.http import HttpResponse
from .models import ProjectSettings

SORRY_TEXT = (
    'В настоящий момент все операторы заняты, обратитесь пожалуйста позднее.'
)


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
            js_res = await response.json()
            answer = js_res.get(
                'result')['alternatives'][0]['message']['text']
            return answer


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
