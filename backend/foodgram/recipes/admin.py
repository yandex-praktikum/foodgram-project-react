from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from recipes.models import (Ingredient, IngredientRecipe, MeasurementUnit, 
                            Recipe, Tag, User)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    empty_value_display = '-пусто-'
    ordering = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'
    ordering = ('slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date', 'text', 'cooking_time',
                    'author', '_tags', '_ingredients')
    empty_value_display = '-пусто-'
    filter_horizontal = ('tags',)
    list_filter = ('name', 'author', 'tags')
    ordering = ('-pub_date',)
    inlines = [IngredientRecipeInline]

    def _tags(self, obj):
        return ", ".join([t.slug for t in obj.tags.all()])

    def _ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj).values_list(
            'ingredient__name', 'ingredient__measurement_unit__name', 'amount')
        return ", ".join([f'{i[0]} ({i[1]}) - {i[2]}' for i in ingredients])


@admin.register(User)
class MyUserAdmin(UserAdmin):
    change_user_password_template = True
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'username', 'email')
    empty_value_display = '-пусто-'
