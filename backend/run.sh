#!/bin/bash

rm db.sqlite3
echo '===================================================================='
python manage.py makemigrations users
python manage.py makemigrations recipes

python manage.py migrate
echo '==================================================================='
python manage.py loaddata dump.json
echo '==================================================================='
python manage.py runserver