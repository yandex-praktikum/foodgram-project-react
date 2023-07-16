'''Загрузка ингредиентов, для запуска python manage.py load_data
'''

import json

from django.core.management.base import BaseCommand

from recipes.constants import INGREDIENTS_NAME_MAX_LENGTH
from recipes.models import Ingredients
from users.models import FoodgramUser


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
                if Ingredients.objects.filter(
                    name=i['name'],
                    measurement_unit=i['measurement_unit']
                ).exists():
                    print(f'Ингредиент {i["name"]},'
                          f'i["measurement_unit"] уже есть')
                    continue
                if not (isinstance(i['name'], str)
                        and len(i['name']) <= INGREDIENTS_NAME_MAX_LENGTH
                        and i['name'] != ''):
                    print(f'Название ингредиента {i["name"]} некорректно')
                    continue
                nubmber_import += 1
                ingredient = Ingredients()
                ingredient.name = i['name'].lower()
                ingredient.measurement_unit = i['measurement_unit']
                ingredient.save()

        print('Импортировано', nubmber_import, 'записей')
