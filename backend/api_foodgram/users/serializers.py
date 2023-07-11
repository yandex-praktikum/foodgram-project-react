from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Обработчик пользователей."""

    count =

    class Meta:
        model = CustomUser
        fields =

