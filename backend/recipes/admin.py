from django.contrib import admin
from recipes.models import (FavoriteList, Ingredient, IngredientInRecipe,
                            Recipe, ShoppingList, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline,)
    list_display = ['title', 'author', 'time', 'get_favorites_count']
    list_filter = ['author', 'title', 'tags']
    search_fields = ['title', 'author__username']

    def get_favorites_count(self, obj):
        return FavoriteList.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    search_fields = ['name']


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(FavoriteList)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']
