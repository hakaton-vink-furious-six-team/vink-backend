from aiohttp import ClientSession

import requests
from environs import Env
env = Env()
env.read_env()

SORRY_TEXT = (
    "Извините, но в настоящий момент все операторы заняты, "
    "обратитесь пожалуйста позднее."
)
YGPT_API_KEY = env("YGPT_API_KEY")
MODEL_URI = env("MODEL_URI")
URL_COMPL = env("URL_COMPL")


async def get_gpt_answer(message):
    from apps.chat.consumers import logger

    async with ClientSession() as session:
        from apps.chat.models import ProjectSettings

        setup = ProjectSettings.objects.select_related("active_bot")  # noqa
        bot = await setup.aget(project="setup")
        bot = bot.active_bot
        prompt = {
            "modelUri": bot.uri + bot.catalog_id + bot.model_base,
            "completionOptions": {
                "stream": False,
                "temperature": bot.temperature,
                "maxTokens": bot.answer_len,
            },
            "messages": [
                {
                    "role": "system",
                    "text": bot.promt
                    + (
                        f" Тебя зовут {bot.bot_name}. "
                        "Отвечай как в чате, коротко."
                    ),
                }
            ],
        }
        auth = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key " + bot.api_key,
        }
        prompt["messages"].extend(message)

        async with session.post(
            url=bot.url_api, headers=auth, json=prompt
        ) as response:
            json_res = await response.json()
            try:
                result = json_res.get("result")
                answer = result["alternatives"][0]["message"]["text"]
            except Exception as ex:
                error = json_res.get("error")
                if error is not None:
                    logger.error(error["message"])
                logger.exception(ex)
                answer = SORRY_TEXT
            return answer


def sync_gpt_answer(messages):
    prompt = {
        "modelUri": MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": 500,
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты онлайн консультант в чате"
                " поддержки пользователей.",
            },
        ],
    }
    prompt["messages"].extend(messages)
    auth = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key " + YGPT_API_KEY,
    }
    response = requests.post(URL_COMPL, headers=auth, json=prompt)
    js_res = response.json()
    result = js_res.get("result")
    if result:
        answer = result["alternatives"][0]["message"]["text"]
    else:
        answer = SORRY_TEXT
    return answer
