from django.contrib import admin
from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    """Управление пользователями через админку."""
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
        'role',
        'auth_token',
    )
    list_editable = ('first_name', 'last_name', 'password',)
    list_select_related = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Subscribe)
