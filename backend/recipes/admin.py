from django.contrib.admin import ModelAdmin, register
from django.db.models import Model
from .models import (
    Ingredient,
    Tag,
    Recipe,
    ShopCart,
    Favorites,
    IngredientInRecipe,
    TagInRecipe
)


class IngridientAdmin(ModelAdmin):
    """Настройка полей модели Ingredient в админке"""
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)


@register(Tag)
class TagAdmin(ModelAdmin):
    """Настройка полей модели Tag в админке"""
    list_display = ('pk', 'name', 'color', 'slug',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """Настройка полей модели Recipe в админке"""
    list_display = ('pk', 'author', 'name',)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author', 'name', 'tags')


@register(ShopCart)
class ShopCartAdmin(ModelAdmin):
    """Настройка полей модели ShopCart в админке"""
    list_display = ('pk', 'user', 'recipe')
    list_filter = ('user', 'recipe')


@register(Favorites)
class FavoriteAdmin(ModelAdmin):
    """Настройка полей модели Favorites в админке"""
    list_display = ('pk', 'user', 'recipe')
    list_filter = ('user', 'recipe')


@register(IngredientInRecipe)
class IngredientInRecipeAdmin(ModelAdmin):
    """Настройка полей модели IngredientInRecipe
    в админке"""
    list_display = ('pk', 'ingredient', 'recipe', 'amount',)
    list_filter = ('ingredient', 'recipe',)


@register(TagInRecipe)
class TagInRecipeAdmin(ModelAdmin):
    """Настройка полей модели TagInRecipe
        в админке"""
    list_display = ('pk', 'tag', 'recipe')
