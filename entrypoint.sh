python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

cp -r /app/collected_static/. /backend/static

daphne -b 0.0.0.0 config.asgi:application
