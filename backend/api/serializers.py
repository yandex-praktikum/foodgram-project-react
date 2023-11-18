import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers
from recipes.models import (Ingredient, IngredientRecipe, Recipe,
                            Tag, TagRecipe, Subscription, Favorite,
                            ShoppingCart)


User = get_user_model()


class GetIsSubscribedMixin:
    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj.id).exists()


class CustomUserSerializer(GetIsSubscribedMixin, UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "is_subscribed")
        read_only_fields = ("is_subscribed",)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "measurement_unit", "id")
        model = Ingredient


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("Для этого цвета нет имени")
        return data


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientRecipeSerializer(source="ingredients_recipes",
                                             many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField(
        required=False, allow_null=True
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class RecipeMinifiedSerializer(RecipesSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipesPostSerializer(RecipesSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipePostSerializer(many=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        lst = []
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
            lst.append(tag)
        recipe.tags.set(lst)
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient=ingredient["id"],
                    recipe=recipe,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.image = validated_data.get("image", instance.image)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            TagRecipe.objects.filter(recipe_id=instance.id).delete()
            lst = []
            for tag in tags_data:
                TagRecipe.objects.create(tag=tag, recipe=instance)
                lst.append(tag)
            instance.tags.set(lst)
        if "ingredients" in validated_data:
            ingredients_data = validated_data.pop("ingredients")
            IngredientRecipe.objects.filter(recipe_id=instance.id).delete()
            IngredientRecipe.objects.bulk_create(
                [
                    IngredientRecipe(
                        ingredient=ingredient["id"],
                        recipe=instance,
                        amount=ingredient["amount"],
                    )
                    for ingredient in ingredients_data
                ]
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance, context=self.context)
        return serializer.data


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField()

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
        request = self.context.get("request")
        if request.method == "POST":
            recipes = obj.recipes.all()
        else:
            recipes_all = self.context.get("recipes", [])
            recipes = recipes_all.filter(author=obj)
        if request:
            recipes_limit = request.GET.get("recipes_limit")
            if recipes_limit:
                recipes = recipes[: int(recipes_limit)]
        serializer = RecipeMinifiedSerializer(recipes, many=True)
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Subscription

    def validate(self, data):
        request = self.context.get("request")
        author = get_object_or_404(
            User, pk=self.context.get("view").kwargs.get("id")
        )
        subscriber = request.user
        if request.method == "POST":
            if author == subscriber:
                raise serializers.ValidationError(
                    "Нельзя подписаться на самого себя!"
                )
            if Subscription.objects.filter(
                author=author, subscriber=subscriber
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже подписаны на этого автора!"
                )
        return data

    def to_representation(self, instance):
        user_query = User.objects.all().annotate(
            recipes_count=Count("recipes")
        )
        sub_query = Subscription.objects.select_related(
            "subscriber").prefetch_related(
                Prefetch("author", queryset=user_query)
        )
        instance = get_object_or_404(
            sub_query, subscriber=instance.subscriber, author=instance.author
        )
        serializer = SubscriptionSerializer(instance.author,
                                            context=self.context)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ()

    def to_representation(self, data):
        serializer = RecipeMinifiedSerializer(data.recipe)
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ()

    def to_representation(self, data):
        serializer = RecipeMinifiedSerializer(data.recipe)
        return serializer.data
