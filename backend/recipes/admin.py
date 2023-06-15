from django.contrib import admin

from .models import Ingredients


class IngredientsrAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'measurement_unit',)
    # Добавляем возможность фильтрации
    list_filter = ('name',)
    # Это свойство сработает для всех колонок:
    # где пусто — там будет эта строка
    empty_value_display = '-пусто-'


admin.site.register(Ingredients, IngredientsrAdmin)
