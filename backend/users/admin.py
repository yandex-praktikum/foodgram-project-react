from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser',
        'followers', 'recipes'
    )
    list_filter = ('email', 'username')

    @admin.display(description='Подписчики')
    def followers(self, obj):
        return obj.users.count()

    @admin.display(description='Рецепты')
    def recipes(self, obj):
        return obj.recipes.all().count()
