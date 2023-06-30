from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from recipes.models import Favorite, Ingredient, Recipes, ShoppingCart, Tag


class TagAdmin(admin.ModelAdmin):
    """Управление Тегами через админку."""


class IngredientResource(resources.ModelResource):
    """Управление Ингридиентами через админку."""

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    """Загрузка Ингридиентов из файла через админку."""
    resource_class = IngredientResource
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class RecipesAdmin(admin.ModelAdmin):
    """Управление Рецептами через админку."""
    search_fields = ('name', 'cooking_time',)
    list_display = ('name', 'author', "cooking_time", "preview",)
    fields = (
        "name",
        "author",
        "cooking_time",
        "preview",
        "image",
        "tags",
        "ingredients",
        "text",
    )
    readonly_fields = ("preview",)

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">')


class FavoriteAdmin(admin.ModelAdmin):
    """Управление Избранным через админку."""


class ShoppingCartAdmin(admin.ModelAdmin):
    """Управление Корзиной через админку."""


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
