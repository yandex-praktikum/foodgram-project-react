import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from foodgram.settings import BASE_DIR

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, help='Путь к CSV файлу с ингредиентами'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs.get('path') or os.path.join(
            BASE_DIR, 'data', 'ingredients.csv'
        )

        if not os.path.exists(file_path):
            raise CommandError(f'Файл {file_path} не найден!')

        self.stdout.write(f'Импорт данных из файла: {file_path}!')

        with open(file_path, encoding='utf-8') as file, transaction.atomic():
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                _, created = Ingredient.objects.update_or_create(
                    name=row[0], defaults={'measurement_unit': row[1]}
                )
                if created:
                    self.stdout.write(f'Добавлен новый ингредиент: {row[0]}!')

        self.stdout.write(self.style.SUCCESS('Импорт ингредиентов завершен!'))
