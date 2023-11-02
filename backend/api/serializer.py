from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..recipes.models import (
    Tag,
    Recipe,
    Ingredient
)
from ..users.models import UserFoodgram, Fallow


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов"""
    class Meta:
        """Метамодель сериализатора TagSerializer"""
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ("id",)


class UserSerializer(ModelSerializer):
    """Сериализатор для юзеров"""
    is_follower = SerializerMethodField()

    class Meta:
        models = UserFoodgram
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_follower",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_is_follower(self, obj):
        """Проверка состояния подписки"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Fallow.objects.filter(
            user=user, auhtor=obj.id
        ).exists()


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов"""
    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe

