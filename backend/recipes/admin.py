from django.contrib import admin

from .models import (Favorites, Ingredients, RecipeIngredient, Recipes,
                     RecipeTag, Shopping_cart, Subscriptions, Tags)


class IngredientsAdmin(admin.ModelAdmin):
    '''Определяет отображение модели Ingredients в админке
    '''
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'measurement_unit',)
    # Добавляем возможность фильтрации
    list_filter = ('name',)
    # Это свойство сработает для всех колонок:
    # где пусто — там будет эта строка
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    '''Определяет отображение модели Tags в админке
    '''
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'slug', 'color')
    # Это свойство сработает для всех колонок:
    # где пусто — там будет эта строка
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    '''Для добавления поля RecipeIngredient
    '''
    model = RecipeIngredient
    extra = 1


class RecipeTagInline(admin.TabularInline):
    '''Для добавления поля RecipeTag
    '''
    model = RecipeTag
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    '''Определяет отображение модели Recipes в админке
    '''
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'author')
    # Добавляем возможность фильтрации
    list_filter = ('name', 'author', 'tags')
    # Это свойство сработает для всех колонок:
    # где пусто — там будет эта строка
    empty_value_display = '-пусто-'
    # Добавляем возможность редактировать поле ingredients и tags
    inlines = (RecipeIngredientInline, RecipeTagInline)


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipes, RecipesAdmin)
# admin.site.register(RecipeTag)
# admin.site.register(RecipeIngredient)
admin.site.register(Subscriptions)
admin.site.register(Shopping_cart)
admin.site.register(Favorites)
