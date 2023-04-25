![yamdb_workflow](https://github.com/vladimir9993/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Foodrgam

 Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`.

## Особенности реализации

- Проект завернут в Docker-контейнеры;
- Образы foodgram_frontend и foodgram_backend запушены на DockerHub;
- Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram;
- Проект был развернут на сервере: <http://158.160.44.57>

## Развертывание проекта

### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker compose`.
2. Создайте файл `/infra/.env`.
3. Выполните команду `docker compose up -d --buld`.
4. Выполните миграции `docker compose exec foodgram-backend python manage.py migrate`.
5. Создайте суперюзера `docker compose exec foodgram-backend python manage.py createsuperuser`.
6. Соберите статику `docker compose exec foodgram-backend python manage.py collectstatic --no-input`.
7. Заполните базу ингредиентами `docker compose exec foodgram-backend python manage.py import_csv --path ingredients.csv`.
8. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**

## Автор

Владимир Кошелев [vladimir9993](https://github.com/vladimir9993)