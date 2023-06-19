#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate
# TODO удалить перед деплоем
python manage.py create_test_data
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi