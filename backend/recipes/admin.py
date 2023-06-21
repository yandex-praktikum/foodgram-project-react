from django.contrib import admin

from recipes.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


admin.site.register(Tag)
