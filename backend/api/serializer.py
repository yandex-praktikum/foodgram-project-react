from rest_framework.serializers import ModelSerializer

from ..recipes.models import (
    Tag,
    Recipe,
    Ingredient
)
from ..users.models import UserFoodgram


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов"""
    class Meta:
        """Метамодель сериализатора TagSerializer"""
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ("id",)


class UserSerializer(ModelSerializer):
    """Сериализатор для юзеров"""


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов"""
    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe

