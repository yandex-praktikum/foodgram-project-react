from django.contrib import admin

from .models import (
    Tag,
    Recipe,
    Ingredient,
    RecipeIngredient,
    ShoppingCart,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
        'color',
        'slug'
    )
    list_filter = (
        'name',
        'color',
        'slug'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
    )
    search_fields = (
        'name',
        'author'
    )
    list_filter = (
        'name',
        'author',
        'tags'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = (
        'recipe',
        'ingredient'
    )
    list_filter = (
        'recipe',
        'ingredient'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe'
    )
    search_fields = (
        'user',
        'recipe'
    )
    list_filter = (
        'user',
        'recipe'
    )
