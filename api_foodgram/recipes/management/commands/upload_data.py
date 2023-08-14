import json

from django.core.management import BaseCommand

from api_foodgram.settings import UPLOAD_FILES_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингридиенты в базу данных из json файла'

    def handle(self, *args, **options):
        with open(
                f'{UPLOAD_FILES_DIR}/ingredients.json',
                encoding='utf-8'
        ) as json_file:
            json_data = json.load(json_file)

            ingredients = [
                Ingredient(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )
                for ingredient in json_data
            ]

            Ingredient.objects.bulk_create(ingredients)
