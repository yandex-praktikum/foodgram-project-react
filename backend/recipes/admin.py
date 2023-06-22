from django.contrib import admin
from recipes.models import Tag, Ingredient
from import_export import resources
from import_export.admin import ImportExportModelAdmin


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


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
