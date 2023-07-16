'''Создание тестовых пользователей, для запуска python manage.py
 create_test_data
'''
# TODO удалить перед деплоем

from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile

from recipes.models import Recipes
from users.models import FoodgramUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

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
                name=f'Рецепт {index}', cooking_time=1, author=user, image=uploaded,
            ))
        Recipes.objects.bulk_create(bulk_data)
