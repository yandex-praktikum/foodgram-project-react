# Загрузка ингредиентов, для запуска python manage.py load_data

from django.core.management.base import BaseCommand
import json

from recipes.models import Ingredients
from recipes.constants import (
    CORRECT_MEASUREMENTS, INGREDIENTS_NAME_MAX_LENGTH,
)


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('../data/ingredients.json', 'rb') as f:
            data = json.load(f)
            nubmber_import = 0
            for i in data:
                if not (isinstance(i, dict) and i.get('name')
                        and i.get('measurement_unit')):
                    print('Ошибка данных', i)
                    continue
                if Ingredients.objects.filter(name=i['name']).exists():
                    print(f'Ингредиент {i["name"]} уже есть')
                    continue
                if not (isinstance(i['name'], str)
                        and len(i['name']) <= INGREDIENTS_NAME_MAX_LENGTH
                        and i['name'] != ''):
                    print(f'Название ингредиента {i["name"]} некорректно')
                    continue
                if i['measurement_unit'] not in CORRECT_MEASUREMENTS:
                    print(f'Значение {i["measurement_unit"]} некорректно')
                    continue
                nubmber_import += 1
                ingredient = Ingredients()
                ingredient.name = i['name']
                ingredient.measurement_unit = i['measurement_unit']
                ingredient.save()

        print('Импортировано', nubmber_import, 'записей')
