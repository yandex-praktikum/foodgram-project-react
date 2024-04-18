#!/bin/bash

while ! telnet db 5432 > /dev/null 2>&1; do
    sleep 0.5
    echo "DB container is not ready yet. LOADING..."
done

echo "Apply database migrations"
python manage.py makemigrations recipes && python manage.py makemigrations users
python manage.py migrate
echo "Migrations Done!"

echo "Collect and copy static files"
python manage.py collectstatic --noinput
cp -r /app/static/. /static/static/
echo "Static files collected and copied!"

echo "Load DB data"
python manage.py loaddata dump.json
echo "DataBase is update!"

echo "Starting server"
gunicorn foodgram.wsgi:application  --bind 0:8000
echo "server is ready"
