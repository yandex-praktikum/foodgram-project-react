from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import UserFoodgram, Fallow


@register(UserFoodgram)
class MyUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@register(Fallow)
class FallowAdmin(MyUserAdmin):
    list_display = ('pk', 'author', 'user', 'date_added',)
    list_filter = ('pk', 'author', 'user', 'date_added',)
    search_fields = ('author', 'user',)
