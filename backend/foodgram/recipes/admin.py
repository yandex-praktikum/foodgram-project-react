from django.contrib.admin import ModelAdmin, site, StackedInline

from recipes.models import (Ingredient,
                            Recipe,
                            RecipeIngredient,
                            Tag,
                            )


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
    list_display = ('id', 'name', 'text', 'author', 'image')
    list_display_links = ('id', 'name')
    inlines = (IngredientInline,)
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)


class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


site.register(Ingredient, IngidientAdmin)
site.register(Tag, TagAdmin)
site.register(Recipe, RecipeAdmin)
site.register(RecipeIngredient, RecipeIngredientAdmin)
