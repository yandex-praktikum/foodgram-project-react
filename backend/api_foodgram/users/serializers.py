from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Subscription


class CustomUserSerializer(UserSerializer):
    """Обработчик пользователей для модели CustomUser."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        """Метод проверяет, подписан ли
        текущий пользователь на автора рецепта.
        """

        request = self.context.get('request')
        return Subscription.objects.filter(subscriber=request.user, author=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Обработчик для регистрации пользователей."""

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
