from django.contrib import admin

from users.models import UserFoodgram


class UserFoodgramAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_display_links = ('pk', 'username')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    empty_value_display = '-пусто-'


admin.site.register(UserFoodgram, UserFoodgramAdmin)
