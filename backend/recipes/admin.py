from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin


from recipes.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
    # User,
    Favorite,
    ShoppingCart,
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    search_fields = ["name"]
    list_per_page = 20
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    ordering = ("slug",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pub_date",
        "text",
        "cooking_time",
        "author",
        "count_favorite",
        "image",
    )
    list_display_links = ("name", "pub_date", "text", "cooking_time", "author")
    list_editable = ("image",)
    list_per_page = 15
    filter_horizontal = ("tags",)
    search_fields = ["name"]
    list_filter = ("author", "tags")
    ordering = ("pub_date",)
    inlines = [IngredientRecipeInline]
    readonly_fields = ("count_favorite",)

    @admin.display(description="Добавили в избранное", ordering="author")
    def count_favorite(self, obj):
        return obj.recipe.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    ordering = ("user",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
