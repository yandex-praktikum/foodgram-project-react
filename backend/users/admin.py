from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import UserFoodgram, Fallow


@register(UserFoodgram)
class MyUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

@register(Fallow)
class FollowAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
