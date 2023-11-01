from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import UserFoodgram


@register(UserFoodgram)
class MyUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
