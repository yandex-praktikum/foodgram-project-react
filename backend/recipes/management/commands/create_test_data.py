'''Создание тестовых пользователей, для запуска python manage.py
 create_test_data
'''
# TODO удалить перед деплоем

from django.core.management.base import BaseCommand

from recipes.models import Recipes
from users.models import FoodgramUser


class Command(BaseCommand):
    def handle(self, *args, **options):

        bulk_data = []
        for index in range(10):
            bulk_data.append(FoodgramUser(
                username=f'user{index}', email=f'{index}@ya.ru'
            ))
        FoodgramUser.objects.bulk_create(bulk_data)

        bulk_data = []
        user = FoodgramUser.objects.get(username='user0')
        for index in range(10):
            bulk_data.append(Recipes(
                name=f'Рецепт {index}', cooking_time=1, author=user
            ))
        Recipes.objects.bulk_create(bulk_data)
