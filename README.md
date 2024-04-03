backend чат-бота с технологией GPT
на сайт компании для предоставления консультаций по материалам и
оборудованию, а также оказания помощи клиентам 24/7.

## Установка
- Создайте виртуальное окружение и установите файл с зависимостями:
```bash
py -3.10 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

- На основе `.env.example` создайте файл `.env`

## Документация API
После запуска сервера доступна по следующим эндпоинтам:
`api/swagger/` - Swagger API description
`api/redoc/` - Redoc API description
`api/doc/` - OpenAPI specification yaml-file download
