from django.contrib import admin

from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
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
