import base64
import uuid

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserSerializer
from recipes.models import (
    Ingredient,
    IngredientInRecipe,
    Favorite,
    Recipe,
    ShoppingCart,
    Tag
)
from services import tags


class IngredientSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    """Обработчик получения ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов при создании рецепта."""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Обработчик тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64DecodingImageField(serializers.ImageField):
    """Обработчик изображения, декодирующий строку Base64."""

    def to_internal_value(self, data) -> ContentFile:
        """Метод декодирования изображения."""

        if isinstance(data, str) and data.startswith('data:image'):
            image_format, str_image = data.split(';base64,')
            file_extension = image_format.split('/')[-1]
            random_unique_id = uuid.uuid4()
            data = ContentFile(
                content=base64.b64decode(str_image),
                name=random_unique_id.urn[9:] + '.' + file_extension
            )

        return super().to_internal_value(data)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Обработчик получения рецептов."""

    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientInRecipeReadSerializer(
        many=True,
        read_only=True,
        source='ingredientinrecipe_set'
    )
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

    def get_is_favorited(self, obj) -> bool:
        """Метод проверки добавления рецепта в избранное."""

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:

            return False

        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        """Метод проверки добавления рецепта в корзину."""

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:

            return False

        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Обработчик создания рецептов."""

    ingredients = IngredientInRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=tags.get_all_tags(),
        many=True
    )
    image = Base64DecodingImageField(use_url=True)

    class Meta:
        """Мета-параметры сериализатора"""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance) -> Recipe:
        """Метод представления модели."""

        serializer = RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )

        return serializer.data

    def create_ingredients(self, ingredients, recipe) -> None:
        """Метод добавления ингредиента."""

        for elem in ingredients:
            ingredient_id = elem.get('id')
            amount = elem.pop('amount')

            IngredientInRecipe.objects.create(
                ingredient_id=ingredient_id,
                recipe=recipe,
                amount=amount
            )

    def create_tags(self, tags, recipe) -> None:
        """Метод добавления тега."""

        recipe.tags.set(tags)

    @transaction.atomic
    def create(self, validated_data) -> Recipe:
        """Метод создания модели Recipe."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)

        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data) -> Recipe:
        """Метод обновления модели Recipe."""

        tags = validated_data.pop('tags')
        instance.tags.clear()
        self.create_tags(tags, instance)

        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)

        return super().update(instance, validated_data)


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    """Обработчик выдачи рецептов в подписках пользователя."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Обработчик добавления рецепта в список избранного."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Обработчик добавления рецепта в список покупок."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
