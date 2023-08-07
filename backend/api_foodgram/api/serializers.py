from rest_framework import serializers
from recipes.models import Ingredient, IngredientInRecipe, Favorite, Recipe, ShoppingCart, Tag
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов в рецепте."""

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Обработчик тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64DecodingImageField(serializers.ImageField):
    """Обработчик изображения, декодирующий строку Base64."""

    def to_internal_value(self, data):
        """Метод декодирования изображения."""

        pass


class RecipeReadSerializer(serializers.ModelSerializer):
    """Обработчик получения рецептов."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Метод проверки добавления рецепта в избранное."""

        user = self.context.get('request').user

        return Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод проверки добавления рецепта в корзину."""

        user = self.context.get('request').user

        return ShoppingCart.objects.filter(
            user=user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Обработчик создания рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    pass


class ShoppingCartSerializer(serializers.ModelSerializer):
    pass
