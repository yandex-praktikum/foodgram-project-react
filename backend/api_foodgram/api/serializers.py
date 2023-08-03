from rest_framework import serializers
from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Обработчик тегов."""

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Обработчик рецептов."""

    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    is_favorited = serializers.BooleanField()  # where should be this field?
    is_in_shopping_cart = serializers.BooleanField()  # where should be this field?

    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    pass


class FavoriteSerializer(serializers.ModelSerializer):
    pass


class ShoppingCartSerializer(serializers.ModelSerializer):
    pass


# class RecipePostSerializer(serializers.ModelSerializer):
#     """Обработчик создания рецептов."""
#
#     class Meta:
#         model = Recipe
#         fields =
