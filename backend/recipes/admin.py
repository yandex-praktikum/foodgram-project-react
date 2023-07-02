from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from recipes.models import (
    Favorite,
    Ingredient,
    Recipes,
    ShoppingCart,
    Tag,
    AmountIngredient,
)


class TagAdmin(admin.ModelAdmin):
    """Управление Тегами через админку."""

    list_display = ("name", "color", "slug")
    list_filter = ("name", "color", "slug")
    search_fields = ("name", "color", "slug")


class IngredientResource(resources.ModelResource):
    """Управление Ингридиентами через админку."""

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    """Загрузка Ингридиентов из файла через админку."""

    resource_class = IngredientResource
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)


class RecipesAdmin(admin.ModelAdmin):
    """Управление Рецептами через админку."""

    search_fields = (
        "name",
        "cooking_time",
    )
    list_display = (
        "name",
        "author",
        "cooking_time",
        "preview",
    )
    list_filter = (
        "author",
        "cooking_time",
        "tags",
    )
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
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
        )


class FavoriteAdmin(admin.ModelAdmin):
    """Управление Избранным через админку."""

    list_display = (
        "user",
        "get_recipe_count",
    )
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("user",)

    def get_recipe_count(self, obj):
        return Favorite.objects.filter(user=obj.user, recipe=obj.recipe).count()

    get_recipe_count.short_description = "Количество рецептов в избранном"


class ShoppingCartAdmin(admin.ModelAdmin):
    """Управление Корзиной через админку."""

    list_display = (
        "user",
        "recipe",
    )
    list_filter = ("user",)
    search_fields = (
        "user",
        "recipe",
    )
    ordering = ("user",)


class AmountIngredientAdmin(admin.ModelAdmin):
    """Управление количеством через админку."""

    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("recipe",)
    search_fields = (
        "recipe",
        "ingredient",
        "amount",
    )
    ordering = ("recipe",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
