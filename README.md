# Foofgram

## Cервис для создания рецептов.

[Перейти](https://baronfel-foodgram.ddns.net/)

### Автор:
- [Михаил Приселков](https://github.com/BaronFAS "Github page")

### Технологии:
- Python 3.9.10
- Django 3.2
- Django REST framework 3.14.0
- библиотека Simple JWT - работа с JWT-токеном
- JS (React)

*Foodgram - это сервис для хранения рецептов, ингридиентов к ним и их изображений. различные пользовали могу загружать свой рецепты, делится ими, смотреть чужие рецепты, подписыватся на интересных авторов и скачивать понарвившиеся им блюда.*

#### Документация к api проекта доступна после запуска сервера по адресу:
```
http://localhost:8000/redoc/
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:BaronFAS/foodgram-project-react.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv .venv
```

```
source venv/scripts/activate
```

Установить зависимости из файлов Pipfile и Pipfile.lock

```
pipenv sync
```

Обновить pip

```
python -m pip install --upgrade pip
```

Создать миграции:

```
python manage.py makemigrations
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```