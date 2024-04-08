# Хакатон Vink чат-бот

### Задача:
создание MVP backend чат-бота с технологией GPT
для интеграции на сайт компании для предоставления консультаций
по материалам и оборудованию, а также оказания помощи клиентам 24/7.

### Общие возможности приложения:
Организация взаимодествия пользователей с чат-ботом через веб-интерфейс,
либо через аккаунт бота в telegram. Админ-панель позволяет настраивать
виртуальных ассистентов и выбирать, того кто осуществляет беседу, смотреть
и сравнивать пользовательские оценки беседы.

## Использованные технологии:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
<img src="https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
<img src="https://img.shields.io/badge/github%20actions%20-%232671E5.svg?&style=for-the-badge&logo=github%20actions&logoColor=white"/>
![YandexGPT](https://github.com/hakaton-vink-furious-six-team/vink-backend/blob/docs/readme/.github/ygpt_logo.png)

### Как настроить проект для запуска:

- Установите [Docker](https://docs.docker.com/engine/install/)
- в выбранной для проекта директории разместите файл `docker-compose.yml`
- Там же создайте файл `.env` на основе `.env.examlpe`:


### Запуск проекта

- В директории проекта выполните:
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

выбрав `добавить Bot YGPT` - назначьте имя ассистенту,
и заполните необходимые поля для доступа к модели

в разделе `Project settings` выберите дежурного бота, обязательно сохранив изменения


## Документация API
После запуска сервера доступна по следующим эндпоинтам:
- `api/swagger/` - Swagger API description
- `api/redoc/` - Redoc API description
- `api/doc/` - OpenAPI specification yaml-file download


## Установка локально
- Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone https://github.com/hakaton-vink-furious-six-team/vink-backend.git

cd vink-backend/
```

- Создайте виртуальное окружение и установите файл с зависимостями:
```bash
py -3.10 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

- На основе `.env.example` создайте файл `.env`
нужно иметь готовую к подключению базу PosgreSQL
или указать другие настройки в DATABASES файла `config\settings.py`

- создайте и примените миграции
```
python manage.py makemigrations
python manage.py migrate
```
- запустите сервер
```
python manage.py runserver
```


___

## Наша команда разработчиков:<br>
- <h4 align="left"><a href="https://github.com/vladimir-shevchenko01" target="_blank">
Владимир Шевченко</a><a href="https://t.me/vsel_live" target="_blank">  🛒</a></h4>
- <h4 align="left"><a href="https://github.com/acunathink" target="_blank">
Тимофей Карпов</a><a href="https://t.me/timofey_the_hiker" target="_blank">  🛒</a></h4>
<br>
<div id="header" align="left">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGE1cjc1ZXpxc2V1bHV0bXM5bWJ3dTBtem1lZGs3aG0wN3g4aXByMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l46CsTPetihC1rX9K/giphy.gif" width="200"/>
</div>
