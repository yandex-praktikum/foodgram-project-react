from django.contrib import admin

from .models import (
    Favorites, Follow, Ingredient,
    Recipe, RecipeIngredient, Tag, ShoppingCart
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image', 'text',
        'cooking_time', 'author', 'favorites'
    )
    list_filter = ('name', 'author', 'tags')
    filter_horizontal = ('tags',)
    inlines = [
        RecipeIngredientInline,
    ]

    def favorites(self, obj):
        return obj.favorites.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
