from django.contrib.admin import ModelAdmin, StackedInline, site

from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)


class IngidientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)


class IngredientInline(StackedInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'text', 'author', 'image')
    list_editable = ('author',)
    inlines = (IngredientInline,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)


class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


class ShoppingCartAdmin(ModelAdmin):
    list_display = ('id', 'author', 'recipe')
    list_editable = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('recipe',)


class FavoriteAdmin(ModelAdmin):
    list_display = ('id', 'author', 'recipe')
    list_editable = ('author', 'recipe')
    list_filter = ('author',)
    search_fields = ('recipe',)


class FollowAdmin(ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_editable = ('user', 'author',)
    list_filter = ('author',)
    search_fields = ('user',)


site.register(Ingredient, IngidientAdmin)
site.register(Tag, TagAdmin)
site.register(Recipe, RecipeAdmin)
site.register(RecipeIngredient, RecipeIngredientAdmin)
site.register(ShoppingCart, ShoppingCartAdmin)
site.register(Favorite, FavoriteAdmin)
site.register(Follow, FollowAdmin)
