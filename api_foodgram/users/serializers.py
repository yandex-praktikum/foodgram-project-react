from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Subscription
from services import recipes
# from api.serializers import RecipeInSubscriptionSerializer


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

        if user.is_anonymous:
            return False

        return Subscription.objects.filter(user=user, author=obj).exists()


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
        # extra_kwargs = {'password': {'write_only': True}}


class SubscriptionSerializer(CustomUserSerializer):
    """Обработчик подписок на пользователей."""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Subscription.objects.all(),
        #         fields=('user', 'author'),
        #         message='Вы уже подписаны на данного автора.'
        #     )
        # ]

    # def validate(self, data):
    #     author = self.instance
    #     user = self.context.get('request').user
    #     if Subscription.objects.filter(author=author, user=user).exists():
    #         raise serializers.ValidationError(
    #             detail='Вы уже подписаны на этого пользователя!'
    #         )
    #     if user == author:
    #         raise serializers.ValidationError(
    #             detail='Нельзя подписаться на самого себя!'
    #         )
    #     return data

    # def validate_subscription(self, data):
    #     """Метод проверяет, что пользователь не подписан на самого себя."""
    #
    #     user = self.context['user']
    #     author = self.context['author']
    #
    #     # if not author:
    #     #     raise serializers.ValidationError('Автор не найден.')
    #
    #     if user == author:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на самого себя.'
    #         )
    #     # if Subscription.objects.filter(
    #     #     user=user,
    #     #     author=author
    #     # ).exists():
    #     #     raise serializers.ValidationError('')
    #     return data

    def get_recipes_count(self, obj) -> int:
        """Метод, считающий общее количество рецептов пользователя."""

        return obj.recipes.count()

    def get_recipes(self, obj):
        """Метод для получения рецептов."""

        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        all_recipes = recipes.get_user_recipes(obj)

        if recipes_limit:
            all_recipes = all_recipes[:int(recipes_limit)]

        return RecipeInSubscriptionSerializer(all_recipes, many=True).data
