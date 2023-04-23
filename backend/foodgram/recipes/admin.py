from django.contrib.admin import ModelAdmin, site, StackedInline

from recipes.models import (Ingredient,
                            Tag,
                            )
                            

class IngidientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_editable = ('color', 'slug')
    search_fields = ('name',)
    list_filter = ('slug',)


site.register(Ingredient, IngidientAdmin)
site.register(Tag, TagAdmin)
