from rest_framework import serializers
from recipes.models import (
    Tag, Ingredient, IngredientInRecipe, Recipe,
)
from users.models import User
from djoser.serializers import UserSerializer, UserCreateSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInREcipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientInRecipe
        fields = '__all__'


class GetRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'



class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name', 'password',
        )


class UserGETSerializer(UserSerializer):
    class Meta:
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name', 'is_subscribed',
        )
    def get_is_subscribed(self, obj):
        return False

