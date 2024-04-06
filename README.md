backend чат-бота с технологией GPT
на сайт компании для предоставления консультаций по материалам и
оборудованию, а также оказания помощи клиентам 24/7.

## Установка локально
- Создайте виртуальное окружение и установите файл с зависимостями:
```bash
py -3.10 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

- На основе `.env.example` создайте файл `.env`

## Документация API
После запуска сервера доступна по следующим эндпоинтам:
- `api/swagger/` - Swagger API description
- `api/redoc/` - Redoc API description
- `api/doc/` - OpenAPI specification yaml-file download


### Как настроить проект для запуска:

- Установите [Docker](https://docs.docker.com/engine/install/)

- Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/hakaton-vink-furious-six-team/vink-backend.git

cd vink-backend/
```

- Создайте файл `.env` на основе `.env.examlpe`:
  Установите пароль для доступа к базе данных (`POSTGRES_PASSWORD`),
  определите по своему усмотрению `DJANGO_SECRET_KEY`.

  Добавьте в настройки доменное имя или ip-адрес связанные с вашим сервером,
  для этого задайте значение `ALLOWED_HOSTS`,
  или установите значение `localhost,127.0.0.1`, тогда сайт будет доступен только локально


### Запуск проекта

- В корневой папке проекта (по умолчанию - `vink-backend`) выполните:
```
docker compose up
```
- при отсутствии ошибок можно остановить работу через ^C и запустить в фоновом режиме,
  используя флаг -d:
```
docker compose up -d
```

- после чего можно создать суперюзера для доступа к адимин-зоне сайта, выполнив
```
docker compose exec -it backend python manage.py createsuperuser
```
вход в админ-зону по эндпоинту `/admin`

выбрав добавить `Bot YGPT` - назначьте имя ассистенту,
и заполните необходимые поля для доступа к модели

в разделе `Project settings` выберите дежурного бота, обязательно сохранив ихменения
