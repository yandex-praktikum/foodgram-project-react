from django.contrib import admin
from django.contrib.auth.models import Group

from .models import FoodgramUser


class FoodgramUserAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('username', 'email',)
    # Добавляем возможность фильтрации
    list_filter = ('username', 'email',)
    # Это свойство сработает для всех колонок:
    # где пусто — там будет эта строка
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
admin.site.register(FoodgramUser, FoodgramUserAdmin)
