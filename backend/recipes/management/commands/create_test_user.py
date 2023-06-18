'''Создание тестовых пользователей, для запуска python manage.py
 create_test_user
'''

from django.core.management.base import BaseCommand

from users.models import FoodgramUser


class Command(BaseCommand):
    def handle(self, *args, **options):

        bulk_data = []
        for index in range(10):
            bulk_data.append(FoodgramUser(username=f'user{index}', email=f'{index}@ya.ru'))
        FoodgramUser.objects.bulk_create(bulk_data)