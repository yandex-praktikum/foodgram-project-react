from django.contrib import admin
from recipes.models import Tag, Ingredient, Recipes, Favorite, ShoppingCart
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe


class TagAdmin(admin.ModelAdmin):
    '''Управление Тегами через админку.'''
    list_display = (
        'name',
        'color',
        'slug'
    )


class IngredientResource(resources.ModelResource):
    'Управление Ингридиентами через админку.'''
    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    'Загрузка Ингридиентов из файла через админку.'''
    resource_class = IngredientResource


class RecipesAdmin(admin.ModelAdmin):
    '''Управление Рецептами через админку.'''
    fields = (
        'name',
        'author',
        'cooking_time',
        'preview',
        'image',
        'tags',
        'ingredients',
        'text',
        )
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
            )


class FavoriteAdmin(admin.ModelAdmin):
    '''Управление Избранным через админку.'''
    fields = ('user', 'recipe',)


class ShoppingCartAdmin(admin.ModelAdmin):
    '''Управление Корзиной через админку.'''
    fields = ('user', 'recipe',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
