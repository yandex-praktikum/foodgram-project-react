# praktikum_new_diplom

### О проекте:
Foodgram или "Продуктовый помощник" - сайт для публикации рецептов. Пользователи могут добавлять рецепты в избранное, подписываться на профили других пользователей и скачивать рецепты.

### Использованные технологии:
DRF, Nginx, Docker, RestApi

### Как запустить проект:
Клонируйте репозиторий и перейдите в него в командной строке:

git clone git@github.com:ByAlexandrow/foodgram-project-react.git

В корне проекта создайте файл .env. В нем укажите переменные: ALLOWED_HOSTS, DEBUG, SECRET_KEY, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT

### Запустить проект:

sudo docker compose up -d

Создайте и выполните миграции:

sudo docker compose backend python manage.py makemigrations

sudo docker compose backend python manage.py migrate

Заполните базу данных ингредиентами:

sudo docker compose exec backend python manage.py load_ing

Создайте администратора:

sudo docker compose backend python manage.py createsuperuser

Приложение будет доступно по адресу - localhost:8000

### Примеры запросов и документация:

Получение списка пользователей(GET) или регистрация нового пользователя(POST):

/api/users/

Получение токена(POST):

/api/auth/token/login/

Получение списка рецептов(GET) или создание нового рецепта(POST):

/api/recipes/

Добавить рецепт в избранное(POST):

/api/recipes/{id}/favorite/

Подписаться на пользователя(POST):

/api/users/{id}/subscribe/

Добавить рецепт в список покупок(POST):

/api/recipes/{id}/shopping_cart/

Скачать список покупок(GET):

/api/recipes/downloan_shopping_cart/

### Данные для использования:

Сайт: https://foodgramever.zapto.org/

Админ: Почта admin@example.com 
Пароль: admin

### Автор:

Александров Егор
Студент 75 когорты Яндекс Практикума на курсе Python-разработчик
https://github.com/ByAlexandrow
