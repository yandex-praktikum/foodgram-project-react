#!/bin/bash
echo "Начинаю удаление говна"
rm recipes/migrations/00*
rm users/migrations/00*
rm db.sqlite3
echo "удалено"
echo "начинаю установку нового говна"
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver

