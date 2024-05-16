from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import (
    Favorites, Follow, Ingredient, Recipe,
    RecipeIngredient, ShoppingCart, Tag
)
from users.models import User
from api.fields import Base64ImageField


class FoodgramUserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = (
            request.user if request and request.user.is_authenticated else None
        )
        return (
            request and user and user.users.filter(following=obj).exists()
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(
        source='recipes_ingredient.id',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'amount', 'measurement_unit'
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)
    author = FoodgramUserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.select_related(
            'recipe'
        ).filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request
            and not request.user.is_anonymous
            and Favorites.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request
            and not request.user.is_anonymous
            and ShoppingCart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'text', 'name', 'image', 'cooking_time'
        )


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    ingredients = CreateIngredientInRecipeSerializer(many=True)

    def validate(self, value):
        if not value.get('ingredients'):
            raise serializers.ValidationError(
                'Заполните поле "Ингредиент"!'
            )
        if not value.get('tags'):
            raise serializers.ValidationError(
                'Заполните поле "Тэг"!'
            )
        return value

    def validate_tags(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError(
                'Теги должны быть уникальными!'
            )
        return value

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        lst_ingredient = []

        for ingredient in ingredients:
            if ingredient['id'] in lst_ingredient:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными!'
                )
            lst_ingredient.append(ingredient['id'])
        if len(lst_ingredient) < 1:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент!'
            )
        return value

    @staticmethod
    def create_ingredients(recipe, ingredients):
        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(create_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data, author=self.context.get('request').user
        )
        self.create_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        instance.ingredients.clear()
        self.create_ingredients(instance, ingredients)
        instance.tags.clear()
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )


class FollowSerializer(FoodgramUserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return FavoriteSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        recipes = obj.recipes.all()
        return recipes.count()


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following',)

    def validate(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )

        if Follow.objects.filter(
            user=data.get('user'),
            following=data.get('following')
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return RecipeSerializer(instance.recipe, context=self.context).data

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return RecipeSerializer(instance.recipe, context=self.context).data

    class Meta:
        model = Favorites
        fields = ('user', 'recipe',)
