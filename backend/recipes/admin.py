from django.contrib import admin
from recipes.models import Tag, Ingredient, Recipes
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource


class RecipesAdmin(admin.ModelAdmin):
    fields = (
        'ingredients',
        'tags',
        'image',
        'preview',
        'name',
        'text',
        'cooking_time',
        )
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
            )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipes, RecipesAdmin)
