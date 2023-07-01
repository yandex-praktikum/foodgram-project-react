import base64

from django.core.files.base import ContentFile
from django.core.validators import EmailValidator
from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import RegexField
from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.settings import MIN_COOKING_TIME, HEX_VALID, INGREDIENT_AMOUNT, INGREDIENT_COUNT_ERROR
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipes,
                            ShoppingCart, Tag)
from users.models import Subscribe, User


TEG_COLOR_VALID = 'Тег с таким цветом уже есть'
INGREDIENT_VALID = 'Такой ингридиент уже есть'
RECIPES_VALID = 'Рецепт с таким именем уже есть'
COOKING_TIME_VALID = f'Время приготовления должно быть не меньше {MIN_COOKING_TIME} минуты'
TAG_VALID = 'Такого тега нет, создайте его'


class CreateUserSerializer(UserCreateSerializer):
    """Сериалайзер для создания пользователя."""

    email = serializers.EmailField(validators=(EmailValidator,))

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """Сериалайзер для получени информации о пользователях."""

    email = serializers.EmailField(validators=(EmailValidator,))
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscribe.objects.filter(user=user, author=obj).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания тегов."""

    color = serializers.CharField(
        validators=(
            RegexField(HEX_VALID),),
        error_messages={
            "invalid": "Введите корректный цвет в формате #RRGGBB"},
    )

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")

    def validate_color(self, value):
        if Tag.objects.filter(color=value).exists():
            raise serializers.ValidationError(TEG_COLOR_VALID)
        return value


class IngredientSerilizer(serializers.ModelSerializer):
    """Сериалайзер для создания ингридиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )

    def validate_name(self, value):
        if Ingredient.objects.filter(name=value).exists():
            raise serializers.ValidationError(INGREDIENT_VALID)
        return value


class GetAmountIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения количества ингридиентов."""

    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name", required=False)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", required=False
    )

    class Meta:
        model = AmountIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецепта."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer(many=False, read_only=True)
    ingredients = GetAmountIngredientSerializer(
        many=True, source="amount_recipe")
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context["request"].user.id
        return Favorite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user.id
        return ShoppingCart.objects.filter(user=user, recipe=obj.id).exists()

    def validate_name(self, value):
        if Recipes.objects.filter(name=value).exists():
            raise serializers.ValidationError(RECIPES_VALID)
        return value

    def validate_cooking_time(self, value):
        if value < MIN_COOKING_TIME:
            raise serializers.ValidationError(COOKING_TIME_VALID)
        return value

    def validate_tags(self, value):
        for tag in value:
            if not Tag.objects.filter(name=tag["name"]).exists():
                raise serializers.ValidationError(TAG_VALID)
        return value

    def validate_ingredients(self, value):
        for ingredient in value:
            if ingredient['amount'] < INGREDIENT_AMOUNT:
                raise serializers.ValidationError(INGREDIENT_COUNT_ERROR)
        return value


class Base64ImageField(serializers.ImageField):
    """Сериалайзер для преобразования картинки."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class RecipesPostUpdateSerializer(RecipesSerializer):
    """Сериалайзер для создания, обновления и удаления рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    @transaction.atomic
    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("amount_recipe")
        recipe = Recipes.objects.create(
            author=self.context["request"].user, **validated_data
        )
        for tag in tags_data:
            recipe.tags.add(tag)
        for ingredient_data in ingredients_data:
            pk = ingredient_data["ingredient"]["id"]
            ingredient = Ingredient.objects.get(pk=pk)
            amount = ingredient_data["amount"]
            AmountIngredient.objects.create(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        tags_data = validated_data.get("tags")
        if tags_data:
            instance.tags.set(tags_data)

        ingredients_data = validated_data.get("amount_recipe")
        if ingredients_data:
            AmountIngredient.objects.filter(recipe=instance).delete()
            for ingredient_data in ingredients_data:
                pk = ingredient_data["ingredient"]["id"]
                ingredient = Ingredient.objects.get(pk=pk)
                amount = ingredient_data["amount"]
                AmountIngredient.objects.create(
                    recipe=instance, ingredient=ingredient, amount=amount
                )
        return instance


class CartSerializer(RecipesSerializer):
    """Сериалайзер для получения части полей Рецепта."""

    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")


class SubscribeSerializer(CustomUserSerializer):
    """Сериалайзер для подписок"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return CartSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
