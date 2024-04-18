#!/bin/bash

python manage.py makemigrations
python manage.py migrate
echo '==================================================================='
python manage.py loaddata dump.json
echo '==================================================================='
python manage.py runserver