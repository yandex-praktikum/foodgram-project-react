from django.contrib import admin

from users.models import CustomUser

from .models import Ingredients, Recipes, Tags


class UserAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('email', 'username', 'first_name', 'last_name', 'password')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('username',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('email', 'username',)


admin.site.register(CustomUser, UserAdmin)


class RecipesAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('author', 'name', 'favorited_count')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('author',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('name', 'author', 'tags')


admin.site.register(Recipes, RecipesAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'measurement_unit')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('name',)


admin.site.register(Ingredients, IngredientsAdmin)


class TagsAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'color', 'slug')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    # Добавляем возможность фильтрации по дате


admin.site.register(Tags, TagsAdmin)
