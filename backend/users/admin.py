from django.contrib.admin import register, ModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group

from .models import UserFoodgram, Fallow


admin.site.unregister(Group)  # Убираем видимость админки групп

@register(UserFoodgram)
class MyUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    verbose_name_plural = 'Мои модели'
    verbose_name = 'Моя модель'


@register(Fallow)
class FollowAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
