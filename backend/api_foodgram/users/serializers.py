from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Subscription


class CustomUserSerializer(UserSerializer):
    """Обработчик пользователей для модели CustomUser."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Метод проверяет, подписан ли
        текущий пользователь на автора рецепта.
        """

        user = self.context.get('request').user
        return Subscription.objects.filter(user=user, author=obj).exists()  # wip


class CustomUserCreateSerializer(UserCreateSerializer):
    """Обработчик для регистрации пользователей."""

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class SubscriptionSerializer(CustomUserSerializer):
    """Обработчик подписок на пользователей."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id'
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на данного автора.'
            )
        ]

    @staticmethod
    def validate_subscription(data):
        """Метод проверяет, что пользователь не подписан на самого себя."""

        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return data

    def get_recipes_count(self, obj) -> int:
        """Метод, считающий общее количество рецептов пользователя."""

        return obj.recipes.count()

    def get_recipes(self, obj):
        """Метод для получения рецептов."""
        pass
